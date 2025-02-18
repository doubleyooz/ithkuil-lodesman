import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, PrivateAttr


class User(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda: str(uuid.uuid4()))
    name: str
    password: str
    email: str
    token_version: Optional[int]


class UserCreateModel(BaseModel):
    name: str
    password: str
    email: str
    token_version: int = 0


class UserUpdateModel(BaseModel):
    name: Optional[str]
    email: Optional[str]
