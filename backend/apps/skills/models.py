from django.db import models
from backend.apps.users.models import CustomUser

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    aliases = models.JSONField(default=list)  # ["React.js", "ReactJS", "React"]
    is_technical = models.BooleanField(default=True)

class UserSkill(models.Model):
    PROFICIENCY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS)
    years_of_experience = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)  # For future skill verification
    
    class Meta:
        unique_together = ['user', 'skill']
