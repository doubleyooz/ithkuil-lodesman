from ..db import db_connection
from .schemas import Translation, TranslationCreateModel, TranslationUpdateModel


class TranslationService:
    def __init__(self):
        self.collection = db_connection.get_collection("translations")

    async def get_all_translations(self):
        translations_ref = self.collection.stream()
        translations = [doc.to_dict() for doc in translations_ref]
        return translations

    async def get_user_translations(self, user_uid: str):
        translations_ref = self.collection.where("user_uid", "==", user_uid).stream()
        translations = [doc.to_dict() for doc in translations_ref]
        return translations

    async def create_book(self, book_data: TranslationCreateModel, user_id: str):
        new_book_ref = self.collection.document()
        new_book = {**book_data.dict(), "user_uid": user_id}
        new_book_ref.set(new_book)
        return new_book

    async def get_book(self, book_uid: str):
        book_ref = self.collection.document(book_uid)
        book = book_ref.get()
        return book.to_dict() if book.exists else None

    async def update_book(
        self, book_uid: str, book_update_data: TranslationUpdateModel
    ):
        book_ref = self.collection.document(book_uid)
        book_ref.update(book_update_data.dict(exclude_unset=True))
        return book_ref.get().to_dict()

    async def delete_book(self, book_uid: str):
        book_ref = self.collection.document(book_uid)
        book_ref.delete()
        return {}
