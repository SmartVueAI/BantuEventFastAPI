"""
User CRUD Operations
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from loguru import logger

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.utils import (
    generate_random_password,
    generate_verification_token,
    generate_security_stamp,
)


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Get user by ID"""
    try:
        result = await db.execute(select(User).where(User.id == 1, User.is_deleted == False))
        # result = await db.execute(select(User).where(User.id == user_id, User.is_deleted == False))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {str(e)}")
        raise


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get user by email"""
    try:
        normalized_email = email.upper()
        result = await db.execute(
            select(User).where(
                User.normalized_email == normalized_email,
                User.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting user by email {email}: {str(e)}")
        raise


async def check_email_exists(db: AsyncSession, email: str) -> bool:
    """Check if email already exists"""
    try:
        user = await get_user_by_email(db, email)
        return user is not None
    except Exception as e:
        logger.error(f"Error checking email existence: {str(e)}")
        raise


async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
    created_by: str
) -> tuple[User, str]:
    """
    Create a new user
    Returns: (user, generated_password)
    """
    try:
        # Generate password and tokens
        generated_password = generate_random_password()
        hashed_password = get_password_hash(generated_password)
        verification_token = generate_verification_token()
        security_stamp = generate_security_stamp()

        # Create user instance
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            normalized_email=user_data.email.upper(),
            gender=user_data.gender,
            user_role=user_data.user_role,
            phone_number=user_data.phone_number,
            location=user_data.location,
            job_title=user_data.job_title,
            hashed_password=hashed_password,
            verification_token=verification_token,
            security_stamp=security_stamp,
            default_password=True,
            email_confirmed=False,
            is_active=True,
            created_by=created_by,
        )

        db.add(user)
        await db.flush()
        await db.refresh(user)

        logger.info(f"User created successfully: {user.email}")
        return user, generated_password

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate,
    modified_by: str
) -> Optional[User]:
    """Update user details"""
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            return None

        # Update fields
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        if user_data.phone_number is not None:
            user.phone_number = user_data.phone_number
        if user_data.location is not None:
            user.location = user_data.location
        if user_data.job_title is not None:
            user.job_title = user_data.job_title
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        user.last_modified_by = modified_by

        await db.flush()
        await db.refresh(user)

        logger.info(f"User updated successfully: {user.email}")
        return user

    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise


async def get_active_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> tuple[List[User], int]:
    """Get paginated list of active users"""
    try:
        # Count query
        count_query = select(func.count()).select_from(User).where(
            User.is_active == True,
            User.is_deleted == False
        )
        total = await db.scalar(count_query)

        # Data query
        query = select(User).where(
            User.is_active == True,
            User.is_deleted == False
        )

        # Sorting
        if sort_order == "desc":
            query = query.order_by(getattr(User, sort_by).desc())
        else:
            query = query.order_by(getattr(User, sort_by).asc())

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        users = result.scalars().all()

        return list(users), total or 0

    except Exception as e:
        logger.error(f"Error getting active users: {str(e)}")
        raise


async def count_active_users(db: AsyncSession) -> int:
    """Count active users"""
    try:
        query = select(func.count()).select_from(User).where(
            User.is_active == True,
            User.is_deleted == False
        )
        result = await db.scalar(query)
        return result or 0
    except Exception as e:
        logger.error(f"Error counting active users: {str(e)}")
        raise


async def search_users(
    db: AsyncSession,
    search_term: str,
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> tuple[List[User], int]:
    """Search users by various fields"""
    try:
        search_pattern = f"%{search_term}%"

        # Count query
        count_query = select(func.count()).select_from(User).where(
            User.is_deleted == False,
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.phone_number.ilike(search_pattern),
                User.created_by.ilike(search_pattern),
            )
        )
        total = await db.scalar(count_query)

        # Data query
        query = select(User).where(
            User.is_deleted == False,
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.phone_number.ilike(search_pattern),
                User.created_by.ilike(search_pattern),
            )
        )

        # Sorting
        if sort_order == "desc":
            query = query.order_by(getattr(User, sort_by).desc())
        else:
            query = query.order_by(getattr(User, sort_by).asc())

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        users = result.scalars().all()

        return list(users), total or 0

    except Exception as e:
        logger.error(f"Error searching users: {str(e)}")
        raise
