"""
Addresses Model
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseDBModel
from app.enums import AddressTypeEnum


class Addresses(BaseDBModel):
    """Addresses database model"""
    __tablename__ = "addresses"
    
    # User Reference
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Address Type
    address_type = Column(SQLEnum(AddressTypeEnum), default=AddressTypeEnum.UNKNOWN, nullable=False)
    
    # Address Details
    address_line1 = Column(String(500), nullable=True)
    address_line2 = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Contact Information
    contact_name = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_email = Column(String(255), nullable=True)
    
    # Flags
    is_default = Column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="addresses")
    branch = relationship("BranchLocations", back_populates="address", uselist=False)