"""
BranchLocations Model
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseDBModel
from app.enums import BranchTypeEnum


class BranchLocations(BaseDBModel):
    """Branch locations database model"""
    __tablename__ = "branch_locations"
    
    # Branch Information
    branch_name = Column(String(255), nullable=False)
    branch_code = Column(String(50), unique=True, index=True, nullable=True)
    branch_type = Column(SQLEnum(BranchTypeEnum), default=BranchTypeEnum.UNKNOWN, nullable=False)
    
    # Address Reference
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False)
    
    # Manager Reference
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Contact Information
    branch_phone = Column(String(50), nullable=True)
    branch_email = Column(String(255), nullable=True)
    
    # Operating Information
    operating_hours = Column(Text, nullable=True)  # JSON string with operating hours
    
    # Capacity and Size
    capacity = Column(Integer, nullable=True)
    size_sqft = Column(Integer, nullable=True)
    
    # Status
    is_operational = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    address = relationship("Addresses", back_populates="branch")
    manager = relationship("User", back_populates="managed_branches")