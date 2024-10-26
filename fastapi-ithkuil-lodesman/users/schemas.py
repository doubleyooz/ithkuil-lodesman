import uuid
from datetime import date, datetime
from typing import List

from pydantic import BaseModel, PrivateAttr



class User(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda: str(uuid.uuid4())) 
    name: str
    password: str
    email: str
  


class UserCreateModel(BaseModel):
    name: str
    password: str
    email: str

class UserUpdateModel(BaseModel):
    name: str
    password: str
    email: str