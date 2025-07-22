from typing import AsyncGenerator

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request

from services.user_service import UserService


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.DB.async_session() as session:
        yield session


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
