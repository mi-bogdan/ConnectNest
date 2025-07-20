from typing import Annotated

from fastapi.params import Depends
from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from .communities_dal import CommunityDataAccessLayer
from .schemas import CreateCommunities

from app.db.session import get_db
from app.db.models.user import User
from app.api.auth.service import get_current_users
from app.resources.image_service import ImageService,get_image_service
from app.utils.mixins import LoggerMixin


class CommunityService(LoggerMixin):
    def __init__(
        self,
        db_session: AsyncSession,
        current_user,
        image_service: ImageService
    ):
        self.db_session = db_session
        self.current_user = current_user
        self.community_dal = CommunityDataAccessLayer(self.db_session)
        self.image_service = image_service  

    async def create_community(self, body: CreateCommunities, image_logo: UploadFile | None):
        self.logger.info("Создание сообщества")
        # Сохраняем изображение
        image_path = await self.image_service.save_image(image_logo)

        # Создаем сообщество
        new_community = await self.community_dal.create_community(
            title=body.title,
            description=body.description,
            image_logo=image_path, 
            admin_id=self.current_user.id
        )
        self.logger.info(f"Создано сообщесто {new_community.title}")
        return new_community
    


def get_community_service(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_users)],
        image_service: Annotated[ImageService, Depends(get_image_service)]
) -> CommunityService:
    return CommunityService(
        db_session=db_session,
        current_user=current_user,
        image_service=image_service
    )
