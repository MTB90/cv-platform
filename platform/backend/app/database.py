from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker


class DB:
    def __init__(self, settings):
        host = settings.CV_BACKEND_DB_HOST
        name = settings.CV_BACKEND_DB_NAME
        user = settings.CV_BACKEND_DB_USER
        password = settings.CV_BACKEND_DB_PASS

        url = f"postgresql+asyncpg://{user}:{password}@{host}/{name}"

        self.engine: AsyncEngine = create_async_engine(url)
        self.async_session: sessionmaker[AsyncSession] = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
