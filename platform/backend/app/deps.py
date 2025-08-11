from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from infra.repo.doc import DocRepository
from infra.repo.user import UserRepository
from services.doc_service import DocService
from services.user_service import UserService
from utils.database import DB
from utils.storage import StorageClient

settings = get_settings()
storage = StorageClient(settings)
database = DB(settings)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # Create new database session
    async with database.async_session() as session:
        yield session


# Utils dependencies
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


# Services dependencies
async def get_user_service(db: DatabaseDep) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)


async def get_doc_service(db: DatabaseDep) -> DocService:
    user_repo = UserRepository(db)
    doc_repo = DocRepository(db)

    return DocService(storage, user_repo, doc_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DocServiceDep = Annotated[DocService, Depends(get_doc_service)]
