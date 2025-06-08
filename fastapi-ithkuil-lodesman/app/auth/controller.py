from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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
        # Sign in with Firebase
        firebase_response = await auth_service.sign_in_with_email_and_password(
            request.email, request.password
        )

        # The important tokens from Firebase response
        id_token = firebase_response.get("idToken")
        refresh_token = firebase_response.get("refreshToken")

        return {
            "access_token": id_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": firebase_response.get("expiresIn"),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    try:
        # Extract the token from the Authorization header
        token = credentials.credentials

        # Call the logout method with the token
        return await auth_service.logout(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
