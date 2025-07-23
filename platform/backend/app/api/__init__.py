from fastapi import APIRouter


from api.v1 import users, docs
from core.config import settings

router = APIRouter()

# Public APIs
router.include_router(users.router, prefix=settings.API_V1)
router.include_router(docs.router, prefix=settings.API_V1)

# Private APIs
