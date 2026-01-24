from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.enums.enums import AuditTypeEnum, UserRoleEnum


class AuditTrailBase(BaseModel):
    """Base schema for audit trail"""
    audit_type: AuditTypeEnum
    module_name: str = Field(..., max_length=100)
    table_name: str = Field(..., max_length=100)
    user_type: Optional[UserRoleEnum] = None
    processed_by: Optional[str] = Field(None, max_length=255)
    processor_email: Optional[str] = Field(None, max_length=255)


class AuditTrailCreate(AuditTrailBase):
    """Schema for creating audit trail entry"""
    old_values: Optional[str] = None  # JSON string
    new_values: Optional[str] = None  # JSON string


class AuditTrailResponse(AuditTrailBase):
    """Schema for audit trail response"""
    id: int
    old_values: Optional[str]
    new_values: Optional[str]
    created_at: datetime
    created_by: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


class AuditTrailListResponse(BaseModel):
    """Schema for paginated audit trail list"""
    items: list[AuditTrailResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_previous: bool


class AuditTrailFilter(BaseModel):
    """Schema for filtering audit trails"""
    audit_type: Optional[AuditTypeEnum] = None
    module_name: Optional[str] = None
    table_name: Optional[str] = None
    processor_email: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None