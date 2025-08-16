from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Job
from backend.apps.users.models import EmployerProfile
from django.contrib.auth.models import User

class JobDataSerializer:
    """Simple serializer for Job model"""
    
    @staticmethod
    def to_dict(job):
        return {
            'id': str(job.id),
            'title': job.title,
            'company': job.employer.company_name if job.employer else 'Unknown Company',
            'location': job.location,
            'salary_range': f"${job.salary_min:,} - ${job.salary_max:,}" if job.salary_min and job.salary_max else 'Not specified',
            'job_type': job.job_type,
            'posted_date': job.created_at.isoformat(),
            'description': job.description[:200] + '...' if len(job.description) > 200 else job.description,
            'experience_required': job.experience_required,
            'is_remote': job.is_remote,
            'status': 'active' if job.is_active else 'inactive'
        }

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_job(request):
    """Create a new job posting"""
    try:
        # Get or create employer profile for the user
        employer_profile, created = EmployerProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'company_name': request.data.get('company', 'Unknown Company'),
                'industry': 'Technology',  # Default value
                'company_size': 'Small',  # Default value
                'website': request.data.get('website', ''),
                'description': request.data.get('company_description', '')
            }
        )
        
        # Create the job
        job = Job.objects.create(
            employer=employer_profile,
            title=request.data.get('title'),
            description=request.data.get('description'),
            job_type=request.data.get('job_type', 'full_time'),
            experience_required=request.data.get('experience_level', 'mid'),
            min_years_experience=request.data.get('min_years_experience', 0),
            location=request.data.get('location'),
            is_remote=request.data.get('remote_work', False),
            salary_min=request.data.get('salary_min'),
            salary_max=request.data.get('salary_max'),
            expires_at=request.data.get('application_deadline') or None
        )
        
        # Return the created job data
        job_data = JobDataSerializer.to_dict(job)
        
        return Response({
            'message': 'Job created successfully',
            'job': job_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_jobs(request):
    """List all active jobs"""
    try:
        jobs = Job.objects.filter(is_active=True).order_by('-created_at')
        jobs_data = [JobDataSerializer.to_dict(job) for job in jobs]
        
        return Response({
            'jobs': jobs_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_job(request, job_id):
    """Get a specific job by ID"""
    try:
        job = get_object_or_404(Job, id=job_id)
        job_data = JobDataSerializer.to_dict(job)
        
        return Response({
            'job': job_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
