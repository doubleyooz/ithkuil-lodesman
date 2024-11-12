from auth.exceptions import InvalidToken, InvalidLogin
from db import db_connection
from users.services import UserService
from .schemas import LoginRequest, ActivateAccountRequest
from datetime import datetime, timedelta
from jose import jwt
from app.config import ACCESS_TOKEN_EXPIRATION, ACCESS_TOKEN_SECRET, ALGORITHM

# for refresh tokens
from app.config import REFRESH_TOKEN_EXPIRATION, REFRESH_TOKEN_SECRET


class AuthService:
    def __init__(self):
        self.collection = db_connection.get_collection("translation")
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

    def create_access_token(data: dict, expiry_time: timedelta | None = None):
        to_encode = data.copy()
        if expiry_time:
            expire = datetime.utcnow() + expiry_time
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    async def logout(self, token: str):
        try:
            decoded_token = auth.verify_id_token(token)
            auth.revoke_refresh_tokens(decoded_token["uid"])
            return {"message": "User logged out successfully"}
        except Exception as e:
            raise InvalidToken
