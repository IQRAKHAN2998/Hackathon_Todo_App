from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

from typing import Union

class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    Used for validation when receiving task creation requests.
    """
    title: str
    description: Optional[str] = None
    priority: str = "medium"  # Default to medium priority
    tags: Optional[Union[list, str]] = []  # Can be a list or JSON string
    due_date: Optional[datetime] = None
    completed: bool = False  # Default to not completed


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[Union[list, str]] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    """
    Schema for task responses returned by the API.
    Used for validation when sending task data to clients.
    """
    id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: Optional[list]  # Always return as list to frontend
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user_id: str


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status.
    Used when receiving requests to update task completion status.
    """
    completed: bool