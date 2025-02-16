from fastapi import APIRouter, Depends, status
from typing import List
from .schemas import Translation, TranslationCreateModel, TranslationUpdateModel
from ..auth.services import AuthService
from .exceptions import TranslationNotFound
from .services import TranslationService

router = APIRouter()
translation_service = TranslationService()
auth_service = AuthService()


@router.get("/", response_model=List[Translation])
async def get_all_translations():

    translations = await translation_service.get_all_translations()
    return translations


@router.get("/user/{user_uid}", response_model=List[Translation])
async def get_user_translation_submissions(user_uid: str):
    translations = await translation_service.get_user_translations(user_uid)
    return translations


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Translation)
async def create_a_translation(
    translation_data: TranslationCreateModel,
    token_details: dict = Depends(auth_service.get_current_user),
):
    user_id = token_details.get("user")["user_uid"]
    new_translation = await translation_service.create_translation(
        translation_data, user_id
    )
    return new_translation


@router.get("/{translation_uid}", response_model=Translation)
async def get_translation(translation_uid: str):
    translation = await translation_service.get_translation(translation_uid)
    if translation:
        return translation
    else:
        raise TranslationNotFound()


@router.patch("/{translation_uid}", response_model=Translation)
async def update_translation(
    translation_uid: str, translation_update_data: TranslationUpdateModel
):
    updated_translation = await translation_service.update_translation(
        translation_uid, translation_update_data
    )
    if updated_translation is None:
        raise TranslationNotFound()
    else:
        return updated_translation


@router.delete("/{translation_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_translation(translation_uid: str):
    translation_to_delete = await translation_service.delete_translation(
        translation_uid
    )
    if translation_to_delete is None:
        raise TranslationNotFound()
    else:
        return {}
