from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as tasks_router
from auth_routes import router as auth_router
from database import engine
from models import Task, User

# Import SQLModel and create all tables in the database
from sqlmodel import SQLModel

# Create all tables in the database
SQLModel.metadata.create_all(engine)

# Ensure default user exists
from models import User
from sqlmodel import Session, select

def ensure_default_user():
    with Session(engine) as session:
        default_user_id = "default-user-123"
        existing_user = session.get(User, default_user_id)
        if not existing_user:
            default_user = User(
                id=default_user_id,
                email="default@example.com",
                password=User.hash_password("temp")
            )
            session.add(default_user)
            session.commit()

# Create the default user when the app starts
ensure_default_user()

# Create the main FastAPI application instance
app = FastAPI(
    title="Todo App API",
    description="Backend API for Todo App with FastAPI and SQLModel",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3000/"],  # Allow requests from Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the auth router with authentication endpoints
app.include_router(auth_router)

# Include the tasks router with all task-related endpoints
app.include_router(tasks_router)

@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    Returns a simple welcome message.
    """
    return {"message": "Todo App Backend API - Ready to manage your tasks!"}

# If running this file directly, start the Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)