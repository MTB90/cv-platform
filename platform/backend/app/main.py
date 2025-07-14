from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import health
from core.config import settings
from database import DB


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up logic
    app.state.DB = DB(
        settings.CV_BACKEND_DB_USER,
        settings.CV_BACKEND_DB_PASS,
        settings.CV_BACKEND_DB_HOST
    )
    yield
    # Clean up logic


def build_app() -> FastAPI:
    application = FastAPI(title=settings.CV_BACKEND_PROJECT_NAME, lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # add here all routes
    application.include_router(health.router, prefix=settings.API_PRIVATE)

    return application


app = build_app()
