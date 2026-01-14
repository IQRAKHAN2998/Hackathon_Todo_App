from sqlmodel import Session, select
from typing import List, Optional
from models.task import Task, TaskCreate, TaskUpdate, TaskRead
from models.user import User


class TaskService:
    """Service class for handling task operations."""

    @staticmethod
    def _convert_task_to_read(task: Task) -> TaskRead:
        """Convert a Task model to TaskRead model with proper tag handling."""
        # Handle tags conversion - be extremely defensive about the input type
        tags_list = []
        if task.tags is None:
            tags_list = []
        elif isinstance(task.tags, list):
            # If it's already a list, use it as-is
            tags_list = [str(item) for item in task.tags if item is not None]
        elif isinstance(task.tags, str):
            try:
                import json
                parsed_tags = json.loads(task.tags)
                if isinstance(parsed_tags, list):
                    tags_list = [str(item) for item in parsed_tags if item is not None]
                else:
                    # If JSON parsing returns a single value, wrap it in a list
                    tags_list = [str(parsed_tags)]
            except (json.JSONDecodeError, TypeError):
                # If JSON parsing fails, treat the string as a single tag
                tags_list = [task.tags] if task.tags else []
        else:
            # Handle cases where tags might be any other type (int, etc.)
            # Convert to string and wrap in a list
            tags_list = [str(task.tags)] if task.tags is not None else []

        # Create TaskRead object with properly converted tags
        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            tags=tags_list,  # This is now a proper list
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=task.user_id
        )

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str) -> List[TaskRead]:
        """Get all tasks for a specific user."""
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        # Convert each task to TaskRead format with proper tags handling
        return [TaskService._convert_task_to_read(task) for task in tasks]

    @staticmethod
    def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[TaskRead]:
        """Get a specific task by ID for a specific user."""
        task = session.get(Task, task_id)
        if task and task.user_id == user_id:
            return TaskService._convert_task_to_read(task)
        return None

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> TaskRead:
        """Create a new task for a user."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            tags=task_data.tags,
            due_date=task_data.due_date,
            completed=task_data.completed,
            user_id=user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return the task in TaskRead format with proper tags handling
        return TaskService._convert_task_to_read(task)

    @staticmethod
    def update_task(session: Session, task_id: str, task_data: TaskUpdate, user_id: str) -> Optional[TaskRead]:
        """Update an existing task for a user."""
        task = session.get(Task, task_id)
        if task and task.user_id == user_id:
            # Update the task with provided values (only non-None values)
            for key, value in task_data.dict(exclude_unset=True).items():
                setattr(task, key, value)
            task.updated_at = task.updated_at  # This will trigger the default_factory to update the timestamp
            session.add(task)
            session.commit()
            session.refresh(task)

            # Return the task in TaskRead format with proper tags handling
            return TaskService._convert_task_to_read(task)
        return None

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """Delete a task for a user."""
        task = session.get(Task, task_id)
        if task and task.user_id == user_id:
            session.delete(task)
            session.commit()
            return True
        return False

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, user_id: str, completed: bool) -> Optional[TaskRead]:
        """Toggle the completion status of a task."""
        task = session.get(Task, task_id)
        if task and task.user_id == user_id:
            task.completed = completed
            task.updated_at = task.updated_at  # This will trigger the default_factory to update the timestamp
            session.add(task)
            session.commit()
            session.refresh(task)

            # Return the task in TaskRead format with proper tags handling
            return TaskService._convert_task_to_read(task)
        return None