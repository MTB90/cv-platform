import logging
import sys

from pythonjsonlogger import json

from core.context import context_request_id


class SensitiveFilter(logging.Filter):
    SENSITIVE_KEYS = {"password", "secret", "token", "authorization", "api_key"}

    def filter(self, record):
        if hasattr(record, "args") and isinstance(record.args, dict):
            record.args = {
                k: ("***" if k.lower() in self.SENSITIVE_KEYS else v)
                for k, v in record.args.items()
            }
        return True


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        try:
            record.request_id = context_request_id.get()
        except LookupError:
            record.request_id = None
        return True


def setup_logging(log_level: str = "INFO"):
    log_level = logging.getLevelName(log_level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = json.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(message)s %(request_id)s",
        rename_fields={"asctime": "timestamp", "levelname": "level"},
    )

    handler.setFormatter(formatter)
    handler.addFilter(SensitiveFilter())
    handler.addFilter(RequestIdFilter())

    # Main app logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Gunicorn logger
    gunicorn_logger = logging.getLogger("gunicorn")
    gunicorn_logger.setLevel(logging.INFO)
    gunicorn_logger.handlers = []
    gunicorn_logger.addHandler(handler)
    gunicorn_logger.propagate = False

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.handlers = []
    uvicorn_logger.addHandler(handler)
    uvicorn_logger.propagate = False

    # Uvicorn error logs (exceptions, tracebacks)
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.setLevel(logging.WARNING)
    uvicorn_error_logger.handlers = []
    uvicorn_error_logger.addHandler(handler)
    uvicorn_error_logger.propagate = False

    # SQLAlchemy engine logs
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine.Engine")
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.handlers = []
    sqlalchemy_logger.addHandler(handler)
    sqlalchemy_logger.propagate = False
