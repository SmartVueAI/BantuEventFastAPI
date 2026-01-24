"""
API Router Aggregator
"""
from fastapi import APIRouter

from app.api.v1.endpoints import user_profile, user_access

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    user_profile.router,
    prefix="/users",
    tags=["User Profile Management"]
)

api_router.include_router(
    user_access.router,
    prefix="/auth",
    tags=["User Access Management"]
)