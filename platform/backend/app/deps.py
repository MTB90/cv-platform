from typing import AsyncGenerator

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request

from core.config import settings
from services.doc_service import DocService
from services.user_service import UserService
from utils.storage import Storage


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.DB.async_session() as session:
        yield session


async def get_storage() -> Storage:
    return Storage(settings)


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_doc_service(
    db: AsyncSession = Depends(get_db), storage: Storage = Depends(get_storage)
) -> DocService:
    return DocService(db, storage)
