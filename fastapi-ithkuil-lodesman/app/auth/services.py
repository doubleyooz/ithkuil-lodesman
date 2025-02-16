from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# for refresh tokens
from app.config import ACCESS_TOKEN_EXPIRATION, ACCESS_TOKEN_SECRET, ALGORITHM

from .exceptions import InvalidToken, InvalidLogin
from ..db import db_connection
from ..users.services import UserService
from .schemas import LoginRequest, ActivateAccountRequest


class AuthService:
    def __init__(self):
        self.userService = UserService()

    async def login(self, request: LoginRequest):
        try:
            user = self.userService.get_user_by_email(request.email)
            # Use Firebase Auth client SDK to sign in the user and get an ID token
            # Assuming you use Firebase client SDK on the frontend for authentication
            return {"token": "idToken"}
        except Exception as e:
            raise InvalidLogin

    async def verifyRecoveryCode(self, request: ActivateAccountRequest):
        return await self.userService.verifyRecoveryCode(
            request.email,
            request.code,
        )

    def create_access_token(self, data: dict, expiry_time: timedelta | None = None):
        to_encode = data.copy()
        if expiry_time:
            expire = datetime.utcnow() + expiry_time
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self,
        auth_token: Annotated[str | None, Header()] = None,
    ):
        """
        Get current user's details from an authentication token
        Args:
            db (Session): database session
            auth_token (str | None): authentication token
        Returns:
            User
        """

        if not auth_token:
            raise InvalidToken
        payload = await jwt.decode(
            auth_token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM]
        )
        if email is None:
            raise InvalidToken
        email = payload.get("email")

        user = self.userService.get_user_by_email(email)
        if user is None:
            raise InvalidToken
        return user

    async def logout(self, token: str):
        try:
            decoded_token = auth.verify_id_token(token)
            auth.revoke_refresh_tokens(decoded_token["uid"])
            return {"message": "User logged out successfully"}
        except Exception as e:
            raise InvalidToken
