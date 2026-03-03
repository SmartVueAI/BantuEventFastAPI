"""
Email HTML Templates
"""
from app.core.config import settings

# ✅ New function to generate plain text version


def get_user_creation_email_text(
    first_name: str,
    verification_link: str,
    generated_password: str,
    to_email: str,
    app_name: str,
) -> str:
    """Generate plain text version of user creation email"""
    return f"""
Hello {first_name},

Welcome to {app_name}!

Thank you for creating an account with us. We're excited to have you join our community. This email contains important information about your new account and the steps you need to take to get started.

═══════════════════════════════════════════════════════════
YOUR ACCOUNT INFORMATION
═══════════════════════════════════════════════════════════

Account Email: {to_email}

Temporary Access Code: {generated_password}

This is a system-generated temporary access code. For your security, you will be required to change this code immediately after your first login. Please keep this information secure and do not share it with anyone.

═══════════════════════════════════════════════════════════
VERIFY YOUR EMAIL ADDRESS (REQUIRED)
═══════════════════════════════════════════════════════════

Before you can access your account, you must verify your email address. This is a security measure to ensure that you are the legitimate owner of this email address.

To verify your email address, please visit the following secure link:

{verification_link}

This verification link is unique to your account and will expire in 24 hours for security purposes. If you do not verify your email within this timeframe, you will need to request a new verification link.

Important Security Note: This verification link was generated specifically for {to_email}. If you received this email but did not create an account with {app_name}, please disregard this message or contact our support team immediately.

═══════════════════════════════════════════════════════════
GETTING STARTED WITH YOUR ACCOUNT
═══════════════════════════════════════════════════════════

Once you've verified your email address, follow these steps:

1. Visit our login page at {app_name}
2. Enter your email address: {to_email}
3. Enter your temporary access code: {generated_password}
4. You will be prompted to change your access code immediately
5. Complete your profile information
6. Explore the platform and start using our services

═══════════════════════════════════════════════════════════
SECURITY BEST PRACTICES
═══════════════════════════════════════════════════════════

- Change your temporary access code to a strong, unique password
- Never share your access code with anyone, including {app_name} staff
- Enable two-factor authentication if available (recommended)
- Log out when using shared or public computers
- Keep your contact information up to date

═══════════════════════════════════════════════════════════
NEED HELP?
═══════════════════════════════════════════════════════════

If you encounter any issues during the verification process or have questions about your account, our support team is here to help:

Email: {settings.SMTP_SUPPORT_EMAIL}
Response Time: Within 24 hours

Common Questions:

Q: I didn't create this account. What should I do?
A: If you did not request this account, please contact us at {settings.SMTP_SUPPORT_EMAIL} immediately. You can safely ignore this email.

Q: My verification link has expired. How do I get a new one?
A: Visit our login page and click "Resend Verification Email" to receive a new link.

Q: I forgot my temporary access code. Can I recover it?
A: For security reasons, we cannot recover temporary access codes. Please use the "Forgot Password" feature on our login page.

═══════════════════════════════════════════════════════════
ABOUT THIS EMAIL
═══════════════════════════════════════════════════════════

This is an automated transactional email sent from a verified {app_name} account. We sent this email to {to_email} because an account was created using this email address.

You are receiving this email as a registered user of {app_name}. This is a required account verification email and cannot be unsubscribed from. However, you can opt out of marketing emails once you complete your account setup.

═══════════════════════════════════════════════════════════

© 2026 {app_name}. All rights reserved.

{app_name}
Email: {settings.SMTP_SUPPORT_EMAIL}
Website: https://bantuevents.com

This email was sent to: {to_email}
This is a transactional email related to your account activity.

═══════════════════════════════════════════════════════════
""".strip()


def get_user_creation_email_template(
    first_name: str,
    verification_link: str,
    generated_password: str,
    to_email: str,
    app_name: str,
) -> str:
    """Generate HTML email template for user creation"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <title>Welcome to {app_name}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header with Branding -->
            <div style="background-color: #D914BA; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 600;">{app_name}</h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.95;">Account Verification Required</p>
            </div>
            
            <!-- Main Content -->
            <div style="background-color: white; padding: 40px 30px; border-left: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">
                
                <!-- Greeting -->
                <p style="margin: 0 0 20px 0; font-size: 16px;">Hello {first_name},</p>
                
                <p style="margin: 0 0 20px 0; font-size: 15px; line-height: 1.7;">
                    Thank you for creating an account with <strong>{app_name}</strong>. We're excited to have you join our community. To complete your registration and access your account, you need to verify your email address.
                </p>
                
                <!-- Why This Email -->
                <div style="background-color: #f0f8ff; border-left: 4px solid #D914BA; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #D914BA; font-size: 14px;">📧 Why am I receiving this email?</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #555;">
                        An account was created on {app_name} using this email address (<strong>{to_email}</strong>). This is a required security step to verify that you own this email address. If you did not create this account, you can safely ignore this email.
                    </p>
                </div>
                
                <!-- Account Info -->
                <div style="background-color: #fafafa; padding: 25px; border-radius: 8px; margin: 25px 0; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 20px 0; color: #D914BA; font-size: 18px; font-weight: 600;">Your Account Information</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="color: #555; font-size: 14px;">Account Email:</strong>
                            </td>
                            <td style="padding: 10px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                                <span style="color: #333; font-size: 14px;">{to_email}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 0;">
                                <strong style="color: #555; font-size: 14px;">Temporary Access Code:</strong>
                            </td>
                            <td style="padding: 10px 0; text-align: right;">
                                <span style="font-family: 'Courier New', monospace; background-color: #fff; padding: 8px 12px; border: 2px dashed #D914BA; border-radius: 4px; color: #D914BA; font-size: 16px; font-weight: 700; letter-spacing: 2px; display: inline-block;">{generated_password}</span>
                            </td>
                        </tr>
                    </table>
                    
                    <div style="background-color: #fff8e1; border: 1px solid #ffecb3; padding: 15px; margin-top: 20px; border-radius: 4px;">
                        <p style="margin: 0; color: #f57c00; font-size: 13px; line-height: 1.6;">
                            <strong>⚠️ Security Reminder:</strong> This is a temporary code. You will be required to change it immediately after your first login. Never share your access code with anyone, including {app_name} staff.
                        </p>
                    </div>
                </div>
                
                <!-- Verification Section -->
                <div style="margin: 30px 0;">
                    <h3 style="margin: 0 0 15px 0; color: #D914BA; font-size: 18px; font-weight: 600;">📋 Verify Your Email Address</h3>
                    <p style="margin: 0 0 20px 0; font-size: 15px; line-height: 1.7; color: #555;">
                        To activate your account and ensure the security of your information, please verify your email address by clicking the button below. This link is unique to your account and will expire in 24 hours.
                    </p>
                    
                    <!-- CTA Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_link}" style="background-color: #D914BA; color: white; padding: 16px 40px; text-decoration: none; display: inline-block; border-radius: 6px; font-weight: 600; font-size: 16px; box-shadow: 0 2px 4px rgba(217, 20, 186, 0.3);">✓ Verify My Email Address</a>
                    </div>
                    
                    <p style="margin: 20px 0 10px 0; font-size: 13px; color: #777; text-align: center;">
                        Button not working? Copy and paste this URL into your web browser:
                    </p>
                    <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 4px; margin: 10px 0;">
                        <p style="margin: 0; word-break: break-all; color: #D914BA; font-size: 12px; font-family: 'Courier New', monospace; line-height: 1.6;">{verification_link}</p>
                    </div>
                    
                    <p style="margin: 15px 0 0 0; font-size: 13px; color: #777; line-height: 1.6;">
                        <strong>Note:</strong> This verification link was generated for <strong>{to_email}</strong> and can only be used once. For security reasons, do not share this link with anyone.
                    </p>
                </div>
                
                <!-- Getting Started -->
                <div style="margin: 30px 0; padding: 25px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 15px 0; color: #D914BA; font-size: 18px; font-weight: 600;">🚀 Getting Started</h3>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555;">Once you've verified your email, follow these steps:</p>
                    <ol style="margin: 0; padding-left: 25px; line-height: 2; font-size: 14px; color: #555;">
                        <li>Click the verification link above to confirm your email</li>
                        <li>Sign in to your account using your email and temporary access code</li>
                        <li>You'll be prompted to create a new, secure password</li>
                        <li>Complete your profile information to personalize your experience</li>
                        <li>Explore our platform and start using our services</li>
                    </ol>
                </div>
                
                <!-- Security Tips -->
                <div style="margin: 30px 0; padding: 20px; background-color: #f0f8ff; border-radius: 8px; border-left: 4px solid #2196f3;">
                    <h4 style="margin: 0 0 12px 0; color: #1976d2; font-size: 16px; font-weight: 600;">🔒 Security Best Practices</h4>
                    <ul style="margin: 0; padding-left: 25px; line-height: 1.8; font-size: 14px; color: #555;">
                        <li>Choose a strong, unique password when setting up your account</li>
                        <li>Never share your login credentials with anyone</li>
                        <li>Be cautious of phishing attempts asking for your password</li>
                        <li>Log out when using shared or public computers</li>
                        <li>Keep your contact information up to date for account recovery</li>
                    </ul>
                </div>
                
                <!-- Support Section -->
                <div style="margin: 30px 0 0 0; padding-top: 25px; border-top: 2px solid #f0f0f0;">
                    <h4 style="margin: 0 0 15px 0; color: #333; font-size: 16px; font-weight: 600;">Need Help?</h4>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        If you're experiencing any issues with the verification process or have questions about your account, our support team is ready to assist you.
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #555;">
                        <strong>Contact Support:</strong><br>
                        📧 Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #D914BA; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a><br>
                        ⏱️ Response Time: Within 24 hours
                    </p>
                </div>
                
                <!-- Did Not Request -->
                <div style="margin: 25px 0 0 0; padding: 20px; background-color: #fff9e6; border-radius: 6px; border: 1px solid #ffe0b2;">
                    <p style="margin: 0; font-size: 13px; color: #e65100; line-height: 1.7;">
                        <strong>⚠️ Didn't create an account?</strong><br>
                        If you did not request this account, you can safely ignore this email. No account will be created without email verification. If you believe someone is attempting to use your email address fraudulently, please contact our support team at <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #D914BA; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a>.
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 30px 25px; text-align: center; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #666; font-weight: 600;">{app_name}</p>
                <p style="margin: 0 0 15px 0; font-size: 12px; color: #888;">
                    Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #D914BA; text-decoration: none;">{settings.SMTP_SUPPORT_EMAIL}</a> | 
                    Website: <a href="https://bantuevents.com" style="color: #D914BA; text-decoration: none;">bantuevents.com</a>
                </p>
                <p style="margin: 0 0 5px 0; font-size: 11px; color: #999;">© 2026 {app_name}. All rights reserved.</p>
                <p style="margin: 0 0 15px 0; font-size: 11px; color: #999; line-height: 1.6;">
                    This is a transactional email related to your account activity.<br>
                    You are receiving this because an account was created with this email address.
                </p>
                <p style="margin: 0; font-size: 11px; color: #aaa;">
                    This email was sent to: <strong>{to_email}</strong>
                </p>
            </div>
        </div>
    </body>
    </html>"""


def get_otp_email_text(
    first_name: str,
    otp: str,
    to_email: str,
    app_name: str
) -> str:
    """Plain text template for OTP email"""
    return f"""
Hello {first_name},

You requested a One-Time Password (OTP) to access your account on {app_name}.

═══════════════════════════════════════
YOUR OTP CODE
═══════════════════════════════════════

{otp}

This code is valid for 10 minutes only.

═══════════════════════════════════════
SECURITY INFORMATION
═══════════════════════════════════════

⚠️ Important Security Reminders:

- Never share this code with anyone, including {app_name} staff
- Our support team will NEVER ask you for your OTP code
- This code expires in 10 minutes from the time it was requested
- Only use this code if you initiated this login attempt
- If you see suspicious activity, contact us immediately

═══════════════════════════════════════
WHY DID I RECEIVE THIS EMAIL?
═══════════════════════════════════════

This email was sent because someone (hopefully you) requested an OTP code for the account associated with {to_email}. This is a security measure to verify your identity.

If you did not request this code:
- You can safely ignore this email - no action is needed
- The code will expire automatically in 10 minutes
- Consider changing your password if you suspect unauthorized access
- Contact our support team for assistance

═══════════════════════════════════════
NEED HELP?
═══════════════════════════════════════

If you're having trouble logging in or have security concerns:

Email: {settings.SMTP_SUPPORT_EMAIL}
Response Time: Within 24 hours

═══════════════════════════════════════

© 2026 {app_name}. All rights reserved.

{app_name}
Email: {settings.SMTP_SUPPORT_EMAIL}
Website: https://bantuevents.com

This is a security-related transactional email sent to: {to_email}
This email was sent because an OTP was requested for your account.

═══════════════════════════════════════
""".strip()


def get_otp_email_template(
    first_name: str,
    otp: str,
    to_email: str,
    app_name: str
) -> str:
    """HTML template for OTP email"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <title>Your OTP Code - {app_name}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background-color: #2196F3; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 600;">🔐 Security Code</h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.95;">One-Time Password</p>
            </div>
            
            <!-- Main Content -->
            <div style="background-color: white; padding: 40px 30px; border-left: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">
                
                <p style="margin: 0 0 20px 0; font-size: 16px;">Hello {first_name},</p>
                
                <p style="margin: 0 0 25px 0; font-size: 15px; line-height: 1.7;">
                    You requested a One-Time Password (OTP) to access your account on <strong>{app_name}</strong>. Use the code below to complete your authentication.
                </p>
                
                <!-- Why This Email -->
                <div style="background-color: #e3f2fd; border-left: 4px solid #2196F3; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #1976d2; font-size: 14px;">📧 Why am I receiving this?</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #555;">
                        Someone (hopefully you) requested an OTP code for the account associated with <strong>{to_email}</strong>. This is a required security step to verify your identity before granting access to your account.
                    </p>
                </div>
                
                <!-- OTP Box -->
                <div style="background-color: #fafafa; padding: 30px; border-radius: 8px; margin: 30px 0; border: 2px solid #e8e8e8; text-align: center;">
                    <p style="margin: 0 0 15px 0; color: #666; font-size: 14px; font-weight: 600;">YOUR ONE-TIME PASSWORD</p>
                    <div style="background-color: #ffffff; border: 3px dashed #2196F3; padding: 20px; margin: 15px 0; border-radius: 8px;">
                        <p style="margin: 0; font-size: 36px; font-weight: 700; letter-spacing: 10px; color: #2196F3; font-family: 'Courier New', monospace;">{otp}</p>
                    </div>
                    <p style="margin: 15px 0 0 0; color: #666; font-size: 13px;">
                        ⏱️ This code is valid for <strong>10 minutes</strong>
                    </p>
                </div>
                
                <!-- Security Warning -->
                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 12px 0; color: #856404; font-weight: 600; font-size: 15px;">⚠️ Important Security Reminders</p>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #856404;">
                        <li><strong>Never share this code</strong> with anyone, including {app_name} staff</li>
                        <li>Our support team will <strong>NEVER</strong> ask you for your OTP code</li>
                        <li>This code expires automatically in 10 minutes from the time it was requested</li>
                        <li>Only use this code if you personally initiated this login attempt</li>
                    </ul>
                </div>
                
                <!-- What to Do Section -->
                <div style="margin: 30px 0; padding: 25px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 15px 0; color: #2196F3; font-size: 18px; font-weight: 600;">How to Use This Code</h3>
                    <ol style="margin: 0; padding-left: 25px; line-height: 2; font-size: 14px; color: #555;">
                        <li>Return to the login page where you requested the OTP</li>
                        <li>Enter the 6-digit code shown above</li>
                        <li>Complete your authentication within 10 minutes</li>
                        <li>You'll be automatically logged in to your account</li>
                    </ol>
                </div>
                
                <!-- Support Section -->
                <div style="margin: 30px 0 0 0; padding-top: 25px; border-top: 2px solid #f0f0f0;">
                    <h4 style="margin: 0 0 15px 0; color: #333; font-size: 16px; font-weight: 600;">Having Trouble?</h4>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        If you're experiencing issues with the OTP code or have security concerns about your account, our support team is here to help.
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #555;">
                        📧 Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #2196F3; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a><br>
                        ⏱️ Response Time: Within 24 hours
                    </p>
                </div>
                
                <!-- Didn't Request -->
                <div style="margin: 25px 0 0 0; padding: 20px; background-color: #fff9e6; border-radius: 6px; border: 1px solid #ffe0b2;">
                    <p style="margin: 0; font-size: 14px; color: #e65100; line-height: 1.7;">
                        <strong>⚠️ Didn't request this code?</strong><br>
                        If you did not initiate this login attempt, you can safely ignore this email. The code will expire automatically in 10 minutes. However, if you're seeing repeated unauthorized attempts, please contact our support team immediately at <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #2196F3; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a> to secure your account.
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 30px 25px; text-align: center; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #666; font-weight: 600;">{app_name}</p>
                <p style="margin: 0 0 15px 0; font-size: 12px; color: #888;">
                    Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #2196F3; text-decoration: none;">{settings.SMTP_SUPPORT_EMAIL}</a> | 
                    Website: <a href="https://bantuevents.com" style="color: #2196F3; text-decoration: none;">bantuevents.com</a>
                </p>
                <p style="margin: 0 0 5px 0; font-size: 11px; color: #999;">© 2026 {app_name}. All rights reserved.</p>
                <p style="margin: 0 0 15px 0; font-size: 11px; color: #999; line-height: 1.6;">
                    This is a security-related transactional email.<br>
                    You received this because an OTP was requested for your account.
                </p>
                <p style="margin: 0; font-size: 11px; color: #aaa;">
                    This email was sent to: <strong>{to_email}</strong>
                </p>
            </div>
        </div>
    </body>
    </html>"""


def get_password_reset_email_text(
    first_name: str,
    reset_link: str,
    to_email: str,
    app_name: str
) -> str:
    """Plain text template for password reset email"""
    return f"""
Hello {first_name},

We received a request to reset the password for your {app_name} account.

═══════════════════════════════════════
PASSWORD RESET REQUEST
═══════════════════════════════════════

To create a new password for your account, please visit the following secure link:

{reset_link}

This link will take you to a secure page where you can set a new password for your account.

═══════════════════════════════════════
IMPORTANT INFORMATION
═══════════════════════════════════════

⏱️ This password reset link will expire in 24 hours for security purposes.

🔒 Your current password remains active and unchanged until you complete the reset process and create a new password.

🛡️ For your security, this link can only be used once. If you need to reset your password again after using this link, you'll need to request a new reset link.

═══════════════════════════════════════
WHY DID I RECEIVE THIS EMAIL?
═══════════════════════════════════════

This email was sent because someone requested a password reset for the account associated with {to_email}. This is a standard security procedure to help you regain access to your account if you've forgotten your password.

If you did not request a password reset:
- You can safely ignore this email
- Your current password will remain unchanged
- No changes will be made to your account
- Consider securing your account if you suspect unauthorized access
- Contact our support team if you have concerns

═══════════════════════════════════════
SECURITY BEST PRACTICES
═══════════════════════════════════════

When creating your new password:

- Use a strong, unique password that you don't use elsewhere
- Make it at least 8 characters long with a mix of letters, numbers, and symbols
- Avoid using personal information like birthdays or names
- Don't share your password with anyone
- Consider using a password manager to keep track of your passwords

═══════════════════════════════════════
NEED HELP?
═══════════════════════════════════════

If you're having trouble resetting your password or have security concerns:

Email: {settings.SMTP_SUPPORT_EMAIL}
Response Time: Within 24 hours

Our support team is available to assist you with any account security questions or concerns you may have.

═══════════════════════════════════════

© 2026 {app_name}. All rights reserved.

{app_name}
Email: {settings.SMTP_SUPPORT_EMAIL}
Website: https://bantuevents.com

This is a security-related transactional email sent to: {to_email}
You received this because a password reset was requested for your account.

═══════════════════════════════════════
""".strip()


def get_password_reset_email_template(
    first_name: str,
    reset_link: str,
    to_email: str,
    app_name: str
) -> str:
    """HTML template for password reset email"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <title>Password Reset Request - {app_name}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background-color: #FF9800; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 600;">🔑 Password Reset</h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.95;">Secure Your Account</p>
            </div>
            
            <!-- Main Content -->
            <div style="background-color: white; padding: 40px 30px; border-left: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">
                
                <p style="margin: 0 0 20px 0; font-size: 16px;">Hello {first_name},</p>
                
                <p style="margin: 0 0 25px 0; font-size: 15px; line-height: 1.7;">
                    We received a request to reset the password for your <strong>{app_name}</strong> account. If you made this request, click the button below to create a new password.
                </p>
                
                <!-- Why This Email -->
                <div style="background-color: #fff3e0; border-left: 4px solid #FF9800; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #e65100; font-size: 14px;">📧 Why am I receiving this?</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #555;">
                        Someone requested a password reset for the account associated with <strong>{to_email}</strong>. This is a standard security procedure to help you regain access to your account if you've forgotten your password.
                    </p>
                </div>
                
                <!-- Reset Button -->
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{reset_link}" style="background-color: #FF9800; color: white; padding: 16px 40px; text-decoration: none; display: inline-block; border-radius: 6px; font-weight: 600; font-size: 16px; box-shadow: 0 2px 4px rgba(255, 152, 0, 0.3);">🔒 Reset My Password</a>
                </div>
                
                <!-- Alternative Link -->
                <p style="margin: 20px 0 10px 0; font-size: 13px; color: #777; text-align: center;">
                    Button not working? Copy and paste this URL into your web browser:
                </p>
                <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 4px; margin: 10px 0;">
                    <p style="margin: 0; word-break: break-all; color: #FF9800; font-size: 12px; font-family: 'Courier New', monospace; line-height: 1.6;">{reset_link}</p>
                </div>
                
                <p style="margin: 15px 0 0 0; font-size: 13px; color: #777; line-height: 1.6; text-align: center;">
                    <strong>Note:</strong> This password reset link was generated for <strong>{to_email}</strong> and can only be used once.
                </p>
                
                <!-- Important Information -->
                <div style="margin: 30px 0; padding: 25px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 15px 0; color: #FF9800; font-size: 18px; font-weight: 600;">⏱️ Important Information</h3>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.9; font-size: 14px; color: #555;">
                        <li>This password reset link will <strong>expire in 24 hours</strong> for security purposes</li>
                        <li>Your current password remains active until you complete the reset process</li>
                        <li>This link can only be used once - you'll need to request a new one if needed</li>
                        <li>Once you set a new password, you'll need to use it for all future logins</li>
                    </ul>
                </div>
                
                <!-- Security Tips -->
                <div style="margin: 30px 0; padding: 20px; background-color: #e8f5e9; border-radius: 8px; border-left: 4px solid #4CAF50;">
                    <h4 style="margin: 0 0 12px 0; color: #2e7d32; font-size: 16px; font-weight: 600;">🔒 Password Security Tips</h4>
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        When creating your new password:
                    </p>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                        <li>Use a strong, unique password you don't use elsewhere</li>
                        <li>Make it at least 8 characters with letters, numbers, and symbols</li>
                        <li>Avoid using personal information like birthdays or names</li>
                        <li>Consider using a password manager to keep track</li>
                        <li>Never share your password with anyone</li>
                    </ul>
                </div>
                
                <!-- Support Section -->
                <div style="margin: 30px 0 0 0; padding-top: 25px; border-top: 2px solid #f0f0f0;">
                    <h4 style="margin: 0 0 15px 0; color: #333; font-size: 16px; font-weight: 600;">Need Assistance?</h4>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        If you're having trouble resetting your password or have security concerns about your account, our support team is ready to help.
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #555;">
                        📧 Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #FF9800; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a><br>
                        ⏱️ Response Time: Within 24 hours
                    </p>
                </div>
                
                <!-- Didn't Request -->
                <div style="margin: 25px 0 0 0; padding: 20px; background-color: #ffebee; border-radius: 6px; border: 1px solid #ffcdd2;">
                    <p style="margin: 0; font-size: 14px; color: #c62828; line-height: 1.7;">
                        <strong>⚠️ Didn't request a password reset?</strong><br>
                        If you did not request this password reset, you can safely ignore this email. Your current password will remain unchanged and no modifications will be made to your account. However, if you're concerned about unauthorized access attempts, please contact our support team at <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #FF9800; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a> immediately.
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 30px 25px; text-align: center; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #666; font-weight: 600;">{app_name}</p>
                <p style="margin: 0 0 15px 0; font-size: 12px; color: #888;">
                    Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #FF9800; text-decoration: none;">{settings.SMTP_SUPPORT_EMAIL}</a> | 
                    Website: <a href="https://bantuevents.com" style="color: #FF9800; text-decoration: none;">bantuevents.com</a>
                </p>
                <p style="margin: 0 0 5px 0; font-size: 11px; color: #999;">© 2026 {app_name}. All rights reserved.</p>
                <p style="margin: 0 0 15px 0; font-size: 11px; color: #999; line-height: 1.6;">
                    This is a security-related transactional email.<br>
                    You received this because a password reset was requested for your account.
                </p>
                <p style="margin: 0; font-size: 11px; color: #aaa;">
                    This email was sent to: <strong>{to_email}</strong>
                </p>
            </div>
        </div>
    </body>
    </html>"""


def get_password_changed_email_text(
    first_name: str,
    to_email: str,
    app_name: str
) -> str:
    """Plain text template for password changed confirmation email"""
    return f"""
Hello {first_name},

This email confirms that your password was successfully changed on your {app_name} account.

═══════════════════════════════════════
PASSWORD CHANGE CONFIRMATION
═══════════════════════════════════════

✅ Your password has been changed successfully!

You can now use your new password to log in to your account. This change was made to enhance the security of your account.

Change Details:
- Account: {to_email}
- Date: Just now
- Action: Password updated successfully

═══════════════════════════════════════
WHAT THIS MEANS
═══════════════════════════════════════

Your old password is no longer valid. From now on, you'll need to use the new password you just created to access your account.

If you made this change:
- No further action is required
- You can continue using {app_name} with your new password
- Make sure to store your new password securely

═══════════════════════════════════════
DIDN'T MAKE THIS CHANGE?
═══════════════════════════════════════

⚠️ URGENT: If you did not change your password, your account may be compromised.

Take these steps immediately:

1. Reset your password again using a secure device
2. Review your account for any unauthorized activity
3. Check your recent login history
4. Contact our support team at {settings.SMTP_SUPPORT_EMAIL}
5. Consider enabling two-factor authentication (if available)

═══════════════════════════════════════
SECURITY BEST PRACTICES
═══════════════════════════════════════

To keep your account secure:

- Use a strong, unique password for {app_name}
- Don't reuse passwords from other websites
- Enable two-factor authentication if available
- Never share your password with anyone
- Be cautious of phishing emails asking for your login information
- Log out when using shared or public computers
- Keep your contact information up to date for account recovery
- Regularly review your account activity

═══════════════════════════════════════
WHY DID I RECEIVE THIS EMAIL?
═══════════════════════════════════════

This is a security notification sent to inform you that the password for the account associated with {to_email} was recently changed. We send these notifications to help you monitor your account security and detect any unauthorized changes.

You will always receive this confirmation email whenever your password is changed, regardless of who initiated the change. This is a standard security measure to protect your account.

═══════════════════════════════════════
NEED HELP?
═══════════════════════════════════════

If you have questions about this password change or concerns about your account security:

Email: {settings.SMTP_SUPPORT_EMAIL}
Response Time: Within 24 hours

Our security team is available to assist with any account-related concerns.

═══════════════════════════════════════

© 2026 {app_name}. All rights reserved.

{app_name}
Email: {settings.SMTP_SUPPORT_EMAIL}
Website: https://bantuevents.com

This is a security notification sent to: {to_email}
You received this because your account password was changed.

═══════════════════════════════════════
""".strip()


def get_password_changed_email_template(
    first_name: str,
    to_email: str,
    app_name: str
) -> str:
    """HTML template for password changed confirmation email"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <title>Password Changed Successfully - {app_name}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background-color: #4CAF50; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 600;">✅ Password Updated</h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.95;">Security Confirmation</p>
            </div>
            
            <!-- Main Content -->
            <div style="background-color: white; padding: 40px 30px; border-left: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">
                
                <p style="margin: 0 0 20px 0; font-size: 16px;">Hello {first_name},</p>
                
                <p style="margin: 0 0 25px 0; font-size: 15px; line-height: 1.7;">
                    This email confirms that the password for your <strong>{app_name}</strong> account was successfully changed. You can now use your new password to access your account.
                </p>
                
                <!-- Success Confirmation -->
                <div style="background-color: #e8f5e9; border-left: 4px solid #4CAF50; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #2e7d32; font-size: 16px;">✅ Password Changed Successfully!</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #555;">
                        Your password has been updated and is now active. You can use your new password for all future logins to {app_name}.
                    </p>
                </div>
                
                <!-- Change Details -->
                <div style="background-color: #fafafa; padding: 25px; border-radius: 8px; margin: 25px 0; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 20px 0; color: #4CAF50; font-size: 18px; font-weight: 600;">Change Details</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="color: #555; font-size: 14px;">Account:</strong>
                            </td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                                <span style="color: #333; font-size: 14px;">{to_email}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="color: #555; font-size: 14px;">Date:</strong>
                            </td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                                <span style="color: #333; font-size: 14px;">Just now</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0;">
                                <strong style="color: #555; font-size: 14px;">Action:</strong>
                            </td>
                            <td style="padding: 12px 0; text-align: right;">
                                <span style="color: #4CAF50; font-size: 14px; font-weight: 600;">Password updated successfully</span>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <!-- What This Means -->
                <div style="margin: 30px 0; padding: 25px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 15px 0; color: #4CAF50; font-size: 18px; font-weight: 600;">What This Means</h3>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        Your old password is no longer valid. From now on, you'll need to use the new password you just created to access your account.
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #555; line-height: 1.7;">
                        <strong>If you made this change:</strong> No further action is required. You can continue using {app_name} with your new password. Make sure to store it securely.
                    </p>
                </div>
                
                <!-- Urgent Warning -->
                <div style="margin: 30px 0; padding: 20px; background-color: #ffebee; border-radius: 6px; border-left: 4px solid #f44336;">
                    <p style="margin: 0 0 15px 0; color: #c62828; font-weight: 600; font-size: 16px;">⚠️ Didn't Make This Change?</p>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #d32f2f; line-height: 1.7;">
                        <strong>URGENT:</strong> If you did not change your password, your account may be compromised. Take immediate action to secure your account.
                    </p>
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; font-weight: 600;">
                        Take these steps immediately:
                    </p>
                    <ol style="margin: 0; padding-left: 20px; line-height: 1.9; font-size: 14px; color: #555;">
                        <li>Reset your password again using a secure device</li>
                        <li>Review your account for any unauthorized activity</li>
                        <li>Check your recent login history</li>
                        <li>Contact our support team at <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #f44336; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a></li>
                        <li>Consider enabling two-factor authentication (if available)</li>
                    </ol>
                </div>
                
                <!-- Security Best Practices -->
                <div style="margin: 30px 0; padding: 20px; background-color: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
                    <h4 style="margin: 0 0 12px 0; color: #1976d2; font-size: 16px; font-weight: 600;">🔒 Security Best Practices</h4>
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        To keep your account secure:
                    </p>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                        <li>Use a strong, unique password for {app_name}</li>
                        <li>Don't reuse passwords from other websites</li>
                        <li>Enable two-factor authentication if available</li>
                        <li>Never share your password with anyone</li>
                        <li>Be cautious of phishing emails</li>
                        <li>Log out when using shared or public computers</li>
                        <li>Keep your contact information up to date</li>
                        <li>Regularly review your account activity</li>
                    </ul>
                </div>
                
                <!-- Why This Email -->
                <div style="background-color: #f0f8ff; border-left: 4px solid #2196F3; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #1976d2; font-size: 14px;">📧 Why am I receiving this?</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #555;">
                        This is a security notification sent to inform you that the password for the account associated with <strong>{to_email}</strong> was recently changed. We send these notifications to help you monitor your account security and detect any unauthorized changes. You will always receive this email whenever your password is changed, regardless of who initiated the change.
                    </p>
                </div>
                
                <!-- Support Section -->
                <div style="margin: 30px 0 0 0; padding-top: 25px; border-top: 2px solid #f0f0f0;">
                    <h4 style="margin: 0 0 15px 0; color: #333; font-size: 16px; font-weight: 600;">Need Help?</h4>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        If you have questions about this password change or concerns about your account security, our support team is here to assist you.
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #555;">
                        📧 Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #4CAF50; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a><br>
                        ⏱️ Response Time: Within 24 hours
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 30px 25px; text-align: center; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #666; font-weight: 600;">{app_name}</p>
                <p style="margin: 0 0 15px 0; font-size: 12px; color: #888;">
                    Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #4CAF50; text-decoration: none;">{settings.SMTP_SUPPORT_EMAIL}</a> | 
                    Website: <a href="https://bantuevents.com" style="color: #4CAF50; text-decoration: none;">bantuevents.com</a>
                </p>
                <p style="margin: 0 0 5px 0; font-size: 11px; color: #999;">© 2026 {app_name}. All rights reserved.</p>
                <p style="margin: 0 0 15px 0; font-size: 11px; color: #999; line-height: 1.6;">
                    This is a security notification.<br>
                    You received this because your account password was changed.
                </p>
                <p style="margin: 0; font-size: 11px; color: #aaa;">
                    This email was sent to: <strong>{to_email}</strong>
                </p>
            </div>
        </div>
    </body>
    </html>"""


def get_account_locked_email_text(
    first_name: str,
    to_email: str,
    app_name: str
) -> str:
    """Plain text template for account locked notification email"""
    return f"""
Hello {first_name},

This is an important security notification regarding your {app_name} account.

═══════════════════════════════════════
⚠️ ACCOUNT SECURITY ALERT
═══════════════════════════════════════

Your account has been temporarily locked for security purposes.

Account: {to_email}
Status: Temporarily Locked
Reason: Multiple failed login attempts detected
Action Required: Yes

═══════════════════════════════════════
WHAT HAPPENED?
═══════════════════════════════════════

Our security system detected multiple consecutive failed login attempts on your account. To protect your account from unauthorized access and potential security threats, we have automatically locked it as a precautionary measure.

This is a standard security protocol designed to prevent:
- Brute force attacks on your account
- Unauthorized access attempts
- Potential account compromise
- Identity theft

The failed login attempts were detected from:
- Multiple incorrect password entries
- Suspicious login patterns
- Potential automated access attempts

═══════════════════════════════════════
HOW TO UNLOCK YOUR ACCOUNT
═══════════════════════════════════════

You have several options to regain access to your account:

Option 1: Reset Your Password (Recommended)
1. Go to the {app_name} login page
2. Click on "Forgot Password" or "Reset Password"
3. Enter your email address: {to_email}
4. Follow the instructions in the password reset email
5. Create a new, strong password
6. Your account will be automatically unlocked

Option 2: Contact Support Team
If you're unable to reset your password or need immediate assistance:
- Email our support team at {settings.SMTP_SUPPORT_EMAIL}
- Include your account email ({to_email}) in your message
- Our team will verify your identity and help unlock your account
- Response time: Within 24 hours

Option 3: Automatic Unlock (if enabled)
Some accounts may be automatically unlocked after 30 minutes of inactivity. However, we strongly recommend resetting your password for security reasons.

═══════════════════════════════════════
DIDN'T TRY TO LOG IN?
═══════════════════════════════════════

⚠️ URGENT: If you did NOT attempt to access your account, someone may be trying to gain unauthorized access.

Take these immediate security steps:

1. Reset your password immediately using a secure device
2. Use a strong, unique password you haven't used before
3. Enable two-factor authentication (if available)
4. Review your account for any suspicious or unauthorized activity
5. Check your recent login history and connected devices
6. Update your security questions and recovery email
7. Contact our support team at {settings.SMTP_SUPPORT_EMAIL} immediately
8. Consider changing passwords on other accounts if you've reused them

═══════════════════════════════════════
SECURITY BEST PRACTICES
═══════════════════════════════════════

To prevent future account lockouts and enhance your security:

Password Security:
- Use a strong, unique password with at least 12 characters
- Include a mix of uppercase, lowercase, numbers, and symbols
- Never reuse passwords from other websites or services
- Change your password regularly (every 3-6 months)
- Use a password manager to store complex passwords securely

Account Protection:
- Enable two-factor authentication (2FA) for an extra layer of security
- Keep your recovery email and phone number up to date
- Never share your password with anyone, including support staff
- Log out when using shared or public computers
- Be cautious of phishing emails asking for login credentials
- Verify URLs before entering your login information
- Monitor your account for suspicious activity regularly

Login Security:
- Always use secure, trusted networks for logging in
- Avoid public Wi-Fi when accessing sensitive accounts
- Keep your devices and browsers updated with latest security patches
- Use antivirus software on your devices
- Clear browser cache and cookies regularly

═══════════════════════════════════════
WHY DID I RECEIVE THIS EMAIL?
═══════════════════════════════════════

This is a critical security notification sent because our automated security system detected multiple failed login attempts on the account associated with {to_email}.

We send these notifications to:
- Alert you of potential security threats to your account
- Prevent unauthorized access to your personal information
- Help you take immediate action to secure your account
- Keep you informed about important account changes

This is NOT a phishing email. We will never ask you to:
- Reply to this email with your password
- Click links to verify your account information (except password reset)
- Provide sensitive information via email
- Transfer money or make payments

All legitimate account recovery must be done through our official website or by contacting our verified support email: {settings.SMTP_SUPPORT_EMAIL}

═══════════════════════════════════════
ADDITIONAL INFORMATION
═══════════════════════════════════════

Account Lock Details:
- This is a temporary security measure
- Your account data remains safe and unchanged
- You can unlock your account at any time by resetting your password
- No information has been compromised at this time

What We DON'T Do:
- We never lock accounts without multiple failed attempts
- We don't request payment to unlock accounts
- We won't ask you to verify account info via email
- We don't disable accounts without cause

═══════════════════════════════════════
NEED IMMEDIATE HELP?
═══════════════════════════════════════

Our security and support teams are available to assist you:

Email: {settings.SMTP_SUPPORT_EMAIL}
Response Time: Within 24 hours (Priority for security issues)

When contacting support, please include:
- Your account email: {to_email}
- A brief description of the issue
- Any relevant timestamps or details about login attempts
- Your preferred contact method

Our team will:
- Verify your identity through secure methods
- Help you regain access to your account
- Review your account security settings
- Provide guidance on preventing future issues
- Answer any questions about account security

═══════════════════════════════════════

© 2026 {app_name}. All rights reserved.

{app_name}
Email: {settings.SMTP_SUPPORT_EMAIL}
Website: https://bantuevents.com

This is a critical security notification sent to: {to_email}
You received this because multiple failed login attempts were detected on your account.

═══════════════════════════════════════
""".strip()


def get_account_locked_email_template(
    first_name: str,
    to_email: str,
    app_name: str
) -> str:
    """HTML template for account locked notification email"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <title>Account Security Alert - {app_name}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background-color: #f44336; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 600;">🔒 Account Security Alert</h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.95;">Temporary Account Lock</p>
            </div>
            
            <!-- Main Content -->
            <div style="background-color: white; padding: 40px 30px; border-left: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">
                
                <p style="margin: 0 0 20px 0; font-size: 16px;">Hello {first_name},</p>
                
                <p style="margin: 0 0 25px 0; font-size: 15px; line-height: 1.7;">
                    This is an important security notification regarding your <strong>{app_name}</strong> account. Please read this message carefully and take appropriate action.
                </p>
                
                <!-- Alert Box -->
                <div style="background-color: #ffebee; border: 3px solid #f44336; padding: 25px; margin: 25px 0; border-radius: 8px; text-align: center;">
                    <h3 style="margin: 0 0 15px 0; color: #c62828; font-size: 20px; font-weight: 700;">⚠️ Your Account Has Been Locked</h3>
                    <p style="margin: 0; color: #d32f2f; font-size: 15px; line-height: 1.7; font-weight: 500;">
                        Due to multiple failed login attempts, your account has been temporarily locked for security purposes.
                    </p>
                </div>
                
                <!-- Account Status -->
                <div style="background-color: #fafafa; padding: 25px; border-radius: 8px; margin: 25px 0; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 20px 0; color: #f44336; font-size: 18px; font-weight: 600;">Account Status</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="color: #555; font-size: 14px;">Account:</strong>
                            </td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                                <span style="color: #333; font-size: 14px;">{to_email}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="color: #555; font-size: 14px;">Status:</strong>
                            </td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                                <span style="color: #f44336; font-size: 14px; font-weight: 700;">Temporarily Locked</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="color: #555; font-size: 14px;">Reason:</strong>
                            </td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                                <span style="color: #333; font-size: 14px;">Multiple failed login attempts</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0;">
                                <strong style="color: #555; font-size: 14px;">Action Required:</strong>
                            </td>
                            <td style="padding: 12px 0; text-align: right;">
                                <span style="color: #f44336; font-size: 14px; font-weight: 600;">Yes - Reset Password</span>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <!-- What Happened -->
                <div style="margin: 30px 0; padding: 25px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e8e8e8;">
                    <h3 style="margin: 0 0 15px 0; color: #f44336; font-size: 18px; font-weight: 600;">What Happened?</h3>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        Our security system detected multiple consecutive failed login attempts on your account. To protect your account from unauthorized access and potential security threats, we have automatically locked it as a precautionary measure.
                    </p>
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; font-weight: 600;">
                        This security protocol helps prevent:
                    </p>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                        <li>Brute force attacks on your account</li>
                        <li>Unauthorized access attempts</li>
                        <li>Potential account compromise</li>
                        <li>Identity theft and data breaches</li>
                    </ul>
                </div>
                
                <!-- How to Unlock -->
                <div style="margin: 30px 0; padding: 25px; background-color: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
                    <h3 style="margin: 0 0 15px 0; color: #1976d2; font-size: 18px; font-weight: 600;">🔓 How to Unlock Your Account</h3>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        You have several options to regain access to your account:
                    </p>
                    
                    <!-- Option 1 -->
                    <div style="background-color: white; padding: 20px; margin: 15px 0; border-radius: 6px; border: 1px solid #90caf9;">
                        <h4 style="margin: 0 0 10px 0; color: #1976d2; font-size: 16px; font-weight: 600;">Option 1: Reset Your Password (Recommended)</h4>
                        <ol style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                            <li>Go to the {app_name} login page</li>
                            <li>Click on "Forgot Password" or "Reset Password"</li>
                            <li>Enter your email address: {to_email}</li>
                            <li>Follow the instructions in the password reset email</li>
                            <li>Create a new, strong password</li>
                            <li>Your account will be automatically unlocked</li>
                        </ol>
                    </div>
                    
                    <!-- Option 2 -->
                    <div style="background-color: white; padding: 20px; margin: 15px 0; border-radius: 6px; border: 1px solid #90caf9;">
                        <h4 style="margin: 0 0 10px 0; color: #1976d2; font-size: 16px; font-weight: 600;">Option 2: Contact Support Team</h4>
                        <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; line-height: 1.7;">
                            If you're unable to reset your password or need immediate assistance:
                        </p>
                        <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                            <li>Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #2196f3; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a></li>
                            <li>Include your account email ({to_email})</li>
                            <li>Response time: Within 24 hours (Priority for security issues)</li>
                        </ul>
                    </div>
                    
                    <!-- Option 3 -->
                    <div style="background-color: white; padding: 20px; margin: 15px 0; border-radius: 6px; border: 1px solid #90caf9;">
                        <h4 style="margin: 0 0 10px 0; color: #1976d2; font-size: 16px; font-weight: 600;">Option 3: Automatic Unlock (if enabled)</h4>
                        <p style="margin: 0; font-size: 14px; color: #555; line-height: 1.7;">
                            Some accounts may be automatically unlocked after 30 minutes of inactivity. However, we <strong>strongly recommend</strong> resetting your password for security reasons.
                        </p>
                    </div>
                </div>
                
                <!-- Urgent Warning -->
                <div style="margin: 30px 0; padding: 20px; background-color: #fff3cd; border-radius: 6px; border-left: 4px solid #ffc107;">
                    <p style="margin: 0 0 15px 0; color: #856404; font-weight: 700; font-size: 16px;">⚠️ Didn't Try to Log In?</p>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #856404; line-height: 1.7;">
                        <strong>URGENT:</strong> If you did NOT attempt to access your account, someone may be trying to gain unauthorized access.
                    </p>
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; font-weight: 600;">
                        Take these immediate security steps:
                    </p>
                    <ol style="margin: 0; padding-left: 20px; line-height: 1.9; font-size: 14px; color: #555;">
                        <li>Reset your password immediately using a secure device</li>
                        <li>Use a strong, unique password you haven't used before</li>
                        <li>Enable two-factor authentication (if available)</li>
                        <li>Review your account for suspicious activity</li>
                        <li>Check your recent login history and connected devices</li>
                        <li>Update security questions and recovery email</li>
                        <li>Contact our support team at <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #f44336; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a></li>
                        <li>Change passwords on other accounts if you've reused them</li>
                    </ol>
                </div>
                
                <!-- Security Best Practices -->
                <div style="margin: 30px 0; padding: 20px; background-color: #e8f5e9; border-radius: 8px; border-left: 4px solid #4CAF50;">
                    <h4 style="margin: 0 0 12px 0; color: #2e7d32; font-size: 16px; font-weight: 600;">🔒 Security Best Practices</h4>
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        To prevent future account lockouts and enhance your security:
                    </p>
                    
                    <div style="margin: 15px 0;">
                        <p style="margin: 0 0 8px 0; font-size: 14px; color: #2e7d32; font-weight: 600;">Password Security:</p>
                        <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                            <li>Use a strong, unique password with at least 12 characters</li>
                            <li>Include uppercase, lowercase, numbers, and symbols</li>
                            <li>Never reuse passwords from other websites</li>
                            <li>Change your password regularly (every 3-6 months)</li>
                            <li>Use a password manager to store complex passwords</li>
                        </ul>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <p style="margin: 0 0 8px 0; font-size: 14px; color: #2e7d32; font-weight: 600;">Account Protection:</p>
                        <ul style="margin: 0; padding-left: 20px; line-height: 1.8; font-size: 14px; color: #555;">
                            <li>Enable two-factor authentication for extra security</li>
                            <li>Keep recovery email and phone number up to date</li>
                            <li>Never share your password with anyone</li>
                            <li>Log out when using shared or public computers</li>
                            <li>Be cautious of phishing emails</li>
                            <li>Monitor your account for suspicious activity</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Why This Email -->
                <div style="background-color: #f0f8ff; border-left: 4px solid #2196F3; padding: 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #1976d2; font-size: 14px;">📧 Why am I receiving this?</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #555;">
                        This is a critical security notification sent because our automated security system detected multiple failed login attempts on the account associated with <strong>{to_email}</strong>. We send these notifications to alert you of potential security threats, prevent unauthorized access, and help you take immediate action to secure your account. This is NOT a phishing email - all legitimate account recovery must be done through our official website or by contacting {settings.SMTP_SUPPORT_EMAIL}.
                    </p>
                </div>
                
                <!-- Support Section -->
                <div style="margin: 30px 0 0 0; padding-top: 25px; border-top: 2px solid #f0f0f0;">
                    <h4 style="margin: 0 0 15px 0; color: #333; font-size: 16px; font-weight: 600;">Need Immediate Help?</h4>
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #555; line-height: 1.7;">
                        Our security and support teams are available to assist you with unlocking your account and addressing any security concerns.
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #555;">
                        📧 Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #f44336; text-decoration: none; font-weight: 600;">{settings.SMTP_SUPPORT_EMAIL}</a><br>
                        ⏱️ Response Time: Within 24 hours (Priority for security issues)
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 30px 25px; text-align: center; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #666; font-weight: 600;">{app_name}</p>
                <p style="margin: 0 0 15px 0; font-size: 12px; color: #888;">
                    Email: <a href="mailto:{settings.SMTP_SUPPORT_EMAIL}" style="color: #f44336; text-decoration: none;">{settings.SMTP_SUPPORT_EMAIL}</a> | 
                    Website: <a href="https://bantuevents.com" style="color: #f44336; text-decoration: none;">bantuevents.com</a>
                </p>
                <p style="margin: 0 0 5px 0; font-size: 11px; color: #999;">© 2026 {app_name}. All rights reserved.</p>
                <p style="margin: 0 0 15px 0; font-size: 11px; color: #999; line-height: 1.6;">
                    This is a critical security notification.<br>
                    You received this because multiple failed login attempts were detected on your account.
                </p>
                <p style="margin: 0; font-size: 11px; color: #aaa;">
                    This email was sent to: <strong>{to_email}</strong>
                </p>
            </div>
        </div>
    </body>
    </html>"""
