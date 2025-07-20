from typing import List

from fastapi import APIRouter, Depends
from fastapi import status

from dependencies.repo import user_repository
from repository.user import UserRepository
from schema.user import UserCreate, User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
async def list_users(user_repo: UserRepository = Depends(user_repository)):
    return await user_repo.get_all()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_repo: UserRepository = Depends(user_repository)):
    return await user_repo.create(user)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, user_repo: UserRepository = Depends(user_repository)):
    return await user_repo.get_by_id(user_id)
