from typing import List
from passlib.context import CryptContext
from .schema import User, UserCreateModel, UserUpdateModel
from .exception import EmailAlreadyTaken, UserNotFound
from ..db import db_connection


class UserService:
    def __init__(self):
        self.collection = db_connection.get_collection("users")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_all_users(self) -> List[User]:
        users_ref = self.collection.stream()
        users = [doc.to_dict() for doc in users_ref]
        return users

    async def get_user_by_email(self, _email: str) -> User | None:
        users_ref = self.collection.where("email", "==", _email).stream()
        user = [doc.to_dict() for doc in users_ref]

        return user

    async def get_user_by_id(self, user_id: str) -> User | None:
        users_ref = self.collection.where("_id", "==", user_id).stream()
        user = users_ref.get()
        return user.to_dict() if user.exists else None

    async def create_user(self, user_data: UserCreateModel) -> User:
        existing_user_ref = self.collection.where("email", "==", user_data.email).get()

        if existing_user_ref:
            raise EmailAlreadyTaken()
        doc_ref = self.collection.document()
        user_data.password = self.get_password_hash(user_data.password)
        doc_ref.set(user_data.model_dump())
        print("Document ID:", doc_ref.id)
        new_user = doc_ref.get().to_dict()
        return new_user

    async def update_user(
        self, user_id: str, user_update_data: UserUpdateModel
    ) -> User:
        user_ref = self.collection.document(user_id)
        user_ref.update(user_update_data.dict(exclude_unset=True))
        return user_ref.get().to_dict()

    async def delete_user(self, user_id: str):
        user_ref = self.collection.document(user_id)
        user_ref.delete()
        return {}

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
