from typing import AsyncGenerator

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request

from repository.user import UserRepository


async def db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.DB.async_session() as session:
        yield session


async def user_repository(db: AsyncSession = Depends(db_session)) -> UserRepository:
    return UserRepository(db)
