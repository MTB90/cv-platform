import logging
from abc import ABC
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


def exception_logger(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except Exception as exc:
            logger.error(
                "database error",
                extra={
                    "type": type(exc).__name__,
                    "exc": str(exc),
                },
            )

            # Optionally log stack trace in debug mode only
            if logger.isEnabledFor(logging.DEBUG):
                logger.exception("database error stack trace")

            raise

    return wrapper


class BaseRepository(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    @exception_logger
    async def add_and_commit(self, obj):
        self.db.add(obj)
        await self.db.commit()

    @exception_logger
    async def add_and_flush(self, obj):
        self.db.add(obj)
        await self.db.flush()
