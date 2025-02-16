from pydantic import BaseModel, PrivateAttr


class LoginRequest(BaseModel):
    email: str
    password: str


class ActivateAccountRequest(BaseModel):
    email: str
    code: str


class TokenData(BaseModel):
    token: str
    token_version: int
