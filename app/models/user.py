"""
User Model
"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseDBModel
from app.enums import GenderEnum, UserRoleEnum


class User(BaseDBModel):
    """User database model"""
    __tablename__ = "users"
    
    # Basic Information
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    normalized_email = Column(String(255), unique=True, index=True, nullable=True)
    email_confirmed = Column(Boolean, default=False, nullable=False)
    gender = Column(SQLEnum(GenderEnum), default=GenderEnum.UNKNOWN, nullable=False)
    user_role = Column(SQLEnum(UserRoleEnum), default=UserRoleEnum.UNKNOWN, nullable=False)
    
    # Contact Information
    phone_number = Column(String(50), nullable=True)
    whatsapp_number = Column(String(50), nullable=True)
    location = Column(String(50), nullable=True)
    branch_code = Column(String(50), nullable=True)
    customer_support_code = Column(String(50), nullable=True)
    
    # OTP Configuration
    otp = Column(String(50), nullable=True)
    use_otp_enabled = Column(Boolean, default=False, nullable=False)
    otp_expires = Column(DateTime, nullable=True)
    
    # Account Lockout
    lockout_date_time = Column(DateTime, nullable=True)
    lockout_enabled = Column(Boolean, default=False, nullable=False)
    access_failed_count = Column(Integer, default=0, nullable=False)
    
    # Profile Image
    profile_image_URL = Column(String(500), nullable=True)
    profile_image_file_name = Column(String(255), nullable=True)
    upload_profile_image_date_time = Column(DateTime, nullable=True)
    
    # Profile Configuration
    profile_URL = Column(String(500), nullable=True)
    selected_theme = Column(String(50), nullable=True)
    selected_theme_date_time = Column(DateTime, nullable=True)
    
    # Security & Authentication
    user_GUID = Column(String(255), unique=True, index=True, nullable=True)
    user_logged_In = Column(Boolean, default=False, nullable=False)
    default_password = Column(Boolean, default=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    security_stamp = Column(String(500), nullable=True)
    last_logged_in_date = Column(DateTime, nullable=True)
    last_password_changed_date = Column(DateTime, nullable=True)
    
    # Email Verification
    verification_token = Column(String(255), nullable=True, unique=True, index=True)
    verified_date = Column(DateTime, nullable=True)
    
    # Job Information
    job_title = Column(String(255), nullable=True)
    job_description = Column(String(1000), nullable=True)
    
    # Refresh Token
    refresh_token = Column(String(500), nullable=True)
    refresh_token_expires = Column(DateTime, nullable=True)
    revoked_token_date = Column(DateTime, nullable=True)
    revoked_by = Column(String(255), nullable=True)
    replaced_by_token = Column(String(500), nullable=True)
    
    # Relationships
    addresses = relationship("Addresses", back_populates="user", cascade="all, delete-orphan")
    managed_branches = relationship("BranchLocations", back_populates="manager", cascade="all, delete-orphan")