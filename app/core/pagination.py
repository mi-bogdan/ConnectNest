
from pickletools import read_uint1
from unittest import result
from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any, Tuple

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class CountService(ABC):

    @abstractmethod
    def count(self, session: AsyncSession) -> int:
        pass


class FetchService(ABC):

    @abstractmethod
    def fetch(self, session: AsyncSession) -> list[Any]:
        pass


class SQLAlchemyCountService(CountService):
    def __init__(self, query):
        self.query = query

    async def count(self, session: AsyncSession) -> int:
        count_query = select(func.count()).select_from(self.query.alias())
        result = await session.execute(count_query)
        return result.scalar()


class SQLAlchemyFetchService(FetchService):
    def __init__(self, query, limit: int, offset: int):
        self.query = query
        self.limit = limit
        self.offset = offset

    async def fetch(self, session: AsyncSession):
        paginate_query = self.query.limit(self.limit).offset(self.offset)
        result = await session.execute(paginate_query)
        return result.scalars().all()


class Paginator:
    def __init__(self, count_service: CountService, fetch_service: FetchService):
        self.count_service = count_service
        self.fetch_service = fetch_service

    async def execute(self, session: AsyncSession):
        total = await self.count_service.count(session)
        items = await self.fetch_service.fetch(session)
        return items, total


def create_paginated_query(model, page: int, size: int, custom_query=None):
    query = select(model) if custom_query is None else custom_query
    offset = (page-1)*size
    limit = size

    count_service = SQLAlchemyCountService(query)
    fetch_service = SQLAlchemyFetchService(query, limit=limit, offset=offset)

    return Paginator(count_service, fetch_service)
