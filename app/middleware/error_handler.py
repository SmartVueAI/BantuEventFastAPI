"""
Global Error Handler Middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from datetime import datetime


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handling middleware
    
    Catches all unhandled exceptions and returns formatted error responses
    """
    try:
        response = await call_next(request)
        return response
    except SQLAlchemyError as e:
        logger.error(
            f"Database error: {str(e)} - "
            f"Path: {request.url.path} - "
            f"Method: {request.method}",
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Database error occurred",
                "code": "DATABASE_ERROR",
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
            }
        )
    except ValueError as e:
        logger.error(
            f"Validation error: {str(e)} - "
            f"Path: {request.url.path} - "
            f"Method: {request.method}",
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(e),
                "code": "VALIDATION_ERROR",
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
            }
        )
    except Exception as e:
        logger.error(
            f"Unhandled error: {str(e)} - "
            f"Path: {request.url.path} - "
            f"Method: {request.method}",
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error occurred",
                "code": "INTERNAL_SERVER_ERROR",
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
            }
        )