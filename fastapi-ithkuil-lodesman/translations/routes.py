from fastapi import APIRouter, Depends, status
from typing import List
from .schemas import Translation, TranslationCreateModel, TranslationUpdateModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.exceptions import TranslationNotFound
from .service import TranslationService

translation_router = APIRouter()
translation_service = TranslationService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

@translation_router.get("/", response_model=List[translation], dependencies=[role_checker])
async def get_all_translations():
    translations = await translation_service.get_all_translations()
    return translations

@translation_router.get("/user/{user_uid}", response_model=List[translation], dependencies=[role_checker])
async def get_user_translation_submissions(user_uid: str):
    translations = await translation_service.get_user_translations(user_uid)
    return translations

@translation_router.post("/", status_code=status.HTTP_201_CREATED, response_model=translation, dependencies=[role_checker])
async def create_a_translation(translation_data: translationCreateModel, token_details: dict = Depends(access_token_bearer)):
    user_id = token_details.get("user")["user_uid"]
    new_translation = await translation_service.create_translation(translation_data, user_id)
    return new_translation

@translation_router.get("/{translation_uid}", response_model=translationDetailModel, dependencies=[role_checker])
async def get_translation(translation_uid: str):
    translation = await translation_service.get_translation(translation_uid)
    if translation:
        return translation
    else:
        raise translationNotFound()

@translation_router.patch("/{translation_uid}", response_model=translation, dependencies=[role_checker])
async def update_translation(translation_uid: str, translation_update_data: translationUpdateModel):
    updated_translation = await translation_service.update_translation(translation_uid, translation_update_data)
    if updated_translation is None:
        raise translationNotFound()
    else:
        return updated_translation

@translation_router.delete("/{translation_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_translation(translation_uid: str):
    translation_to_delete = await translation_service.delete_translation(translation_uid)
    if translation_to_delete is None:
        raise translationNotFound()
    else:
        return {}
