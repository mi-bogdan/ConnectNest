from uuid import UUID
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import RegisterUsers, ShowUsers, DeleteUserShow, TokenInfo
from .service import UserService, AuthService, get_auth_service, get_current_users_refresh, get_current_users
from app.exceptions import UniqueError, NotNullConstraintViolationException, NotFoundException
from app.db.models.user import User
from app.utils.mixins import DataMaskinMixinEmail

import logging

from typing import Annotated


router = APIRouter()


@router.post("/register/", response_model=ShowUsers, status_code=status.HTTP_201_CREATED)
async def create_users(body: RegisterUsers, user_service: Annotated[UserService, Depends()]) -> ShowUsers:
    logger = logging.getLogger(__name__)
    logger.info(
        "Получен запрос на регистрацию пользователя",
        extra={
            "username": body.username,
            "email": DataMaskinMixinEmail.mask_email(body.email)
        }
    )
    try:
        new_users = await user_service.create_user(body)
        logger.info(
            "Пользователь успешно зарегистрирован",
            extra={
                "user_id": new_users.id,
                "username": new_users.username
            }
        )
        return new_users
    except UniqueError as e:
        logger.warning(
            "Ошибка регистрации: конфликт данных",
            extra={
                "username": body.username,
                "email": DataMaskinMixinEmail.mask_email(body.email),
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except NotNullConstraintViolationException as e:
        logger.error(
            "Ошибка регистрации: нарушение ограничений NOT NULL",
            extra={
                "username": body.username,
                "email": DataMaskinMixinEmail.mask_email(body.email),
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.critical(
            "Критическая ошибка при регистрации пользователя",
            extra={
                "username": body.username,
                "email": DataMaskinMixinEmail.mask_email(body.email),
                "error": str(e)
            },
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутреняя ошибка сервера")


@router.delete("/delete_user/{user_id}", response_model=DeleteUserShow, status_code=status.HTTP_200_OK)
async def delete_users(user_id: UUID, user_service: Annotated[UserService, Depends()]):
    logger = logging.getLogger(__name__)
    logger.info(
        "Получен запрос на удаление пользователя",
        extra={"user_id": user_id}
    )
    try:
        user = await user_service.delete_user(user_id)
        logger.info(
            "Пользователь успешно удален",
            extra={
                "user_id": user_id,
                "username": user.username,
                "email": DataMaskinMixinEmail.mask_email(user.email)
            }
        )
        return user
    except NotFoundException as e:
        logger.warning(
            "Попытка удаления несуществующего пользователя",
            extra={
                "user_id": user_id,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден!")


@router.post("/login/", response_model=TokenInfo)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: Annotated[AuthService, Depends(get_auth_service)]) -> TokenInfo:
    logger = logging.getLogger(__name__)
    logger.info("Получен запрос на аунтентификацию пользователя")
    try:
        user = await auth_service.authenticate_user(form_data.username, form_data.password)
    except NotFoundException as e:
        logger.warning("Неудачная попытка входа, пользователя не найден!", extra={
                       "username": form_data.username})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден!")
    if not user:
        logger.warning("Неудачная попытка входа, неверный логин или пароль", extra={
                       "username": form_data.username})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)

    logger.info(f"Успешный вход пользователя: {form_data.username}")

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: Annotated[User, Depends(get_current_users_refresh)], auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    logger = logging.getLogger(__name__)
    logger.info("Получен запрос на обновение ACCESS токена")
    access_token = auth_service.create_access_token(user)
    logger.info("Токен успешно обновлен")
    return TokenInfo(access_token=access_token)


@router.get("/users/me/", response_model=ShowUsers)
def auth_user_check_self_info(user: ShowUsers = Depends(get_current_users)) -> ShowUsers:
    return user
