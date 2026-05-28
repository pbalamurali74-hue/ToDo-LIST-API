import os
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from app.database import engine, Base
from app.middleware import limiter, rate_limit_handler
from app.routers import auth, todos

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List RESTful API",
    description="Secure RESTful API to manage to-do lists, with user authentication and rate limiting.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure SlowAPI Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


# Custom handler for Pydantic input validation errors to return 400 Bad Request
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        loc = error.get("loc", [])
        field = (
            ".".join([str(x) for x in loc[1:]])
            if len(loc) > 1
            else ".".join([str(x) for x in loc])
        )
        errors.append({"field": field, "message": error.get("msg")})

    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "errors": errors},
    )


# Centralized error fallback for internal server errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    if os.getenv("APP_ENV") != "test":
        import traceback

        print(f"Generic error caught: {str(exc)}")
        traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


# Register API routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(todos.router, prefix="/todos", tags=["Todos"])

# Ensure static files directory exists and mount it
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Serve the user-friendly Single-Page Application (SPA) dashboard at the root
@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")
