from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
