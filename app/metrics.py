import time

from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, Counter, Histogram, generate_latest, PROCESS_COLLECTOR
from prometheus_client.gc_collector import GC_COLLECTOR
from prometheus_client.platform_collector import PLATFORM_COLLECTOR
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

METRICS_ENDPOINT = "/metrics"

REGISTRY.unregister(GC_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(PROCESS_COLLECTOR)

request_count = Counter(
    "http_requests_total",
    "Total number of HTTP requests, by status code",
    ["status_code"],
)

request_latency = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
)


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == METRICS_ENDPOINT:
            return await call_next(request)

        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        request_count.labels(status_code=response.status_code).inc()
        request_latency.observe(duration)

        return response


def get_metrics() -> Response:
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
