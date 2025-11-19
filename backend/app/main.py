import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .core.config import settings
from .db.session import Base, engine
from .api.v1.auth import router as auth_router
from .api.v1.tasks import router as tasks_router
from .services.cache import close_redis_connection

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, enabled=settings.RATE_LIMIT_ENABLED)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Handles:
    - Database table creation (if enabled)
    - Database connection verification
    - Cleanup on shutdown
    """
    # Startup
    logger.info("Starting up application...")

    if settings.AUTO_CREATE_TABLES:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

    # Verify database connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection verified")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    close_redis_connection()
    engine.dispose()
    logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A RESTful API for task management with JWT authentication. "
                "Provides endpoints for user registration, authentication, and task management.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware - Only allow specified origins in production
# Wildcard is only used in development when CORS_ORIGINS is empty
if settings.ENVIRONMENT == "production" and not settings.CORS_ORIGINS:
    logger.error("CORS_ORIGINS must be set in production")
    raise ValueError("CORS_ORIGINS must be set in production")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Root endpoint
@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="API Information",
    description="Get basic information about the API",
    tags=["General"]
)
def root():
    """
    Root endpoint providing API information.
    
    Returns basic information about the API including name, version, and available endpoints.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "description": "A RESTful API for task management with JWT authentication",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": {
                "register": "POST /auth/register",
                "login": "POST /auth/login"
            },
            "tasks": {
                "list": "GET /tasks",
                "create": "POST /tasks",
                "get": "GET /tasks/{task_id}",
                "update": "PUT /tasks/{task_id}",
                "delete": "DELETE /tasks/{task_id}"
            }
        }
    }


# Health check endpoint
@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check the health status of the API and database connection",
    tags=["General"]
)
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns the health status of the API and database connection.
    """
    health_status = {
        "status": "healthy",
        "api": "operational",
        "database": "unknown"
    }
    
    try:
        # Check database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = "disconnected"
        health_status["error"] = str(e)
        logger.error(f"Health check failed: {e}")
    
    if health_status["status"] == "unhealthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )
    
    return health_status


# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])


# Exception handlers
def _handle_integrity_error(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (e.g., unique constraint violations).
    """
    text = str(getattr(exc, "orig", exc))
    msg = "Resource conflict"
    
    if "users" in text.lower() and "email" in text.lower():
        msg = "Email already registered"
    elif "unique" in text.lower():
        msg = "Resource already exists"
    
    logger.warning(f"Integrity error: {msg}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": msg}
    )


def _handle_operational_error(request: Request, exc: OperationalError):
    """
    Handle database operational errors.
    """
    logger.error(f"Database operational error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )


def _handle_jwt_error(request: Request, exc: JWTError):
    """
    Handle JWT token validation errors.
    """
    logger.warning(f"JWT validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )


def _handle_value_error(request: Request, exc: ValueError):
    """
    Handle value validation errors.
    """
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc) or "Invalid input"}
    )


# Register exception handlers
app.add_exception_handler(IntegrityError, _handle_integrity_error)
app.add_exception_handler(OperationalError, _handle_operational_error)
app.add_exception_handler(JWTError, _handle_jwt_error)
app.add_exception_handler(ValueError, _handle_value_error)