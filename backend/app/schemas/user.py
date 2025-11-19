from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr = Field(description="User email address (must be unique)")
    username: str = Field(
        min_length=3,
        max_length=50,
        description="User display name (3-50 characters)"
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description="User password (minimum 8 characters, will be hashed)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login (not used with OAuth2, but kept for reference)."""
    email: EmailStr = Field(description="User email address")
    password: str = Field(description="User password")


class UserOut(BaseModel):
    """Schema for user output/response (password is never included)."""
    id: int = Field(description="User ID")
    email: EmailStr = Field(description="User email address")
    username: str = Field(description="User display name")
    created_at: datetime = Field(description="Timestamp when the user was created")
    
    model_config = ConfigDict(from_attributes=True)