from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from uuid import UUID
from app.exceptions import NotFoundException


class UserDataAccessLayer:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user(self, username: str, email: str, password: str) -> User:
        new_user = User(username=username, email=email, password=password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, id: UUID) -> User:
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException(f"Пользователь с id={id} не найден!")
        await self.db_session.delete(user)
        await self.db_session.flush()
        return user

    async def get_user_by_username(self, username):
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException(
                f"Пользователь с логиным {username!r} не существует")
        return user

    async def get_user_by_id(self, id):
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException(
                f"Пользователь не существует")
        return user
