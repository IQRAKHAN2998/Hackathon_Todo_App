"""
Task service for the Todo CLI application.
"""
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from src.models.task import Task, Priority, Recurrence
from src.services.storage_service import StorageService


class TaskService:
    """Business logic service for task operations."""

    def __init__(self, storage_service: StorageService):
        """Initialize the task service."""
        self.storage = storage_service
        self._next_numeric_id = 1

    def _get_numeric_id_mapping(self) -> Dict[int, str]:
        """Get a mapping of numeric IDs to UUIDs for all tasks."""
        tasks = self.storage.get_all_tasks()
        # Sort tasks by creation date to maintain consistent numeric IDs
        sorted_tasks = sorted(tasks, key=lambda t: t.created_at)
        return {i + 1: task.id for i, task in enumerate(sorted_tasks)}

    def _get_uuid_from_numeric_id(self, numeric_id: int) -> Optional[str]:
        """Convert a numeric ID to a UUID."""
        mapping = self._get_numeric_id_mapping()
        return mapping.get(numeric_id)

    def _get_numeric_id_from_uuid(self, uuid: str) -> Optional[int]:
        """Convert a UUID to a numeric ID."""
        mapping = self._get_numeric_id_mapping()
        for num_id, uuid_val in mapping.items():
            if uuid_val == uuid:
                return num_id
        return None

    def _resolve_task_id(self, task_id: str) -> Optional[str]:
        """Resolve a task ID (numeric or UUID) to the actual UUID."""
        # Check if task_id is a numeric ID
        try:
            numeric_id = int(task_id)
            uuid = self._get_uuid_from_numeric_id(numeric_id)
            return uuid
        except ValueError:
            # Not a numeric ID, treat as UUID
            return task_id if self.storage.task_exists(task_id) else None

    def generate_unique_id(self) -> str:
        """Generate a unique ID for a new task."""
        return str(uuid.uuid4())

    def create_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM,
                   tags: List[str] = None, due_date: datetime = None,
                   recurrence: Recurrence = None) -> Optional[Task]:
        """Create a new task with a unique ID."""
        if tags is None:
            tags = []

        task_id = self.generate_unique_id()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags.copy(),
            due_date=due_date,
            recurrence=recurrence
        )

        if self.storage.add_task(task):
            return task
        return None

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID (supports both UUID and numeric ID)."""
        # Check if task_id is a numeric ID
        try:
            numeric_id = int(task_id)
            uuid = self._get_uuid_from_numeric_id(numeric_id)
            if uuid:
                return self.storage.get_task(uuid)
        except ValueError:
            # Not a numeric ID, treat as UUID
            pass

        # Treat as UUID
        return self.storage.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.storage.get_all_tasks()

    def update_task(self, task_id: str, title: str = None, description: str = None,
                   completed: bool = None, priority: Priority = None,
                   tags: List[str] = None, due_date: datetime = None,
                   recurrence: Recurrence = None) -> bool:
        """Update a task with provided values."""
        # Convert numeric ID to UUID if needed
        actual_task_id = self._resolve_task_id(task_id)
        if not actual_task_id:
            return False

        existing_task = self.storage.get_task(actual_task_id)
        if not existing_task:
            return False

        # Update only provided fields
        if title is not None:
            existing_task.title = title
        if description is not None:
            existing_task.description = description
        if completed is not None:
            existing_task.completed = completed
        if priority is not None:
            existing_task.priority = priority
        if tags is not None:
            existing_task.tags = tags.copy()
        if due_date is not None:
            existing_task.due_date = due_date
        if recurrence is not None:
            existing_task.recurrence = recurrence

        return self.storage.update_task(actual_task_id, existing_task)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID (supports both UUID and numeric ID)."""
        # Convert numeric ID to UUID if needed
        actual_task_id = self._resolve_task_id(task_id)
        if not actual_task_id:
            return False

        return self.storage.delete_task(actual_task_id)

    def mark_task_complete(self, task_id: str) -> bool:
        """Mark a task as complete (supports both UUID and numeric ID)."""
        # Convert numeric ID to UUID if needed
        actual_task_id = self._resolve_task_id(task_id)
        if not actual_task_id:
            return False

        task = self.storage.get_task(actual_task_id)
        if not task:
            return False
        task.mark_complete()
        return self.storage.update_task(actual_task_id, task)

    def mark_task_incomplete(self, task_id: str) -> bool:
        """Mark a task as incomplete (supports both UUID and numeric ID)."""
        # Convert numeric ID to UUID if needed
        actual_task_id = self._resolve_task_id(task_id)
        if not actual_task_id:
            return False

        task = self.storage.get_task(actual_task_id)
        if not task:
            return False
        task.mark_incomplete()
        return self.storage.update_task(actual_task_id, task)

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description."""
        all_tasks = self.storage.get_all_tasks()
        keyword_lower = keyword.lower()
        return [
            task for task in all_tasks
            if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
        ]

    def filter_tasks(self, completed: Optional[bool] = None,
                    priority: Optional[Priority] = None,
                    tag: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status, priority, or tag."""
        all_tasks = self.storage.get_all_tasks()
        filtered_tasks = []

        for task in all_tasks:
            match = True

            if completed is not None and task.completed != completed:
                match = False
            if priority is not None and task.priority != priority:
                match = False
            if tag is not None and tag.lower() not in [t.lower() for t in task.tags]:
                match = False

            if match:
                filtered_tasks.append(task)

        return filtered_tasks

    def sort_tasks(self, sort_by: str = "created_at", reverse: bool = False) -> List[Task]:
        """Sort tasks by various criteria."""
        all_tasks = self.storage.get_all_tasks()

        if sort_by == "title":
            return sorted(all_tasks, key=lambda t: t.title.lower(), reverse=reverse)
        elif sort_by == "priority":
            return sorted(all_tasks, key=lambda t: t.priority.value, reverse=reverse)
        elif sort_by == "due_date":
            return sorted(all_tasks, key=lambda t: t.due_date or datetime.max, reverse=reverse)
        elif sort_by == "completed":
            return sorted(all_tasks, key=lambda t: t.completed, reverse=reverse)
        else:  # Default: sort by creation date
            return sorted(all_tasks, key=lambda t: t.created_at, reverse=reverse)

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get all tasks with a specific priority."""
        all_tasks = self.storage.get_all_tasks()
        return [task for task in all_tasks if task.priority == priority]

    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Get all tasks with a specific tag."""
        all_tasks = self.storage.get_all_tasks()
        return [task for task in all_tasks if tag.lower() in [t.lower() for t in task.tags]]

    def process_recurring_tasks(self) -> List[Task]:
        """Process recurring tasks and create new instances if needed."""
        all_tasks = self.storage.get_all_tasks()
        new_tasks = []

        for task in all_tasks:
            if task.recurrence and not task.completed:
                # Check if the task should create a new instance based on recurrence
                now = datetime.now()

                # For simplicity, we'll just check if the due date has passed and the task is recurring
                if task.due_date and task.due_date < now:
                    if task.recurrence == Recurrence.DAILY:
                        # Create a new instance for tomorrow
                        new_task = Task(
                            id=self.generate_unique_id(),
                            title=task.title,
                            description=task.description,
                            priority=task.priority,
                            tags=task.tags.copy(),
                            due_date=datetime(now.year, now.month, now.day + 1) if task.due_date else None,
                            recurrence=task.recurrence
                        )
                        if self.storage.add_task(new_task):
                            new_tasks.append(new_task)
                    elif task.recurrence == Recurrence.WEEKLY:
                        # Create a new instance for next week
                        new_task = Task(
                            id=self.generate_unique_id(),
                            title=task.title,
                            description=task.description,
                            priority=task.priority,
                            tags=task.tags.copy(),
                            due_date=datetime(now.year, now.month, now.day + 7) if task.due_date else None,
                            recurrence=task.recurrence
                        )
                        if self.storage.add_task(new_task):
                            new_tasks.append(new_task)

        return new_tasks

    def get_upcoming_reminders(self, days: int = 1) -> List[Task]:
        """Get tasks with due dates within the specified number of days."""
        all_tasks = self.storage.get_all_tasks()
        now = datetime.now()
        future_date = now.replace(day=now.day + days) if now.day + days <= now.day + 30 else now  # Simple calculation
        return [
            task for task in all_tasks
            if not task.completed and task.due_date and now <= task.due_date <= future_date
        ]