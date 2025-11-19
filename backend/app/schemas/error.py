from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    detail: str = Field(description="Error message describing what went wrong")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Error message here"
            }
        }
    }


class ValidationErrorDetail(BaseModel):
    """Detail for validation errors."""
    loc: List[str | int] = Field(description="Location of the error in the request")
    msg: str = Field(description="Error message")
    type: str = Field(description="Error type")


class ValidationErrorResponse(BaseModel):
    """Detailed validation error response."""
    detail: List[ValidationErrorDetail] = Field(description="List of validation errors")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email"
                    }
                ]
            }
        }
    }


class NotFoundErrorResponse(BaseModel):
    """Error response for resource not found."""
    detail: str = Field(description="Error message")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Resource not found"
            }
        }
    }


class UnauthorizedErrorResponse(BaseModel):
    """Error response for authentication failures."""
    detail: str = Field(description="Error message")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Could not validate credentials"
            }
        }
    }