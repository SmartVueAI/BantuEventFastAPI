"""
Email Service
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
import smtplib
import time  # For Message-ID generation
from loguru import logger

from app.core.config import settings
from app.utils.email_templates import (
    get_user_creation_email_text,
    get_user_creation_email_template,
    get_otp_email_text,
    get_otp_email_template,
    get_password_reset_email_text,
    get_password_reset_email_template,
    get_password_changed_email_text,
    get_password_changed_email_template,
    get_account_locked_email_text,
    get_account_locked_email_template
)


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str = None,
) -> bool:
    """Send email using SMTP"""
    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # ✅ FIX 1: Add Date header (was missing, caused -1.396 penalty)
        message["Date"] = formatdate(localtime=True)

        # ✅ FIX 2: Add proper Message-ID
        domain = settings.SMTP_FROM.split(
            '@')[1] if '@' in settings.SMTP_FROM else 'sonmahair.com'
        message["Message-ID"] = make_msgid(domain=domain)

        # ✅ FIX 3: Add List-Unsubscribe header (helps with spam score)
        message["List-Unsubscribe"] = f"<mailto:unsubscribe@{domain}>"
        message["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

        # ✅ Add anti-spam headers
        # or your support email
        message["Reply-To"] = settings.SMTP_SUPPORT_EMAIL
        message["X-Mailer"] = f"{settings.SMTP_FROM_NAME} Account System"
        message["X-Auto-Response-Suppress"] = "OOF, AutoReply"
        message["Precedence"] = "bulk"  # Indicates transactional email

        # ✅ Attach plain text first (required for spam filters)
        text_part = MIMEText(text_content, "plain", "utf-8")
        message.attach(text_part)

        # ✅ Then attach HTML version
        html_part = MIMEText(html_content, "html", "utf-8")
        message.attach(html_part)

        response = await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            # start_tls=True,
            use_tls=True,  # ✅ Changed from start_tls=True
            timeout=30,    # ✅ Added timeout
        )
        
        logger.info(f"SMTP Response: {response}")  # ✅ Log the response
        logger.info(f"Email sent successfully to: {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {str(e)}")
        logger.exception(e)  # ✅ Full stack trace
        return False


async def send_user_creation_email(
    to_email: str,
    first_name: str,
    verification_token: str,
    generated_password: str,
    frontend_base_url: str = settings.FRONTEND_BASE_URL,
) -> bool:
    """Send user creation email"""
    verification_link = f"{frontend_base_url}/verify-email?token={verification_token}&email={to_email}"
    app_name = settings.APP_NAME

   # ✅ Generate HTML content
    html_content = get_user_creation_email_template(
        first_name=first_name,
        verification_link=verification_link,
        generated_password=generated_password,
        to_email=to_email,
        app_name=app_name,
    )

    # ✅ Generate plain text content
    text_content = get_user_creation_email_text(
        first_name=first_name,
        verification_link=verification_link,
        generated_password=generated_password,
        to_email=to_email,
        app_name=app_name,
    )
    # ✅ Send with both versions
    return await send_email(
        to_email=to_email,
        subject=f"Welcome to {app_name} - Please Verify Your Email",
        html_content=html_content,
        text_content=text_content,  # ✅ Added plain text
    )


async def send_otp_email(to_email: str, first_name: str, otp: str) -> bool:
    """Send OTP email"""
    # html_content = get_otp_email_template(first_name=first_name, otp=otp)

    app_name = settings.APP_NAME

    # ✅ Generate HTML content
    html_content = get_otp_email_template(
        first_name=first_name,
        otp=otp,
        to_email=to_email,
        app_name=app_name,
    )

    # ✅ Generate plain text content
    text_content = get_otp_email_text(
        first_name=first_name,
        otp=otp,
        to_email=to_email,
        app_name=app_name,
    )
    # ✅ Send with both versions

    return await send_email(
        to_email=to_email,
        subject="Your One-Time Password (OTP)",
        html_content=html_content,
        text_content=text_content,
    )


async def send_password_reset_email(
    to_email: str,
    first_name: str,
    reset_token: str,
    frontend_base_url: str = settings.FRONTEND_BASE_URL,
) -> bool:
    """Send password reset email"""
    reset_link = f"{frontend_base_url}/reset-password?token={reset_token}&email={to_email}"

    app_name = settings.APP_NAME

    # ✅ Generate HTML content
    html_content = get_password_reset_email_template(
        first_name=first_name,
        reset_link=reset_link,
        to_email=to_email,
        app_name=app_name,
    )

    # ✅ Generate plain text content
    text_content = get_password_reset_email_text(
        first_name=first_name,
        reset_link=reset_link,
        to_email=to_email,
        app_name=app_name,
    )
    # ✅ Send with both versions

    return await send_email(
        to_email=to_email,
        subject="Password Reset Request",
        html_content=html_content,
        text_content=text_content,  # ✅ Added plain text
    )


async def send_password_changed_email(to_email: str, first_name: str) -> bool:
    """Send password changed email"""
    # html_content = get_password_changed_email_template(first_name=first_name)

    app_name = settings.APP_NAME

    # ✅ Generate HTML content
    html_content = get_password_changed_email_template(
        first_name=first_name,
        to_email=to_email,
        app_name=app_name,
    )

    # ✅ Generate plain text content
    text_content = get_password_changed_email_text(
        first_name=first_name,
        to_email=to_email,
        app_name=app_name,
    )
    # ✅ Send with both versions
    return await send_email(
        to_email=to_email,
        subject="Password Changed Successfully",
        html_content=html_content,
        text_content=text_content,  # ✅ Added plain text
    )


async def send_account_locked_email(to_email: str, first_name: str) -> bool:
    """Send account locked email"""
    # html_content = get_account_locked_email_template(first_name=first_name)

    app_name = settings.APP_NAME

    # ✅ Generate HTML content
    html_content = get_account_locked_email_template(
        first_name=first_name,
        to_email=to_email,
        app_name=app_name,
    )

    # ✅ Generate plain text content
    text_content = get_account_locked_email_text(
        first_name=first_name,
        to_email=to_email,
        app_name=app_name,
    )
    # ✅ Send with both versions
    return await send_email(
        to_email=to_email,
        subject="Account Locked - Security Alert",
        html_content=html_content,
        text_content=text_content,  # ✅ Added plain text
    )