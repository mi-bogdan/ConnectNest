from fastapi import Depends
from app.utils.mixins import LoggerMixin
from .topic_dal import ITopicRepositiry, get_topic_dal

from app.exceptions import PermissionsError


class TopicService(LoggerMixin):
    def __init__(self, topic_dal: ITopicRepositiry):
        self.topic_dal = topic_dal

    async def create_topic(self, title, current_user):
        self.logger.info("Создание темы")
        if current_user.username != "admin":
            self.logger.warning("У пользователя нету прав доступа!")
            raise PermissionsError(
                f"Недостаточно прав у пользователя {current_user.username}")

        new_topic = await self.topic_dal.create(title=title)
        self.logger.info(f"Тема созданна: {new_topic.title}")
        return new_topic


def get_service_topic(dal: ITopicRepositiry = Depends(get_topic_dal)) -> TopicService:
    return TopicService(topic_dal=dal)
