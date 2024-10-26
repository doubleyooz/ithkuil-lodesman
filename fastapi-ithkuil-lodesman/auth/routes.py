from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth

router = APIRouter()


@router.post("/login")
async def login(request: LoginRequest):
    try:
        user = auth.get_user_by_email(request.email)
        # Use Firebase Auth client SDK to sign in the user and get an ID token
        # Assuming you use Firebase client SDK on the frontend for authentication
        return {"token": "idToken"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/logout")
async def logout(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        auth.revoke_refresh_tokens(decoded_token['uid'])
        return {"message": "User logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
