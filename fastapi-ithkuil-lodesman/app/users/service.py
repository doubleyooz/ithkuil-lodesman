from typing import List
from firebase_admin import auth, credentials
from .schema import User, UserCreateModel, UserUpdateModel
from .exception import EmailAlreadyTaken, UserNotFound
from ..db import db_connection


class UserService:
    def __init__(self):
        self.collection = db_connection.get_collection("users")

    async def get_all_users(self) -> List[User]:
        users_ref = self.collection.stream()
        users = [doc.to_dict() for doc in users_ref]
        return users

    async def get_user_by_email(self, email: str) -> User | None:
        users_ref = self.collection.where("email", "==", email).limit(1).stream()
        user_doc = next(users_ref, None)
        if user_doc:
            return user_doc.to_dict()
        return None

    async def get_user_by_id(self, user_id: str) -> User | None:
        users_ref = self.collection.where("_id", "==", user_id).stream()
        user = users_ref.get()
        return user.to_dict() if user.exists else None

    async def create_user(self, user_data: UserCreateModel) -> User:

        # Create the user in Firebase Authentication
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.name,
        )

        # Return the user record
        return {
            "uid": user_record.uid,
            "email": user_record.email,
            "name": user_record.display_name,
        }

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
