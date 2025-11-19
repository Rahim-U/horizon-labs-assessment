from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Token(BaseModel):
    """JWT token response schema with access and refresh tokens."""
    access_token: str = Field(description="JWT access token for authentication")
    refresh_token: Optional[str] = Field(default=None, description="JWT refresh token for obtaining new access tokens")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer' for OAuth2)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )