"""
Task model for the Todo CLI application.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field


class Priority(Enum):
    """Priority levels for tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recurrence(Enum):
    """Recurrence patterns for tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Task:
    """Represents a single todo task with all required attributes."""

    id: str
    title: str
    description: str = ""
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    recurrence: Optional[Recurrence] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if self.priority not in Priority.__members__.values():
            raise ValueError(f"Invalid priority: {self.priority}")

        if self.recurrence and self.recurrence not in Recurrence.__members__.values():
            raise ValueError(f"Invalid recurrence: {self.recurrence}")

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False

    def add_tag(self, tag: str):
        """Add a tag to the task."""
        tag = tag.strip().lower()
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Remove a tag from the task."""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority.value,
            'tags': self.tags,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'recurrence': self.recurrence.value if self.recurrence else None,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Task instance from a dictionary."""
        priority = Priority(data.get('priority', 'medium'))
        recurrence = Recurrence(data.get('recurrence')) if data.get('recurrence') else None
        due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        created_at = datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else datetime.now()

        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            priority=priority,
            tags=data.get('tags', []),
            due_date=due_date,
            recurrence=recurrence,
            created_at=created_at
        )