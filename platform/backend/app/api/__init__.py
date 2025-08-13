from fastapi import APIRouter

from api.v1 import users, docs, jobs
from api.private import webhooks
from core.config import get_settings

settings = get_settings()
router = APIRouter()

# Public APIs
router.include_router(users.router, prefix=settings.API_V1)
router.include_router(docs.router, prefix=settings.API_V1)
router.include_router(jobs.router, prefix=settings.API_V1)

# Private APIs
router.include_router(webhooks.router, prefix=settings.API_PRIVATE)
