import logging
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.user import User
from infra.mapper import UserMapper
from infra.models import UserModel
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    async def get_all(self, db_session) -> Sequence[User]:
        result = await db_session.execute(select(UserModel))
        user_records = result.scalars().all()

        return [UserMapper.to_domain(user_record) for user_record in user_records]

    async def get_by_id(self, db_session, user_id: UUID) -> Optional[User]:
        result = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
        user_record = result.scalar_one_or_none()

        if user_record is None:
            return None

        return UserMapper.to_domain(user_record)

    async def create(self, db_session, user: User) -> User:
        user_record = UserMapper.from_domain(user)

        try:
            await self.add_and_commit(db_session, user_record)
        except IntegrityError:
            raise ConflictError(
                message="User Creation Failed",
                field="email",
                expected="unique email",
            )
        return user
