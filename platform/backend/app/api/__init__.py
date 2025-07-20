from fastapi import APIRouter

from app.api.private import health
from app.api.v1 import users
from core.config import settings

router = APIRouter()

# Public APIs
router.include_router(users.router, prefix=settings.API_V1, tags=["users"])

# Private APIs
router.include_router(health.router, prefix=settings.API_PRIVATE, tags=["health"])
