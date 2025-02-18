from fastapi import APIRouter, Depends, status
from typing import List
from .schema import User, UserCreateModel, UserUpdateModel
from .exception import EmailAlreadyTaken, UserNotFound
from .service import UserService

router = APIRouter(prefix="/users")
user_service = UserService()


@router.get("/", response_model=List[User])
async def get_all_users():
    users = await user_service.get_all_users()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_data: UserCreateModel):
    new_user = await user_service.create_user(user_data)
    return new_user


@router.get("/{user_uid}", response_model=User)
async def get_user(user_uid: str):
    user = await user_service.get_user(user_uid)
    if user:
        return user
    else:
        raise UserNotFound()


@router.patch("/{user_uid}", response_model=User)
async def update_user(user_uid: str, user_update_data: UserUpdateModel):
    updated_user = await user_service.update_user(user_uid, user_update_data)
    if updated_user is None:
        raise UserNotFound()
    else:
        return updated_user


@router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uid: str):
    user_to_delete = await user_service.delete_user(user_uid)
    if user_to_delete is None:
        raise UserNotFound()
    else:
        return {}
