"""
Application-wide constants
"""

"""
Application Constants
"""

# Password Generation
PASSWORD_LENGTH = 12
PASSWORD_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"

# Token Generation
VERIFICATION_TOKEN_LENGTH = 32
OTP_LENGTH = 6

SUPPORT_CODE_LENGTH = 6

# Account Lockout
MAX_LOGIN_ATTEMPTS = 3

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Image Processing
MAX_IMAGE_DIMENSION = 800
IMAGE_QUALITY = 85

# Internal IP Ranges (for SSRF protection)
INTERNAL_IP_RANGES = [
    "127.0.0.0/8",
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "169.254.0.0/16",  # AWS metadata
]

# Blocked Paths (for SSRF protection)
BLOCKED_PATHS = [
    "/latest/meta-data",
    "/computeMetadata",
    "/metadata",
]

# File Upload
PROFILE_IMAGE_DIRECTORY = "static/profile_images"

# HTTP Status Messages
HTTP_200_OK = "Success"
HTTP_201_CREATED = "Resource created successfully"
HTTP_204_NO_CONTENT = "Resource deleted successfully"
HTTP_400_BAD_REQUEST = "Bad request"
HTTP_401_UNAUTHORIZED = "Unauthorized"
HTTP_403_FORBIDDEN = "Forbidden"
HTTP_404_NOT_FOUND = "Resource not found"
HTTP_409_CONFLICT = "Resource already exists"
HTTP_422_UNPROCESSABLE_ENTITY = "Validation error"
HTTP_429_TOO_MANY_REQUESTS = "Too many requests"
HTTP_500_INTERNAL_SERVER_ERROR = "Internal server error"
HTTP_503_SERVICE_UNAVAILABLE = "Service unavailable"

# Pagination Defaults
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1

# Token Expiry (in minutes/days)
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 2
VERIFICATION_TOKEN_EXPIRE_HOURS = 24
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 1
OTP_EXPIRE_MINUTES = 10

# Password Requirements
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGIT = True
PASSWORD_REQUIRE_SPECIAL_CHAR = True

# Account Security
MAX_LOGIN_ATTEMPTS = 3
ACCOUNT_LOCKOUT_DURATION_MINUTES = 30

# File Upload
MAX_PROFILE_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']
MAX_IMAGE_WIDTH = 800
MAX_IMAGE_HEIGHT = 800
IMAGE_QUALITY = 85

# Rate Limiting
RATE_LIMIT_LOGIN = "5/minute"
RATE_LIMIT_OTP = "3/minute"
RATE_LIMIT_PASSWORD_RESET = "3/minute"
RATE_LIMIT_EMAIL_VERIFICATION = "3/minute"
RATE_LIMIT_GENERAL = "100/minute"

# Email Settings
EMAIL_VERIFICATION_REQUIRED = True
EMAIL_FROM_NAME = "Sonma Hair Platform"

# Audit Log Settings
AUDIT_LOG_RETENTION_DAYS = 90

# Session Settings
SESSION_TIMEOUT_MINUTES = 120

# API Version
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Regex Patterns
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^\+?[1-9]\d{1,14}$'
UUID_REGEX = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

# Database
DB_POOL_SIZE = 20
DB_MAX_OVERFLOW = 0
DB_POOL_RECYCLE = 3600
DB_POOL_PRE_PING = True

# Redis
REDIS_DEFAULT_EXPIRE = 3600  # 1 hour in seconds
REDIS_SESSION_EXPIRE = 7200  # 2 hours in seconds

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
CORS_ALLOW_HEADERS = ["*"]
CORS_EXPOSE_HEADERS = ["X-Total-Count", "X-Page", "X-Page-Size"]

# Security Headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}

# Blocked Internal IP Ranges (for SSRF protection)
BLOCKED_IP_RANGES = [
    "127.0.0.0/8",      # Loopback
    "10.0.0.0/8",       # Private network
    "172.16.0.0/12",    # Private network
    "192.168.0.0/16",   # Private network
    "169.254.0.0/16",   # Link-local
    "::1/128",          # IPv6 loopback
    "fc00::/7",         # IPv6 private
    "fe80::/10",        # IPv6 link-local
]

# Metadata Endpoints (for SSRF protection)
BLOCKED_METADATA_PATHS = [
    "/latest/meta-data",
    "/latest/user-data",
    "/latest/dynamic",
]

BLOCKED_METADATA_HOSTS = [
    "169.254.169.254",  # AWS, Azure, GCP
    "metadata.google.internal",
    "169.254.169.123",  # Oracle Cloud
]

# Default Values
DEFAULT_GENDER = "unknown"
DEFAULT_USER_ROLE = "customer"
DEFAULT_ADDRESS_TYPE = "unknown"
DEFAULT_BRANCH_TYPE = "unknown"
DEFAULT_AUDIT_TYPE = "unknown"

# Status Values
STATUS_ACTIVE = True
STATUS_INACTIVE = False
STATUS_DELETED = False

# Sort Orders
SORT_ORDER_ASC = "asc"
SORT_ORDER_DESC = "desc"
VALID_SORT_ORDERS = [SORT_ORDER_ASC, SORT_ORDER_DESC]

# Default Sort Fields
DEFAULT_SORT_FIELD = "created_at"
DEFAULT_SORT_ORDER = SORT_ORDER_DESC

# Error Codes
ERROR_CODE_VALIDATION = "VALIDATION_ERROR"
ERROR_CODE_NOT_FOUND = "NOT_FOUND"
ERROR_CODE_DUPLICATE = "DUPLICATE"
ERROR_CODE_UNAUTHORIZED = "UNAUTHORIZED"
ERROR_CODE_FORBIDDEN = "FORBIDDEN"
ERROR_CODE_INTERNAL = "INTERNAL_ERROR"
ERROR_CODE_DATABASE = "DATABASE_ERROR"
ERROR_CODE_RATE_LIMIT = "RATE_LIMIT_EXCEEDED"

# Success Messages
MSG_USER_CREATED = "User created successfully"
MSG_USER_UPDATED = "User updated successfully"
MSG_USER_DELETED = "User deleted successfully"
MSG_LOGIN_SUCCESS = "Login successful"
MSG_LOGOUT_SUCCESS = "Logout successful"
MSG_PASSWORD_CHANGED = "Password changed successfully"
MSG_PASSWORD_RESET = "Password reset successful"
MSG_EMAIL_VERIFIED = "Email verified successfully"
MSG_EMAIL_SENT = "Email sent successfully"
MSG_OTP_SENT = "OTP sent successfully"
MSG_OTP_VERIFIED = "OTP verified successfully"

# Error Messages
MSG_INVALID_CREDENTIALS = "Invalid email or password"
MSG_EMAIL_EXISTS = "Email already exists"
MSG_USER_NOT_FOUND = "User not found"
MSG_ACCOUNT_LOCKED = "Account is locked due to multiple failed login attempts"
MSG_EMAIL_NOT_CONFIRMED = "Email not confirmed. Please verify your email."
MSG_INVALID_TOKEN = "Invalid or expired token"
MSG_INVALID_OTP = "Invalid OTP"
MSG_PASSWORDS_DONT_MATCH = "Passwords do not match"
MSG_WEAK_PASSWORD = "Password does not meet security requirements"
MSG_FILE_TOO_LARGE = "File size exceeds maximum limit"
MSG_INVALID_FILE_TYPE = "Invalid file type"
MSG_PERMISSION_DENIED = "You don't have permission to perform this action"

# Logging
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
LOG_ROTATION = "00:00"
LOG_RETENTION = "30 days"
ERROR_LOG_RETENTION = "90 days"
LOG_LEVEL_DEV = "DEBUG"
LOG_LEVEL_PROD = "INFO"