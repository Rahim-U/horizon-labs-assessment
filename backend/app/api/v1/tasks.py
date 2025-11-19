import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...schemas.task import TaskCreate, TaskUpdate, TaskOut, TaskStatus, TaskPriority
from ...schemas.error import ErrorResponse, ValidationErrorResponse, NotFoundErrorResponse, UnauthorizedErrorResponse
from ...api.dependencies import get_db, get_current_user
from ...services.tasks import list_tasks, get_task, create_task, update_task, delete_task
from ...models.user import User
from ...core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized - Invalid or missing authentication token"
        },
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error - Invalid query parameters"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - Database or server error"
        },
    },
    summary="Get user's tasks",
    description="Retrieve a paginated list of tasks for the authenticated user. Supports filtering by status, priority, search query, and sorting by various fields.",
    response_description="List of tasks belonging to the authenticated user",
)
def get_tasks(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of tasks to return (1-100)"),
    offset: int = Query(default=0, ge=0, description="Number of tasks to skip for pagination (>= 0)"),
    status: Optional[TaskStatus] = Query(default=None, description="Filter tasks by status"),
    priority: Optional[TaskPriority] = Query(default=None, description="Filter tasks by priority"),
    search: Optional[str] = Query(default=None, max_length=200, description="Search tasks by title or description"),
    sort_by: str = Query(
        default="created_at",
        description="Field to sort by",
        regex="^(created_at|updated_at|due_date|title|status|priority)$"
    ),
    sort_order: str = Query(
        default="desc",
        regex="^(asc|desc)$",
        description="Sort order: asc or desc"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get tasks for the authenticated user.

    **Query Parameters:**
    - **limit**: Maximum number of tasks to return (1-100, default: 50)
    - **offset**: Number of tasks to skip for pagination (>= 0, default: 0)
    - **status**: Optional filter by task status (pending, in-progress, completed)
    - **priority**: Optional filter by task priority (low, medium, high)
    - **search**: Optional search query to filter by title or description (max 200 chars)
    - **sort_by**: Field to sort by (created_at, updated_at, due_date, title, status, priority, default: created_at)
    - **sort_order**: Sort order - 'asc' or 'desc' (default: desc)

    **Response:**
    - **200 OK**: List of tasks (may be empty)
    - **401 Unauthorized**: Invalid or missing authentication token
    - **422 Unprocessable Entity**: Invalid query parameters
    - **500 Internal Server Error**: Database or server error

    Returns a list of tasks that belong to the authenticated user.
    """
    try:
        # Convert enum to string if provided
        status_str = status.value if status else None
        priority_str = priority.value if priority else None

        # Validate sort_by field exists on Task model
        valid_sort_fields = ["created_at", "updated_at", "due_date", "title", "status", "priority"]
        if sort_by not in valid_sort_fields:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid sort_by field. Must be one of: {', '.join(valid_sort_fields)}"
            )

        tasks = list_tasks(
            db,
            current_user.id,
            limit=limit,
            offset=offset,
            status=status_str,
            priority=priority_str,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        logger.info(f"Retrieved {len(tasks)} tasks for user {current_user.id}")
        return tasks
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error while retrieving tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized - Invalid or missing authentication token"
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
    summary="Create a new task",
    description="Create a new task for the authenticated user. All fields except description and due_date are required.",
    response_description="The newly created task with ID and timestamps",
)
async def create_new_task(
    request: Request,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.
    
    **Request Body:**
    - **title**: Task title (required, 1-255 characters)
    - **description**: Task description (optional, max 2000 characters)
    - **status**: Task status - pending, in-progress, or completed (required)
    - **priority**: Task priority - low, medium, or high (required)
    - **due_date**: Optional due date (must be in the future, ISO 8601 format)
    
    **Response:**
    - **201 Created**: Task successfully created
    - **401 Unauthorized**: Invalid or missing authentication token
    - **422 Unprocessable Entity**: Validation error (invalid data format, due_date in past, etc.)
    - **500 Internal Server Error**: Database or server error
    
    Returns the created task with generated ID and timestamps.
    """
    try:
        # Validate required fields are present
        if not payload.title or not payload.title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title is required and cannot be empty"
            )
        
        if not payload.status:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task status is required"
            )
        
        if not payload.priority:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task priority is required"
            )
        
        # Validate title length
        if len(payload.title.strip()) > 255:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title cannot exceed 255 characters"
            )
        
        # Validate description length if provided
        if payload.description and len(payload.description) > 2000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task description cannot exceed 2000 characters"
            )
        
        # Create task
        task = await create_task(db, current_user.id, payload.model_dump())
        
        logger.info(f"Task created successfully: {task.id} for user {current_user.id}")
        return task
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Database integrity error while creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation. Please check your input."
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error while creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized - Invalid or missing authentication token"
        },
        404: {
            "model": NotFoundErrorResponse,
            "description": "Task not found or does not belong to the user"
        },
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error - Invalid task_id format"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - Database or server error"
        },
    },
    summary="Get a single task",
    description="Retrieve a specific task by ID. Only tasks belonging to the authenticated user can be accessed.",
    response_description="The requested task",
)
def get_single_task(
    request: Request,
    task_id: int = Path(..., description="ID of the task to retrieve", ge=1, le=2147483647),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single task by ID for the authenticated user.
    
    **Path Parameters:**
    - **task_id**: The ID of the task to retrieve (must be >= 1)
    
    **Response:**
    - **200 OK**: Task found and returned
    - **401 Unauthorized**: Invalid or missing authentication token
    - **404 Not Found**: Task not found or does not belong to the user
    - **422 Unprocessable Entity**: Invalid task_id format
    - **500 Internal Server Error**: Database or server error
    
    Returns the task if it exists and belongs to the authenticated user.
    Raises 404 if the task is not found or doesn't belong to the user.
    """
    try:
        # Validate task_id is positive
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task ID must be a positive integer"
            )
        
        task = get_task(db, current_user.id, task_id)
        
        if not task:
            logger.warning(f"Task {task_id} not found for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        logger.info(f"Task {task_id} retrieved for user {current_user.id}")
        return task
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error while retrieving task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.put(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad request - Empty update payload or invalid data"
        },
        401: {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized - Invalid or missing authentication token"
        },
        404: {
            "model": NotFoundErrorResponse,
            "description": "Task not found or does not belong to the user"
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
    summary="Update a task",
    description="Update an existing task. Only tasks belonging to the authenticated user can be updated. All fields are optional - only provided fields will be updated.",
    response_description="The updated task",
)
async def update_existing_task(
    request: Request,
    task_id: int = Path(..., description="ID of the task to update", ge=1, le=2147483647),
    payload: TaskUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing task for the authenticated user.
    
    **Path Parameters:**
    - **task_id**: The ID of the task to update (must be >= 1)
    
    **Request Body (all fields optional):**
    - **title**: Task title (1-255 characters if provided)
    - **description**: Task description (max 2000 characters if provided)
    - **status**: Task status - pending, in-progress, or completed
    - **priority**: Task priority - low, medium, or high
    - **due_date**: Due date (must be in the future if provided, ISO 8601 format)
    
    **Response:**
    - **200 OK**: Task successfully updated
    - **400 Bad Request**: Empty update payload
    - **401 Unauthorized**: Invalid or missing authentication token
    - **404 Not Found**: Task not found or does not belong to the user
    - **422 Unprocessable Entity**: Validation error (invalid data format, due_date in past, etc.)
    - **500 Internal Server Error**: Database or server error
    
    Only provided fields will be updated. The updated_at timestamp is automatically updated.
    """
    try:
        # Validate task_id is positive
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task ID must be a positive integer"
            )
        
        # Validate that at least one field is being updated
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update"
            )
        
        # Validate title if provided
        if "title" in update_data:
            if not update_data["title"] or not update_data["title"].strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Task title cannot be empty"
                )
            if len(update_data["title"].strip()) > 255:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Task title cannot exceed 255 characters"
                )
        
        # Validate description length if provided
        if "description" in update_data and update_data["description"] is not None:
            if len(update_data["description"]) > 2000:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Task description cannot exceed 2000 characters"
                )
        
        # Attempt to update task
        task = await update_task(db, current_user.id, task_id, update_data)
        
        if not task:
            logger.warning(f"Task {task_id} not found for update by user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        logger.info(f"Task {task_id} updated successfully by user {current_user.id}")
        return task
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Database integrity error while updating task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation. Please check your input."
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error while updating task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized - Invalid or missing authentication token"
        },
        404: {
            "model": NotFoundErrorResponse,
            "description": "Task not found or does not belong to the user"
        },
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error - Invalid task_id format"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - Database or server error"
        },
    },
    summary="Delete a task",
    description="Delete a task by ID. Only tasks belonging to the authenticated user can be deleted. This operation cannot be undone.",
    response_description="No content on successful deletion",
)
async def delete_existing_task(
    request: Request,
    task_id: int = Path(..., description="ID of the task to delete", ge=1, le=2147483647),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task for the authenticated user.
    
    **Path Parameters:**
    - **task_id**: The ID of the task to delete (must be >= 1)
    
    **Response:**
    - **204 No Content**: Task successfully deleted
    - **401 Unauthorized**: Invalid or missing authentication token
    - **404 Not Found**: Task not found or does not belong to the user
    - **422 Unprocessable Entity**: Invalid task_id format
    - **500 Internal Server Error**: Database or server error
    
    Permanently deletes the task if it exists and belongs to the authenticated user.
    This operation cannot be undone.
    """
    try:
        # Validate task_id is positive
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task ID must be a positive integer"
            )
        
        # Attempt to delete task
        ok = await delete_task(db, current_user.id, task_id)
        
        if not ok:
            logger.warning(f"Task {task_id} not found for deletion by user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        logger.info(f"Task {task_id} deleted successfully by user {current_user.id}")
        return None
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error while deleting task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )