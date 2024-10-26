from fastapi import APIRouter, Depends, status
from typing import List
from .schemas import User, UserCreateModel, UserUpdateModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.exceptions import UserNotFound
from .service import UserService

user_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

@user_router.get("/", response_model=List[user], dependencies=[role_checker])
async def get_all_users():
    users = await user_service.get_all_users()
    return users

@user_router.get("/user/{user_uid}", response_model=List[user], dependencies=[role_checker])
async def get_user_user_submissions(user_uid: str):
    users = await user_service.get_user_users(user_uid)
    return users

@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=user, dependencies=[role_checker])
async def create_a_user(user_data: userCreateModel, token_details: dict = Depends(access_token_bearer)):
    user_id = token_details.get("user")["user_uid"]
    new_user = await user_service.create_user(user_data, user_id)
    return new_user

@user_router.get("/{user_uid}", response_model=userDetailModel, dependencies=[role_checker])
async def get_user(user_uid: str):
    user = await user_service.get_user(user_uid)
    if user:
        return user
    else:
        raise UserNotFound()

@user_router.patch("/{user_uid}", response_model=user, dependencies=[role_checker])
async def update_user(user_uid: str, user_update_data: userUpdateModel):
    updated_user = await user_service.update_user(user_uid, user_update_data)
    if updated_user is None:
        raise UserNotFound()
    else:
        return updated_user

@user_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_user(user_uid: str):
    user_to_delete = await user_service.delete_user(user_uid)
    if user_to_delete is None:
        raise UserNotFound()
    else:
        return {}
