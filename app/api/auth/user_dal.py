from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from uuid import UUID
from app.exceptions import NotFoundException
from app.utils.mixins import LoggerMixin, DataMaskinMixinEmail


class UserDataAccessLayer(LoggerMixin, DataMaskinMixinEmail):
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user(self, username: str, email: str, password: str) -> User:
        self.logger.info(
            "Попытка создания пользователя в базу данных",
            extra={
                "username": username,
                "email": self.mask_email(email)
            }
        )
        new_user = User(username=username, email=email, password=password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        self.logger.info(
            "Пользователь успешно создан в базе данных",
            extra={
                "user_id": new_user.id,
                "username": username
            }
        )
        return new_user

    async def delete_user(self, id: UUID) -> User:
        self.logger.info("Удаление пользовтаеля по id", extra={"id": id})
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            self.logger.error(
                "Пользователя не был найден по id",
                extra={"id": id}
            )
            raise NotFoundException(f"Пользователь с id={id} не найден!")
        await self.db_session.delete(user)
        await self.db_session.flush()
        self.logger.info(
            "Пользователь был удален с базы данных",
            extra={
                "id": user.id,
                "username": user.username,
                "email": self.mask_email(user.email)
            }
        )
        return user

    async def get_user_by_username(self, username):
        self.logger.info("Попытка найти пользователя в базе данных по username",
                         extra={"username": username}
                         )
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            self.logger.error(
                "Пользователь не был найден в базе данных по username",
                extra={"username": username})
            raise NotFoundException(
                f"Пользователь с логиным {username!r} не существует")
        self.logger.info(
            "Пользователь найден в базе данных по username",
            extra={
                "id": user.id,
                "username": user.username,
                "email": self.mask_email(user.email)
            }
        )
        return user

    async def get_user_by_id(self, id):
        self.logger.info("Получение пользователя из базы данных по id")
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            self.logger.error(
                "Пользователь не был найден в базе данных по id",
                extra={"id": id})
            raise NotFoundException(
                f"Пользователь не существует")
        self.logger.info(
            "Пользователь найден в базе данных по id",
            extra={
                "id": user.id,
                "username": user.username,
                "email": self.mask_email(user.email)
            }
        )
        return user
