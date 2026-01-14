from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timezone
import json

from database import get_session
from models.task import Task, TaskCreate, TaskUpdate, TaskRead
from models.user import User
from routes.auth import get_current_user

import uuid

# Fixed UUID for the dummy user to ensure consistency across requests
DUMMY_USER_ID = "11111111-1111-1111-1111-111111111111"

# Simple function to return the dummy user directly
def get_current_user_bypass():
    """Bypass authentication for development - returns the dummy user"""
    # Create a dummy user with the consistent UUID
    dummy_user = User()
    dummy_user.id = DUMMY_USER_ID
    dummy_user.email = "dev@example.com"
    dummy_user.password = "dummy_hash"
    return dummy_user

from services.task_service import TaskService

# Create a router for task-related endpoints
router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(current_user: User = Depends(get_current_user_bypass), session: Session = Depends(get_session)):
    """Get all tasks for the authenticated user."""
    # Query tasks for the authenticated user
    tasks = TaskService.get_tasks_by_user(session, current_user.id)
    return tasks


@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user_bypass), session: Session = Depends(get_session)):
    """Create a new task for the authenticated user."""
    # Create the task using the task service
    db_task = TaskService.create_task(session, task, current_user.id)
    return db_task


@router.get("/tasks/{id}", response_model=TaskRead)
def get_task(id: str, current_user: User = Depends(get_current_user_bypass), session: Session = Depends(get_session)):
    """Get a specific task by ID for the authenticated user."""
    # Get the task using the task service
    db_task = TaskService.get_task_by_id(session, id, current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/tasks/{id}", response_model=TaskRead)
def update_task(id: str, task_update: TaskUpdate, current_user: User = Depends(get_current_user_bypass), session: Session = Depends(get_session)):
    """Update a specific task for the authenticated user."""
    # Update the task using the task service
    db_task = TaskService.update_task(session, id, task_update, current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/tasks/{id}")
def delete_task(id: str, current_user: User = Depends(get_current_user_bypass), session: Session = Depends(get_session)):
    """Delete a specific task for the authenticated user."""
    # Delete the task using the task service
    success = TaskService.delete_task(session, id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "message": "Task deleted successfully"}


@router.patch("/tasks/{id}/complete", response_model=TaskRead)
def toggle_task_completion(
    id: str,
    completion_data: dict,  # Accepting a dict with completed status
    current_user: User = Depends(get_current_user_bypass),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a specific task for the authenticated user."""
    completed = completion_data.get("completed", True)

    # Toggle the task completion using the task service
    db_task = TaskService.toggle_task_completion(session, id, current_user.id, completed)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task