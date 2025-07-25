import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import api
from core.config import get_settings
from core.context import context_request_id
from core.exceptions import BaseError
from core.logging import setup_logging
from utils.database import DB

settings = get_settings()
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


@app.get("/healthz")
async def health():
    return {"message": "ok"}


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    # Ignore specific endpoints
    if request.url.path in ["/healthz"]:
        return await call_next(request)

    # Save to context var and request.state
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    context_request_id.set(request_id)
    request.state.request_id = request_id

    logger.info("request", extra={"method": request.method, "path": request.url.path})
    response = await call_next(request)

    if response.status_code < 400:
        logger.info("response", extra={"status_code": response.status_code})
    else:
        logger.error("response", extra={"status_code": response.status_code})

    # Add to response headers
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(BaseError)
async def business_error_handler(request: Request, exc: BaseError):
    logger.error(
        f"error: {exc.message}",
        extra={"type": type(exc).__name__, "exc": str(exc)},
    )

    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

    # Also add it to headers for consistency
    request_id = getattr(request.state, "request_id", None)
    if request_id:
        response.headers["X-Request-ID"] = request_id

    return response


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.error("unexpected error", exc_info=True)

    response = JSONResponse(
        status_code=500, content={"detail": "Internal server error"}
    )

    # Also add it to headers for consistency
    request_id = getattr(request.state, "request_id", None)
    if request_id:
        response.headers["X-Request-ID"] = request_id

    return response
