from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from .base import TimestampMixin
import uuid


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


class Task(SQLModel, table=True):
    """Task model representing a user's to-do item."""
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    title: str = Field(max_length=255, nullable=False)  # Title is required
    description: Optional[str] = Field(default=None, max_length=1000)  # Optional description
    completed: bool = Field(default=False)  # Whether the task is completed
    priority: str = Field(default="medium", regex="^(low|medium|high)$")  # Priority level
    tags: Optional[str] = Field(default=None)  # Optional tags for the task (stored as JSON string)
    due_date: Optional[datetime] = None  # Optional due date
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Creation timestamp
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Update timestamp
    user_id: str = Field(foreign_key="user.id", nullable=False)  # Link to the user who owns the task


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None


from typing import List
import json


class TaskRead(SQLModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: Optional[List[str]]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user_id: str