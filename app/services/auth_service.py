"""
Authentication Service
"""
from datetime import datetime
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.crud.user import get_user_by_email, get_user_by_id, get_user_by_refresh_token, logout_user
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.utils import (
    generate_otp,
    generate_guid,
    generate_verification_token,
    generate_random_password,
    generate_security_stamp,
)
from app.services.email_service import (
    send_otp_email,
    send_password_reset_email,
    send_password_changed_email,
    send_user_creation_email,
    send_account_locked_email,
)
from app.services.audit_service import AuditService
from app.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserNotActiveException,
    DefaultPasswordException,
    AccountLockedException,
    EmailNotConfirmedException,
    InvalidOTPException,
    InvalidTokenException,
)
from app.enums import AuditTypeEnum
from app.core.constants import MAX_LOGIN_ATTEMPTS


class AuthService:
    """Authentication business logic service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit_service = AuditService(db)
    

    async def login(self, email: str, password: str) -> dict:
        """
        User login
        
        Returns:
            Login response with tokens
        """
        try:
            # Get user
            user = await get_user_by_email(self.db, email)
            if not user:
                raise InvalidCredentialsException()

            # Check if user is active
            if not user.is_active:
                raise UserNotActiveException()

            # Check if email is confirmed
            if not user.email_confirmed:
                raise EmailNotConfirmedException()

            # Check if user is using default password
            if user.default_password:
                raise DefaultPasswordException()

            # Check if account is locked
            if user.lockout_enabled:
                # Log failed attempt
                await self.audit_service.log_audit(
                    audit_type=AuditTypeEnum.LOGIN,
                    user_role=user.user_role,
                    module_name="Authentication",
                    table_name="users",
                    processor_email=email,
                    processed_by=f"{user.first_name} {user.last_name}",
                    old_values=None,
                    new_values='{"status": "locked"}'
                )

                # Send account locked email
                await send_account_locked_email(
                    to_email=user.email,
                    first_name=user.first_name or "User"
                )

                raise AccountLockedException()

            # Verify password
            if not verify_password(password, user.hashed_password):
                # Increment failed attempt count
                user.access_failed_count += 1

                # Lock account if max attempts reached
                if user.access_failed_count >= MAX_LOGIN_ATTEMPTS:
                    user.lockout_enabled = True
                    user.lockout_date_time = datetime.utcnow()

                    await self.db.commit()

                    # Send account locked email
                    await send_account_locked_email(
                        to_email=user.email,
                        first_name=user.first_name or "User"
                    )

                    raise AccountLockedException()

                await self.db.commit()
                raise InvalidCredentialsException()

            # Reset failed attempt count
            user.access_failed_count = 0
            user.user_logged_In = True
            user.last_logged_in_date = datetime.utcnow()
            user.user_GUID = generate_guid()

            # Check if OTP is enabled
            if user.use_otp_enabled:
                # Generate and send OTP
                otp = generate_otp()
                user.otp = otp

                await self.db.commit()

                # Send OTP email
                await send_otp_email(
                    to_email=user.email,
                    first_name=user.first_name or "User",
                    otp=otp
                )

                return {
                    "access_token": "",
                    "refresh_token": "",
                    "token_type": "bearer",
                    "requires_otp": True,
                    "requires_password_change": user.default_password,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "user_role": user.user_role.value,
                        "gender": user.gender,
                        "phone_number": user.phone_number,
                        "location": user.location,
                        "job_title": user.job_title,
                        "email_confirmed": user.email_confirmed,
                        "is_active": user.is_active,
                        "user_logged_In": user.user_logged_In,
                        "last_logged_in_date": user.last_logged_in_date,
                        "profile_image_URL": user.profile_image_URL,
                        "created_at": user.created_at,
                        "created_by": user.created_by,
                        "last_modified_date": user.last_modified_date,
                        "last_modified_by": user.last_modified_by,
                    }
                }

            # Generate tokens
            access_token = create_access_token({
                "email": user.email,
                "user_id": user.id,
                "role": user.user_role.value
            })

            refresh_token = create_refresh_token({
                "email": user.email,
                "user_id": user.id
            })

            user.refresh_token = refresh_token
            user.refresh_token_expires = datetime.utcnow()

            await self.db.commit()

            # Log successful login
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.LOGIN,
                user_role=user.user_role,
                module_name="Authentication",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}"
            )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "requires_otp": False,
                "requires_password_change": user.default_password,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_role": user.user_role.value,
                    "gender": user.gender,
                    "phone_number": user.phone_number,
                    "location": user.location,
                    "job_title": user.job_title,
                    "email_confirmed": user.email_confirmed,
                    "is_active": user.is_active,
                    "user_logged_In": user.user_logged_In,
                    "last_logged_in_date": user.last_logged_in_date,
                    "profile_image_URL": user.profile_image_URL,
                    "created_at": user.created_at,
                    "created_by": user.created_by,
                    "last_modified_date": user.last_modified_date,
                    "last_modified_by": user.last_modified_by,
                }
            }

        except Exception as e:
            logger.error(f"Login error for {email}: {str(e)}")
            await self.db.rollback()
            raise
    async def resend_otp(self, email: str):
        """Resend OTP to user"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()
            
            # Generate new OTP
            otp = generate_otp()
            user.otp = otp
            
            await self.db.commit()
            
            # Send OTP email
            await send_otp_email(
                to_email=user.email,
                first_name=user.first_name or "User",
                otp=otp
            )
            
            logger.info(f"OTP resent to: {email}")
            
        except Exception as e:
            logger.error(f"Resend OTP error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def verify_otp(self, email: str, otp: str) -> dict:
        """Verify OTP and return tokens"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()
            
            # Verify OTP
            if user.otp != otp:
                raise InvalidOTPException()
            
            # Clear OTP
            user.otp = None
            
            # Generate tokens
            access_token = create_access_token({
                "email": user.email,
                "user_id": user.id,
                "role": user.user_role.value
            })
            
            refresh_token = create_refresh_token({
                "email": user.email,
                "user_id": user.id
            })
            
            user.refresh_token = refresh_token
            user.refresh_token_expires = datetime.utcnow()
            
            await self.db.commit()
            
            # Log successful login
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.LOGIN,
                user_role=user.user_role,
                module_name="Authentication",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}"
            )
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "requires_otp": False,
                "requires_password_change": user.default_password,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_role": user.user_role.value,
                        "gender": user.gender,
                        "phone_number": user.phone_number,
                        "location": user.location,
                        "job_title": user.job_title,
                        "email_confirmed": user.email_confirmed,
                        "is_active": user.is_active,
                        "user_logged_In": user.user_logged_In,
                        "last_logged_in_date": user.last_logged_in_date,
                        "profile_image_URL": user.profile_image_URL,
                        "created_at": user.created_at,
                        "created_by": user.created_by,
                        "last_modified_date": user.last_modified_date,
                        "last_modified_by": user.last_modified_by,
                }
            }
            
        except Exception as e:
            logger.error(f"Verify OTP error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def forgot_password(self, email: str):
        """Request password reset"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()
            
            # Generate reset token
            reset_token = generate_verification_token()
            user.verification_token = reset_token
            
            await self.db.commit()
            
            # Send password reset email
            await send_password_reset_email(
                to_email=user.email,
                first_name=user.first_name or "User",
                reset_token=reset_token
            )
            
            logger.info(f"Password reset email sent to: {email}")
            
        except Exception as e:
            logger.error(f"Forgot password error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def reset_password(self, email: str, token: str, new_password: str):
        """Reset password with token"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()
            
            # Verify token
            if user.verification_token != token:
                raise InvalidTokenException()

            # Prevent password reuse
            if verify_password(new_password, user.hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail="New password must be different from your current password."
                )

            # Update password
            user.hashed_password = get_password_hash(new_password)
            user.default_password = False
            user.last_password_changed_date = datetime.utcnow()
            user.last_modified_by = user.email
            user.last_modified_date = datetime.utcnow()
            user.verification_token = None
            
            await self.db.commit()
            
            # Send confirmation email
            await send_password_changed_email(
                to_email=user.email,
                first_name=user.first_name or "User"
            )
            
            # Log password change
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=user.user_role,
                module_name="Authentication",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}",
                new_values='{"password": "changed"}'
            )
            
            logger.info(f"Password reset for: {email}")
            
        except Exception as e:
            logger.error(f"Reset password error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def change_password(self, user_id: int, old_password: str, new_password: str):
        """Change password for authenticated user"""
        try:
            user = await get_user_by_id(self.db, user_id)
            if not user:
                raise UserNotFoundException()
            
            # Verify old password
            if not verify_password(old_password, user.hashed_password):
                raise InvalidCredentialsException("Current password is incorrect")

            # Prevent password reuse
            if verify_password(new_password, user.hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail="New password must be different from your current password."
                )

            # Update password
            user.hashed_password = get_password_hash(new_password)
            user.default_password = False
            user.last_password_changed_date = datetime.utcnow()
            user.last_modified_by = user.email
            user.last_modified_date = datetime.utcnow()

            await self.db.commit()

            # Send confirmation email
            await send_password_changed_email(
                to_email=user.email,
                first_name=user.first_name or "User"
            )

            # Log password change
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=user.user_role,
                module_name="Authentication",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}",
                new_values='{"password": "changed"}'
            )

            logger.info(f"Password changed for user: {user_id}")

        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            await self.db.rollback()
            raise

    async def new_user_change_password(self, email: str, old_password: str, new_password: str):
        """Change password for authenticated user"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()

            # Verify old password
            if not verify_password(old_password, user.hashed_password):
                raise InvalidCredentialsException(
                    "Current password is incorrect")

            # Prevent password reuse
            if verify_password(new_password, user.hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail="New password must be different from your current password."
                )

            # Update password
            user.hashed_password = get_password_hash(new_password)
            user.default_password = False
            user.last_password_changed_date = datetime.utcnow()
            user.last_modified_by = user.email
            user.last_modified_date = datetime.utcnow()

            await self.db.commit()

            # Send confirmation email
            await send_password_changed_email(
                to_email=user.email,
                first_name=user.first_name or "User"
            )

            # Log password change
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=user.user_role,
                module_name="Authentication",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}",
                new_values='{"password": "changed"}'
            )

            logger.info(f"Password changed for user: {email}")

        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            await self.db.rollback()
            raise

    async def verify_email(self, email: str, token: str):
        """Verify user email"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()
            
            # Verify token
            if user.verification_token != token:
                raise InvalidTokenException()
            
            # Update user
            user.email_confirmed = True
            user.verified_date = datetime.utcnow()
            user.verification_token = None
            
            await self.db.commit()
            
            logger.info(f"Email verified for: {email}")
            
        except Exception as e:
            logger.error(f"Verify email error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def resend_verification_email(self, email: str):
        """Resend verification email with new password"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                raise UserNotFoundException()
            
            # Generate new password and token
            new_password = generate_random_password()
            user.hashed_password = get_password_hash(new_password)
            user.security_stamp = generate_security_stamp()
            user.verification_token = generate_verification_token()
            
            await self.db.commit()
            
            # Send verification email
            await send_user_creation_email(
                to_email=user.email,
                first_name=user.first_name or "User",
                verification_token=user.verification_token,
                generated_password=new_password
            )
            
            logger.info(f"Verification email resent to: {email}")
            
        except Exception as e:
            logger.error(f"Resend verification email error: {str(e)}")
            await self.db.rollback()
            raise
    
    async def validate_guid(self, email: str, guid: str) -> bool:
        """Validate user GUID"""
        try:
            user = await get_user_by_email(self.db, email)
            if not user:
                return False

            return user.user_GUID == guid

        except Exception as e:
            logger.error(f"Validate GUID error: {str(e)}")
            return False

    async def logout(self, user_id: int, user_email: str):
        """
        Logout user by clearing their GUID and refresh token.
        This invalidates the server-side session so existing refresh tokens
        can no longer be used to generate new access tokens.
        """
        try:
            user = await logout_user(self.db, user_id, modified_by=user_email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            await self.db.commit()

            # Log logout
            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.LOGOUT,
                user_role=user.user_role,
                module_name="Authentication",
                table_name="users",
                processor_email=user.email,
                processed_by=f"{user.first_name} {user.last_name}",
                new_values='{"status": "logged_out"}'
            )

            logger.info(f"User logged out: {user_email}")

        except Exception as e:
            logger.error(f"Logout error for user {user_id}: {str(e)}")
            await self.db.rollback()
            raise

    async def generate_access_token(self, refresh_token: str) -> dict:
        """
        Generate a new access token from a valid refresh token.
        Does not rotate the refresh token.
        """
        try:
            # Look up user by refresh token
            user = await get_user_by_refresh_token(self.db, refresh_token)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired refresh token."
                )

            # Verify the refresh token is still valid (decode + check expiry)
            try:
                payload = decode_token(refresh_token)
            except HTTPException:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired refresh token."
                )

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired refresh token."
                )

            if not user.is_active:
                raise HTTPException(
                    status_code=403,
                    detail="User account is inactive."
                )

            # Generate new access token
            access_token = create_access_token({
                "email": user.email,
                "user_id": user.id,
                "role": user.user_role.value
            })

            logger.info(f"Access token generated for user: {user.email}")

            return {
                "success": True,
                "message": "Access token generated successfully.",
                "data": {
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Generate access token error: {str(e)}")
            raise