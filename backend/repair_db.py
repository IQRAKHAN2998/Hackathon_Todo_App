#!/usr/bin/env python3
"""
Script to repair database issues with the tags column in the Task table.
"""

from sqlmodel import SQLModel, Session, create_engine, select
from models import Task
import json
import sqlite3

def repair_database():
    """Repair database by fixing invalid tags values."""

    # Connect to the database
    DATABASE_URL = "sqlite:///./todo_app_local.db"
    engine = create_engine(DATABASE_URL)

    # Check if there are any invalid tags values
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

        print(f"Found {len(tasks)} tasks in the database")

        for task in tasks:
            print(f"Task ID: {task.id}, Tags: {task.tags} (type: {type(task.tags)})")

            # Fix invalid tags values
            if task.tags is not None and not isinstance(task.tags, str):
                print(f"  Fixing tags for task {task.id}: {task.tags} -> '{task.tags}'")
                task.tags = str(task.tags)

        # Commit the changes
        session.commit()
        print("Database repair completed!")

if __name__ == "__main__":
    repair_database()