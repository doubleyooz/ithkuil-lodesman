from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth

router = APIRouter()

user_service = UserService()
@router.post("/login")
async def login(request: LoginRequest):
    try:
        user = user_service.login(request)
        # Use Firebase Auth client SDK to sign in the user and get an ID token
        # Assuming you use Firebase client SDK on the frontend for authentication
   
        return {"token": user}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/logout")
async def logout(token: str):
    try:
      
      
        return user_service.logout(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
