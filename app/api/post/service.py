from uuid import UUID
from app.utils.mixins import LoggerMixin
from .post_dal import IPostRepository, get_post_dal
from fastapi import Depends


class ServicePost(LoggerMixin):
    def __init__(self, post_dal: IPostRepository):
        self.post_dal = post_dal

    def create(self, title: str, description: str, author_id: UUID, communities_id: UUID, image: str, current_user):
        pass


def get_service_post(post_dal: IPostRepository = Depends(get_post_dal)):
    return ServicePost(post_dal=post_dal)
