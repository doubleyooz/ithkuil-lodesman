from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreateModel(BaseModel):
    name: str
    password: str
    email: str


class UserUpdateModel(BaseModel):
    name: Optional[str]
    email: Optional[str]


class User(UserBase):
    uid: str  # This will be populated after Firebase creates the user

    class Config:
        from_attributes = True  # Enable ORM mode (if needed)
