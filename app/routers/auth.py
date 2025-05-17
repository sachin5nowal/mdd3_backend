# app/routers/auth.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from ..services.firebase_service import firebase_service
import requests
import json
from ..config import settings

class UserLogin(BaseModel):
    email: EmailStr
    password: str



router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(user_data: UserLogin):
    """Login with email and password and get a token"""
    try:
        # Check if user exists first
        user = firebase_service.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist"
            )
        
        # Use Firebase REST API to verify credentials and get ID token
        firebase_api_key = settings.FIREBASE_API_KEY
        auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
        
        payload = {
            "email": user_data.email,
            "password": user_data.password,
            "returnSecureToken": True
        }
        
        response = requests.post(auth_url, data=json.dumps(payload))
        data = response.json()
        
        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {error_message}"
            )
        
        # Successfully authenticated
        return {
            "message": "Login successful",
            "token": data.get("idToken"),  # This is the ID token to use for authentication
            "user_id": data.get("localId"),
            "email": data.get("email"),
            "expires_in": data.get("expiresIn")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during authentication: {str(e)}"
        )