from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from services.doc_service import DocService
from services.user_service import UserService
from utils.database import DB
from utils.storage import StorageClient

_settings = get_settings()
_storage = StorageClient(_settings)
_database = DB(_settings)


async def get_storage() -> StorageClient:
    # Storage client (Minio) use connection pool internally,
    # stateless, and safe to share singleton pattern improves performance
    # and avoid problems with closing aiohttp.ClientSession
    return _storage


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # Create new database session
    async with _database.async_session() as session:
        yield session


# Utils dependencies
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
StorageDep = Annotated[StorageClient, Depends(get_storage)]


# Services dependencies
async def get_user_service(db: DatabaseDep) -> UserService:
    return UserService(db)


async def get_doc_service(db: DatabaseDep, storage: StorageDep) -> DocService:
    return DocService(db, storage)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DocServiceDep = Annotated[DocService, Depends(get_doc_service)]
