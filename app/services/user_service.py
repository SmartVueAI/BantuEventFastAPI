"""
User Service
"""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from loguru import logger
import json

from app.crud.user import (
    create_user as crud_create_user,
    update_user as crud_update_user,
    get_active_users as crud_get_active_users,
    count_active_users as crud_count_active_users,
    search_users as crud_search_users,
    get_user_by_email as crud_get_user_by_email,
    check_email_exists as crud_check_email_exists,
    get_user_by_id,
)
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.audit_service import AuditService
from app.services.image_service import ImageService
from app.services.email_service import send_user_creation_email
from app.exceptions import (
    UserNotFoundException,
    DuplicateEmailException,
    InsufficientPermissionsException,
)
from app.enums import AuditTypeEnum, UserRoleEnum
import math


class UserService:
    """User business logic service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit_service = AuditService(db)
        self.image_service = ImageService()
    
    async def create_user(self, user_data: UserCreate, created_by: str) -> UserResponse:
        """Create a new user"""
        try:
            # Check if email exists
            exists = await crud_check_email_exists(self.db, user_data.email)
            if exists:
                raise DuplicateEmailException()
            
            # Create user
            user, generated_password = await crud_create_user(self.db, user_data, created_by)
            
            # Send creation email
            await send_user_creation_email(
                to_email=user.email,
                first_name=user.first_name or "User",
                verification_token=user.verification_token,
                generated_password=generated_password
            )
            
            # Log audit
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.CREATE,
                user_role=user.user_role,
                module_name="User Management",
                table_name="users",
                processor_email=created_by,
                processed_by=created_by,
                new_values=json.dumps({
                    "id": user.id,
                    "email": user.email,
                    "user_role": user.user_role.value
                })
            )
            
            await self.db.commit()
            
            return UserResponse.model_validate(user)
            
        except Exception as e:
            logger.error(f"Create user error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def check_email_exists(self, email: str) -> bool:
        """Check if email exists"""
        return await crud_check_email_exists(self.db, email)
    
    async def get_user_by_email(self, email: str) -> UserResponse:
        """Get user by email"""
        user = await crud_get_user_by_email(self.db, email)
        if not user:
            raise UserNotFoundException()
        return UserResponse.model_validate(user)
    
    async def get_active_users(
        self, skip: int, limit: int, sort_by: str, sort_order: str
    ) -> dict:
        """Get paginated active users"""
        users, total = await crud_get_active_users(
            self.db, skip, limit, sort_by, sort_order
        )
        
        pages = math.ceil(total / limit) if total > 0 else 0
        current_page = (skip // limit) + 1
        
        return {
            "items": [UserResponse.model_validate(u) for u in users],
            "total": total,
            "page": current_page,
            "page_size": limit,
            "pages": pages,
            "has_next": current_page < pages,
            "has_previous": current_page > 1,
        }
    
    async def count_active_users(self) -> int:
        """Count active users"""
        return await crud_count_active_users(self.db)
    
    async def upload_profile_image(self, user_id: int, file: UploadFile) -> str:
        """Upload user profile image"""
        try:
            user = await get_user_by_id(self.db, user_id)
            if not user:
                raise UserNotFoundException()
            
            # Process image
            image_url = await self.image_service.process_profile_image(
                file=file,
                user_id=user_id,
                old_filename=user.profile_image_file_name
            )
            
            # Update user
            user.profile_image_URL = image_url
            user.profile_image_file_name = image_url.split("/")[-1]
            user.upload_profile_image_date_time = datetime.utcnow()
            
            await self.db.commit()
            
            # Log audit
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=user.user_role,
                module_name="User Management",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}",
                new_values=json.dumps({"profile_image_URL": image_url})
            )
            
            return image_url
            
        except Exception as e:
            logger.error(f"Upload profile image error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def update_user(
        self, user_id: int, user_data: UserUpdate, modified_by: str, current_user: dict
    ) -> UserResponse:
        """Update user"""
        try:
            # Check permissions
            if current_user["id"] != user_id:
                # Only staff+ can update other users
                if current_user["user_role"] not in [
                    UserRoleEnum.STAFF.value,
                    UserRoleEnum.SUPERVISOR.value,
                    UserRoleEnum.SUPERADMIN.value,
                ]:
                    raise InsufficientPermissionsException()
            
            # Get old values
            old_user = await get_user_by_id(self.db, user_id)
            if not old_user:
                raise UserNotFoundException()
            
            old_values = {
                "first_name": old_user.first_name,
                "last_name": old_user.last_name,
                "phone_number": old_user.phone_number,
                "location": old_user.location,
            }
            
            # Update user
            user = await crud_update_user(self.db, user_id, user_data, modified_by)
            if not user:
                raise UserNotFoundException()
            
            new_values = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "location": user.location,
            }
            
            await self.db.commit()
            
            # Log audit
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=user.user_role,
                module_name="User Management",
                table_name="users",
                processor_email=modified_by,
                processed_by=modified_by,
                old_values=json.dumps(old_values),
                new_values=json.dumps(new_values)
            )
            
            return UserResponse.model_validate(user)
            
        except Exception as e:
            logger.error(f"Update user error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def search_users(
        self, search_term: str, skip: int, limit: int, sort_by: str, sort_order: str
    ) -> dict:
        """Search users"""
        users, total = await crud_search_users(
            self.db, search_term, skip, limit, sort_by, sort_order
        )
        
        pages = math.ceil(total / limit) if total > 0 else 0
        current_page = (skip // limit) + 1
        
        return {
            "items": [UserResponse.model_validate(u) for u in users],
            "total": total,
            "page": current_page,
            "page_size": limit,
            "pages": pages,
            "has_next": current_page < pages,
            "has_previous": current_page > 1,
        }