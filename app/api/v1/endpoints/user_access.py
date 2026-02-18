"""
User Access Management Endpoints
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.dependencies.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    ResendOTPRequest,
    VerifyOTPRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    NewUserChangePasswordRequest,
    ChangePasswordRequest,
    VerifyEmailRequest,
    ValidateGUIDRequest,
    ValidateGUIDResponse,
    GenerateAccessTokenRequest,
)
from app.schemas.common import SuccessResponse
from app.services.auth_service import AuthService
from app.core.security import get_current_user

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="""
    Authenticate user with email and password.
    
    Features:
    - Email verification check
    - Account lockout after 3 failed attempts
    - Optional OTP verification
    - Default password detection
    - JWT token generation
    
    **No authentication required**
    """,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        403: {"description": "Account locked or email not confirmed"},
    }
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """User login endpoint"""
    try:
        auth_service = AuthService(db)
        result = await auth_service.login(
            email=login_data.email,
            password=login_data.password
        )
        return result
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise


@router.post(
    "/resend-otp",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Resend OTP",
    description="Resend OTP code to user's email for two-factor authentication.",
    responses={
        200: {"description": "OTP sent successfully"},
        404: {"description": "User not found"},
    }
)
async def resend_otp(
    request: ResendOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    """Resend OTP to user"""
    try:
        auth_service = AuthService(db)
        await auth_service.resend_otp(email=request.email)
        return SuccessResponse(
            message="OTP has been sent to your email",
            data={"email": request.email}
        )
    except Exception as e:
        logger.error(f"Resend OTP error: {str(e)}")
        raise


@router.post(
    "/verify-otp",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP",
    description="Verify OTP code and complete authentication process.",
    responses={
        200: {"description": "OTP verified successfully"},
        401: {"description": "Invalid or expired OTP"},
        404: {"description": "User not found"},
    }
)
async def verify_otp(
    request: VerifyOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    """Verify OTP and get tokens"""
    try:
        auth_service = AuthService(db)
        result = await auth_service.verify_otp(
            email=request.email,
            otp=request.otp
        )
        return result
    except Exception as e:
        logger.error(f"Verify OTP error: {str(e)}")
        raise


@router.post(
    "/forgot-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Forgot password",
    description="Initiate password reset process by sending reset link to email.",
    responses={
        200: {"description": "Password reset email sent"},
        404: {"description": "User not found"},
    }
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset"""
    try:
        auth_service = AuthService(db)
        await auth_service.forgot_password(email=request.email)
        return SuccessResponse(
            message="Password reset instructions have been sent to your email",
            data={"email": request.email}
        )
    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}")
        raise


@router.post(
    "/reset-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset password",
    description="Reset password using token from email.",
    responses={
        200: {"description": "Password reset successfully"},
        400: {"description": "Invalid or expired token"},
        404: {"description": "User not found"},
    }
)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Reset password with token"""
    try:
        auth_service = AuthService(db)
        await auth_service.reset_password(
            email=request.email,
            token=request.token,
            new_password=request.new_password
        )
        return SuccessResponse(
            message="Password has been reset successfully. You can now login with your new password."
        )
    except Exception as e:
        logger.error(f"Reset password error: {str(e)}")
        raise


@router.post(
    "/change-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Change password",
    description="""
    Change password for authenticated user.
    
    **Authentication required**
    """,
    responses={
        200: {"description": "Password changed successfully"},
        401: {"description": "Invalid old password or not authenticated"},
    }
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change password for authenticated user"""
    try:
        auth_service = AuthService(db)
        await auth_service.change_password(
            user_id=current_user["id"],
            old_password=request.old_password,
            new_password=request.new_password
        )
        return SuccessResponse(
            message="Password has been changed successfully"
        )
    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        raise


@router.post(
    "/verify-email",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify email",
    description="Verify email address using token from registration email.",
    responses={
        200: {"description": "Email verified successfully"},
        400: {"description": "Invalid or expired token"},
        404: {"description": "User not found"},
    }
)
async def verify_email(
    request: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    """Verify user email with token"""
    try:
        auth_service = AuthService(db)
        await auth_service.verify_email(
            email=request.email,
            token=request.token
        )
        return SuccessResponse(
            message="Email verified successfully. You can now login."
        )
    except Exception as e:
        logger.error(f"Verify email error: {str(e)}")
        raise


@router.post(
    "/resend-verification-email",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Resend verification email",
    description="Resend email verification link with new password.",
    responses={
        200: {"description": "Verification email sent"},
        404: {"description": "User not found"},
    }
)
async def resend_verification_email(
    request: ResendOTPRequest,  # Reusing same schema as it only has email
    db: AsyncSession = Depends(get_db)
):
    """Resend verification email"""
    try:
        auth_service = AuthService(db)
        await auth_service.resend_verification_email(email=request.email)
        return SuccessResponse(
            message="Verification email has been sent with new password",
            data={"email": request.email}
        )
    except Exception as e:
        logger.error(f"Resend verification email error: {str(e)}")
        raise


@router.post(
    "/new-user-change-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Change password for new user",
    description="""
    Change password for new user.
    
    **Authentication required**
    """,
    responses={
        200: {"description": "Password changed successfully"},
        401: {"description": "Invalid old password or not authenticated"},
    }
)
async def new_user_change_password(
    request: NewUserChangePasswordRequest,
    # current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change password for authenticated user"""
    try:
        auth_service = AuthService(db)
        await auth_service.new_user_change_password(
            email=request.email,
            old_password=request.old_password,
            new_password=request.new_password
        )
        return SuccessResponse(
            message="Password has been changed successfully"
        )
    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        raise
@router.post(
    "/validate-guid",
    response_model=ValidateGUIDResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate user GUID",
    description="Validate if a GUID belongs to a specific user.",
    responses={
        200: {"description": "GUID validation result"},
    }
)
async def validate_guid(
    request: ValidateGUIDRequest,
    db: AsyncSession = Depends(get_db)
):
    """Validate user GUID"""
    try:
        auth_service = AuthService(db)
        is_valid = await auth_service.validate_guid(
            email=request.email,
            guid=request.guid
        )
        return ValidateGUIDResponse(valid=is_valid)
    except Exception as e:
        logger.error(f"Validate GUID error: {str(e)}")
        raise


@router.post(
    "/logout",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="User logout",
    description="""
    Logout the authenticated user.

    Clears the user's GUID and refresh token from the database so that
    existing tokens can no longer be used to generate new access tokens.

    **Authentication required**
    """,
    responses={
        200: {"description": "Logged out successfully"},
        401: {"description": "Not authenticated"},
        404: {"description": "User not found"},
    }
)
async def logout(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Logout the authenticated user"""
    try:
        auth_service = AuthService(db)
        await auth_service.logout(
            user_id=current_user["id"],
            user_email=current_user["email"]
        )
        return SuccessResponse(message="User logged out successfully.")
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise


@router.post(
    "/generate-access-token",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate new access token",
    description="""
    Generate a fresh access token using a valid refresh token.

    Use this endpoint when the access token has expired.
    The refresh token remains unchanged until it expires or the user logs out.

    **No authentication required** — accepts the refresh token in the request body.
    """,
    responses={
        200: {"description": "Access token generated successfully"},
        401: {"description": "Invalid or expired refresh token"},
    }
)
async def generate_access_token(
    request: GenerateAccessTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate a new access token from a valid refresh token"""
    try:
        auth_service = AuthService(db)
        result = await auth_service.generate_access_token(
            refresh_token=request.refresh_token
        )
        return SuccessResponse(
            message=result["message"],
            data=result["data"]
        )
    except Exception as e:
        logger.error(f"Generate access token error: {str(e)}")
        raise