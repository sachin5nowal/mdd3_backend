# app/services/firebase_service.py
import firebase_admin
from firebase_admin import credentials, auth
from ..config import settings



class FirebaseService:
    def __init__(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {
                    'projectId': settings.FIREBASE_PROJECT_ID
                })
        except Exception as e:
            raise

    def verify_token(self, token: str):
        """Verify Firebase ID token with clock tolerance"""
        try:
            decoded_token = auth.verify_id_token(
                token, 
                clock_skew_seconds=10
            )
            return decoded_token
        except Exception as e:
            raise Exception(f"Invalid authentication credentials: {str(e)}")

    def get_user_by_email(self, email: str):
        """Get user by email"""
        try:
            user = auth.get_user_by_email(email)
            return user
        except Exception:
            return None

    def create_user(self, email: str, password: str):
        """Create a new user with email and password"""
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return user
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")

# Create singleton instance
firebase_service = FirebaseService()
