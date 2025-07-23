import contextvars

context_request_id = contextvars.ContextVar("request_id", default=None)
