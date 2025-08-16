from rest_framework import serializers
from .models import JobSeekerProfile
from backend.apps.skills.models import UserSkill

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ('user', 'extracted_skills', 'extracted_experience')
    
    def get_skills(self, obj):
        user_skills = UserSkill.objects.filter(user=obj.user)
        return [{
            'skill_name': us.skill.name,
            'proficiency_level': us.proficiency_level,
            'years_of_experience': us.years_of_experience
        } for us in user_skills]

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume']

class ExtractedSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['extracted_skills']

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['skill', 'proficiency_level', 'years_of_experience', 'is_verified']
