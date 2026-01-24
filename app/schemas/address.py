from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from app.enums.enums import AddressTypeEnum


class AddressBase(BaseModel):
    """Base schema for address"""
    address_type: AddressTypeEnum = AddressTypeEnum.UNKNOWN
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field("USA", max_length=100)
    landmark: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    is_default: bool = False


class AddressCreate(AddressBase):
    """Schema for creating address"""
    user_id: Optional[int] = None
    user_email: Optional[str] = None


class AddressUpdate(BaseModel):
    """Schema for updating address"""
    id: int
    address_type: Optional[AddressTypeEnum] = None
    address_line1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    landmark: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class AddressResponse(AddressBase):
    """Schema for address response"""
    id: int
    user_id: Optional[int]
    user_email: Optional[str]
    created_at: datetime
    created_by: Optional[str]
    last_modified_date: Optional[datetime]
    last_modified_by: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


class AddressListResponse(BaseModel):
    """Schema for paginated address list"""
    items: list[AddressResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_previous: bool


class UserAddressesResponse(BaseModel):
    """Schema for user's addresses"""
    user_id: int
    user_email: str
    addresses: list[AddressResponse]
    total_addresses: int
    default_address: Optional[AddressResponse] = None


class AddressValidation(BaseModel):
    """Schema for address validation"""
    is_valid: bool
    errors: Optional[list[str]] = None
    suggestions: Optional[list[dict]] = None


class SetDefaultAddressRequest(BaseModel):
    """Schema for setting default address"""
    address_id: int
    user_id: int