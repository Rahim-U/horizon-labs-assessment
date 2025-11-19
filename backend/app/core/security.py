from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from .config import settings

# Configure password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def create_access_token(subject: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Dictionary containing token claims (typically includes 'sub' for user ID)
        expires_delta: Optional custom expiration time. If not provided, uses default from settings.

    Returns:
        Encoded JWT token string
    """
    to_encode = subject.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": now,  # Issued at time
        "type": "access"  # Token type
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token.

    Args:
        subject: Dictionary containing token claims (typically includes 'sub' for user ID)
        expires_delta: Optional custom expiration time. If not provided, uses default from settings.

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = subject.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({
        "exp": expire,
        "iat": now,  # Issued at time
        "type": "refresh"  # Token type
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_email_verification_token(email: str) -> str:
    """
    Create a JWT token for email verification.

    Args:
        email: User email address

    Returns:
        Encoded JWT token string
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
    to_encode = {
        "sub": email,
        "exp": expire,
        "iat": now,
        "type": "email_verification"
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_password_reset_token(email: str) -> str:
    """
    Create a JWT token for password reset.

    Args:
        email: User email address

    Returns:
        Encoded JWT token string
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=settings.PASSWORD_RESET_EXPIRE_HOURS)
    to_encode = {
        "sub": email,
        "exp": expire,
        "iat": now,
        "type": "password_reset"
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, expected_type: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string
        expected_type: Expected token type ('access', 'refresh', 'email_verification', 'password_reset')

    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        if token_type != expected_type:
            return None
        return payload
    except jwt.JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Bcrypt hashed password string
    """
    return pwd_context.hash(password)