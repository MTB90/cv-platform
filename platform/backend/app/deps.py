from typing import AsyncGenerator, Annotated, cast

from fastapi import Depends
from fastapi import Request
from sqlmodel.ext.asyncio.session import AsyncSession

from infra.repo.doc import DocRepository
from infra.repo.job import JobRepository
from infra.repo.user import UserRepository
from services.doc_service import DocService
from services.job_service import JobService
from services.user_service import UserService
from utils.database import DB
from utils.storage import StorageClient


class AppState:
    database: DB
    storage: StorageClient


def get_app_state(request: Request) -> AppState:
    return cast(AppState, request.app.state)


AppStateDep = Annotated[AppState, Depends(get_app_state)]


async def get_db(app_state: AppStateDep) -> AsyncGenerator[AsyncSession, None]:
    # Create new database session
    async with app_state.database.async_session() as session:
        yield session


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


# Services dependencies
async def get_user_service(db: DatabaseDep) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)


async def get_doc_service(app_state: AppStateDep, db: DatabaseDep) -> DocService:
    user_repo = UserRepository(db)
    doc_repo = DocRepository(db)
    return DocService(app_state.storage, user_repo, doc_repo)


async def get_job_service(db: DatabaseDep) -> JobService:
    user_repo = UserRepository(db)
    doc_repo = DocRepository(db)
    job_repo = JobRepository(db)
    return JobService(user_repo, doc_repo, job_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DocServiceDep = Annotated[DocService, Depends(get_doc_service)]
JobServiceDep = Annotated[JobService, Depends(get_job_service)]
