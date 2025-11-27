import time
import random
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RandomDelayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # apply delay ONLY for needed endpoints
        if request.url.path in (
            "/api/submit",
            "/api/history",
        ):
            time.sleep(random.uniform(0.1, 3.0))

        response = await call_next(request)
        return response
