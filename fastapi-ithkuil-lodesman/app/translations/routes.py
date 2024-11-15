from fastapi import APIRouter, Depends, status
from typing import List
from .schemas import Translation, TranslationCreateModel, TranslationUpdateModel
from auth.services import AuthService
from .exceptions import TranslationNotFound
from .services import TranslationService

translation_router = APIRouter()
translation_service = TranslationService()
auth_service = AuthService()
access_token_bearer = AccessTokenBearer()


@translation_router.get("/", response_model=List[Translation])
async def get_all_translations():
    translations = await translation_service.get_all_translations()
    return translations


@translation_router.get("/user/{user_uid}", response_model=List[Translation])
async def get_user_translation_submissions(user_uid: str):
    translations = await translation_service.get_user_translations(user_uid)
    return translations


@translation_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=Translation
)
async def create_a_translation(
    translation_data: translationCreateModel,
    token_details: dict = Depends(access_token_bearer),
):
    user_id = token_details.get("user")["user_uid"]
    new_translation = await translation_service.create_translation(
        translation_data, user_id
    )
    return new_translation


@translation_router.get("/{translation_uid}", response_model=translationDetailModel)
async def get_translation(translation_uid: str):
    translation = await translation_service.get_translation(translation_uid)
    if translation:
        return translation
    else:
        raise TranslationNotFound()


@translation_router.patch("/{translation_uid}", response_model=translation)
async def update_translation(
    translation_uid: str, translation_update_data: translationUpdateModel
):
    updated_translation = await translation_service.update_translation(
        translation_uid, translation_update_data
    )
    if updated_translation is None:
        raise TranslationNotFound()
    else:
        return updated_translation


@translation_router.delete("/{translation_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_translation(translation_uid: str):
    translation_to_delete = await translation_service.delete_translation(
        translation_uid
    )
    if translation_to_delete is None:
        raise TranslationNotFound()
    else:
        return {}
