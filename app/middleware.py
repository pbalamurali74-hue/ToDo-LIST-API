import os
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

app_env = os.getenv("APP_ENV", "development")

# Initialize slowapi rate limiter, disabled in test environment
limiter = Limiter(
    key_func=get_remote_address,
    enabled=(app_env != "test"),
)


def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "message": "Too many requests, please try again after 15 minutes"
        },
    )
