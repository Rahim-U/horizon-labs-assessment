from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from ..db.session import Base


class User(Base):
    """
    User model representing an application user.

    Attributes:
        id: Primary key
        email: User email address (unique, indexed)
        username: User display name
        hashed_password: Bcrypt hashed password
        is_verified: Email verification status
        is_active: Account active status
        failed_login_attempts: Counter for failed login attempts
        last_failed_login: Timestamp of last failed login
        account_locked_until: Timestamp when account lockout expires
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
        tasks: Relationship to user's tasks
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_failed_login = Column(DateTime(timezone=True), nullable=True)
    account_locked_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")