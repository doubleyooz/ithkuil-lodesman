from typing import List
from ..db import db_connection
from .schemas import Translation, TranslationCreateModel, TranslationUpdateModel


class TranslationService:
    def __init__(self):
        self.collection = db_connection.get_collection("translations")

    async def get_all_translations(self) -> List[Translation]:
        translations_ref = self.collection.stream()
        translations = [doc.to_dict() for doc in translations_ref]
        return translations

    async def get_user_translations(self, user_id: str) -> List[Translation]:
        translations_ref = self.collection.where("user_id", "==", user_id).stream()
        translations = [doc.to_dict() for doc in translations_ref]
        return translations

    async def create_translation(self, translation_data: TranslationCreateModel):
        new_translation = self.collection.document().create(translation_data)
        return new_translation

    async def get_translation(self, translation_id: str) -> Translation | None:
        translation_ref = self.collection.document(translation_id)
        translation = translation_ref.get()
        return translation.to_dict() if translation.exists else None

    async def update_translation(
        self, translation_id: str, translation_update_data: TranslationUpdateModel
    ):
        translation_ref = self.collection.document(translation_id)
        translation_ref.update(translation_update_data.dict(exclude_unset=True))
        return translation_ref.get().to_dict()

    async def delete_book(self, translation_id: str):
        translation_ref = self.collection.document(translation_id)
        translation_ref.delete()
        return {}
