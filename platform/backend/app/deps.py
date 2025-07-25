from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request

from core.config import get_settings
from services.doc_service import DocService
from services.user_service import UserService
from utils.storage import MinioClient

settings = get_settings()

# Minio client use connection pool internally, stateless, and safe to share
# singleton pattern improves performance and avoid problems with closing aiohttp.ClientSession
storage_client = MinioClient(settings)


async def get_storage_client() -> MinioClient:
    return storage_client


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.DB.async_session() as session:
        yield session


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_doc_service(
    db: AsyncSession = Depends(get_db),
    storage: MinioClient = Depends(get_storage_client),
) -> DocService:
    return DocService(db, storage)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DocServiceDep = Annotated[DocService, Depends(get_doc_service)]
