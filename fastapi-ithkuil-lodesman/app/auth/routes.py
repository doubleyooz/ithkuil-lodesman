from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth
from ..users.services import UserService
from .schemas import LoginRequest
from .services import AuthService

router = APIRouter()

user_service = UserService()
auth_service = AuthService()


@router.post("/login")
async def login(request: LoginRequest):
    try:
        user = auth_service.login(request)
        token = auth_service.create_access_token(
            {"email": user.email, "token_version": user.token_version}
        )
        # Use Firebase Auth client SDK to sign in the user and get an ID token
        # Assuming you use Firebase client SDK on the frontend for authentication

        return {"data": user, "access_token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout")
async def logout(token: str):
    try:

        return user_service.logout(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
