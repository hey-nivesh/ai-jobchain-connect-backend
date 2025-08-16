# urls.py
# URL configuration for the backend project
from django.urls import path
from backend.apps.users.views import (
    JobSeekerProfileView,
    GetProfileView,
    JobSeekerProfileUpdateView,
    ResumeUploadView,
    ExtractedSkillsView,
    UserSkillsUpdateView,
)
from backend.apps.jobs.views import create_job, list_jobs, get_job

urlpatterns = [
    # Profile Management
    path('api/users/profile/', JobSeekerProfileView.as_view(), name='user-profile'),
    path('api/users/<uuid:user_id>/profile/', GetProfileView.as_view(), name='get-user-profile'),
    path('api/users/job-seeker-profile/', JobSeekerProfileUpdateView.as_view(), name='job-seeker-profile'),
    path('api/users/upload-resume/', ResumeUploadView.as_view(), name='upload-resume'),
    path('api/users/<uuid:user_id>/extracted-skills/', ExtractedSkillsView.as_view(), name='extracted-skills'),
    path('api/users/skills/', UserSkillsUpdateView.as_view(), name='user-skills'),
    
    # Job Management
    path('api/jobs/', create_job, name='create-job'),
    path('api/jobs/list/', list_jobs, name='list-jobs'),
    path('api/jobs/<uuid:job_id>/', get_job, name='get-job'),
]
