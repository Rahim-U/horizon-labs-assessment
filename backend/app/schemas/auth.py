from pydantic import BaseModel, Field, ConfigDict
from .token import Token
from .user import UserOut


class AuthResponse(BaseModel):
    """Authentication response schema with user data and token."""
    user: UserOut = Field(description="Authenticated user data")
    token: Token = Field(description="JWT access token")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "username": "johndoe",
                    "created_at": "2025-01-01T12:00:00"
                },
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
                }
            }
        }
    )
