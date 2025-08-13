import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from core.exceptions import UserNotFoundError
from domain.user import User
from infra.repo.user import UserRepository
from schema.user import UserCreate, UserResponse

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def list_all_users(self):
        logger.info("list all users")
        users = await self._user_repo.get_all()
        return [UserResponse(**user.__dict__) for user in users]

    async def get_user_by_id(self, user_id: UUID):
        logger.info("get user", extra={"user_id": user_id})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        return UserResponse(**user.__dict__)

    async def create_user(self, data: UserCreate) -> UserResponse:
        logger.info("creating new user", extra={"user_name": data.name})
        user_create = User(
            id=uuid4(),
            name=data.name,
            email=data.email,
            created_at=datetime.now(timezone.utc),
        )
        user = await self._user_repo.create(user_create)

        logger.info("user created", extra={"user_name": data.name})
        return UserResponse(**user.__dict__)
