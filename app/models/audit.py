"""
AuditTrail Model
"""
from sqlalchemy import Column, String, Text, Enum as SQLEnum

from app.models.base import BaseDBModel
from app.enums import AuditTypeEnum, UserRoleEnum


class AuditTrail(BaseDBModel):
    """Audit trail database model for tracking all system changes"""
    __tablename__ = "audit_trail"
    
    # Audit Information
    audit_type = Column(SQLEnum(AuditTypeEnum), default=AuditTypeEnum.UNKNOWN, nullable=False)
    user_type = Column(SQLEnum(UserRoleEnum), default=UserRoleEnum.UNKNOWN, nullable=False)
    
    # Module and Table Information
    module_name = Column(String(255), nullable=True)
    table_name = Column(String(255), nullable=True)
    
    # Change Tracking (stored as JSON strings)
    old_values = Column(Text, nullable=True)  # JSON string of old values
    new_values = Column(Text, nullable=True)  # JSON string of new values
    
    # Processor Information
    processed_by = Column(String(255), nullable=True)
    processor_email = Column(String(255), nullable=True)