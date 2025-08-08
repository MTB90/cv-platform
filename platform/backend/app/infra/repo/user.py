import logging
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.user import User
from infra.models import UserModel
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    async def get_all(self) -> Sequence[User]:
        result = await self.db.execute(select(UserModel))
        user_records = result.scalars().all()

        return [User(**user_record.__dict__) for user_record in user_records]

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user_record = result.scalar_one_or_none()

        if user_record is None:
            return None

        return User(**user_record.__dict__)

    async def create(self, user: User) -> User:
        user_record = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
        )

        try:
            await self.add_and_commit(user_record)
        except IntegrityError:
            raise ConflictError(
                message="User Creation Failed",
                field="email",
                expected="unique email",
            )
        await self.db.refresh(user_record)

        user.created_at = user_record.created_at
        return user
