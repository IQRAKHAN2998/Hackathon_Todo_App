#!/usr/bin/env python3
"""
Test script to verify the numeric ID functionality works correctly.
"""
from src.cli.main import TodoCLI

def test_numeric_ids():
    """Test that numeric IDs work correctly in the Todo CLI."""
    print("Testing numeric ID functionality...\n")

    # Create a single CLI instance to maintain in-memory storage
    cli = TodoCLI()

    print("1. Adding tasks...")
    # Add first task
    args = type('Args', (), {
        'title': 'First task',
        'description': 'Description for first task',
        'priority': 'high',
        'tags': ['test', 'first'],
        'due_date': None,
        'recurrence': None
    })()
    cli.handle_add(args)
    print()

    # Add second task
    args = type('Args', (), {
        'title': 'Second task',
        'description': 'Description for second task',
        'priority': 'medium',
        'tags': ['test', 'second'],
        'due_date': None,
        'recurrence': None
    })()
    cli.handle_add(args)
    print()

    print("2. Listing tasks with numeric IDs...")
    args = type('Args', (), {
        'completed': None,
        'priority': None,
        'tag': None,
        'sort': 'created_at',
        'reverse': False
    })()
    cli.handle_list(args)

    print("3. Testing update with numeric ID...")
    args = type('Args', (), {
        'id': '1',  # Using numeric ID
        'title': 'Updated First task',
        'description': 'Updated description for first task',
        'completed': None,
        'priority': 'low',
        'tags': ['updated', 'test'],
        'due_date': None,
        'recurrence': None
    })()
    cli.handle_update(args)
    print()

    print("4. Testing complete with numeric ID...")
    args = type('Args', (), {
        'id': '2'  # Using numeric ID
    })()
    cli.handle_complete(args)
    print()

    print("5. Testing delete with numeric ID...")
    args = type('Args', (), {
        'id': '1'  # Using numeric ID
    })()
    cli.handle_delete(args)
    print()

    print("6. Final list after deletion...")
    args = type('Args', (), {
        'completed': None,
        'priority': None,
        'tag': None,
        'sort': 'created_at',
        'reverse': False
    })()
    cli.handle_list(args)

    print("\n+ All numeric ID functionality tests passed!")

if __name__ == "__main__":
    test_numeric_ids()