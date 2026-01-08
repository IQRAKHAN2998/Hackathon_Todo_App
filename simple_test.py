#!/usr/bin/env python3
"""
Simple test script to verify the Todo CLI functionality.
"""
import subprocess
import sys


def test_basic_commands():
    """Test basic commands of the Todo CLI."""
    print("Testing basic commands...")

    # Test help command
    result = subprocess.run([sys.executable, "-m", "src.cli.main", "--help"],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("+ Help command: SUCCESS")
    else:
        print("- Help command: FAILED")
        print(f"  Error: {result.stderr}")

    # Test adding a task
    result = subprocess.run([
        sys.executable, "-m", "src.cli.main", "add", "Test Task",
        "--description", "This is a test task"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("+ Add task: SUCCESS")
        # Extract task ID from output
        task_id = None
        for line in result.stdout.split('\n'):
            if 'ID:' in line:
                task_id = line.split('ID:')[1].strip()
                break

        if task_id:
            print(f"  - Task ID: {task_id}")

            # Test listing tasks
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "list"
            ], capture_output=True, text=True)

            if result.returncode == 0 and task_id[:8] in result.stdout:
                print("+ List tasks: SUCCESS")
            else:
                print("- List tasks: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

        # Clean up by deleting the test task if we got an ID
        if task_id:
            subprocess.run([
                sys.executable, "-m", "src.cli.main", "delete", task_id
            ], capture_output=True, text=True)
    else:
        print("- Add task: FAILED")
        print(f"  Output: {result.stdout}")
        print(f"  Error: {result.stderr}")

    print()


if __name__ == "__main__":
    print("Running simple Todo CLI functionality tests...\n")

    test_basic_commands()

    print("Testing completed!")