from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.application.core.config.config import settings

engine: AsyncEngine = create_async_engine(url=settings.PG.PG_URL.get_secret_value())


session_factory: async_sessionmaker = async_sessionmaker(
    bind=engine, class_=AsyncSession
)


class Base(DeclarativeBase): ...


async def get_session() -> AsyncGenerator[Any, Any]:
    try:
        async with session_factory() as session:
            yield session
    finally:
        await session.close()
