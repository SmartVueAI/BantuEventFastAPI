"""
Token Generation Utilities
"""
import secrets
import uuid
import random
import string
from app.core.constants import VERIFICATION_TOKEN_LENGTH, OTP_LENGTH, SUPPORT_CODE_LENGTH


def generate_verification_token(length: int = VERIFICATION_TOKEN_LENGTH) -> str:
    """
    Generate a random verification token
    
    Args:
        length: Length of token (default: 32)
    
    Returns:
        Random hex token string
    """
    return secrets.token_hex(length // 2)


def generate_otp(length: int = OTP_LENGTH) -> str:
    """
    Generate a numeric OTP code
    
    Args:
        length: Length of OTP (default: 6)
    
    Returns:
        Numeric OTP string
    """
    return "".join([str(secrets.randbelow(10)) for _ in range(length)])


def generate_guid() -> str:
    """
    Generate a GUID (UUID4)
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def generate_security_stamp() -> str:
    """
    Generate a security stamp (UUID4)

    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def generate_support_code(length: int = SUPPORT_CODE_LENGTH) -> str:
    """
    Generate a zero-padded numeric customer support code.

    Args:
        length: Length of the support code (default: SUPPORT_CODE_LENGTH from constants)

    Returns:
        Zero-padded numeric string of the specified length (e.g., "042891")
    """
    return "".join(random.choices(string.digits, k=length))