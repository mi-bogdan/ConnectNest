from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker
from app.config import settings

import redis.asyncio as redis

# Подключение к Redis


async def get_redis():
    client = redis.from_url(
        settings.get_redis_url(),
        encoding="utf-8",
        decode_responses=True
    )
    try:
        yield client
    finally:
        await client.close()

DATABASE_URL = settings.get_database_string()

# Подключение Базы данных
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
