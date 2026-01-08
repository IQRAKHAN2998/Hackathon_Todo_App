#!/usr/bin/env python3
"""
Test script to verify the Todo CLI functionality.
"""
import subprocess
import sys
import tempfile
import os


def test_basic_functionality():
    """Test basic functionality of the Todo CLI."""
    print("Testing basic functionality...")

    # Test adding a task
    result = subprocess.run([
        sys.executable, "-m", "src.cli.main", "add", "Test Task",
        "--description", "This is a test task"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Add task: SUCCESS")
        task_id = None
        # Extract task ID from output
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
                print("✓ List tasks: SUCCESS")
            else:
                print("✗ List tasks: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

            # Test updating a task
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "update", task_id,
                "--title", "Updated Test Task"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("✓ Update task: SUCCESS")
            else:
                print("✗ Update task: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

            # Test completing a task
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "complete", task_id
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("✓ Complete task: SUCCESS")
            else:
                print("✗ Complete task: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

            # Test deleting a task
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "delete", task_id
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("✓ Delete task: SUCCESS")
            else:
                print("✗ Delete task: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")
        else:
            print("✗ Add task: FAILED - Could not extract task ID")
            print(f"  Output: {result.stdout}")
    else:
        print("✗ Add task: FAILED")
        print(f"  Output: {result.stdout}")
        print(f"  Error: {result.stderr}")

    print()


def test_advanced_functionality():
    """Test advanced functionality of the Todo CLI."""
    print("Testing advanced functionality...")

    # Test adding a task with priority and tags
    result = subprocess.run([
        sys.executable, "-m", "src.cli.main", "add", "Advanced Test Task",
        "--priority", "high",
        "--tags", "work", "important",
        "--due-date", "2026-12-31"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Add task with advanced features: SUCCESS")
        task_id = None
        # Extract task ID from output
        for line in result.stdout.split('\n'):
            if 'ID:' in line:
                task_id = line.split('ID:')[1].strip()
                break

        if task_id:
            # Test search functionality
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "search", "Advanced"
            ], capture_output=True, text=True)

            if result.returncode == 0 and task_id[:8] in result.stdout:
                print("✓ Search functionality: SUCCESS")
            else:
                print("✗ Search functionality: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

            # Test filtering by priority
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "list", "--priority", "high"
            ], capture_output=True, text=True)

            if result.returncode == 0 and task_id[:8] in result.stdout:
                print("✓ Filter by priority: SUCCESS")
            else:
                print("✗ Filter by priority: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

            # Test sorting
            result = subprocess.run([
                sys.executable, "-m", "src.cli.main", "list", "--sort", "priority"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("✓ Sort functionality: SUCCESS")
            else:
                print("✗ Sort functionality: FAILED")
                print(f"  Output: {result.stdout}")
                print(f"  Error: {result.stderr}")

            # Clean up
            subprocess.run([
                sys.executable, "-m", "src.cli.main", "delete", task_id
            ], capture_output=True, text=True)
    else:
        print("✗ Add task with advanced features: FAILED")
        print(f"  Output: {result.stdout}")
        print(f"  Error: {result.stderr}")

    print()


if __name__ == "__main__":
    print("Running Todo CLI functionality tests...\n")

    test_basic_functionality()
    test_advanced_functionality()

    print("Testing completed!")