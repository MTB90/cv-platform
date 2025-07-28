import logging
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from models import User
from repository.base import BaseRepository
from schema.user import UserCreate

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    async def get_all(self) -> Sequence[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            name=user_data.name,
            email=user_data.email,
        )

        try:
            await self.add_and_commit(user)
        except IntegrityError:
            raise ConflictError(
                message="User Creation Failed",
                field="email",
                expected="unique email",
            )

        await self.db.refresh(user)
        return user
