"""
Custom Exception Classes
"""
from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    """Exception raised when user is not found"""
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateEmailException(HTTPException):
    """Exception raised when email already exists"""
    def __init__(self, detail: str = "Email already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidCredentialsException(HTTPException):
    """Exception raised when login credentials are invalid"""
    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class DefaultPasswordException(HTTPException):
    """Exception raised when login credentials are invalid"""

    def __init__(self, detail: str = "User must change default password before logging in"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserNotActiveException(HTTPException):
    """Exception raised when login credentials are invalid"""

    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AccountLockedException(HTTPException):
    """Exception raised when account is locked"""
    def __init__(self, detail: str = "Account is locked due to multiple failed login attempts"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class TokenExpiredException(HTTPException):
    """Exception raised when token has expired"""
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidTokenException(HTTPException):
    """Exception raised when token is invalid"""
    def __init__(self, detail: str = "Invalid or malformed token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class EmailNotConfirmedException(HTTPException):
    """Exception raised when email is not confirmed"""
    def __init__(self, detail: str = "Email address not confirmed. Please verify your email."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class InvalidOTPException(HTTPException):
    """Exception raised when OTP is invalid"""
    def __init__(self, detail: str = "Invalid or expired OTP"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class PasswordMismatchException(HTTPException):
    """Exception raised when passwords don't match"""
    def __init__(self, detail: str = "Passwords do not match"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class WeakPasswordException(HTTPException):
    """Exception raised when password is too weak"""
    def __init__(self, detail: str = "Password does not meet security requirements"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidFileTypeException(HTTPException):
    """Exception raised when file type is not allowed"""
    def __init__(self, detail: str = "Invalid file type"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class FileTooLargeException(HTTPException):
    """Exception raised when file is too large"""
    def __init__(self, detail: str = "File size exceeds maximum allowed size"):
        super().__init__(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=detail)


class InsufficientPermissionsException(HTTPException):
    """Exception raised when user doesn't have required permissions"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)