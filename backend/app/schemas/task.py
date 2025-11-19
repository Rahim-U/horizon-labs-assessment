from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime, timezone
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    """Base task schema with common fields."""
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description"
    )
    status: TaskStatus = Field(description="Task status")
    priority: TaskPriority = Field(description="Task priority")
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date for the task"
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    
    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate that due date is not in the past."""
        if v:
            # Ensure timezone-aware comparison
            now = datetime.now(timezone.utc)
            if v.tzinfo is None:
                # If due_date is naive, assume UTC
                v = v.replace(tzinfo=timezone.utc)
            if v < now:
                raise ValueError("due_date cannot be in the past")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the API",
                "status": "in-progress",
                "priority": "high",
                "due_date": "2024-12-31T23:59:59Z"
            }
        }
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description"
    )
    status: Optional[TaskStatus] = Field(
        default=None,
        description="Task status"
    )
    priority: Optional[TaskPriority] = Field(
        default=None,
        description="Task priority"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date for the task"
    )
    
    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate that due date is not in the past."""
        if v:
            # Ensure timezone-aware comparison
            now = datetime.now(timezone.utc)
            if v.tzinfo is None:
                # If due_date is naive, assume UTC
                v = v.replace(tzinfo=timezone.utc)
            if v < now:
                raise ValueError("due_date cannot be in the past")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated task title",
                "status": "completed",
                "priority": "medium"
            }
        }
    )


class TaskOut(BaseModel):
    """Schema for task output/response."""
    id: int = Field(description="Task ID")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    status: TaskStatus = Field(description="Task status")
    priority: TaskPriority = Field(description="Task priority")
    due_date: Optional[datetime] = Field(default=None, description="Task due date")
    user_id: int = Field(description="ID of the user who owns the task")
    created_at: datetime = Field(description="Timestamp when the task was created")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp when the task was last updated")
    
    model_config = ConfigDict(from_attributes=True)