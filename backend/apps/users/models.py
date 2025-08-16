from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class JobSeekerProfile(models.Model):
    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior Level (6-10 years)'),
        ('expert', 'Expert Level (10+ years)'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)  # e.g., "Frontend Developer"
    bio = models.TextField(max_length=500, blank=True)
    
    # Resume and Documents
    resume = models.FileField(upload_to='resumes/', blank=True)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Experience and Skills
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    total_experience_years = models.IntegerField(default=0)
    
    # Location and Preferences
    current_location = models.CharField(max_length=100)
    preferred_locations = models.JSONField(default=list)  # ["Remote", "New York", "San Francisco"]
    willing_to_relocate = models.BooleanField(default=False)
    
    # Salary Expectations
    expected_salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    
    # Availability
    availability = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediately'),
        ('2_weeks', 'Within 2 weeks'),
        ('1_month', 'Within 1 month'),
        ('3_months', 'Within 3 months'),
    ])
    
    # Extracted data from resume
    extracted_skills = models.JSONField(default=list)
    extracted_experience = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_description = models.TextField()
    company_website = models.URLField(blank=True)
    company_size = models.CharField(max_length=20, choices=[
        ('startup', '1-10 employees'),
        ('small', '11-50 employees'),
        ('medium', '51-200 employees'),
        ('large', '201-1000 employees'),
        ('enterprise', '1000+ employees'),
    ])
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
