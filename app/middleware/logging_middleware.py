"""
Request/Response Logging Middleware
"""
from fastapi import Request
from loguru import logger
import time
from app.core.logging_config import sanitize_log_data


async def log_requests(request: Request, call_next):
    """
    Log all incoming requests and outgoing responses
    
    Logs:
    - Request method, path, and client IP
    - Request headers (sanitized)
    - Response status code
    - Processing time
    """
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        f"Incoming request: {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )
    
    # Log request details (debug level)
    if logger.level("DEBUG").no <= logger._core.min_level:
        logger.debug(
            f"Request details - "
            f"Method: {request.method}, "
            f"Path: {request.url.path}, "
            f"Query params: {dict(request.query_params)}"
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
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} - "
            f"Time: {process_time:.3f}s - "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise