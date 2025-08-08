from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import Settings


class DB:
    def __init__(self, settings: Settings):
        url = self._connection_url(settings)
        engine = AsyncEngine(create_engine(url, future=True))

        self.async_session: sessionmaker[AsyncSession] = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

    @staticmethod
    def _connection_url(settings: Settings) -> str:
        host = settings.CV_BACKEND_DB_HOST
        name = settings.CV_BACKEND_DB_NAME
        user = settings.CV_BACKEND_DB_USER
        password = settings.CV_BACKEND_DB_PASS

        return f"postgresql+asyncpg://{user}:{password}@{host}/{name}"
