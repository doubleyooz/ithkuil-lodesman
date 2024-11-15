import uuid
from datetime import date, datetime
from typing import List

from pydantic import BaseModel, PrivateAttr



class Translation(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda: str(uuid.uuid4())) 
    title: str
    author: str
    english: str
    ithkuil: str
  



class TranslationCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class TranslationUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str