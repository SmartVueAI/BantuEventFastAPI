"""
Email HTML Templates
"""


def get_user_creation_email_template(
    first_name: str,
    verification_link: str,
    generated_password: str,
    app_name: str = "E-Commerce Platform"
) -> str:
    """
    HTML template for user creation email
    
    Args:
        first_name: User's first name
        verification_link: Email verification link with token
        generated_password: Generated password
        app_name: Application name
    
    Returns:
        HTML email content
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; }}
            .button {{ background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; display: inline-block; border-radius: 4px; margin: 10px 0; }}
            .password-box {{ background-color: #fff; border: 2px dashed #4CAF50; padding: 15px; margin: 15px 0; font-family: monospace; font-size: 16px; text-align: center; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            .warning {{ color: #f44336; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to {app_name}!</h1>
            </div>
            <div class="content">
                <p>Hello {first_name},</p>
                
                <p>Your account has been successfully created! We're excited to have you on board.</p>
                
                <h3>Your Login Credentials:</h3>
                <p><strong>Email:</strong> Your registered email address</p>
                <p><strong>Temporary Password:</strong></p>
                <div class="password-box">
                    {generated_password}
                </div>
                
                <p class="warning">⚠️ Please change this password after your first login for security reasons.</p>
                
                <h3>Email Verification Required:</h3>
                <p>Before you can log in, please verify your email address by clicking the button below:</p>
                
                <p style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Email Address</a>
                </p>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{verification_link}</p>
                
                <h3>Next Steps:</h3>
                <ol>
                    <li>Click the verification link above</li>
                    <li>Log in with your email and temporary password</li>
                    <li>Change your password immediately</li>
                    <li>Complete your profile</li>
                </ol>
                
                <p>If you didn't request this account, please ignore this email or contact our support team.</p>
            </div>
            <div class="footer">
                <p>© 2026 {app_name}. All rights reserved.</p>
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_otp_email_template(
    first_name: str,
    otp: str,
    app_name: str = "E-Commerce Platform"
) -> str:
    """
    HTML template for OTP email
    
    Args:
        first_name: User's first name
        otp: OTP code
        app_name: Application name
    
    Returns:
        HTML email content
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; }}
            .otp-box {{ background-color: #fff; border: 3px solid #2196F3; padding: 20px; margin: 20px 0; text-align: center; }}
            .otp-code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #2196F3; font-family: monospace; }}
            .warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 15px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Your OTP Code</h1>
            </div>
            <div class="content">
                <p>Hello {first_name},</p>
                
                <p>You requested a One-Time Password (OTP) for authentication. Use the code below to complete your login:</p>
                
                <div class="otp-box">
                    <p style="margin: 0; color: #666;">Your OTP Code:</p>
                    <p class="otp-code">{otp}</p>
                    <p style="margin: 0; color: #666; font-size: 12px;">Valid for 10 minutes</p>
                </div>
                
                <div class="warning">
                    <p style="margin: 0;"><strong>⚠️ Security Warning:</strong></p>
                    <ul style="margin: 5px 0;">
                        <li>Never share this code with anyone</li>
                        <li>Our team will never ask for your OTP</li>
                        <li>This code expires in 10 minutes</li>
                    </ul>
                </div>
                
                <p>If you didn't request this code, please ignore this email and ensure your account is secure.</p>
            </div>
            <div class="footer">
                <p>© 2026 {app_name}. All rights reserved.</p>
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_password_reset_email_template(
    first_name: str,
    reset_link: str,
    app_name: str = "E-Commerce Platform"
) -> str:
    """
    HTML template for password reset email
    
    Args:
        first_name: User's first name
        reset_link: Password reset link with token
        app_name: Application name
    
    Returns:
        HTML email content
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #FF9800; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; }}
            .button {{ background-color: #FF9800; color: white; padding: 12px 24px; text-decoration: none; display: inline-block; border-radius: 4px; margin: 10px 0; }}
            .warning {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 15px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔑 Password Reset Request</h1>
            </div>
            <div class="content">
                <p>Hello {first_name},</p>
                
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </p>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{reset_link}</p>
                
                <div class="warning">
                    <p style="margin: 0;"><strong>⚠️ Security Notice:</strong></p>
                    <ul style="margin: 5px 0;">
                        <li>This link expires in 24 hours</li>
                        <li>If you didn't request this reset, please ignore this email</li>
                        <li>Your current password remains unchanged until you create a new one</li>
                    </ul>
                </div>
                
                <p>If you didn't request a password reset, please contact our support team immediately to secure your account.</p>
            </div>
            <div class="footer">
                <p>© 2026 {app_name}. All rights reserved.</p>
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_password_changed_email_template(
    first_name: str,
    app_name: str = "E-Commerce Platform"
) -> str:
    """
    HTML template for password changed confirmation email
    
    Args:
        first_name: User's first name
        app_name: Application name
    
    Returns:
        HTML email content
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; }}
            .success {{ background-color: #e8f5e9; border-left: 4px solid #4CAF50; padding: 10px; margin: 15px 0; }}
            .warning {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 15px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Password Changed Successfully</h1>
            </div>
            <div class="content">
                <p>Hello {first_name},</p>
                
                <div class="success">
                    <p style="margin: 0;"><strong>Your password has been changed successfully!</strong></p>
                </div>
                
                <p>This email confirms that your password was recently changed. You can now use your new password to log in to your account.</p>
                
                <div class="warning">
                    <p style="margin: 0;"><strong>⚠️ Didn't make this change?</strong></p>
                    <p style="margin: 5px 0;">If you didn't change your password, your account may be compromised. Please contact our support team immediately:</p>
                    <ul style="margin: 5px 0;">
                        <li>Reset your password again</li>
                        <li>Check your account for any unauthorized activity</li>
                        <li>Contact support for assistance</li>
                    </ul>
                </div>
                
                <h3>Security Tips:</h3>
                <ul>
                    <li>Use a strong, unique password for your account</li>
                    <li>Enable two-factor authentication if available</li>
                    <li>Never share your password with anyone</li>
                    <li>Be cautious of phishing emails</li>
                </ul>
            </div>
            <div class="footer">
                <p>© 2026 {app_name}. All rights reserved.</p>
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_account_locked_email_template(
    first_name: str,
    app_name: str = "E-Commerce Platform"
) -> str:
    """
    HTML template for account locked notification email
    
    Args:
        first_name: User's first name
        app_name: Application name
    
    Returns:
        HTML email content
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; }}
            .alert {{ background-color: #ffebee; border: 2px solid #f44336; padding: 15px; margin: 15px 0; text-align: center; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 Account Locked</h1>
            </div>
            <div class="content">
                <p>Hello {first_name},</p>
                
                <div class="alert">
                    <h3 style="margin-top: 0; color: #f44336;">⚠️ Your account has been locked</h3>
                    <p>Due to multiple failed login attempts, your account has been temporarily locked for security purposes.</p>
                </div>
                
                <h3>What happened?</h3>
                <p>We detected 3 or more failed login attempts on your account. To protect your account from unauthorized access, we've temporarily locked it.</p>
                
                <h3>How to unlock your account:</h3>
                <ol>
                    <li>Use the "Forgot Password" feature to reset your password</li>
                    <li>Contact our support team for assistance</li>
                    <li>Wait 30 minutes for automatic unlock (if enabled)</li>
                </ol>
                
                <h3>Didn't try to log in?</h3>
                <p>If you didn't attempt to access your account, someone may be trying to access it without your permission. We recommend:</p>
                <ul>
                    <li>Change your password immediately</li>
                    <li>Enable two-factor authentication</li>
                    <li>Review your account for any suspicious activity</li>
                    <li>Contact our support team</li>
                </ul>
            </div>
            <div class="footer">
                <p>© 2026 {app_name}. All rights reserved.</p>
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """