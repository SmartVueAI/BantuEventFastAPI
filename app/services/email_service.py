"""
Email Service
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger

from app.core.config import settings
from app.utils.email_templates import (
    get_user_creation_email_template,
    get_otp_email_template,
    get_password_reset_email_template,
    get_password_changed_email_template,
    get_account_locked_email_template,
)


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
) -> bool:
    """Send email using SMTP"""
    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        
        logger.info(f"Email sent successfully to: {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {str(e)}")
        return False


async def send_user_creation_email(
    to_email: str,
    first_name: str,
    verification_token: str,
    generated_password: str,
    base_url: str = "http://localhost:8000"
) -> bool:
    """Send user creation email"""
    verification_link = f"{base_url}/verify-email?token={verification_token}&email={to_email}"
    html_content = get_user_creation_email_template(
        first_name=first_name,
        verification_link=verification_link,
        generated_password=generated_password,
    )
    return await send_email(
        to_email=to_email,
        subject="Welcome! Please Verify Your Email",
        html_content=html_content,
    )


async def send_otp_email(to_email: str, first_name: str, otp: str) -> bool:
    """Send OTP email"""
    html_content = get_otp_email_template(first_name=first_name, otp=otp)
    return await send_email(
        to_email=to_email,
        subject="Your One-Time Password (OTP)",
        html_content=html_content,
    )


async def send_password_reset_email(
    to_email: str,
    first_name: str,
    reset_token: str,
    base_url: str = "http://localhost:8000"
) -> bool:
    """Send password reset email"""
    reset_link = f"{base_url}/reset-password?token={reset_token}&email={to_email}"
    html_content = get_password_reset_email_template(
        first_name=first_name,
        reset_link=reset_link,
    )
    return await send_email(
        to_email=to_email,
        subject="Password Reset Request",
        html_content=html_content,
    )


async def send_password_changed_email(to_email: str, first_name: str) -> bool:
    """Send password changed email"""
    html_content = get_password_changed_email_template(first_name=first_name)
    return await send_email(
        to_email=to_email,
        subject="Password Changed Successfully",
        html_content=html_content,
    )


async def send_account_locked_email(to_email: str, first_name: str) -> bool:
    """Send account locked email"""
    html_content = get_account_locked_email_template(first_name=first_name)
    return await send_email(
        to_email=to_email,
        subject="Account Locked - Security Alert",
        html_content=html_content,
    )