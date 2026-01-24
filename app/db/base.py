"""
Database Base
"""
from app.models.base import Base

# Import all models to ensure they are registered with SQLAlchemy
from app.models.user import User  # noqa
from app.models.audit import AuditTrail  # noqa
from app.models.address import Addresses  # noqa
from app.models.branchlocation import BranchLocations  # noqa

__all__ = ["Base"]