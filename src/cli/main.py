"""
Main CLI interface for the Todo CLI application.
"""
import argparse
import sys
from datetime import datetime
from typing import List, Optional

from src.services.storage_service import StorageService
from src.services.task_service import TaskService
from src.models.task import Task, Priority, Recurrence


class TodoCLI:
    """Command-line interface for the Todo application."""

    def __init__(self):
        """Initialize the CLI with services."""
        self.storage_service = StorageService()
        self.task_service = TaskService(self.storage_service)

    def run(self):
        """Run the main CLI loop."""
        parser = argparse.ArgumentParser(
            description="Todo CLI Application - Manage your tasks in memory",
            prog="todo"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add task command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Task title")
        add_parser.add_argument("--description", "-d", help="Task description")
        add_parser.add_argument("--priority", "-p", choices=["low", "medium", "high"],
                               default="medium", help="Task priority")
        add_parser.add_argument("--tags", "-t", nargs="*", help="Task tags")
        add_parser.add_argument("--due-date", help="Due date in YYYY-MM-DD format")
        add_parser.add_argument("--recurrence", choices=["daily", "weekly"],
                               help="Recurrence pattern")

        # List tasks command
        list_parser = subparsers.add_parser("list", help="List all tasks")
        list_parser.add_argument("--completed", choices=["true", "false"],
                                help="Filter by completion status")
        list_parser.add_argument("--priority", choices=["low", "medium", "high"],
                                help="Filter by priority")
        list_parser.add_argument("--tag", help="Filter by tag")
        list_parser.add_argument("--sort", choices=["title", "priority", "due_date", "completed"],
                                default="created_at", help="Sort by field")
        list_parser.add_argument("--reverse", action="store_true",
                                help="Reverse sort order")

        # Update task command
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", help="Task ID to update")
        update_parser.add_argument("--title", help="New task title")
        update_parser.add_argument("--description", "-d", help="New task description")
        update_parser.add_argument("--completed", choices=["true", "false"],
                                  help="Set completion status")
        update_parser.add_argument("--priority", choices=["low", "medium", "high"],
                                  help="New priority")
        update_parser.add_argument("--tags", "-t", nargs="*", help="New tags")
        update_parser.add_argument("--due-date", help="New due date in YYYY-MM-DD format")
        update_parser.add_argument("--recurrence", choices=["daily", "weekly"],
                                  help="New recurrence pattern")

        # Delete task command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", help="Task ID to delete")

        # Complete task command
        complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
        complete_parser.add_argument("id", help="Task ID to mark complete")

        # Incomplete task command
        incomplete_parser = subparsers.add_parser("incomplete", help="Mark task as incomplete")
        incomplete_parser.add_argument("id", help="Task ID to mark incomplete")

        # Search tasks command
        search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
        search_parser.add_argument("keyword", help="Keyword to search for")

        # Reminders command
        reminder_parser = subparsers.add_parser("reminders", help="Show upcoming reminders")
        reminder_parser.add_argument("--days", type=int, default=1,
                                   help="Number of days to check for reminders")

        # Process recurring tasks command
        recurring_parser = subparsers.add_parser("process-recurring",
                                                help="Process recurring tasks")

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            sys.exit(1)

        try:
            if args.command == "add":
                self.handle_add(args)
            elif args.command == "list":
                self.handle_list(args)
            elif args.command == "update":
                self.handle_update(args)
            elif args.command == "delete":
                self.handle_delete(args)
            elif args.command == "complete":
                self.handle_complete(args)
            elif args.command == "incomplete":
                self.handle_incomplete(args)
            elif args.command == "search":
                self.handle_search(args)
            elif args.command == "reminders":
                self.handle_reminders(args)
            elif args.command == "process-recurring":
                self.handle_process_recurring(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string in YYYY-MM-DD format."""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")

    def handle_add(self, args):
        """Handle the add command."""
        priority = Priority(args.priority)
        tags = args.tags or []
        due_date = self.parse_date(args.due_date) if args.due_date else None
        recurrence = Recurrence(args.recurrence) if args.recurrence else None

        task = self.task_service.create_task(
            title=args.title,
            description=args.description or "",
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )

        if task:
            # Get the numeric ID for the newly created task
            all_tasks = self.task_service.get_all_tasks()
            sorted_tasks = sorted(all_tasks, key=lambda t: t.created_at)
            numeric_id = None
            for i, t in enumerate(sorted_tasks, start=1):
                if t.id == task.id:
                    numeric_id = i
                    break
            if numeric_id:
                print(f"Task added successfully with ID: {numeric_id}")
            else:
                print(f"Task added successfully with ID: {task.id}")
            self.print_task(task)
        else:
            print("Failed to add task. ID may already exist.", file=sys.stderr)
            sys.exit(1)

    def handle_list(self, args):
        """Handle the list command."""
        # Apply filters
        completed_filter = None
        if args.completed == "true":
            completed_filter = True
        elif args.completed == "false":
            completed_filter = False

        priority_filter = Priority(args.priority) if args.priority else None
        tag_filter = args.tag

        tasks = self.task_service.get_all_tasks()

        # Apply filters if specified
        if completed_filter is not None:
            tasks = [t for t in tasks if t.completed == completed_filter]
        if priority_filter:
            tasks = [t for t in tasks if t.priority == priority_filter]
        if tag_filter:
            tasks = [t for t in tasks if tag_filter.lower() in [tag.lower() for tag in t.tags]]

        # Sort tasks
        reverse = args.reverse
        tasks = self.task_service.sort_tasks(args.sort, reverse)

        if not tasks:
            print("No tasks found.")
        else:
            print(f"Found {len(tasks)} task(s):")
            # Display tasks with proper sequential numeric IDs based on the current view
            sorted_tasks = sorted(tasks, key=lambda t: t.created_at)
            for i, task in enumerate(sorted_tasks, start=1):
                # Temporarily set the numeric ID for display purposes
                status = "X" if task.completed else "O"
                priority_symbol = {
                    Priority.HIGH: "!",
                    Priority.MEDIUM: "~",
                    Priority.LOW: "."
                }[task.priority]

                print(f"[{status}] {priority_symbol} [{i}] {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                if task.tags:
                    print(f"    Tags: {', '.join(task.tags)}")
                if task.due_date:
                    print(f"    Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
                if task.recurrence:
                    print(f"    Recurrence: {task.recurrence.value}")
                print()

    def handle_update(self, args):
        """Handle the update command."""
        # Convert string values to appropriate types
        title = args.title
        description = args.description
        completed = None
        if args.completed == "true":
            completed = True
        elif args.completed == "false":
            completed = False
        priority = Priority(args.priority) if args.priority else None
        tags = args.tags
        due_date = self.parse_date(args.due_date) if args.due_date else None
        recurrence = Recurrence(args.recurrence) if args.recurrence else None

        success = self.task_service.update_task(
            task_id=args.id,
            title=title,
            description=description,
            completed=completed,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )

        if success:
            # Get the numeric ID for the task to display in the message
            updated_task = self.task_service.get_task(args.id)
            if updated_task:
                all_tasks = self.task_service.get_all_tasks()
                sorted_tasks = sorted(all_tasks, key=lambda t: t.created_at)
                numeric_id = None
                for i, t in enumerate(sorted_tasks, start=1):
                    if t.id == updated_task.id:
                        numeric_id = i
                        break
                if numeric_id:
                    print(f"Task {numeric_id} updated successfully")
                else:
                    print(f"Task {args.id} updated successfully")
                self.print_task(updated_task)
            else:
                print(f"Task updated successfully")
        else:
            print(f"Failed to update task {args.id}. Task may not exist.", file=sys.stderr)
            sys.exit(1)

    def handle_delete(self, args):
        """Handle the delete command."""
        # Get the numeric ID before deletion to display in the message
        task_to_delete = self.task_service.get_task(args.id)
        if task_to_delete:
            all_tasks = self.task_service.get_all_tasks()
            sorted_tasks = sorted(all_tasks, key=lambda t: t.created_at)
            numeric_id = None
            for i, t in enumerate(sorted_tasks, start=1):
                if t.id == task_to_delete.id:
                    numeric_id = i
                    break

        success = self.task_service.delete_task(args.id)

        if success:
            if numeric_id:
                print(f"Task {numeric_id} deleted successfully")
            else:
                print(f"Task {args.id} deleted successfully")
        else:
            print(f"Failed to delete task {args.id}. Task may not exist.", file=sys.stderr)
            sys.exit(1)

    def handle_complete(self, args):
        """Handle the complete command."""
        success = self.task_service.mark_task_complete(args.id)

        if success:
            # Get the numeric ID for the task to display in the message
            task = self.task_service.get_task(args.id)
            if task:
                all_tasks = self.task_service.get_all_tasks()
                sorted_tasks = sorted(all_tasks, key=lambda t: t.created_at)
                numeric_id = None
                for i, t in enumerate(sorted_tasks, start=1):
                    if t.id == task.id:
                        numeric_id = i
                        break
                if numeric_id:
                    print(f"Task {numeric_id} marked as complete")
                else:
                    print(f"Task {args.id} marked as complete")
                self.print_task(task)
            else:
                print(f"Task marked as complete")
        else:
            print(f"Failed to mark task {args.id} as complete. Task may not exist.", file=sys.stderr)
            sys.exit(1)

    def handle_incomplete(self, args):
        """Handle the incomplete command."""
        success = self.task_service.mark_task_incomplete(args.id)

        if success:
            # Get the numeric ID for the task to display in the message
            task = self.task_service.get_task(args.id)
            if task:
                all_tasks = self.task_service.get_all_tasks()
                sorted_tasks = sorted(all_tasks, key=lambda t: t.created_at)
                numeric_id = None
                for i, t in enumerate(sorted_tasks, start=1):
                    if t.id == task.id:
                        numeric_id = i
                        break
                if numeric_id:
                    print(f"Task {numeric_id} marked as incomplete")
                else:
                    print(f"Task {args.id} marked as incomplete")
                self.print_task(task)
            else:
                print(f"Task marked as incomplete")
        else:
            print(f"Failed to mark task {args.id} as incomplete. Task may not exist.", file=sys.stderr)
            sys.exit(1)

    def handle_search(self, args):
        """Handle the search command."""
        tasks = self.task_service.search_tasks(args.keyword)

        if not tasks:
            print(f"No tasks found containing '{args.keyword}'")
        else:
            print(f"Found {len(tasks)} task(s) containing '{args.keyword}':")
            # For search results, show with sequential IDs based on the search results
            for i, task in enumerate(tasks, start=1):
                # Temporarily override the print_task method to show search result index
                status = "X" if task.completed else "O"
                priority_symbol = {
                    Priority.HIGH: "!",
                    Priority.MEDIUM: "~",
                    Priority.LOW: "."
                }[task.priority]

                print(f"[{status}] {priority_symbol} [{i}] {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                if task.tags:
                    print(f"    Tags: {', '.join(task.tags)}")
                if task.due_date:
                    print(f"    Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
                if task.recurrence:
                    print(f"    Recurrence: {task.recurrence.value}")
                print()

    def handle_reminders(self, args):
        """Handle the reminders command."""
        tasks = self.task_service.get_upcoming_reminders(args.days)

        if not tasks:
            print(f"No upcoming reminders in the next {args.days} day(s)")
        else:
            print(f"Upcoming reminders in the next {args.days} day(s):")
            # For reminders, show with sequential IDs based on the reminder results
            for i, task in enumerate(tasks, start=1):
                status = "X" if task.completed else "O"
                priority_symbol = {
                    Priority.HIGH: "!",
                    Priority.MEDIUM: "~",
                    Priority.LOW: "."
                }[task.priority]

                print(f"[{status}] {priority_symbol} [{i}] {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                if task.tags:
                    print(f"    Tags: {', '.join(task.tags)}")
                if task.due_date:
                    print(f"    Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
                if task.recurrence:
                    print(f"    Recurrence: {task.recurrence.value}")
                print()

    def handle_process_recurring(self, args):
        """Handle the process-recurring command."""
        new_tasks = self.task_service.process_recurring_tasks()

        if not new_tasks:
            print("No recurring tasks processed")
        else:
            print(f"Created {len(new_tasks)} new task(s) from recurring tasks:")
            # For recurring tasks, show with sequential IDs based on the results
            for i, task in enumerate(new_tasks, start=1):
                status = "X" if task.completed else "O"
                priority_symbol = {
                    Priority.HIGH: "!",
                    Priority.MEDIUM: "~",
                    Priority.LOW: "."
                }[task.priority]

                print(f"[{status}] {priority_symbol} [{i}] {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                if task.tags:
                    print(f"    Tags: {', '.join(task.tags)}")
                if task.due_date:
                    print(f"    Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
                if task.recurrence:
                    print(f"    Recurrence: {task.recurrence.value}")
                print()

    def print_task(self, task: Task):
        """Print a task in a formatted way."""
        status = "X" if task.completed else "O"
        priority_symbol = {
            Priority.HIGH: "!",
            Priority.MEDIUM: "~",
            Priority.LOW: "."
        }[task.priority]

        # Get the numeric ID for the task (this will be the position when all tasks are sorted by creation date)
        all_tasks = self.task_service.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda t: t.created_at)
        numeric_id = None
        for i, t in enumerate(sorted_tasks, start=1):
            if t.id == task.id:
                numeric_id = i
                break

        if numeric_id:
            print(f"[{status}] {priority_symbol} [{numeric_id}] {task.title}")
        else:
            print(f"[{status}] {priority_symbol} [{task.id[:8]}...] {task.title}")

        if task.description:
            print(f"    Description: {task.description}")
        if task.tags:
            print(f"    Tags: {', '.join(task.tags)}")
        if task.due_date:
            print(f"    Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        if task.recurrence:
            print(f"    Recurrence: {task.recurrence.value}")
        print()


def main():
    """Main entry point."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()