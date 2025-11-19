import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...schemas.user import UserCreate, UserOut
from ...schemas.token import Token
from ...schemas.auth import AuthResponse
from ...schemas.error import ErrorResponse, ValidationErrorResponse, UnauthorizedErrorResponse
from ...services.auth import (
    register_user,
    authenticate_user,
    refresh_access_token,
    verify_email,
    request_password_reset,
    reset_password,
    resend_verification_email
)
from ...services.email import send_verification_email, send_password_reset_email
from ...core.security import create_email_verification_token
from ...api.dependencies import get_db
from ...core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VerifyEmailRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class ResendVerificationRequest(BaseModel):
    email: str


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Email already registered or weak password"},
        422: {"model": ValidationErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Register a new user",
    description="Create a new user account with email verification. Password must meet strength requirements.",
)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def register(
    request: Request,
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user with email verification.

    Password requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    try:
        if not payload.email or not payload.username or not payload.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email, username, and password are required"
            )

        if payload.email.strip() == "" or payload.username.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and username cannot be empty or whitespace only"
            )

        # Register user (validates password strength)
        user = register_user(db, payload.email.strip().lower(), payload.username.strip(), payload.password)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        logger.info(f"User registered successfully: {user.email}")

        # Send verification email
        verification_token = create_email_verification_token(user.email)
        await send_verification_email(user.email, user.username, verification_token)
        logger.info(f"Verification email sent to: {user.email}")

        # Generate JWT tokens for the new user
        _, tokens = authenticate_user(db, user.email, payload.password)

        return AuthResponse(
            user=UserOut.model_validate(user),
            token=Token(
                access_token=tokens["access_token"],
                refresh_token=tokens.get("refresh_token"),
                token_type=tokens["token_type"]
            )
        )

    except ValueError as e:
        # Password strength validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Database integrity error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": UnauthorizedErrorResponse, "description": "Invalid credentials or account locked"},
        422: {"model": ValidationErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="User login",
    description="Authenticate user and return access and refresh tokens.",
)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens.

    Account will be locked for 15 minutes after 5 failed login attempts.
    """
    try:
        if not form_data.username or not form_data.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username (email) and password are required"
            )

        email = form_data.username.strip().lower()
        if "@" not in email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email format"
            )

        # Attempt authentication
        user, tokens = authenticate_user(db, email, form_data.password)

        if user is None or tokens is None:
            logger.warning(f"Failed login attempt for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password, or account is locked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"User logged in successfully: {user.email}")
        return AuthResponse(
            user=UserOut.model_validate(user),
            token=Token(
                access_token=tokens["access_token"],
                refresh_token=tokens.get("refresh_token"),
                token_type=tokens["token_type"]
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": UnauthorizedErrorResponse, "description": "Invalid or expired refresh token"},
    },
    summary="Refresh access token",
    description="Generate new access token using refresh token.",
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def refresh_token(
    request: Request,
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using valid refresh token.

    Returns new access and refresh tokens.
    """
    tokens = refresh_access_token(db, payload.refresh_token)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenRefreshResponse(**tokens)


@router.post(
    "/verify-email",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid or expired token"},
    },
    summary="Verify email address",
    description="Verify user email with verification token.",
)
async def verify_user_email(
    payload: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """Verify user email address with token from verification email."""
    success = verify_email(db, payload.token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )

    return {"message": "Email verified successfully"}


@router.post(
    "/resend-verification",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Email not found or already verified"},
    },
    summary="Resend verification email",
    description="Resend email verification link to user.",
)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def resend_verification(
    request: Request,
    payload: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    """Resend verification email to user."""
    user = resend_verification_email(db, payload.email.strip().lower())

    if not user:
        # Return success even if user not found to prevent email enumeration
        return {"message": "If the email exists and is not verified, a verification email has been sent"}

    # Send verification email
    verification_token = create_email_verification_token(user.email)
    await send_verification_email(user.email, user.username, verification_token)
    logger.info(f"Verification email resent to: {user.email}")

    return {"message": "Verification email sent"}


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Request password reset",
    description="Request password reset link via email.",
)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def forgot_password(
    request: Request,
    payload: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset link.

    Always returns success to prevent email enumeration.
    """
    email = payload.email.strip().lower()
    reset_token = request_password_reset(db, email)

    if reset_token:
        # User exists, send password reset email
        from sqlalchemy import select
        from ...models.user import User
        user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

        if user:
            await send_password_reset_email(user.email, user.username, reset_token)
            logger.info(f"Password reset email sent to: {user.email}")

    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid token or weak password"},
    },
    summary="Reset password",
    description="Reset password using reset token from email.",
)
async def reset_user_password(
    payload: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Reset password with token from password reset email."""
    try:
        success = reset_password(db, payload.token, payload.new_password)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        return {"message": "Password reset successfully"}

    except ValueError as e:
        # Password strength validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
