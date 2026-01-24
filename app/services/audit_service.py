"""
Audit Service
"""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import json

from app.models.audit import AuditTrail
from app.enums import AuditTypeEnum, UserRoleEnum


class AuditService:
    """Audit trail service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log_audit(
        self,
        audit_type: AuditTypeEnum,
        user_role: UserRoleEnum,
        module_name: str | None = None,
        table_name: str | None = None,
        old_values: str | None = None,
        new_values: str | None = None,
        processed_by: str | None = None,
        processor_email: str | None = None,
    ):
        """Log audit trail entry"""
        try:
            audit_entry = AuditTrail(
                audit_type=audit_type,
                user_type=user_role,
                module_name=module_name,
                table_name=table_name,
                old_values=old_values,
                new_values=new_values,
                processed_by=processed_by,
                processor_email=processor_email,
                created_by=processor_email,
                created_at=datetime.utcnow(),
            )
            
            self.db.add(audit_entry)
            await self.db.flush()
            
            logger.debug(f"Audit logged: {audit_type.value} on {table_name}")
            
        except Exception as e:
            logger.error(f"Audit logging error: {str(e)}")
            # Don't fail the main operation if audit logging fails