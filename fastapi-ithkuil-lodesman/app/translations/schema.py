import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, PrivateAttr


class Translation(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda: str(uuid.uuid4()))
    title: str
    author: int
    english: str
    ithkuil: str


class TranslationCreateModel(BaseModel):
    title: str
    author: int
    publisher: str
    published_date: str
    page_count: int
    language: str


class TranslationUpdateModel(BaseModel):
    title: Optional[str]
    author: Optional[int]
    publisher: Optional[str]
    page_count: Optional[int]
    language: Optional[str]
