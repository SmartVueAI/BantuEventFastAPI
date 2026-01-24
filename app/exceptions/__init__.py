"""
Exceptions Package
"""
from app.exceptions.custom_exceptions import (
    UserNotFoundException,
    DuplicateEmailException,
    InvalidCredentialsException,
    AccountLockedException,
    TokenExpiredException,
    InvalidTokenException,
    EmailNotConfirmedException,
    InvalidOTPException,
    PasswordMismatchException,
    WeakPasswordException,
    InvalidFileTypeException,
    FileTooLargeException,
    InsufficientPermissionsException,
)

__all__ = [
    "UserNotFoundException",
    "DuplicateEmailException",
    "InvalidCredentialsException",
    "AccountLockedException",
    "TokenExpiredException",
    "InvalidTokenException",
    "EmailNotConfirmedException",
    "InvalidOTPException",
    "PasswordMismatchException",
    "WeakPasswordException",
    "InvalidFileTypeException",
    "FileTooLargeException",
    "InsufficientPermissionsException",
]