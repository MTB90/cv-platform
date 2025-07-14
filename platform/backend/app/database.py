from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker


class DB:
    def __init__(self, url: str) -> None:
        self.engine: AsyncEngine = create_async_engine(url)
        self.async_session: sessionmaker[AsyncSession] = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
