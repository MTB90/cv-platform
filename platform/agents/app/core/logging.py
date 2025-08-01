import logging
import sys

from pythonjsonlogger import json
from core.context import context_request_id


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
    handler.addFilter(RequestIdFilter())

    # Main app logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
