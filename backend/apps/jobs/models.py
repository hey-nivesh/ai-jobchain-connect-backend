from django.db import models
import uuid
from backend.apps.users.models import EmployerProfile
from backend.apps.skills.models import Skill, UserSkill

class Job(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    )
    
    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('expert', 'Expert Level'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Job Details
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    min_years_experience = models.IntegerField(default=0)
    
    # Location
    location = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=False)
    
    # Salary
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    
    # Requirements (extracted from job description)
    extracted_skills = models.JSONField(default=list)
    extracted_requirements = models.JSONField(default=dict)
    
    # Status and Visibility
    is_active = models.BooleanField(default=True)
    applications_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.CharField(max_length=20, choices=[
        ('required', 'Required'),
        ('preferred', 'Preferred'),
        ('nice_to_have', 'Nice to Have'),
    ])
    min_proficiency = models.CharField(max_length=20, choices=UserSkill.PROFICIENCY_LEVELS)
