"""
User Profile Management Endpoints
"""
from fastapi import APIRouter, Depends, status, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from typing import List

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_staff
from app.dependencies.pagination import PaginationParams
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    EmailCheckResponse,
    UserCountResponse,
)
from app.schemas.common import PaginatedResponse, SuccessResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/create",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="""
    Create a new user account with the following features:
    - Generates secure random password
    - Sends email confirmation link
    - Logs audit trail
    - Returns user details (excluding sensitive data)
    
    **Required permissions**: STAFF, SUPERVISOR, or SUPERADMIN role
    """,
    response_description="Successfully created user",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "user_role": "customer",
                        "is_active": True
                    }
                }
            }
        },
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"},
    }
)
async def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(require_staff),
    db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    try:
        user_service = UserService(db)
        user = await user_service.create_user(
            user_data=user_data,
            created_by=current_user["email"]
        )
        return user
    except Exception as e:
        logger.error(f"Create user error: {str(e)}")
        raise


@router.get(
    "/check-email/{email}",
    response_model=EmailCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Check email existence",
    description="Check if an email address is already registered in the system.",
    responses={
        200: {"description": "Email check result"},
    }
)
async def check_email(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Check if email exists"""
    try:
        user_service = UserService(db)
        exists = await user_service.check_email_exists(email=email)
        return EmailCheckResponse(exists=exists)
    except Exception as e:
        logger.error(f"Check email error: {str(e)}")
        raise


@router.get(
    "/email/{email}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by email",
    description="""
    Fetch user details by email address.
    
    **Required permissions**: STAFF, SUPERVISOR, or SUPERADMIN role
    """,
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
    }
)
async def get_user_by_email(
    email: str,
    current_user: dict = Depends(require_staff),
    db: AsyncSession = Depends(get_db)
):
    """Get user by email"""
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_email(email=email)
        return user
    except Exception as e:
        logger.error(f"Get user by email error: {str(e)}")
        raise


@router.get(
    "/active",
    response_model=PaginatedResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List active users",
    description="""
    Get paginated list of all active users.
    
    Supports:
    - Pagination (page, page_size)
    - Sorting (sort_by, sort_order)
    
    **Required permissions**: STAFF, SUPERVISOR, or SUPERADMIN role
    """,
    responses={
        200: {"description": "List of active users"},
    }
)
async def get_active_users(
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(require_staff),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of active users"""
    try:
        user_service = UserService(db)
        result = await user_service.get_active_users(
            skip=pagination.skip,
            limit=pagination.page_size,
            sort_by=pagination.sort_by,
            sort_order=pagination.sort_order
        )
        return result
    except Exception as e:
        logger.error(f"Get active users error: {str(e)}")
        raise


@router.get(
    "/active/count",
    response_model=UserCountResponse,
    status_code=status.HTTP_200_OK,
    summary="Count active users",
    description="""
    Get total count of active users.
    
    **Required permissions**: STAFF, SUPERVISOR, or SUPERADMIN role
    """,
    responses={
        200: {"description": "Count of active users"},
    }
)
async def count_active_users(
    current_user: dict = Depends(require_staff),
    db: AsyncSession = Depends(get_db)
):
    """Count active users"""
    try:
        user_service = UserService(db)
        count = await user_service.count_active_users()
        return UserCountResponse(count=count)
    except Exception as e:
        logger.error(f"Count active users error: {str(e)}")
        raise


@router.post(
    "/upload-profile-image",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload profile image",
    description="""
    Upload user profile image.
    
    Features:
    - Accepts jpg, jpeg, png, gif, webp
    - Converts to WebP format
    - Resizes to max 800x800
    - Maintains aspect ratio
    
    **Authentication required**
    """,
    responses={
        200: {"description": "Image uploaded successfully"},
        400: {"description": "Invalid file type or size"},
        413: {"description": "File too large"},
    }
)
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload user profile image"""
    try:
        user_service = UserService(db)
        image_url = await user_service.upload_profile_image(
            user_id=current_user["id"],
            file=file
        )
        return SuccessResponse(
            message="Profile image uploaded successfully",
            data={"image_url": image_url}
        )
    except Exception as e:
        logger.error(f"Upload profile image error: {str(e)}")
        raise


@router.put(
    "/update",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user details",
    description="""
    Update user information.
    
    **Authentication required**
    
    Note: User can only update their own profile unless they have STAFF+ role.
    """,
    responses={
        200: {"description": "User updated successfully"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "User not found"},
    }
)
async def update_user(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user details"""
    try:
        user_service = UserService(db)
        user = await user_service.update_user(
            user_id=user_data.id,
            user_data=user_data,
            modified_by=current_user["email"],
            current_user=current_user
        )
        return user
    except Exception as e:
        logger.error(f"Update user error: {str(e)}")
        raise


@router.get(
    "/search/{search}",
    response_model=PaginatedResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Search users",
    description="""
    Search users by various fields:
    - First name
    - Last name
    - Email
    - Phone number
    - Created by
    
    Supports pagination and sorting.
    
    **Required permissions**: STAFF, SUPERVISOR, or SUPERADMIN role
    """,
    responses={
        200: {"description": "Search results"},
    }
)
async def search_users(
    search: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(require_staff),
    db: AsyncSession = Depends(get_db)
):
    """Search users"""
    try:
        user_service = UserService(db)
        skip = (page - 1) * page_size
        result = await user_service.search_users(
            search_term=search,
            skip=skip,
            limit=page_size,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return result
    except Exception as e:
        logger.error(f"Search users error: {str(e)}")
        raise