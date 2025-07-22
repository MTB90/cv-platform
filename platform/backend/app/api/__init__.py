from fastapi import APIRouter

from app.api.private import health
from app.api.v1 import users, docs
from core.config import settings

router = APIRouter()

# Public APIs
router.include_router(users.router, prefix=settings.API_V1)
router.include_router(docs.router, prefix=settings.API_V1)

# Private APIs
router.include_router(health.router, prefix=settings.API_PRIVATE)
