import logging
import sys

from app.config import app_name, settings

from .middlewares import get_trace_id


class TraceFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_trace_id()
        return True


logging.basicConfig(
    stream=sys.stdout,
    level=settings.logging_level,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",  # noqa: E501
)

logger = logging.getLogger(app_name)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(settings.logging_level)
stream_handler.addFilter(TraceFilter())
stream_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] [%(trace_id)s] %(message)s"  # noqa: E501
    )
)
logger.addHandler(stream_handler)
