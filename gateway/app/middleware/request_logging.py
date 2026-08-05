import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("gateway.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started_at = time.perf_counter()
        request_id = getattr(getattr(request, "state", None), "request_id", "unknown")

        logger.info("Started %s %s [request_id=%s]", request.method, request.url.path, request_id)

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "Unhandled exception while processing %s %s [request_id=%s]",
                request.method,
                request.url.path,
                request_id,
            )
            raise

        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.info(
            "Completed %s %s -> %s in %.2fms [request_id=%s]",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )
        return response
