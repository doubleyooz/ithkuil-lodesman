from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from firebase_admin import auth, credentials
import httpx

# for refresh tokens
from app.config import API_KEY, ACCESS_TOKEN_SECRET, ALGORITHM

from .exception import InvalidToken, InvalidLogin
from ..db import db_connection
from ..users.service import UserService
from .schema import LoginRequest, ActivateAccountRequest


class AuthService:
    def __init__(self):
        self.userService = UserService()

    async def sign_in_with_email_and_password(self, email: str, password: str):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
        print("before response")

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            print("after response")

            if response.status_code == 200:
                return response.json()  # This is a JSON-serializable dict
            else:
                error_message = (
                    response.json().get("error", {}).get("message", "Unknown error")
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to sign in: {error_message}",
                )

    @classmethod
    async def get_current_user(
        cls,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        try:

            token = credentials.credentials
            decoded_token = auth.verify_id_token(token)

            # Check if token was revoked
            user = auth.get_user(decoded_token["uid"])
            if (
                user.tokens_valid_after_timestamp
                and decoded_token["auth_time"] * 1000
                < user.tokens_valid_after_timestamp
            ):
                raise HTTPException(status_code=401, detail="Token revoked")

            return decoded_token
        except ValueError:
            # Invalid token
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        except auth.ExpiredIdTokenError:
            raise HTTPException(status_code=401, detail="Token expired")
        except auth.RevokedIdTokenError:
            raise HTTPException(status_code=401, detail="Token revoked")
        except auth.InvalidIdTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    # dependencies.py

    async def logout(self, token: str):
        try:
            decoded_token = auth.verify_id_token(token)
            auth.revoke_refresh_tokens(decoded_token["uid"])
            return {"message": "User logged out successfully"}
        except Exception as e:
            raise InvalidToken

    async def verify_recovery_code(self, request: ActivateAccountRequest):
        return await self.userService.verify_recovery_code(
            request.email,
            request.code,
        )
