from firebase_admin import firestore
from .schemas import User, UserCreateModel, UserUpdateModel

class UserService:
    def __init__(self):
        self.collection = firestore.client().collection('users')

    async def get_all_users(self):
        users_ref = self.collection.stream()
        users = [doc.to_dict() for doc in users_ref]
        return users

    async def get_user_users(self, user_uid: str):
        users_ref = self.collection.where('user_uid', '==', user_uid).stream()
        users = [doc.to_dict() for doc in users_ref]
        return users

    async def create_user(self, user_data: UserCreateModel, user_id: str):
        new_user_ref = self.collection.document()
        new_user = {
            **user_data.dict(),
            'user_uid': user_id
        }
        new_user_ref.set(new_user)
        return new_user

    async def get_book(self, book_uid: str):
        book_ref = self.collection.document(book_uid)
        book = book_ref.get()
        return book.to_dict() if book.exists else None

    async def update_book(self, book_uid: str, book_update_data: UserUpdateModel):
        book_ref = self.collection.document(book_uid)
        book_ref.update(book_update_data.dict(exclude_unset=True))
        return book_ref.get().to_dict()

    async def delete_book(self, book_uid: str):
        book_ref = self.collection.document(book_uid)
        book_ref.delete()
        return {}
