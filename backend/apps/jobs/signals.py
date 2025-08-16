from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Job
from backend.apps.users.models import JobSeekerProfile

@receiver(post_save, sender=Job)
def job_created_handler(sender, instance, created, **kwargs):
    if created:  # Only for new jobs
        # Get all job seekers
        job_seekers = JobSeekerProfile.objects.all()
        channel_layer = get_channel_layer()
        
        for seeker in job_seekers:
            # Calculate match score (simplified logic)
            match_score = calculate_job_match(seeker, instance)
            
            # Only send to users with good match (>60%)
            if match_score > 60:
                # Send to user's WebSocket group
                async_to_sync(channel_layer.group_send)(
                    f'user_{seeker.user.id}',
                    {
                        'type': 'job_update',
                        'job_data': {
                            'id': instance.id,
                            'title': instance.title,
                            'company': instance.employer.company_name if instance.employer else 'Unknown Company',
                            'location': instance.location,
                            'salary_range': f"${instance.salary_min:,} - ${instance.salary_max:,}" if instance.salary_min and instance.salary_max else 'Not specified',
                            'job_type': instance.job_type,
                            'posted_date': instance.created_at.isoformat(),
                            'description': instance.description[:200] + '...' if len(instance.description) > 200 else instance.description,
                        },
                        'match_score': match_score
                    }
                )

def calculate_job_match(seeker, job):
    """
    Calculate match score between job seeker and job
    This is a simplified version - you can enhance this with more sophisticated matching logic
    """
    score = 0
    
    # Location match (30% weight)
    if hasattr(seeker, 'preferred_location') and seeker.preferred_location and job.location:
        if seeker.preferred_location.lower() in job.location.lower():
            score += 30
        elif seeker.preferred_location.lower() == job.location.lower():
            score += 30
    
    # Skills match (40% weight)
    if hasattr(seeker, 'extracted_skills') and seeker.extracted_skills and hasattr(job, 'extracted_skills') and job.extracted_skills:
        seeker_skills = set(skill.lower() for skill in seeker.extracted_skills)
        job_skills = set(skill.lower() for skill in job.extracted_skills)
        if job_skills:
            skill_match = len(seeker_skills.intersection(job_skills)) / len(job_skills)
            score += int(skill_match * 40)
    
    # Experience level match (20% weight)
    if hasattr(seeker, 'experience_level') and seeker.experience_level and job.experience_required:
        if seeker.experience_level == job.experience_required:
            score += 20
        elif abs(seeker.experience_level - job.experience_required) <= 1:
            score += 15
    
    # Job type preference (10% weight)
    if hasattr(seeker, 'preferred_job_type') and seeker.preferred_job_type and job.job_type:
        if seeker.preferred_job_type == job.job_type:
            score += 10
    
    return min(score, 100)  # Cap at 100%
