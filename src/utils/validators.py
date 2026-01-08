"""
Validation utilities for the Todo CLI application.
"""
from datetime import datetime
from typing import Optional


def validate_task_title(title: str) -> bool:
    """Validate that a task title is not empty."""
    return bool(title and title.strip())


def validate_task_description(description: str) -> bool:
    """Validate that a task description is valid."""
    return description is not None


def validate_date_format(date_str: str) -> Optional[datetime]:
    """Validate and parse date string in YYYY-MM-DD format."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")


def validate_priority(priority: str) -> bool:
    """Validate that a priority value is valid."""
    return priority in ["low", "medium", "high"]


def validate_recurrence(recurrence: str) -> bool:
    """Validate that a recurrence value is valid."""
    return recurrence in ["daily", "weekly", None]