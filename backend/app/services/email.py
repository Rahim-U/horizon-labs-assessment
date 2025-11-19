import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import aiosmtplib
from jinja2 import Template
from ..core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send an email using SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content (optional, fallback for HTML)

    Returns:
        True if email was sent successfully, False otherwise
    """
    if not settings.SMTP_USER or not settings.SMTP_FROM_EMAIL:
        logger.warning("SMTP not configured, skipping email send")
        return False

    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = subject

        # Add text and HTML parts
        if text_content:
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
        )

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


async def send_verification_email(email: str, username: str, token: str) -> bool:
    """
    Send email verification link to user.

    Args:
        email: User email address
        username: User display name
        token: Email verification token

    Returns:
        True if email was sent successfully, False otherwise
    """
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #4F46E5; color: white; padding: 20px; text-align: center; }
            .content { padding: 30px; background-color: #f9f9f9; }
            .button {
                display: inline-block;
                padding: 12px 30px;
                background-color: #4F46E5;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }
            .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Verify Your Email</h1>
            </div>
            <div class="content">
                <p>Hi {{ username }},</p>
                <p>Thank you for registering! Please verify your email address to activate your account.</p>
                <p style="text-align: center;">
                    <a href="{{ verification_url }}" class="button">Verify Email Address</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #4F46E5;">{{ verification_url }}</p>
                <p>This link will expire in {{ expire_hours }} hours.</p>
                <p>If you didn't create an account, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Task Management. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """)

    html_content = html_template.render(
        username=username,
        verification_url=verification_url,
        expire_hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS
    )

    text_content = f"""
    Hi {username},

    Thank you for registering! Please verify your email address to activate your account.

    Click here to verify: {verification_url}

    This link will expire in {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours.

    If you didn't create an account, you can safely ignore this email.
    """

    return await send_email(
        to_email=email,
        subject="Verify your email address",
        html_content=html_content,
        text_content=text_content
    )


async def send_password_reset_email(email: str, username: str, token: str) -> bool:
    """
    Send password reset link to user.

    Args:
        email: User email address
        username: User display name
        token: Password reset token

    Returns:
        True if email was sent successfully, False otherwise
    """
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #DC2626; color: white; padding: 20px; text-align: center; }
            .content { padding: 30px; background-color: #f9f9f9; }
            .button {
                display: inline-block;
                padding: 12px 30px;
                background-color: #DC2626;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }
            .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
            .warning {
                background-color: #FEF2F2;
                border-left: 4px solid #DC2626;
                padding: 12px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Reset Your Password</h1>
            </div>
            <div class="content">
                <p>Hi {{ username }},</p>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{{ reset_url }}" class="button">Reset Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #DC2626;">{{ reset_url }}</p>
                <p>This link will expire in {{ expire_hours }} hour(s).</p>
                <div class="warning">
                    <strong>Security Notice:</strong> If you didn't request a password reset, please ignore this email.
                    Your password will remain unchanged.
                </div>
            </div>
            <div class="footer">
                <p>&copy; 2024 Task Management. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """)

    html_content = html_template.render(
        username=username,
        reset_url=reset_url,
        expire_hours=settings.PASSWORD_RESET_EXPIRE_HOURS
    )

    text_content = f"""
    Hi {username},

    We received a request to reset your password. Click the link below to create a new password:

    {reset_url}

    This link will expire in {settings.PASSWORD_RESET_EXPIRE_HOURS} hour(s).

    Security Notice: If you didn't request a password reset, please ignore this email.
    Your password will remain unchanged.
    """

    return await send_email(
        to_email=email,
        subject="Reset your password",
        html_content=html_content,
        text_content=text_content
    )
