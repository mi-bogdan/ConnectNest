from abc import ABC, abstractmethod
from app.utils.mixins import LoggerMixin
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.topic import Topic
from fastapi import Depends
from app.db.session import get_db
from app.exceptions import UniqueError, DatabaseException

from sqlalchemy.exc import IntegrityError


class ITopicRepositiry(ABC):

    @abstractmethod
    def create(self, title: str):
        """Создание тем"""
        pass


class TopicDataAccessLayer(ITopicRepositiry, LoggerMixin):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, title):
        self.logger.info("Создания темы в БД")
        try:
            topic = Topic(title=title)
            self.db_session.add(topic)
            await self.db_session.commit()
            self.logger.info(f"Тема: {title} была записана в БД")
            return topic
        except IntegrityError as e:
            await self.db_session.rollback()
            if "duplicate key value violates unique constraint" in str(e.orig):
                raise UniqueError(f"Тема с название {title} уже существует!")
            else:
                raise DatabaseException("Ошибка БД")


def get_topic_dal(db_session: AsyncSession = Depends(get_db)) -> ITopicRepositiry:
    return TopicDataAccessLayer(db_session=db_session)
