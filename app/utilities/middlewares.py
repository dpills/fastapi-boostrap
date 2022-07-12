from contextvars import ContextVar
from uuid import uuid4

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request

_trace_id_ctx_var: ContextVar[str] = ContextVar("trace_id", default=None)


def get_trace_id() -> str:
    return _trace_id_ctx_var.get()


class RequestContextTraceMiddleware(BaseHTTPMiddleware):
    """
    FastAPI Trace ID middleware implementation
    source: https://github.com/tiangolo/fastapi/issues/397
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        trace_id = _trace_id_ctx_var.set(str(uuid4()))
        response = await call_next(request)
        response.headers["X-Trace-ID"] = get_trace_id()

        _trace_id_ctx_var.reset(trace_id)
        return response
