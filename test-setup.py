#!/usr/bin/env python
"""
Test script to verify Django setup is working correctly.
"""

import os
import sys
import django

def test_django_setup():
    """Test if Django is properly configured."""
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.development')
        django.setup()
        
        print("✅ Django setup is working correctly!")
        print("✅ Settings module loaded successfully!")
        
        # Test imports
        from backend.apps.users.models import CustomUser
        from backend.apps.skills.models import Skill
        from backend.apps.jobs.models import Job
        from backend.apps.applications.models import JobApplication
        
        print("✅ All models imported successfully!")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✅ Database connection working!")
            else:
                print("❌ Database connection failed!")
                
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_django_setup()
    if success:
        print("\n🎉 All tests passed! Django is ready to run.")
        print("You can now run: python manage.py runserver")
    else:
        print("\n❌ Setup failed. Please check the configuration.")
        sys.exit(1)
