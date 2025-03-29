# from typing import Generator
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# from sqlalchemy.orm import sessionmaker
# from config import settings

# DATABASE_URL = settings.get_database_string()

# # Подключение Базы данных
# engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession)


# async def get_db() -> Generator:
#     """Dependency for getting async session"""
#     try:
#         session: AsyncSession = async_session()
#         yield session
#     finally:
#         await session.close()
