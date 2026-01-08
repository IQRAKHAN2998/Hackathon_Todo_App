"""
Interactive menu-driven CLI for the Todo application.
"""
import sys
from datetime import datetime
from src.services.storage_service import StorageService
from src.services.task_service import TaskService
from src.models.task import Priority, Recurrence


class TodoMenuCLI:
    """Interactive menu-driven CLI for the Todo application."""

    def __init__(self):
        """Initialize the menu CLI with services."""
        self.storage_service = StorageService()
        self.task_service = TaskService(self.storage_service)

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("           TODO APPLICATION - MAIN MENU")
        print("="*50)
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete")
        print("6. Mark Incomplete")
        print("7. Search Tasks")
        print("8. Process Recurring Tasks")
        print("9. Exit")
        print("="*50)

    def get_user_input(self, prompt: str) -> str:
        """Get input from user with a prompt."""
        return input(prompt).strip()

    def print_task(self, task):
        """Print a task in a formatted way."""
        status = "X" if task.completed else "O"
        priority_symbol = {
            Priority.HIGH: "!",
            Priority.MEDIUM: "~",
            Priority.LOW: "."
        }[task.priority]

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

    def handle_add_task(self):
        """Handle adding a new task."""
        print("\n--- ADD TASK ---")

        title = self.get_user_input("Enter task title: ")
        if not title:
            print("Task title cannot be empty!")
            return

        description = self.get_user_input("Enter task description (optional): ")

        # Get priority
        print("Select priority:")
        print("1. High")
        print("2. Medium (default)")
        print("3. Low")
        priority_choice = self.get_user_input("Enter choice (1-3, default 2): ")

        if priority_choice == "1":
            priority = Priority.HIGH
        elif priority_choice == "3":
            priority = Priority.LOW
        else:
            priority = Priority.MEDIUM

        # Get tags
        tags_input = self.get_user_input("Enter tags separated by commas (optional): ")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

        # Get due date
        due_date_input = self.get_user_input("Enter due date (YYYY-MM-DD, optional): ")
        due_date = None
        if due_date_input:
            try:
                due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Using no due date.")
                due_date = None

        # Get recurrence
        print("Select recurrence:")
        print("1. Daily")
        print("2. Weekly")
        print("3. None (default)")
        recurrence_choice = self.get_user_input("Enter choice (1-3, default 3): ")

        recurrence = None
        if recurrence_choice == "1":
            recurrence = Recurrence.DAILY
        elif recurrence_choice == "2":
            recurrence = Recurrence.WEEKLY

        # Create task
        task = self.task_service.create_task(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )

        if task:
            print(f"\nTask added successfully with ID: {task.id}")
            self.print_task(task)
        else:
            print("\nFailed to add task. ID may already exist.")

    def handle_list_tasks(self):
        """Handle listing all tasks."""
        print("\n--- LIST TASKS ---")

        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"Found {len(tasks)} task(s):\n")
        for task in tasks:
            self.print_task(task)

    def handle_update_task(self):
        """Handle updating a task."""
        print("\n--- UPDATE TASK ---")

        task_id = self.get_user_input("Enter task ID to update: ")
        if not task_id:
            print("Task ID cannot be empty!")
            return

        # Check if task exists
        existing_task = self.task_service.get_task(task_id)
        if not existing_task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Current task: {existing_task.title}")
        print("Leave blank to keep current value.\n")

        # Get new values (empty string means keep current)
        new_title = self.get_user_input(f"Enter new title (current: {existing_task.title}): ")
        if not new_title:
            new_title = None

        new_description = self.get_user_input(f"Enter new description (current: {existing_task.description}): ")
        if not new_description:
            new_description = None

        # Get new priority
        print(f"Current priority: {existing_task.priority.value}")
        print("Select new priority (leave blank to keep current):")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        priority_choice = self.get_user_input("Enter choice (1-3, blank to keep current): ")

        new_priority = None
        if priority_choice == "1":
            new_priority = Priority.HIGH
        elif priority_choice == "2":
            new_priority = Priority.MEDIUM
        elif priority_choice == "3":
            new_priority = Priority.LOW

        # Get new tags
        current_tags = ", ".join(existing_task.tags) if existing_task.tags else "None"
        tags_input = self.get_user_input(f"Enter new tags (current: {current_tags}): ")
        new_tags = None
        if tags_input:
            new_tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        elif tags_input == "":  # Empty string means clear tags
            new_tags = []

        # Get new due date
        current_due_date = existing_task.due_date.strftime('%Y-%m-%d') if existing_task.due_date else "None"
        due_date_input = self.get_user_input(f"Enter new due date (YYYY-MM-DD, current: {current_due_date}): ")
        new_due_date = None
        if due_date_input:
            try:
                new_due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format.")
                return
        elif due_date_input == "":  # Empty string means clear due date
            new_due_date = None

        # Get new recurrence
        current_recurrence = existing_task.recurrence.value if existing_task.recurrence else "None"
        print(f"Current recurrence: {current_recurrence}")
        print("Select new recurrence (leave blank to keep current):")
        print("1. Daily")
        print("2. Weekly")
        print("3. None")
        recurrence_choice = self.get_user_input("Enter choice (1-3, blank to keep current): ")

        new_recurrence = None
        if recurrence_choice == "1":
            new_recurrence = Recurrence.DAILY
        elif recurrence_choice == "2":
            new_recurrence = Recurrence.WEEKLY
        elif recurrence_choice == "3":
            new_recurrence = None

        # Update task
        success = self.task_service.update_task(
            task_id=task_id,
            title=new_title,
            description=new_description,
            priority=new_priority,
            tags=new_tags,
            due_date=new_due_date,
            recurrence=new_recurrence
        )

        if success:
            print(f"\nTask {task_id} updated successfully")
            updated_task = self.task_service.get_task(task_id)
            if updated_task:
                self.print_task(updated_task)
        else:
            print(f"\nFailed to update task {task_id}.")

    def handle_delete_task(self):
        """Handle deleting a task."""
        print("\n--- DELETE TASK ---")

        task_id = self.get_user_input("Enter task ID to delete: ")
        if not task_id:
            print("Task ID cannot be empty!")
            return

        success = self.task_service.delete_task(task_id)

        if success:
            print(f"\nTask {task_id} deleted successfully")
        else:
            print(f"\nFailed to delete task {task_id}. Task may not exist.")

    def handle_mark_complete(self):
        """Handle marking a task as complete."""
        print("\n--- MARK COMPLETE ---")

        task_id = self.get_user_input("Enter task ID to mark complete: ")
        if not task_id:
            print("Task ID cannot be empty!")
            return

        success = self.task_service.mark_task_complete(task_id)

        if success:
            print(f"\nTask {task_id} marked as complete")
            task = self.task_service.get_task(task_id)
            if task:
                self.print_task(task)
        else:
            print(f"\nFailed to mark task {task_id} as complete. Task may not exist.")

    def handle_mark_incomplete(self):
        """Handle marking a task as incomplete."""
        print("\n--- MARK INCOMPLETE ---")

        task_id = self.get_user_input("Enter task ID to mark incomplete: ")
        if not task_id:
            print("Task ID cannot be empty!")
            return

        success = self.task_service.mark_task_incomplete(task_id)

        if success:
            print(f"\nTask {task_id} marked as incomplete")
            task = self.task_service.get_task(task_id)
            if task:
                self.print_task(task)
        else:
            print(f"\nFailed to mark task {task_id} as incomplete. Task may not exist.")

    def handle_search_tasks(self):
        """Handle searching tasks."""
        print("\n--- SEARCH TASKS ---")

        keyword = self.get_user_input("Enter keyword to search: ")
        if not keyword:
            print("Keyword cannot be empty!")
            return

        tasks = self.task_service.search_tasks(keyword)

        if not tasks:
            print(f"\nNo tasks found containing '{keyword}'")
        else:
            print(f"\nFound {len(tasks)} task(s) containing '{keyword}':\n")
            for task in tasks:
                self.print_task(task)

    def handle_process_recurring_tasks(self):
        """Handle processing recurring tasks."""
        print("\n--- PROCESS RECURRING TASKS ---")

        new_tasks = self.task_service.process_recurring_tasks()

        if not new_tasks:
            print("\nNo recurring tasks processed")
        else:
            print(f"\nCreated {len(new_tasks)} new task(s) from recurring tasks:")
            for task in new_tasks:
                self.print_task(task)

    def run(self):
        """Run the main menu loop."""
        print("Welcome to the Todo Application!")

        while True:
            self.display_menu()

            try:
                choice = self.get_user_input("Select an option (1-9): ")

                if choice == "1":
                    self.handle_add_task()
                elif choice == "2":
                    self.handle_list_tasks()
                elif choice == "3":
                    self.handle_update_task()
                elif choice == "4":
                    self.handle_delete_task()
                elif choice == "5":
                    self.handle_mark_complete()
                elif choice == "6":
                    self.handle_mark_incomplete()
                elif choice == "7":
                    self.handle_search_tasks()
                elif choice == "8":
                    self.handle_process_recurring_tasks()
                elif choice == "9":
                    print("\nThank you for using the Todo Application!")
                    break
                else:
                    print("\nInvalid option. Please select a number between 1 and 9.")

                # Pause to let user see the result
                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")


def main():
    """Main entry point."""
    cli = TodoMenuCLI()
    cli.run()


if __name__ == "__main__":
    main()