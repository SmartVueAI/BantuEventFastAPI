"""
Authentication Dependencies
"""
from app.core.security import get_current_user, check_user_role
from app.enums import UserRoleEnum

# Re-export for convenience
__all__ = ["get_current_user", "check_user_role"]

# Pre-defined role checkers
require_staff = check_user_role([
    UserRoleEnum.STAFF,
    UserRoleEnum.SUPERVISOR,
    UserRoleEnum.SUPERADMIN
])

require_supervisor = check_user_role([
    UserRoleEnum.SUPERVISOR,
    UserRoleEnum.SUPERADMIN
])

require_superadmin = check_user_role([
    UserRoleEnum.SUPERADMIN
])