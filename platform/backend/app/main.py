import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import api
from core.context import context_request_id
from core.config import settings
from core.exceptions import BaseApiError
from core.logging import setup_logging
from utils.database import DB

setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up logic
    app.state.DB = DB(settings)
    yield
    # Clean up logic


def build_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api.router)
    return application


app = build_app()


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    # Save to context var and request.state
    context_request_id.set(request_id)
    request.state.request_id = request_id

    logger.info(
        "Request received", extra={"method": request.method, "path": request.url.path}
    )

    # Endpoint call
    response = await call_next(request)

    # Add to response headers
    response.headers["X-Request-ID"] = request_id

    logger.info("Response sent", extra={"status_code": response.status_code})
    return response


@app.exception_handler(BaseApiError)
async def exception_handler(request: Request, exc: BaseApiError):
    logger.error(f"Exception: {exc}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
