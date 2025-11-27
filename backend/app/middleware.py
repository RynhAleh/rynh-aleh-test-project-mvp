import asyncio
import random
from starlette.middleware.base import BaseHTTPMiddleware


class RandomDelayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path in ("/api/submit", "/api/history"):
            await asyncio.sleep(random.uniform(0.1, 3.0))
        return await call_next(request)
