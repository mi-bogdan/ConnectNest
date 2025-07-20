from app.db.models.communities import Communities
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.mixins import LoggerMixin


class CommunityDataAccessLayer(LoggerMixin):
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

    def delete_comminity(self, id):
        pass
