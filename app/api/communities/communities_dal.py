from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.db.models.user import User
from app.db.session import get_db
from app.db.models.communities import Communities
from app.utils.mixins import LoggerMixin
from abc import ABC, abstractmethod
from uuid import UUID


class ICommunityRepository(ABC):

    @abstractmethod
    def create_community(self, title: str, description: str, image_logo: str, admin_id: UUID):
        """Создание сообщества"""
        pass

    @abstractmethod
    def get_all(self):
        """получения всех сообществ"""
        pass

    @abstractmethod
    def get_all_by_admin(self, user_id: UUID):
        """Получения всех сообществ созданным пользователем"""
        pass


class CommunityDataAccessLayer(ICommunityRepository, LoggerMixin):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_community(self, title, description, image_logo, admin_id):
        self.logger.info("Попытка создать сообщества в БД")

        new_community = Communities(
            title=title,
            description=description,
            image_logo=image_logo,
            admin_id=admin_id
        )

        self.db_session.add(new_community)
        await self.db_session.commit()
        self.logger.info(f"Сообщество было создано в БД {new_community.title}")
        return new_community

    async def get_all(self):
        self.logger.info("Получение все сообщеста из БД")
        query = select(Communities).order_by(desc(Communities.date_create))
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_all_by_admin(self, user_id):
        self.logger.info("Попытка получения сообществ созданные пользователем")
        query = select(Communities).where(Communities.admin_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()


def get_community_dal(db_session: AsyncSession = Depends(get_db)) -> ICommunityRepository:
    return CommunityDataAccessLayer(db_session)
