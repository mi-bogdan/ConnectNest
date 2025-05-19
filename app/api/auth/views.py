from uuid import UUID
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import RegisterUsers, ShowUsers, DeleteUserShow, TokenInfo
from .service import UserService, AuthService, get_auth_service, get_current_users_refresh, get_current_users
from app.exceptions import UniqueError, NotNullConstraintViolationException, NotFoundException
from app.db.models.user import User


from typing import Annotated


router = APIRouter()


@router.post("/register/", response_model=ShowUsers, status_code=status.HTTP_201_CREATED)
async def create_users(body: RegisterUsers, user_service: Annotated[UserService, Depends()]) -> ShowUsers:
    try:
        new_users = await user_service.create_user(body)
        return new_users
    except UniqueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except NotNullConstraintViolationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутреняя ошибка сервера")


@router.delete("/delete_user/{user_id}", response_model=DeleteUserShow, status_code=status.HTTP_200_OK)
async def delete_users(user_id: UUID, user_service: Annotated[UserService, Depends()]):
    try:
        user = await user_service.delete_user(user_id)
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден!")


@router.post("/login/", response_model=TokenInfo)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: Annotated[AuthService, Depends(get_auth_service)]) -> TokenInfo:
    try:
        user = await auth_service.authenticate_user(form_data.username, form_data.password)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден!")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.get("/users/me/", response_model=ShowUsers)
def auth_user_check_self_info(user: ShowUsers = Depends(get_current_users)) -> ShowUsers:
    return user


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: Annotated[User, Depends(get_current_users_refresh)], auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    access_token = auth_service.create_access_token(user)
    return TokenInfo(access_token=access_token)
