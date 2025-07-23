from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class DB:
    def __init__(self, settings):
        host = settings.CV_BACKEND_DB_HOST
        name = settings.CV_BACKEND_DB_NAME
        user = settings.CV_BACKEND_DB_USER
        password = settings.CV_BACKEND_DB_PASS

        url = f"postgresql+asyncpg://{user}:{password}@{host}/{name}"

        self.engine = AsyncEngine(create_engine(url, future=True))

        self.async_session: sessionmaker[AsyncSession] = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
