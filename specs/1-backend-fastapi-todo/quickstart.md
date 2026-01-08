# Quickstart: Backend API for Todo App with FastAPI and SQLModel

## Prerequisites

- Python 3.9+
- PostgreSQL database (or Neon Serverless PostgreSQL account)
- pip package manager

## Setup Instructions

1. **Create backend directory**:
   ```bash
   mkdir backend
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi sqlmodel pydantic python-dotenv uvicorn psycopg2-binary
   ```

3. **Create environment file**:
   ```bash
   # Create .env file with your database URL
   echo "DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/todo_db" > .env
   ```

4. **Create the project structure**:
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

## Running the Application

1. **Start the development server**:
   ```bash
   cd backend
   uvicorn app:app --reload --port 8000
   ```

2. **API Documentation**: Visit `http://localhost:8000/docs` for interactive API documentation

## Testing the API

1. **Create a task**:
   ```bash
   curl -X POST "http://localhost:8000/api/user123/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample task", "description": "Sample description"}'
   ```

2. **Get all tasks for a user**:
   ```bash
   curl "http://localhost:8000/api/user123/tasks"
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (required)