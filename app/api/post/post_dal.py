from abc import ABC, abstractmethod
from uuid import UUID


class IPostRepository(ABC):

    @abstractmethod
    def create_post(self, title: str, image: str, author_id: UUID,communities_id:UUID):
        """Создание поста"""
        pass
