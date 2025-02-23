from fastapi import APIRouter, Depends, HTTPException
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials
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
        print("request", request)
        user = await auth_service.sign_in_with_email_and_password(
            request.email, request.password
        )
        print("user", user)

        # Use Firebase Auth client SDK to sign in the user and get an ID token
        # Assuming you use Firebase client SDK on the frontend for authentication

        return {"data": user, "access_token": user}
    except Exception as e:
        print("e", e)
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        # Extract the token from the Authorization header
        token = credentials.credentials

        # Call the logout method with the token
        return await auth_service.logout(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
