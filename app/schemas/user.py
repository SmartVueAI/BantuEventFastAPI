from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
from app.enums.enums import GenderEnum, UserRoleEnum


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    gender: GenderEnum = GenderEnum.UNKNOWN
    phone_number: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=255)
    user_role: UserRoleEnum = UserRoleEnum.CUSTOMER
    job_title: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class AdminUserCreate(UserBase):
    use_otp_enabled: Optional[bool] = False

class UserUpdate(BaseModel):
    """Schema for updating user details"""
    id: int
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    job_title: Optional[str] = Field(None, max_length=100)
    job_description: Optional[str] = Field(None, max_length=1000)
    gender: Optional[GenderEnum] = None
    is_active: Optional[bool] = None


class AdminUserUpdate(BaseModel):
    """Schema for updating user details"""
    id: int
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=50)
    job_title: Optional[str] = Field(None, max_length=100)
    job_description: Optional[str] = Field(None, max_length=1000)
    gender: Optional[GenderEnum] = None
    user_role: Optional[UserRoleEnum] = None
    use_otp_enabled: Optional[bool] = False
    is_active: Optional[bool] = False


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    first_name: str
    last_name: str
    email: str
    gender: GenderEnum
    phone_number: Optional[str]
    location: Optional[str]
    user_role: UserRoleEnum
    job_title: Optional[str]
    email_confirmed: bool
    is_active: bool
    user_logged_In: bool
    last_logged_in_date: Optional[datetime]
    profile_image_URL: Optional[str]
    created_at: datetime
    created_by: Optional[str]
    last_modified_date: Optional[datetime]
    last_modified_by: Optional[str]
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for paginated user list response"""
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_previous: bool


class EmailCheckResponse(BaseModel):
    """Schema for email existence check"""
    exists: bool


class UserCountResponse(BaseModel):
    """Schema for user count"""
    count: int


class ProfileImageUploadResponse(BaseModel):
    """Schema for profile image upload response"""
    message: str
    profile_image_URL: str
    upload_date: datetime