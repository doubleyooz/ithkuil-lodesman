from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth
from ..users.service import UserService
from .schema import LoginRequest
from .service import AuthService

router = APIRouter()

user_service = UserService()
auth_service = AuthService()


@router.post("/login")
async def login(request: LoginRequest):
    try:
        user = await auth_service.login(request)
        print("user", user)
        token = auth_service.create_access_token(
            {"email": user["email"], "token_version": user["token_version"]}
        )
        print("token", token)
        # Use Firebase Auth client SDK to sign in the user and get an ID token
        # Assuming you use Firebase client SDK on the frontend for authentication

        return {"data": user, "access_token": token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout")
async def logout(token: str):
    try:

        return user_service.logout(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
