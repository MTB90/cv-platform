from typing import AsyncGenerator, Annotated

from fastapi import Depends
from infra.repo.doc import DocRepository
from infra.repo.job import JobRepository
from infra.repo.user import UserRepository
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from services.doc_service import DocService
from services.user_service import UserService
from utils.database import DB
from utils.storage import StorageClient

settings = get_settings()
storage = StorageClient(settings)
database = DB(settings)

user_repo = UserRepository()
doc_repo = DocRepository()
job_repo = JobRepository()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # Create new database session
    async with database.async_session() as session:
        yield session


# Utils dependencies
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


# Services dependencies
async def get_user_service(db: DatabaseDep) -> UserService:
    return UserService(db, user_repo)


async def get_doc_service(db: DatabaseDep) -> DocService:
    return DocService(db, storage, user_repo, doc_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DocServiceDep = Annotated[DocService, Depends(get_doc_service)]
