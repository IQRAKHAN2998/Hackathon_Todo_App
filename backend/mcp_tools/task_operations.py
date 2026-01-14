from typing import List, Optional
from sqlmodel import Session
from services.task_service import TaskService
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from services.ai_processor import ai_processor, IntentType


def add_task(query: str, user_id: str, session: Session) -> Optional[Task]:
    """
    MCP tool to create a task from natural language query.

    Args:
        query: Natural language description of the task to create
        user_id: ID of the user requesting the task creation
        session: Database session for the operation

    Returns:
        Created Task object or None if creation failed
    """
    # Process the natural language query to extract intent and entities
    intent, entities = ai_processor.extract_intent_and_entities(query, user_id)

    if intent != IntentType.CREATE_TASK:
        # If the intent is not to create a task, we'll still try to extract task info
        # This handles cases where user phrasing might be ambiguous
        pass

    # Extract task details from entities
    title = entities.get('title', query.split('.')[0] if '.' in query else query)
    description = entities.get('description', '')
    priority = entities.get('priority', 'medium')
    due_date = entities.get('due_date', None)
    tags = entities.get('tags', None)

    # Create task data object
    task_create_data = TaskCreate(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        tags=tags,
        completed=False
    )

    # Use the task service to create the task
    created_task = TaskService.create_task(session, task_create_data, user_id)
    return created_task


def list_tasks(query: str, user_id: str, session: Session) -> List[Task]:
    """
    MCP tool to list tasks based on natural language query.

    Args:
        query: Natural language query for filtering tasks
        user_id: ID of the user requesting the task list
        session: Database session for the operation

    Returns:
        List of Task objects matching the query
    """
    # Process the natural language query to extract intent and entities
    intent, entities = ai_processor.extract_intent_and_entities(query, user_id)

    # Get all tasks for the user
    tasks = TaskService.get_tasks_by_user(session, user_id)

    # Apply any filters from the entities if needed
    # For now, we'll return all tasks for the user
    # In a more advanced implementation, we could filter based on priority, due date, etc.

    return tasks


def complete_task(query: str, user_id: str, session: Session) -> Optional[Task]:
    """
    MCP tool to mark a task as complete based on natural language query.

    Args:
        query: Natural language description of which task to complete
        user_id: ID of the user requesting the task completion
        session: Database session for the operation

    Returns:
        Updated Task object or None if completion failed
    """
    # Process the natural language query to extract intent and entities
    intent, entities = ai_processor.extract_intent_and_entities(query, user_id)

    # Get all tasks for the user to identify which one to complete
    user_tasks = TaskService.get_tasks_by_user(session, user_id)

    # Find the task to complete based on the query
    # This is a simplified implementation - in reality, you'd want more sophisticated matching
    task_identifier = entities.get('identifier', query.lower())

    for task in user_tasks:
        if (task_identifier in task.title.lower() or
            task_identifier in (task.description or '').lower() or
            task_identifier.isdigit() and str(len(user_tasks) - user_tasks.index(task)) == task_identifier):
            # Toggle the task completion status
            completed_task = TaskService.toggle_task_completion(session, task.id, user_id, True)
            return completed_task

    # If no specific task matched, complete the most recent incomplete task
    for task in reversed(user_tasks):
        if not task.completed:
            completed_task = TaskService.toggle_task_completion(session, task.id, user_id, True)
            return completed_task

    return None


def delete_task(query: str, user_id: str, session: Session) -> bool:
    """
    MCP tool to delete a task based on natural language query.

    Args:
        query: Natural language description of which task to delete
        user_id: ID of the user requesting the task deletion
        session: Database session for the operation

    Returns:
        True if deletion was successful, False otherwise
    """
    # Process the natural language query to extract intent and entities
    intent, entities = ai_processor.extract_intent_and_entities(query, user_id)

    # Get all tasks for the user to identify which one to delete
    user_tasks = TaskService.get_tasks_by_user(session, user_id)

    # Find the task to delete based on the query
    task_identifier = entities.get('identifier', query.lower())

    for task in user_tasks:
        if (task_identifier in task.title.lower() or
            task_identifier in (task.description or '').lower() or
            task_identifier.isdigit() and str(len(user_tasks) - user_tasks.index(task)) == task_identifier):
            # Delete the task
            success = TaskService.delete_task(session, task.id, user_id)
            return success

    # If no specific task matched, return False
    return False


def update_task(query: str, user_id: str, session: Session) -> Optional[Task]:
    """
    MCP tool to update a task based on natural language query.

    Args:
        query: Natural language description of which task to update and how
        user_id: ID of the user requesting the task update
        session: Database session for the operation

    Returns:
        Updated Task object or None if update failed
    """
    # Process the natural language query to extract intent and entities
    intent, entities = ai_processor.extract_intent_and_entities(query, user_id)

    # Get all tasks for the user to identify which one to update
    user_tasks = TaskService.get_tasks_by_user(session, user_id)

    # Find the task to update based on the query
    task_identifier = entities.get('identifier', query.lower())

    for task in user_tasks:
        if (task_identifier in task.title.lower() or
            task_identifier in (task.description or '').lower() or
            task_identifier.isdigit() and str(len(user_tasks) - user_tasks.index(task)) == task_identifier):

            # Prepare update data based on entities
            update_data = {}

            if 'title' in entities:
                update_data['title'] = entities['title']
            if 'description' in entities:
                update_data['description'] = entities['description']
            if 'priority' in entities:
                update_data['priority'] = entities['priority']
            if 'due_date' in entities:
                update_data['due_date'] = entities['due_date']
            if 'completed' in entities:
                update_data['completed'] = entities['completed']

            # Create TaskUpdate object
            task_update = TaskUpdate(**{k: v for k, v in update_data.items() if v is not None})

            # Update the task
            updated_task = TaskService.update_task(session, task.id, task_update, user_id)
            return updated_task

    return None