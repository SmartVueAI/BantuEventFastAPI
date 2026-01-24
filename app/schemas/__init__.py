"""
Schemas Package
"""
from app.schemas.common import PaginatedResponse, SuccessResponse, ErrorResponse
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    EmailCheckResponse,
    UserCountResponse,
)
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    ResendOTPRequest,
    VerifyOTPRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    VerifyEmailRequest,
    ValidateGUIDRequest,
    ValidateGUIDResponse,
)

__all__ = [
    # Common
    "PaginatedResponse",
    "SuccessResponse",
    "ErrorResponse",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "EmailCheckResponse",
    "UserCountResponse",
    # Auth
    "LoginRequest",
    "LoginResponse",
    "ResendOTPRequest",
    "VerifyOTPRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    "ChangePasswordRequest",
    "VerifyEmailRequest",
    "ValidateGUIDRequest",
    "ValidateGUIDResponse",
]