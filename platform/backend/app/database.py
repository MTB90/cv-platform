from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker


class DB:
    def __init__(self, settings):
        url = (
            f"postgresql+asyncpg://{settings.CV_BACKEND_DB_USER}:{settings.CV_BACKEND_DB_PASS}"
            f"@{settings.CV_BACKEND_DB_HOST}/{settings.CV_BACKEND_DB_NAME}"
        )

        self.engine: AsyncEngine = create_async_engine(url)
        self.async_session: sessionmaker[AsyncSession] = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
