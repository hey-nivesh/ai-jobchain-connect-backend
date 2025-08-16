from django.db import models
import uuid
from backend.apps.jobs.models import Job
from backend.apps.users.models import JobSeekerProfile

class JobApplication(models.Model):
    APPLICATION_STATUS = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    
    # Application Details
    cover_letter = models.TextField(blank=True)
    custom_resume = models.FileField(upload_to='application_resumes/', blank=True)
    
    # AI Matching Scores
    overall_match_score = models.FloatField(default=0.0)
    skill_match_score = models.FloatField(default=0.0)
    experience_match_score = models.FloatField(default=0.0)
    location_match_score = models.FloatField(default=0.0)
    
    # Status
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    employer_notes = models.TextField(blank=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'applicant']
