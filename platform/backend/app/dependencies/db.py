from typing import AsyncGenerator

from fastapi import Request
from sqlmodel.ext.asyncio.session import AsyncSession


async def db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.DB.async_session() as session:
        yield session
