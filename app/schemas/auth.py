from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from app.schemas.user import UserResponse

"""
Authentication Schemas
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.password import validate_password_strength


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    requires_otp: bool = False
    requires_password_change: bool = False
    user: dict


class ResendOTPRequest(BaseModel):
    """Resend OTP request schema"""
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    """Verify OTP request schema"""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    email: EmailStr
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    old_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class VerifyEmailRequest(BaseModel):
    """Verify email request schema"""
    email: EmailStr
    token: str


class ValidateGUIDRequest(BaseModel):
    """Validate GUID request schema"""
    email: EmailStr
    guid: str


class ValidateGUIDResponse(BaseModel):
    """Validate GUID response schema"""
    valid: bool
#================================
class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    requires_otp: bool = False
    requires_password_change: bool = False
    user: UserResponse


class OTPRequest(BaseModel):
    """Schema for OTP request"""
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    """Schema for OTP verification"""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for reset password request"""
    email: EmailStr
    token: str = Field(..., min_length=32)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class ChangePasswordRequest(BaseModel):
    """Schema for change password request"""
    old_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class VerifyEmailRequest(BaseModel):
    """Schema for email verification"""
    email: EmailStr
    token: str = Field(..., min_length=32)


class ResendVerificationRequest(BaseModel):
    """Schema for resend verification email"""
    email: EmailStr


class ValidateGUIDRequest(BaseModel):
    """Schema for GUID validation"""
    email: EmailStr
    guid: str = Field(..., min_length=36, max_length=36)


class ValidateGUIDResponse(BaseModel):
    """Schema for GUID validation response"""
    valid: bool


class MessageResponse(BaseModel):
    """Schema for simple message response"""
    message: str
    detail: Optional[str] = None