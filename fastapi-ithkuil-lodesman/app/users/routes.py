from fastapi import APIRouter, Depends, status
from typing import List
from .schemas import User, UserCreateModel, UserUpdateModel
from .exceptions import UserNotFound
from .services import UserService

router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@router.get("/", response_model=List[User], dependencies=[role_checker])
async def get_all_users():
    users = await user_service.get_all_users()
    return users


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    dependencies=[role_checker],
)
async def create_a_user(
    user_data: UserCreateModel, token_details: dict = Depends(access_token_bearer)
):
    user_id = token_details.get("user")["user_uid"]
    new_user = await user_service.create_user(user_data, user_id)
    return new_user


@router.get("/{user_uid}", response_model=User, dependencies=[role_checker])
async def get_user(user_uid: str):
    user = await user_service.get_user(user_uid)
    if user:
        return user
    else:
        raise UserNotFound()


@router.patch("/{user_uid}", response_model=User, dependencies=[role_checker])
async def update_user(user_uid: str, user_update_data: UserUpdateModel):
    updated_user = await user_service.update_user(user_uid, user_update_data)
    if updated_user is None:
        raise UserNotFound()
    else:
        return updated_user


@router.delete(
    "/{user_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_user(user_uid: str):
    user_to_delete = await user_service.delete_user(user_uid)
    if user_to_delete is None:
        raise UserNotFound()
    else:
        return {}
