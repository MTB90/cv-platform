from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.DB.async_session() as session:
        yield session
