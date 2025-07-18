from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies.db import db_session
from repository.user import UserRepository


async def user_repository(db: AsyncSession = Depends(db_session)) -> UserRepository:
    return UserRepository(db)
