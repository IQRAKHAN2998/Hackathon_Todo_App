"""
In-memory storage service for the Todo CLI application.
"""
from typing import Dict, List, Optional
from src.models.task import Task
import threading


class StorageService:
    """Manages in-memory storage of tasks with thread-safe operations."""

    def __init__(self):
        """Initialize the in-memory storage."""
        self._tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()

    def add_task(self, task: Task) -> bool:
        """Add a task to storage. Returns True if successful, False if ID already exists."""
        with self._lock:
            if task.id in self._tasks:
                return False
            self._tasks[task.id] = task
            return True

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        with self._lock:
            return self._tasks.get(task_id)

    def update_task(self, task_id: str, updated_task: Task) -> bool:
        """Update a task. Returns True if successful, False if task doesn't exist."""
        with self._lock:
            if task_id not in self._tasks:
                return False
            self._tasks[task_id] = updated_task
            return True

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID. Returns True if successful, False if task doesn't exist."""
        with self._lock:
            if task_id not in self._tasks:
                return False
            del self._tasks[task_id]
            return True

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        with self._lock:
            return list(self._tasks.values())

    def clear_all(self):
        """Clear all tasks from storage."""
        with self._lock:
            self._tasks.clear()

    def task_exists(self, task_id: str) -> bool:
        """Check if a task exists by ID."""
        with self._lock:
            return task_id in self._tasks