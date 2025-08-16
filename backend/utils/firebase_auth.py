import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import os
from pathlib import Path

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with service account"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # First try to get from environment variable (base64 encoded)
            firebase_json_b64 = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
            
            if firebase_json_b64:
                # Decode base64 and parse JSON
                import base64
                import json
                try:
                    firebase_json = base64.b64decode(firebase_json_b64).decode('utf-8')
                    firebase_creds = json.loads(firebase_json)
                    cred = credentials.Certificate(firebase_creds)
                    firebase_admin.initialize_app(cred)
                    print("Firebase initialized with environment variable credentials")
                    return
                except Exception as e:
                    print(f"Error decoding Firebase credentials: {e}")
            
            # Fallback to file-based approach
            current_dir = Path(__file__).resolve().parent  # backend/utils/
            backend_root = current_dir.parent.parent  # backend/ (go up 2 levels)
            service_account_path = backend_root / 'firebase-service-account.json'
            
            if service_account_path.exists():
                cred = credentials.Certificate(str(service_account_path))
                firebase_admin.initialize_app(cred)
                print(f"Firebase initialized with service account file: {service_account_path}")
            else:
                # For development, you can use environment variables
                # or create a minimal service account
                print("Warning: Firebase service account not found. Using default credentials.")
                firebase_admin.initialize_app()
    except Exception as e:
        print(f"Firebase initialization error: {e}")

class FirebaseAuthentication(authentication.BaseAuthentication):
    """Custom authentication class for Firebase"""
    
    def authenticate(self, request):
        # Get the authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        # Extract the token
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
        except IndexError:
            return None
            
        if not token:
            return None
            
        try:
            # Verify the Firebase token
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            name = decoded_token.get('name', '')
            
            # Get or create Django user
            user, created = User.objects.get_or_create(
                username=firebase_uid,
                defaults={
                    'email': email,
                    'first_name': name.split()[0] if name else '',
                    'last_name': ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else '',
                }
            )
            
            if created:
                print(f"Created new user: {user.username}")
            
            return (user, None)
            
        except Exception as e:
            print(f"Firebase authentication error: {e}")
            raise AuthenticationFailed('Invalid Firebase token')
    
    def authenticate_header(self, request):
        return 'Bearer realm="api"'

# Initialize Firebase when the module is imported
initialize_firebase()
