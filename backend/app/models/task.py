from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, CheckConstraint, Index
from sqlalchemy.orm import relationship
from ..db.session import Base


class Task(Base):
    """
    Task model representing a user's task.
    
    Attributes:
        id: Primary key
        title: Task title (required)
        description: Task description (optional)
        status: Task status - pending, in-progress, or completed
        priority: Task priority - low, medium, or high
        due_date: Optional due date for the task
        user_id: Foreign key to the user who owns the task
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, index=True)
    priority = Column(String(20), nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Add check constraints for status and priority
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'in-progress', 'completed')", name="check_status"),
        CheckConstraint("priority IN ('low', 'medium', 'high')", name="check_priority"),
        Index("idx_user_status", "user_id", "status"),
        Index("idx_user_priority", "user_id", "priority"),
        Index("idx_user_due_date", "user_id", "due_date"),
    )

    user = relationship("User", back_populates="tasks")