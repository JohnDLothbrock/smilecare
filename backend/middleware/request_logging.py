import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.core.logger import get_logger


logger = get_logger("requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        client_host = "unknown"

        if request.client is not None:
            client_host = request.client.host

        try:
            response = await call_next(request)

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            logger.info(
                "request_id=%s method=%s path=%s status_code=%s duration_ms=%s client=%s",
                request_id,
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
                client_host
            )

            response.headers["X-Request-ID"] = request_id

            return response

        except Exception:
            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            logger.exception(
                "request_id=%s method=%s path=%s unhandled_error duration_ms=%s client=%s",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
                client_host
            )

            raise