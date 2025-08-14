import json

from typing import Annotated, Any, Optional

from fastapi.params import Depends
from fastapi import UploadFile

from redis import Redis
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .communities_dal import CommunityDataAccessLayer, get_community_dal, ICommunityRepository
from .schemas import CreateCommunities, CommunityAll, CommunityAllAdmin


from app.db.session import get_db, get_redis
from app.db.models.user import User
from app.db.models.communities import Communities
from app.api.auth.service import get_current_users
from app.resources.image_service import ImageService, get_image_service
from app.utils.mixins import LoggerMixin
from app.core.pagination import create_paginated_query, PaginatedResponse


class CommunityService(LoggerMixin):
    def __init__(
        self,
        db_session: AsyncSession,
        current_user,
        community_dal: ICommunityRepository,
        image_service: ImageService,
        redis_client: Redis
    ):
        self.db_session = db_session
        self.current_user = current_user
        self.community_dal = community_dal
        self.image_service = image_service
        self.redis_client = redis_client

    async def create_community(self, body: CreateCommunities, image_logo: Optional[UploadFile]):
        self.logger.info("Создание сообщества")
        # Сохраняем изображение
        image_path = ""
        if image_logo and image_logo.filename:
            image_path = await self.image_service.save_image(image_logo)

        # Создаем сообщество
        new_community = await self.community_dal.create_community(
            title=body.title,
            description=body.description,
            image_logo=image_path,
            admin_id=self.current_user.id
        )
        self.logger.info(f"Создано сообщесто {new_community.title}")

        await self._invalide_community_all_cache()  # Инвалидация кэша всех страниц
        await self._inavlid_cache_admin_community(self.current_user.id)
        return new_community

    async def _invalide_community_all_cache(self):
        """Очистка всех кэша пагинации сообщества"""

        pattern = "community_all_cache_*"

        keys = await self.redis_client.keys(pattern)
        if keys:
            await self.redis_client.delete(*keys)
            self.logger.info(
                f"Очищено {len(keys)} кэш-ключей пагинации сообщества")

    async def _inavlid_cache_admin_community(self, id_user):
        if id_user:
            key = f"admin_all_communities:{id_user}"
            self.logger.info(
                f"Удаление кэша получения сообществ для пользователя {id_user}")
            await self.redis_client.delete(key)


class ReadCommunotyService(LoggerMixin):
    """Сервис получения записей"""
    CACHE_TTL = 300  # 5 мин

    def __init__(self, db_session: AsyncSession, redis_client: Any) -> None:
        self.db_session = db_session
        self.redis_client = redis_client

    async def get(self, page: int, size: int):
        self.logger.info(f"Получения сообществ старница {page}")
        cache_key = f"community_all_cache_{page}_{size}"

        cached = await self.redis_client.get(cache_key)
        if cached:
            self.logger.info("Получения сообщества из КЭША")
            data = json.loads(cached)
            return PaginatedResponse[CommunityAll](**data)

        custom_query = select(Communities).order_by(
            Communities.date_create.desc())

        paginator = create_paginated_query(
            Communities, page, size, custom_query=custom_query)
        items, total = await paginator.execute(self.db_session)
        pages = (total + size - 1) // size

        result = PaginatedResponse[CommunityAll](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            next_page=page+1 if page < pages else None,
            prev_page=page-1 if page > 1 else None
        )

        await self.redis_client.setex(cache_key, self.CACHE_TTL, result.model_dump_json())

        self.logger.info("Данные получены напрямую из БД")
        return result


class GetCommunityAllAdmin(LoggerMixin):
    """Получение сообщество которые пользователь создал"""
    CACHE_TTL = 300
    _prefix_cached = "admin_all_communities"

    def __init__(self, community_dal: CommunityDataAccessLayer, redis_client: Any) -> None:
        self.community_dal = community_dal
        self.redis_client = redis_client

    async def get(self, user: User):
        self.logger.info(
            f"Получения созданных сообщества пользователя, {user.username}")
        cache_key = f"{self._prefix_cached}:{user.id}"
        cached = await self.redis_client.get(cache_key)

        if cached:
            self.logger.info(
                f"Получение из кэша созданных сообществ пользователя, {user.username}")
            data = json.loads(cached)
            return [CommunityAllAdmin(**item) for item in data]

        communities = await self.community_dal.get_all_by_admin(user_id=user.id)
        result = [CommunityAllAdmin.model_validate(
            community).model_dump() for community in communities]

        await self.redis_client.setex(cache_key, self.CACHE_TTL, json.dumps(result, default=str))
        return communities


def get_community_service(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_users)],
        community_dal: Annotated[ICommunityRepository,
                                 Depends(get_community_dal)],
        image_service: Annotated[ImageService, Depends(get_image_service)],
        redis_client: Annotated[Redis, Depends(get_redis)]
) -> CommunityService:
    return CommunityService(
        db_session=db_session,
        current_user=current_user,
        community_dal=community_dal,
        image_service=image_service,
        redis_client=redis_client
    )


def get_community_all(db_session: Annotated[AsyncSession, Depends(get_db)], redis_client: Annotated[Redis, Depends(get_redis)]) -> ReadCommunotyService:
    return ReadCommunotyService(db_session, redis_client)


def get_community_all_admin(community_dal: Annotated[CommunityDataAccessLayer, Depends(get_community_dal)], redis_client: Annotated[Redis, Depends(get_redis)]) -> ReadCommunotyService:
    return GetCommunityAllAdmin(community_dal, redis_client)
