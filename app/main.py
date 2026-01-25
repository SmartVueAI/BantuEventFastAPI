"""
Main FastAPI Application Entry Point
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
from loguru import logger
from pathlib import Path

from app.core.config import settings
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()

# Initialize FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sonma Hair E-Commerce Platform API",
    docs_url="/documentation",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Page", "X-Page-Size"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts_list,
)

# Ensure static directories exist
Path("static/profile_images").mkdir(parents=True, exist_ok=True)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# SSRF Protection Middleware
@app.middleware("http")
async def ssrf_protection(request: Request, call_next):
    """Block access to metadata endpoints and internal IPs"""
    path = request.url.path
    
    # Block metadata endpoint access
    if "/latest/meta-data" in path or "169.254.169.254" in str(request.url):
        logger.warning(f"Blocked SSRF attempt: {request.url} from {request.client.host}")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Access forbidden"}
        )
    
    response = await call_next(request)
    return response

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    #response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    start_time = time.time()
    
    # Log request
    logger.info(
        f"Request: {request.method} {request.url.path} from {request.client.host}"
    )
    
    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"Path: {request.url.path}"
        )
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Error processing request: {request.method} {request.url.path} - "
            f"Time: {process_time:.3f}s - Error: {str(e)}",
            exc_info=True
        )
        raise

# Include API Routers
from app.api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")

# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time()
    }

# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/documentation",
        "redoc": "/redoc",
        "health": "/health",
        "status": "running"
    }

# Startup Event
@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info("Application startup complete")

# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")
    logger.info("Application shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )