from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models.post import Post

from fastapi import Depends


class IPostRepository(ABC):

    @abstractmethod
    def create_post(self, title: str, image: str, author_id: UUID, communities_id: UUID):
        """Создание поста"""
        pass


class PostDataAccessLayer(IPostRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_post(self, title, description, image, author_id, communities_id):
        post = Post(
            title=title,
            description=description,
            image=image,
            author_id=author_id,
            communities_id=communities_id
        )
        self.db_session.add(post)
        await self.db_session.commit()
        return post


def get_post_dal(db_session: AsyncSession = Depends(get_db)) -> IPostRepository:
    return PostDataAccessLayer(db_session=db_session)
