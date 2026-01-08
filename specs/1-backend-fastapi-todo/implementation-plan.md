# Step-by-Step Implementation Plan: Backend API for Todo App with FastAPI and SQLModel

## Overview
This document provides a detailed step-by-step implementation plan for creating the backend API using FastAPI and SQLModel. All code will be contained within the `backend/` folder as required.

## Step 1: Project Setup
1. Create the backend directory structure:
   ```
   backend/
   ├── app.py
   ├── models.py
   ├── database.py
   ├── schemas.py
   ├── routes/
   │   └── tasks.py
   └── .env
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi sqlmodel pydantic python-dotenv uvicorn psycopg2-binary
   ```

3. Create the `.env` file with database configuration:
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/todo_db
   ```

## Step 2: Database Setup (database.py)
1. Create the database engine and session generator:
   ```python
   from sqlmodel import create_engine
   from sqlalchemy import create_engine as _create_engine
   import os
   from dotenv import load_dotenv

   load_dotenv()

   DATABASE_URL = os.getenv("DATABASE_URL")

   connect_args = {"check_same_thread": False}
   engine = create_engine(DATABASE_URL, echo=True)

   def get_session():
       with Session(engine) as session:
           yield session
   ```

## Step 3: Define Models (models.py)
1. Create the User model:
   ```python
   from sqlmodel import SQLModel, Field
   from typing import Optional
   from datetime import datetime

   class User(SQLModel, table=True):
       id: str = Field(default=None, primary_key=True)
       created_at: datetime = Field(default_factory=datetime.utcnow)
       updated_at: datetime = Field(default_factory=datetime.utcnow)
   ```

2. Create the Task model:
   ```python
   from sqlmodel import SQLModel, Field, Relationship
   from typing import Optional, List
   from datetime import datetime
   import uuid

   class Task(SQLModel, table=True):
       id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
       title: str = Field(max_length=255)
       description: Optional[str] = Field(default=None, max_length=1000)
       completed: bool = Field(default=False)
       priority: str = Field(default="medium", regex="^(low|medium|high)$")
       tags: Optional[List[str]] = Field(default=None)
       due_date: Optional[datetime] = None
       created_at: datetime = Field(default_factory=datetime.utcnow)
       updated_at: datetime = Field(default_factory=datetime.utcnow)
       user_id: str = Field(foreign_key="user.id")
   ```

## Step 4: Define Pydantic Schemas (schemas.py)
1. Create TaskCreate schema for task creation:
   ```python
   from pydantic import BaseModel
   from typing import Optional, List
   from datetime import datetime

   class TaskCreate(BaseModel):
       title: str
       description: Optional[str] = None
       priority: str = "medium"
       tags: Optional[List[str]] = []
       due_date: Optional[datetime] = None
       completed: bool = False
   ```

2. Create TaskUpdate schema for task updates:
   ```python
   class TaskUpdate(BaseModel):
       title: Optional[str] = None
       description: Optional[str] = None
       completed: Optional[bool] = None
       priority: Optional[str] = None
       tags: Optional[List[str]] = None
       due_date: Optional[datetime] = None
   ```

3. Create TaskResponse schema for API responses:
   ```python
   class TaskResponse(BaseModel):
       id: str
       title: str
       description: Optional[str]
       completed: bool
       priority: str
       tags: Optional[List[str]]
       due_date: Optional[datetime] = None
       created_at: datetime
       updated_at: datetime
       user_id: str
   ```

## Step 5: Implement API Endpoints (routes/tasks.py)
1. Create the tasks router:
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from sqlmodel import Session, select
   from typing import List
   from backend.database import get_session
   from backend.models import Task, User
   from backend.schemas import TaskCreate, TaskUpdate, TaskResponse

   router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])

   # GET /api/{user_id}/tasks - Get all tasks for a user
   @router.get("/tasks", response_model=List[TaskResponse])
   def get_tasks(user_id: str, session: Session = Depends(get_session)):
       # Query tasks for the specific user
       tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
       return tasks

   # POST /api/{user_id}/tasks - Create a new task for a user
   @router.post("/tasks", response_model=TaskResponse)
   def create_task(user_id: str, task: TaskCreate, session: Session = Depends(get_session)):
       # Create a new task with the provided user_id
       db_task = Task(user_id=user_id, **task.dict())
       session.add(db_task)
       session.commit()
       session.refresh(db_task)
       return db_task

   # GET /api/{user_id}/tasks/{id} - Get a specific task
   @router.get("/tasks/{id}", response_model=TaskResponse)
   def get_task(user_id: str, id: str, session: Session = Depends(get_session)):
       # Query for the specific task belonging to the user
       task = session.get(Task, id)
       if not task or task.user_id != user_id:
           raise HTTPException(status_code=404, detail="Task not found")
       return task

   # PUT /api/{user_id}/tasks/{id} - Update a task
   @router.put("/tasks/{id}", response_model=TaskResponse)
   def update_task(user_id: str, id: str, task_update: TaskUpdate, session: Session = Depends(get_session)):
       # Get the existing task
       db_task = session.get(Task, id)
       if not db_task or db_task.user_id != user_id:
           raise HTTPException(status_code=404, detail="Task not found")

       # Update the task with provided values
       for key, value in task_update.dict(exclude_unset=True).items():
           setattr(db_task, key, value)

       session.add(db_task)
       session.commit()
       session.refresh(db_task)
       return db_task

   # DELETE /api/{user_id}/tasks/{id} - Delete a task
   @router.delete("/tasks/{id}")
   def delete_task(user_id: str, id: str, session: Session = Depends(get_session)):
       # Get the task to delete
       task = session.get(Task, id)
       if not task or task.user_id != user_id:
           raise HTTPException(status_code=404, detail="Task not found")

       session.delete(task)
       session.commit()
       return {"success": True, "message": "Task deleted successfully"}

   # PATCH /api/{user_id}/tasks/{id}/complete - Toggle task completion
   @router.patch("/tasks/{id}/complete", response_model=TaskResponse)
   def toggle_task_completion(user_id: str, id: str, completed: bool, session: Session = Depends(get_session)):
       # Get the task to update
       task = session.get(Task, id)
       if not task or task.user_id != user_id:
           raise HTTPException(status_code=404, detail="Task not found")

       # Update the completion status
       task.completed = completed
       session.add(task)
       session.commit()
       session.refresh(task)
       return task
   ```

## Step 6: Create Main Application (app.py)
1. Create the main FastAPI application:
   ```python
   from fastapi import FastAPI
   from backend.routes.tasks import router as tasks_router
   from backend.database import engine
   from backend.models import Task, User

   # Create tables in the database
   from sqlmodel import SQLModel
   SQLModel.metadata.create_all(engine)

   app = FastAPI(
       title="Todo App API",
       description="Backend API for Todo App with FastAPI and SQLModel",
       version="1.0.0"
   )

   # Include the tasks router
   app.include_router(tasks_router)

   @app.get("/")
   def read_root():
       return {"message": "Todo App Backend API"}

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

## Step 7: Test Each Endpoint
1. Start the development server:
   ```bash
   cd backend
   uvicorn app:app --reload --port 8000
   ```

2. Test the GET endpoint for user tasks:
   ```bash
   curl -X GET "http://localhost:8000/api/user123/tasks"
   ```

3. Test the POST endpoint to create a task:
   ```bash
   curl -X POST "http://localhost:8000/api/user123/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample task", "description": "Sample description"}'
   ```

4. Test the GET endpoint for a specific task:
   ```bash
   curl -X GET "http://localhost:8000/api/user123/tasks/{task_id}"
   ```

5. Test the PUT endpoint to update a task:
   ```bash
   curl -X PUT "http://localhost:8000/api/user123/tasks/{task_id}" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated task title", "completed": true}'
   ```

6. Test the DELETE endpoint to delete a task:
   ```bash
   curl -X DELETE "http://localhost:8000/api/user123/tasks/{task_id}"
   ```

7. Test the PATCH endpoint to toggle task completion:
   ```bash
   curl -X PATCH "http://localhost:8000/api/user123/tasks/{task_id}/complete" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
   ```

## Step 8: Frontend Integration Example
1. The frontend can interact with the API using fetch requests:
   ```javascript
   // Example: Get all tasks for a user
   async function getUserTasks(userId) {
     const response = await fetch(`/api/${userId}/tasks`);
     const data = await response.json();
     return data;
   }

   // Example: Create a new task
   async function createTask(userId, taskData) {
     const response = await fetch(`/api/${userId}/tasks`, {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify(taskData),
     });
     const data = await response.json();
     return data;
   }
   ```

## Step 9: Validation and Error Handling
1. Add validation to ensure user_id is properly linked to tasks
2. Implement proper error responses with appropriate HTTP status codes
3. Add input validation using Pydantic schemas
4. Implement database transaction handling for data consistency

## Step 10: Final Testing
1. Verify all endpoints work correctly
2. Confirm multi-user data isolation works (user A can't access user B's tasks)
3. Test edge cases and error conditions
4. Validate API responses match the defined schemas
5. Confirm the database properly stores and retrieves data