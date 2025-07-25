import logging
from abc import ABC

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_and_commit(self, obj):
        try:
            self.db.add(obj)
            await self.db.commit()
        except DatabaseError as exc:
            logger.error(
                "database error",
                extra={
                    "type": type(exc).__name__,
                    "object": str(obj.__class__.__name__),
                    "exc": str(exc),
                },
            )

            # Optionally log stack trace in debug mode only
            if logger.isEnabledFor(logging.DEBUG):
                logger.exception("database error stack trace")

            raise

    async def add_and_flush(self, obj):
        try:
            self.db.add(obj)
            await self.db.flush()
        except DatabaseError as exc:
            logger.error(
                "database error",
                extra={
                    "type": type(exc).__name__,
                    "object": str(obj.__class__.__name__),
                    "exc": str(exc),
                },
            )

            # Optionally log stack trace in debug mode only
            if logger.isEnabledFor(logging.DEBUG):
                logger.exception("database error stack trace")

            raise
