import logging
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from infra.repo.base import BaseRepository
from infra.models import UserModel
from schema.user import UserCreate

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    async def get_all(self) -> Sequence[UserModel]:
        result = await self.db.execute(select(UserModel))
        return result.scalars().all()

    async def get_by_id(self, user_id: UUID) -> Optional[UserModel]:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> UserModel:
        user = UserModel(
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
