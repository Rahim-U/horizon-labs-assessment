import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ...schemas.user import UserCreate, UserOut
from ...schemas.token import Token
from ...schemas.auth import AuthResponse
from ...schemas.error import ErrorResponse, ValidationErrorResponse, NotFoundErrorResponse, UnauthorizedErrorResponse
from ...services.auth import register_user, authenticate_user
from ...core.security import create_access_token
from ...api.dependencies import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad request - Email already registered or invalid input"
        },
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error - Invalid request data format or constraints"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - Database or server error"
        },
    },
    summary="Register a new user",
    description="Create a new user account and automatically log them in. Email must be unique and password must be at least 8 characters long.",
    response_description="The newly created user and JWT access token",
)
def register(
    request: Request,
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    **Request Body:**
    - **email**: User email address (required, must be valid email format, unique)
    - **username**: User display name (required, 3-50 characters)
    - **password**: User password (required, 8-100 characters, will be hashed with bcrypt)
    
    **Response:**
    - **201 Created**: User successfully created
    - **400 Bad Request**: Email already registered or invalid input
    - **422 Unprocessable Entity**: Validation error (invalid email format, password too short, etc.)
    - **500 Internal Server Error**: Database or server error
    
    Returns the created user object (without password).
    """
    try:
        # Validate payload is not empty
        if not payload.email or not payload.username or not payload.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email, username, and password are required"
            )
        
        # Additional validation: check for whitespace-only values
        if payload.email.strip() == "" or payload.username.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and username cannot be empty or whitespace only"
            )
        
        # Attempt to register user
        user = register_user(db, payload.email.strip().lower(), payload.username.strip(), payload.password)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        logger.info(f"User registered successfully: {user.email}")

        # Generate JWT token for the new user
        token = create_access_token({"sub": str(user.id)})

        return AuthResponse(
            user=UserOut.model_validate(user),
            token=Token(access_token=token)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except IntegrityError as e:
        logger.error(f"Database integrity error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered or database constraint violation"
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized - Invalid email or password"
        },
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error - Missing username or password"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - Database or server error"
        },
    },
    summary="User login",
    description="Authenticate a user with email and password. Returns user data and JWT access token for use in subsequent requests.",
    response_description="User data and JWT access token",
)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    Uses OAuth2 password flow. The username field should contain the user's email address.
    
    **Request Body (form-data):**
    - **username**: User email address (required, OAuth2 standard uses 'username' field)
    - **password**: User password (required)
    
    **Response:**
    - **200 OK**: Authentication successful, returns JWT token
    - **401 Unauthorized**: Invalid email or password
    - **422 Unprocessable Entity**: Missing username or password
    - **500 Internal Server Error**: Database or server error
    
    Returns a JWT access token that expires after the configured time (default: 60 minutes).
    The token should be included in the Authorization header as: `Bearer <token>`
    """
    try:
        # Validate that username and password are provided
        if not form_data.username or not form_data.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username (email) and password are required"
            )
        
        # Validate email format (basic check)
        email = form_data.username.strip().lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email format"
            )
        
        # Validate password is not empty
        if len(form_data.password.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password cannot be empty"
            )
        
        # Attempt authentication
        user, token = authenticate_user(db, email, form_data.password)
        
        if user is None or token is None:
            logger.warning(f"Failed login attempt for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"User logged in successfully: {user.email}")
        return AuthResponse(
            user=UserOut.model_validate(user),
            token=Token(access_token=token)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )