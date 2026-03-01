from fastapi import Request
from fastapi.responses import JSONResponse

from utils.config import CORS_ORIGINS


async def check_allowed_origin(request: Request, call_next):
    origin = request.headers.get("origin")
    if origin and origin in CORS_ORIGINS.split(","):
        response = await call_next(request)
        return response
    else:
        return JSONResponse(
            status_code=403,
            content={"detail": "Origin not allowed"}
        )
