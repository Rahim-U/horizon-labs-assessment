from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..core.config import settings
from ..db.session import SessionLocal
from ..models.user import User

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="Bearer",
    description="JWT token authentication. Use format: Bearer <token>"
)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.
    
    Creates a database session and ensures it's properly closed after use.
    This should be used as a FastAPI dependency for route handlers that need database access.
    
    Yields:
        SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user from JWT token.
    
    This dependency extracts the JWT token from the Authorization header,
    validates it, and returns the corresponding user.
    
    Args:
        token: JWT token extracted from Authorization header
        db: Database session
    
    Returns:
        User object for the authenticated user
    
    Raises:
        HTTPException: If token is invalid, expired, or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Extract user ID from token
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Verify token type
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    try:
        user = db.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()
    except (ValueError, TypeError):
        raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return user