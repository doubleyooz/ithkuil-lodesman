from fastapi import APIRouter, Depends, HTTPException, status
from firebase_admin import auth, credentials
from typing import List

from .schema import User, UserCreateModel, UserUpdateModel
from .exception import EmailAlreadyTaken, UserNotFound
from .service import UserService
from ..auth.service import AuthService

router = APIRouter(prefix="/users")
user_service = UserService()
auth_service = AuthService()

from firebase_admin import auth, credentials


@router.get("/", response_model=List[User])
async def get_all_users():
    users = await user_service.get_all_users()
    return users


@router.get("/protected-route")
async def protected_route(
    current_user: dict = Depends(auth_service.get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    print("Protected route accessed by user:")
    print(current_user)
    return {"message": "You are authenticated", "user": current_user}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_data: UserCreateModel):
    try:
        new_user = await user_service.create_user(user_data)

        return new_user
    except auth.EmailAlreadyExistsError:
        print("Error: A user with this email already exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: A user with this email already exists.",
        )
    except Exception as e:
        print("e", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}",
        )


@router.get("/{user_uid}", response_model=User)
async def get_user(user_uid: str):
    user = await user_service.get_user(user_uid)
    if not user:
        raise UserNotFound()
    return user


@router.patch("/{user_uid}", response_model=User)
async def update_user(user_uid: str, user_update_data: UserUpdateModel):
    updated_user = await user_service.update_user(user_uid, user_update_data)
    if not updated_user:
        raise UserNotFound()
    else:
        return updated_user


@router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uid: str):
    user_to_delete = await user_service.delete_user(user_uid)
    if not user_to_delete:
        raise UserNotFound()
    else:
        return None
