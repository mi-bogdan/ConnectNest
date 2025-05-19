from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.db.models.user import User
from app.db.db_exception_handler import get_db_exception_handler
from app.db.session import get_db
from app.exceptions import NotFoundException, TokenValidationsException
from app.config import settings

from .user_dal import UserDataAccessLayer
from .schemas import RegisterUsers
from .security import get_password_hashing, verify_password
from .utils_jwt import JWTManager, get_jwt_manager

from uuid import UUID
from typing import Annotated

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

http_bearer = HTTPBearer(auto_error=False)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


class UserService:
    def __init__(self, db_session: Annotated[AsyncSession, Depends(get_db)]) -> None:
        self.db_session = db_session
        self.user_dal = UserDataAccessLayer(db_session)
        self.db_exceptio_handler = get_db_exception_handler()

    async def create_user(self, user_register: RegisterUsers) -> User | None:
        try:
            hashing_password = get_password_hashing(
                password=user_register.password)
            new_user = await self.user_dal.create_user(
                username=user_register.username,
                email=user_register.email,
                password=hashing_password
            )
            await self.db_session.commit()
            return new_user
        except IntegrityError as e:
            await self.db_session.rollback()
            self.db_exceptio_handler.handle_exception(e)

    async def delete_user(self, id: UUID) -> User:
        del_user = await self.user_dal.delete_user(id)
        await self.db_session.commit()
        return del_user


class AuthService:

    def __init__(
        self,
        db_session: AsyncSession,
        jwt_manager: JWTManager
    ):
        self.db_session = db_session
        self.user_dal = UserDataAccessLayer(db_session)
        self.jwt_manager = jwt_manager

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_dal.get_user_by_username(username)
        if user and verify_password(password, user.password):
            return user
        return None

    def validations_token_type(self, payload, token_type):
        current_token_type = payload.get(TOKEN_TYPE_FIELD)
        if current_token_type == token_type:
            return True
        raise TokenValidationsException(
            f"Invalid token type {current_token_type!r} expected {token_type!r}")

    async def get_user_by_token_sub(self, payload: dict):
        id = payload.get("sub")
        if not id:
            raise TokenValidationsException(
                "Отсутствует идентификатор пользователя")
        user = await self.user_dal.get_user_by_id(id)
        if not user:
            raise NotFoundException("Такого пользователя не существует!")
        return {"user": user, "payload": payload}

    async def validate_token(self, token: str, token_type: str):
        try:
            payload = self.jwt_manager.decode_jwt(token=token)
            self.validations_token_type(payload, token_type)
            return await self.get_user_by_token_sub(payload=payload)
        except ExpiredSignatureError:
            raise TokenValidationsException("Срок действия токена истек")
        except InvalidSignatureError:
            raise TokenValidationsException("Некорректная подпись токена")
        except DecodeError:
            raise TokenValidationsException("Ошибка декодирования токена")

    def create_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.jwt_manager.encode_jwt(payload=jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta)

    def create_access_token(self, user: User) -> str:
        payload_jwt = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email
        }
        access_token = self.create_jwt(
            token_type=ACCESS_TOKEN_TYPE,
            token_data=payload_jwt,
            expire_minutes=settings.access_token_expire_minutes)
        return access_token

    def create_refresh_token(self, user: User):
        payload_jwt = {
            "sub": str(user.id),
        }
        refresh_token = self.create_jwt(
            token_type=REFRESH_TOKEN_TYPE,
            token_data=payload_jwt,
            expire_timedelta=timedelta(days=settings.refresh_token_expire_days)
        )
        return refresh_token


# Dependency для получения сервиса
def get_auth_service(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)]) -> AuthService:
    return AuthService(
        db_session=db_session,
        jwt_manager=jwt_manager
    )


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        token: Annotated[str, Depends(oauth2_schema)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
    ):
        try:
            
            token_data = await auth_service.validate_token(token, self.token_type)
            return token_data["user"]
        except (NotFoundException, TokenValidationsException) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"})


get_current_users = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_users_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)

# Dependenсy для получения текущего пользователя


# async def get_current_users(token: str = Depends(oauth2_schema), auth_service: AuthService = Depends(get_auth_service)):
#     try:
#         token_data = await auth_service.validate_token(token)
#         return token_data["user"]
#     except (NotFoundException, TokenValidationsException) as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=str(e),
#             headers={"WWW-Authenticate": "Bearer"}
#         )
