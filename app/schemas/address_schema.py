"""
Address Schemas — Customer Address Management

Customer-facing schemas restrict address_type to billing and shipping only.
Internal types (branch, supplier, warehouse) are not permitted via these endpoints.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List

from app.enums import AddressTypeEnum

# Address types permitted for customer-facing endpoints
CUSTOMER_ALLOWED_TYPES = {AddressTypeEnum.BILLING, AddressTypeEnum.SHIPPING}


class AddressCreate(BaseModel):
    """Schema for creating a customer address.

    Restricts address_type to billing and shipping.
    """
    address_type: AddressTypeEnum = AddressTypeEnum.BILLING
    address_line1: str = Field(..., min_length=1, max_length=500, description="Primary address line")
    address_line2: Optional[str] = Field(None, max_length=500, description="Secondary address line (apt, suite, etc.)")
    city: str = Field(..., min_length=1, max_length=100, description="City")
    state: str = Field(..., min_length=1, max_length=100, description="State or province")
    country: str = Field("USA", max_length=100, description="Country")
    postal_code: str = Field(..., min_length=1, max_length=20, description="Postal / ZIP code")
    contact_name: Optional[str] = Field(None, max_length=255, description="Contact person name")
    contact_phone: Optional[str] = Field(None, max_length=50, description="Contact phone number")
    contact_email: Optional[str] = Field(None, max_length=255, description="Contact email address")
    is_default: bool = Field(False, description="Set as the default address")

    @field_validator("address_type")
    @classmethod
    def validate_customer_address_type(cls, v: AddressTypeEnum) -> AddressTypeEnum:
        if v not in CUSTOMER_ALLOWED_TYPES:
            raise ValueError(
                f"Address type '{v.value}' is not allowed for customer addresses. "
                f"Allowed types: {[t.value for t in CUSTOMER_ALLOWED_TYPES]}"
            )
        return v


class AddressUpdate(BaseModel):
    """Schema for updating a customer address.

    All fields are optional. address_type is restricted to billing and shipping.
    """
    address_type: Optional[AddressTypeEnum] = None
    address_line1: Optional[str] = Field(None, min_length=1, max_length=500)
    address_line2: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=50)
    contact_email: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

    @field_validator("address_type")
    @classmethod
    def validate_customer_address_type(cls, v: Optional[AddressTypeEnum]) -> Optional[AddressTypeEnum]:
        if v is not None and v not in CUSTOMER_ALLOWED_TYPES:
            raise ValueError(
                f"Address type '{v.value}' is not allowed for customer addresses. "
                f"Allowed types: {[t.value for t in CUSTOMER_ALLOWED_TYPES]}"
            )
        return v


class AddressResponse(BaseModel):
    """Schema for a single address response."""
    id: int
    user_id: int
    user_email: Optional[str] = None
    address_type: AddressTypeEnum
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    is_default: bool
    is_active: bool
    is_deleted: bool
    created_at: datetime
    created_by: Optional[str] = None
    last_modified_date: Optional[datetime] = None
    last_modified_by: Optional[str] = None

    class Config:
        from_attributes = True


class AddressListResponse(BaseModel):
    """Schema for paginated address list response."""
    items: List[AddressResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_previous: bool
