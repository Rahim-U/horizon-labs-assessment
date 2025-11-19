from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, Tuple, Dict
from ..models.user import User
from ..core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_email_verification_token,
    create_password_reset_token,
    verify_token
)
from ..core.validators import is_strong_password

# Account lockout settings
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


def register_user(db: Session, email: str, username: str, password: str) -> Optional[User]:
    """
    Register a new user in the database.

    Args:
        db: Database session
        email: User email address
        username: User display name
        password: Plain text password (will be hashed)

    Returns:
        User object if registration successful, None if email already exists

    Raises:
        ValueError: If password does not meet strength requirements
        Exception: If database operation fails
    """
    # Validate password strength (raises ValueError if weak)
    is_strong_password(password)

    # Create new user with hashed password
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        is_verified=False,  # User must verify email
        is_active=True
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        # Email already exists (database constraint violation)
        db.rollback()
        return None
    except Exception as e:
        db.rollback()
        raise


def authenticate_user(db: Session, email: str, password: str) -> Tuple[Optional[User], Optional[Dict[str, str]]]:
    """
    Authenticate a user and generate JWT tokens.

    Args:
        db: Database session
        email: User email address
        password: Plain text password

    Returns:
        Tuple of (User object, tokens dict) if authentication successful,
        (None, None) if authentication fails

    Tokens dict contains:
        - access_token: Short-lived access token
        - refresh_token: Long-lived refresh token
        - token_type: Always "bearer"
    """
    # Find user by email
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    if not user:
        return None, None

    # Check if account is locked
    if user.account_locked_until:
        if datetime.now(timezone.utc) < user.account_locked_until:
            return None, None
        else:
            # Lockout expired, reset counter
            user.account_locked_until = None
            user.failed_login_attempts = 0
            db.commit()

    # Check if account is active
    if not user.is_active:
        return None, None

    # Verify password
    if not verify_password(password, user.hashed_password):
        # Increment failed attempts
        user.failed_login_attempts += 1
        user.last_failed_login = datetime.now(timezone.utc)

        # Lock account if too many failed attempts
        if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
            user.account_locked_until = datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_DURATION_MINUTES)

        db.commit()
        return None, None

    # Reset failed attempts on successful login
    if user.failed_login_attempts > 0:
        user.failed_login_attempts = 0
        user.last_failed_login = None
        db.commit()

    # Generate JWT tokens with user ID as subject
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

    return user, tokens


def refresh_access_token(db: Session, refresh_token: str) -> Optional[Dict[str, str]]:
    """
    Generate new access token using refresh token.

    Args:
        db: Database session
        refresh_token: Valid refresh token

    Returns:
        New tokens dict if successful, None otherwise
    """
    # Verify refresh token
    payload = verify_token(refresh_token, "refresh")
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    # Verify user exists and is active
    user = db.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        return None

    # Generate new tokens
    access_token = create_access_token({"sub": str(user.id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


def verify_email(db: Session, token: str) -> bool:
    """
    Verify user email with verification token.

    Args:
        db: Database session
        token: Email verification token

    Returns:
        True if verification successful, False otherwise
    """
    # Verify token
    payload = verify_token(token, "email_verification")
    if not payload:
        return False

    email = payload.get("sub")
    if not email:
        return False

    # Find user and mark as verified
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        return False

    if user.is_verified:
        return True  # Already verified

    user.is_verified = True
    db.commit()
    return True


def request_password_reset(db: Session, email: str) -> Optional[str]:
    """
    Generate password reset token for user.

    Args:
        db: Database session
        email: User email address

    Returns:
        Password reset token if user exists, None otherwise
    """
    # Find user by email
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    # Always return None to prevent email enumeration
    # But generate token if user exists
    if not user:
        return None

    return create_password_reset_token(email)


def reset_password(db: Session, token: str, new_password: str) -> bool:
    """
    Reset user password with reset token.

    Args:
        db: Database session
        token: Password reset token
        new_password: New password (plain text, will be hashed)

    Returns:
        True if password reset successful, False otherwise

    Raises:
        ValueError: If new password does not meet strength requirements
    """
    # Validate new password strength
    is_strong_password(new_password)

    # Verify token
    payload = verify_token(token, "password_reset")
    if not payload:
        return False

    email = payload.get("sub")
    if not email:
        return False

    # Find user and update password
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        return False

    user.hashed_password = get_password_hash(new_password)
    # Reset failed login attempts
    user.failed_login_attempts = 0
    user.last_failed_login = None
    user.account_locked_until = None
    db.commit()
    return True


def resend_verification_email(db: Session, email: str) -> Optional[User]:
    """
    Get user for resending verification email.

    Args:
        db: Database session
        email: User email address

    Returns:
        User object if exists and not verified, None otherwise
    """
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    if not user or user.is_verified:
        return None

    return user
