from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import json
from database import get_session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskToggleComplete

# Create a router for task-related endpoints
router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(session: Session = Depends(get_session)):
    """
    Get all tasks for a default user (for testing without auth).

    Args:
        session: Database session for querying

    Returns:
        List of tasks belonging to the default user
    """
    # Use a default user_id for testing without auth
    default_user_id = "default-user-123"

    # Query tasks for the default user
    tasks = session.exec(select(Task).where(Task.user_id == default_user_id)).all()

    # Convert tasks to response format with tags as lists
    response_tasks = []
    for task in tasks:
        tags_as_list = []
        if task.tags is not None:
            try:
                tags_as_list = json.loads(task.tags)
            except (json.JSONDecodeError, TypeError):
                tags_as_list = []  # Default to empty list if JSON is invalid

        # Create response object with tags as list
        response_task = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'priority': task.priority,
            'tags': tags_as_list,
            'due_date': task.due_date,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
            'user_id': task.user_id
        }
        response_tasks.append(response_task)

    return response_tasks

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """
    Create a new task for a default user (for testing without auth).

    Args:
        task: Task creation data
        session: Database session for creating

    Returns:
        The created task with its ID and timestamps
    """
    # Use a default user_id for testing without auth
    default_user_id = "default-user-123"

    # Convert tags from list to JSON string for database storage
    task_dict = task.dict()
    if task_dict.get('tags') is not None:
        if isinstance(task_dict['tags'], list):
            task_dict['tags'] = json.dumps(task_dict['tags'])
        # If it's already a string (JSON), keep it as is

    # Create a new task instance with the provided data and default user_id
    db_task = Task(user_id=default_user_id, **task_dict)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Convert tags from JSON string back to list for API response
    tags_as_list = []
    if db_task.tags is not None:
        try:
            tags_as_list = json.loads(db_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_as_list = []  # Default to empty list if JSON is invalid

    # Create response object with tags as list
    response_data = {
        'id': db_task.id,
        'title': db_task.title,
        'description': db_task.description,
        'completed': db_task.completed,
        'priority': db_task.priority,
        'tags': tags_as_list,
        'due_date': db_task.due_date,
        'created_at': db_task.created_at,
        'updated_at': db_task.updated_at,
        'user_id': db_task.user_id
    }

    return response_data

@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task(id: str, session: Session = Depends(get_session)):
    """
    Get a specific task by ID for the default user (for testing without auth).

    Args:
        id: The ID of the task to retrieve
        session: Database session for querying

    Returns:
        The requested task
    """
    # Use a default user_id for testing without auth
    default_user_id = "default-user-123"

    # Query for the specific task belonging to the default user
    db_task = session.get(Task, id)

    # Check if the task exists and belongs to the default user
    if not db_task or db_task.user_id != default_user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Convert tags from JSON string back to list for API response
    tags_as_list = []
    if db_task.tags is not None:
        try:
            tags_as_list = json.loads(db_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_as_list = []  # Default to empty list if JSON is invalid

    # Create response object with tags as list
    response_data = {
        'id': db_task.id,
        'title': db_task.title,
        'description': db_task.description,
        'completed': db_task.completed,
        'priority': db_task.priority,
        'tags': tags_as_list,
        'due_date': db_task.due_date,
        'created_at': db_task.created_at,
        'updated_at': db_task.updated_at,
        'user_id': db_task.user_id
    }

    return response_data

@router.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: str, task_update: TaskUpdate, session: Session = Depends(get_session)):
    """
    Update a specific task for the default user (for testing without auth).

    Args:
        id: The ID of the task to update
        task_update: Task update data
        session: Database session for updating

    Returns:
        The updated task
    """
    # Use a default user_id for testing without auth
    default_user_id = "default-user-123"

    # Get the existing task
    db_task = session.get(Task, id)

    # Check if the task exists and belongs to the default user
    if not db_task or db_task.user_id != default_user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the task with provided values (only non-None values)
    for key, value in task_update.dict(exclude_unset=True).items():
        if key == 'tags' and value is not None:
            # Convert tags from list to JSON string for database storage
            if isinstance(value, list):
                setattr(db_task, key, json.dumps(value))
            else:
                setattr(db_task, key, value)  # If it's already a string, use as is
        else:
            setattr(db_task, key, value)

    # Update the timestamp
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Convert tags from JSON string back to list for API response
    tags_as_list = []
    if db_task.tags is not None:
        try:
            tags_as_list = json.loads(db_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_as_list = []  # Default to empty list if JSON is invalid

    # Create response object with tags as list
    response_data = {
        'id': db_task.id,
        'title': db_task.title,
        'description': db_task.description,
        'completed': db_task.completed,
        'priority': db_task.priority,
        'tags': tags_as_list,
        'due_date': db_task.due_date,
        'created_at': db_task.created_at,
        'updated_at': db_task.updated_at,
        'user_id': db_task.user_id
    }

    return response_data

@router.delete("/tasks/{id}")
def delete_task(id: str, session: Session = Depends(get_session)):
    """
    Delete a specific task for the default user (for testing without auth).

    Args:
        id: The ID of the task to delete
        session: Database session for deleting

    Returns:
        Success message
    """
    # Use a default user_id for testing without auth
    default_user_id = "default-user-123"

    # Get the task to delete
    task = session.get(Task, id)

    # Check if the task exists and belongs to the default user
    if not task or task.user_id != default_user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"success": True, "message": "Task deleted successfully"}

@router.patch("/tasks/{id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    id: str,
    completion_data: TaskToggleComplete,
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the default user (for testing without auth).

    Args:
        id: The ID of the task to update
        completion_data: Contains the new completion status
        session: Database session for updating

    Returns:
        The updated task with new completion status
    """
    # Use a default user_id for testing without auth
    default_user_id = "default-user-123"

    # Get the task to update
    db_task = session.get(Task, id)

    # Check if the task exists and belongs to the default user
    if not db_task or db_task.user_id != default_user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the completion status
    db_task.completed = completion_data.completed
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Convert tags from JSON string back to list for API response
    tags_as_list = []
    if db_task.tags is not None:
        try:
            tags_as_list = json.loads(db_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_as_list = []  # Default to empty list if JSON is invalid

    # Create response object with tags as list
    response_data = {
        'id': db_task.id,
        'title': db_task.title,
        'description': db_task.description,
        'completed': db_task.completed,
        'priority': db_task.priority,
        'tags': tags_as_list,
        'due_date': db_task.due_date,
        'created_at': db_task.created_at,
        'updated_at': db_task.updated_at,
        'user_id': db_task.user_id
    }

    return response_data