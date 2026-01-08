# Todo App Backend

This is the backend for the Todo application built with FastAPI and SQLModel.

## Features

- Full CRUD operations for tasks
- Multi-user support via user_id
- Task completion toggling
- RESTful API endpoints
- Proper data isolation between users

## Tech Stack

- FastAPI - Web framework
- SQLModel - ORM for database operations
- Pydantic - Data validation
- PostgreSQL - Database
- uvicorn - ASGI server

## API Endpoints

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your PostgreSQL database and update the DATABASE_URL in `.env`

3. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (required)

## Frontend Integration

This backend is designed to work with the existing Next.js frontend. The API endpoints follow the pattern expected by the frontend integration.