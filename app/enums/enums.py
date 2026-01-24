"""
Application Enums
"""
from enum import Enum


class UserRoleEnum(str, Enum):
    """User role enumeration"""
    UNKNOWN = "unknown"
    GUEST = "guest"
    CUSTOMER = "customer"
    STAFF = "staff"
    VENDOR = "vendor"
    CONTENTMANAGER = "contentmanager"
    REPORTANALYST = "reportanalyst"
    INVENTORYMANAGER = "inventorymanager"
    SUPERVISOR = "supervisor"
    SUPERADMIN = "superadmin"


class AuditTypeEnum(str, Enum):
    """Audit action type enumeration"""
    UNKNOWN = "unknown"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    VIEW = "view"


class GenderEnum(str, Enum):
    """Gender enumeration"""
    UNKNOWN = "unknown"
    MALE = "male"
    FEMALE = "female"
    OTHERS = "others"


class AddressTypeEnum(str, Enum):
    """Address type enumeration"""
    UNKNOWN = "unknown"
    BILLING = "billing"
    SHIPPING = "shipping"
    BRANCH = "branch"
    SUPPLIER = "supplier"
    WAREHOUSE = "warehouse"


class BranchTypeEnum(str, Enum):
    """Branch type enumeration"""
    UNKNOWN = "unknown"
    WAREHOUSE = "warehouse"
    RETAIL = "retail_store"
    OFFICE = "office"