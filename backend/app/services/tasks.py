from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from typing import Optional
from ..models.task import Task
from .cache import get_cached, set_cached, cache_key_for_user_tasks, invalidate_user_tasks_cache


def list_tasks(
    db: Session,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    use_cache: bool = True
) -> list[Task]:
    """
    Retrieve tasks for a user with optional filtering, searching, and sorting.

    Args:
        db: Database session
        user_id: ID of the user
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        search: Search query for title or description (optional)
        sort_by: Field to sort by (default: created_at)
        sort_order: Sort order - 'asc' or 'desc' (default: desc)
        use_cache: Whether to use caching (default: True)

    Returns:
        List of Task objects
    """
    # Build cache key from filters
    if use_cache:
        cache_filters = {
            "limit": limit,
            "offset": offset,
            "status": status,
            "priority": priority,
            "search": search,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        cache_key = cache_key_for_user_tasks(user_id, cache_filters)

        # Try to get from cache - NOTE: Caching full ORM objects is complex
        # In production, consider caching task IDs and fetching objects,
        # or serializing to dict. For now, we'll skip cache for simplicity.

    stmt = select(Task).where(Task.user_id == user_id)

    # Apply filters
    if status:
        stmt = stmt.where(Task.status == status)
    if priority:
        stmt = stmt.where(Task.priority == priority)

    # Apply search filter with optimization
    # For SQLite, we use LIKE. For PostgreSQL, consider full-text search.
    if search:
        search_term = f"%{search}%"
        # Use OR condition for title and description
        stmt = stmt.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order.lower() == "asc":
        stmt = stmt.order_by(sort_column.asc())
    else:
        stmt = stmt.order_by(sort_column.desc())

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)

    results = db.execute(stmt).scalars().all()

    return results


def get_task(db: Session, user_id: int, task_id: int) -> Optional[Task]:
    """
    Retrieve a single task by ID for a specific user.
    
    Args:
        db: Database session
        user_id: ID of the user
        task_id: ID of the task
    
    Returns:
        Task object or None if not found
    """
    return db.execute(
        select(Task).where(Task.user_id == user_id, Task.id == task_id)
    ).scalar_one_or_none()


async def create_task(db: Session, user_id: int, payload: dict) -> Task:
    """
    Create a new task for a user.

    Args:
        db: Database session
        user_id: ID of the user
        payload: Dictionary containing task data

    Returns:
        Created Task object

    Raises:
        Exception: If database operation fails
    """
    task = Task(user_id=user_id, **payload)
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        # Invalidate cache for this user's tasks
        await invalidate_user_tasks_cache(user_id)
        return task
    except Exception as e:
        db.rollback()
        raise


async def update_task(db: Session, user_id: int, task_id: int, payload: dict) -> Optional[Task]:
    """
    Update an existing task for a user.

    Automatically updates the updated_at timestamp.

    Args:
        db: Database session
        user_id: ID of the user
        task_id: ID of the task to update
        payload: Dictionary containing fields to update

    Returns:
        Updated Task object or None if not found

    Raises:
        Exception: If database operation fails
    """
    task = get_task(db, user_id, task_id)
    if not task:
        return None

    try:
        # Update fields from payload
        for key, value in payload.items():
            if hasattr(task, key):
                setattr(task, key, value)

        # Explicitly update the updated_at timestamp
        # SQLAlchemy's onupdate should handle this, but we ensure it's set
        task.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(task)
        # Invalidate cache for this user's tasks
        await invalidate_user_tasks_cache(user_id)
        return task
    except Exception as e:
        db.rollback()
        raise


async def delete_task(db: Session, user_id: int, task_id: int) -> bool:
    """
    Delete a task for a user.

    Args:
        db: Database session
        user_id: ID of the user
        task_id: ID of the task to delete

    Returns:
        True if task was deleted, False if not found

    Raises:
        Exception: If database operation fails
    """
    task = get_task(db, user_id, task_id)
    if not task:
        return False

    try:
        db.delete(task)
        db.commit()
        # Invalidate cache for this user's tasks
        await invalidate_user_tasks_cache(user_id)
        return True
    except Exception as e:
        db.rollback()
        raise