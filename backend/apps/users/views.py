from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import CustomUser, JobSeekerProfile
from backend.apps.skills.models import UserSkill, Skill
from .serializers import JobSeekerProfileSerializer, ResumeUploadSerializer, ExtractedSkillsSerializer, UserSkillSerializer
from backend.services.resume_parser import ResumeProcessor

class JobSeekerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    def get_object(self):
        profile, created = JobSeekerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get(self, request, *args, **kwargs):
        """Get user profile data"""
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def perform_update(self, serializer):
        # Calculate profile completion percentage
        profile = serializer.save()
        profile.user.is_profile_complete = self.calculate_completion(profile)
        profile.user.save()

    def calculate_completion(self, profile):
        """Calculate profile completion percentage"""
        required_fields = [
            profile.first_name, profile.last_name, profile.title,
            profile.current_location, profile.experience_level,
            profile.total_experience_years, profile.availability
        ]
        
        completed_fields = sum(1 for field in required_fields if field)
        completion_percentage = (completed_fields / len(required_fields)) * 100
        
        return completion_percentage >= 80  # Mark as complete if 80% or more

class GetProfileView(views.APIView):
    """Get profile for a specific user ID"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            profile = get_object_or_404(JobSeekerProfile, user__id=user_id)
            serializer = JobSeekerProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class JobSeekerProfileUpdateView(generics.UpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = JobSeekerProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def perform_update(self, serializer):
        # Calculate profile completion percentage
        profile = serializer.save()
        profile.user.is_profile_complete = self.calculate_completion(profile)
        profile.user.save()

    def calculate_completion(self, profile):
        """Calculate profile completion percentage"""
        required_fields = [
            profile.first_name, profile.last_name, profile.title,
            profile.current_location, profile.experience_level,
            profile.total_experience_years, profile.availability
        ]
        
        completed_fields = sum(1 for field in required_fields if field)
        completion_percentage = (completed_fields / len(required_fields)) * 100
        
        return completion_percentage >= 80  # Mark as complete if 80% or more

class ResumeUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({'error': 'Resume file required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Process resume and extract skills
            processor = ResumeProcessor()
            extracted_data = processor.process_resume(resume_file)
            
            # Update user profile with extracted data
            profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
            profile.resume = resume_file
            profile.extracted_skills = extracted_data.get('skills', [])
            profile.extracted_experience = extracted_data.get('experience', {})
            profile.save()
            
            return Response({
                'message': 'Resume uploaded successfully',
                'extracted_skills': extracted_data.get('skills', []),
                'extracted_experience': extracted_data.get('experience', {})
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExtractedSkillsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            profile = get_object_or_404(JobSeekerProfile, user__id=user_id)
            serializer = ExtractedSkillsSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class UserSkillsUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserSkillSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
