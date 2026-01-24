"""
Rate Limiting Middleware
"""
from fastapi import Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from redis import asyncio as aioredis
from typing import Optional
from loguru import logger

from app.core.config import settings


class RateLimiter:
    """
    Custom rate limiter with Redis backend
    
    Provides:
    - Per-IP rate limiting
    - Per-user rate limiting
    - Different limits for different endpoint types
    """
    
    def __init__(self):
        self.redis_client: Optional[aioredis.Redis] = None
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("Redis rate limiter initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Redis for rate limiting: {str(e)}")
            self.redis_client = None
    
    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int = 60
    ) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            key: Unique identifier (IP, user_id, etc.)
            limit: Maximum number of requests
            window: Time window in seconds
        
        Returns:
            True if within limit, False otherwise
        """
        if not self.redis_client:
            # If Redis is not available, allow request
            return True
        
        try:
            current = await self.redis_client.get(key)
            
            if current is None:
                # First request
                await self.redis_client.setex(key, window, 1)
                return True
            
            current_count = int(current)
            
            if current_count >= limit:
                return False
            
            # Increment counter
            await self.redis_client.incr(key)
            return True
            
        except Exception as e:
            logger.error(f"Rate limit check error: {str(e)}")
            # On error, allow request
            return True
    
    async def get_rate_limit_key(
        self,
        request: Request,
        endpoint: str
    ) -> str:
        """
        Generate rate limit key
        
        Uses:
        - User ID if authenticated
        - IP address otherwise
        """
        # Try to get user from request state
        user_id = getattr(request.state, "user_id", None)
        
        if user_id:
            return f"rate_limit:user:{user_id}:{endpoint}"
        
        # Fall back to IP address
        client_ip = get_remote_address(request)
        return f"rate_limit:ip:{client_ip}:{endpoint}"
    
    async def check_login_rate_limit(self, request: Request) -> bool:
        """
        Check rate limit for login endpoint
        
        Limit: 5 requests per minute per IP
        """
        client_ip = get_remote_address(request)
        key = f"rate_limit:login:{client_ip}"
        
        is_allowed = await self.check_rate_limit(
            key=key,
            limit=settings.LOGIN_RATE_LIMIT_PER_MINUTE,
            window=60
        )
        
        if not is_allowed:
            logger.warning(f"Login rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please try again later.",
                headers={"Retry-After": "60"}
            )
        
        return True
    
    async def check_general_rate_limit(self, request: Request) -> bool:
        """
        Check rate limit for general endpoints
        
        Limit: 100 requests per minute per user/IP
        """
        key = await self.get_rate_limit_key(request, "general")
        
        is_allowed = await self.check_rate_limit(
            key=key,
            limit=settings.RATE_LIMIT_PER_MINUTE,
            window=60
        )
        
        if not is_allowed:
            logger.warning(f"Rate limit exceeded for key: {key}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": "60"}
            )
        
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()