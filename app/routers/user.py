# app/routers/user.py
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from ..services.database_service import firestore_service
from ..dependencies import verify_firebase_token

router = APIRouter(prefix="/users", tags=["Users"])

class EmailCheckRequest(BaseModel):
    email_id: EmailStr

@router.post("/check-email")
async def check_user_by_email(request: EmailCheckRequest):
    """Check if a user exists in the database by email_id"""
    try:
        # Query Firestore to check if user exists
        users_ref = firestore_service.db.collection('user_info1')
        query = users_ref.where('email_id', '==', request.email_id).limit(1)
        
        results = query.get()
        
        # Check if we got any results
        for user in results:
            return {
                "exists": True,
                "message": "User found in the database",
                "user_id": user.to_dict().get("user_id", "unknown")
            }
        
        # No user found
        return {
            "exists": False,
            "message": "User not found in the database"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking user existence: {str(e)}"
        )

# If you want to make this endpoint require authentication, use:
@router.post("/check-email-protected")
async def check_user_by_email_protected(
    request: EmailCheckRequest,
    decoded_token: dict = Depends(verify_firebase_token)
):
    """Protected endpoint to check if a user exists in the database by email_id"""
    # Same implementation as above
    try:
        # Query Firestore to check if user exists
        users_ref = firestore_service.db.collection('user_info1')
        query = users_ref.where('email_id', '==', request.email_id).limit(1)
        
        results = query.get()
        
        # Check if we got any results
        for user in results:
            return {
                "exists": True,
                "message": "User found in the database",
                "user_id": user.to_dict().get("user_id", "unknown")
            }
        
        # No user found
        return {
            "exists": False,
            "message": "User not found in the database"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking user existence: {str(e)}"
        )