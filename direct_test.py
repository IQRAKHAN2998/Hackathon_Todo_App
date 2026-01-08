#!/usr/bin/env python3
"""
Direct test of the Todo services to verify functionality.
"""
from src.services.storage_service import StorageService
from src.services.task_service import TaskService
from src.models.task import Task, Priority, Recurrence
from datetime import datetime


def test_all_functionality():
    """Test all functionality directly through services."""
    print("Testing all functionality through services...")

    # Initialize services
    storage_service = StorageService()
    task_service = TaskService(storage_service)

    # Test 1: Create a task (Basic Feature)
    print("\n1. Testing Basic Features:")
    task = task_service.create_task(
        title="Test Task",
        description="This is a test task",
        priority=Priority.HIGH
    )

    if task:
        print(f"   + Task created with ID: {task.id}")
        print(f"   + Title: {task.title}")
        print(f"   + Description: {task.description}")
        print(f"   + Priority: {task.priority.value}")
    else:
        print("   - Task creation failed")
        return False

    # Test 2: Get all tasks
    all_tasks = task_service.get_all_tasks()
    if len(all_tasks) == 1:
        print(f"   + Retrieved {len(all_tasks)} task(s)")
    else:
        print(f"   - Expected 1 task, got {len(all_tasks)}")
        return False

    # Test 3: Update task
    success = task_service.update_task(
        task_id=task.id,
        title="Updated Test Task",
        completed=True
    )

    if success:
        updated_task = task_service.get_task(task.id)
        print(f"   + Task updated: {updated_task.title}")
        print(f"   + Completed status: {updated_task.completed}")
    else:
        print("   - Task update failed")
        return False

    # Test 4: Mark task complete/incomplete
    success = task_service.mark_task_incomplete(task.id)
    if success:
        task_check = task_service.get_task(task.id)
        print(f"   + Task marked incomplete: {not task_check.completed}")
    else:
        print("   - Mark task incomplete failed")
        return False

    # Test 5: Intermediate Features - Search
    print("\n2. Testing Intermediate Features:")
    search_results = task_service.search_tasks("Updated")
    if len(search_results) == 1:
        print(f"   + Search found {len(search_results)} task(s)")
    else:
        print(f"   - Search failed, found {len(search_results)} task(s)")
        return False

    # Test 6: Filter tasks
    filtered = task_service.filter_tasks(priority=Priority.HIGH)
    if len(filtered) == 1:
        print(f"   + Filter by priority found {len(filtered)} task(s)")
    else:
        print(f"   - Filter failed, found {len(filtered)} task(s)")
        return False

    # Test 7: Sort tasks
    sorted_tasks = task_service.sort_tasks("title")
    if len(sorted_tasks) == 1:
        print(f"   + Sort returned {len(sorted_tasks)} task(s)")
    else:
        print(f"   - Sort failed")
        return False

    # Test 8: Advanced Features - Recurring tasks
    print("\n3. Testing Advanced Features:")
    recurring_task = task_service.create_task(
        title="Recurring Task",
        description="This is a recurring task",
        recurrence=Recurrence.DAILY,
        due_date=datetime.now()
    )

    if recurring_task:
        print(f"   + Recurring task created with ID: {recurring_task.id}")
        print(f"   + Recurrence: {recurring_task.recurrence.value}")
    else:
        print("   - Recurring task creation failed")
        return False

    # Test 9: Process recurring tasks
    new_tasks = task_service.process_recurring_tasks()
    print(f"   + Processed recurring tasks, created {len(new_tasks)} new task(s)")

    # Test 10: Reminders
    reminders = task_service.get_upcoming_reminders(days=1)
    print(f"   + Found {len(reminders)} upcoming reminder(s)")

    # Test 11: Delete task
    print("\n4. Testing Delete Feature:")
    success = task_service.delete_task(task.id)
    if success:
        print("   + Task deleted successfully")
        remaining_tasks = task_service.get_all_tasks()
        print(f"   + Remaining tasks: {len(remaining_tasks)}")
    else:
        print("   - Task deletion failed")
        return False

    print("\n+ All functionality tests PASSED!")
    return True


if __name__ == "__main__":
    print("Running direct service functionality tests...")

    success = test_all_functionality()

    if success:
        print("\n+ All tests passed! Phase 1 implementation is working correctly.")
    else:
        print("\n- Some tests failed.")