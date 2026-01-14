from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import User, Task, Conversation, ChatMessage
from sqlmodel import SQLModel, Session, select
from routes import auth, tasks, chat
from config.settings import settings
import uuid


# Create all tables in the database
SQLModel.metadata.create_all(engine)

# Initialize dummy user for auth bypass (Better Auth disabled)
try:
    DUMMY_USER_ID = "11111111-1111-1111-1111-111111111111"
    with Session(engine) as session:
        # Check if dummy user already exists
        existing_user = session.exec(select(User).where(User.id == DUMMY_USER_ID)).first()
        if not existing_user:
            # Create dummy user with hashed password
            dummy_user = User(
                id=DUMMY_USER_ID,
                email="dev@example.com",
                password=User.hash_password("dummy_password")
            )
            session.add(dummy_user)
            session.commit()
            print("Dummy user created successfully")
        else:
            print("Dummy user already exists")
except Exception as e:
    print(f"Error initializing dummy user: {e}")


# Create the main FastAPI application instance
app = FastAPI(
    title="Todo AI Chatbot API",
    description="Backend API for Todo AI Chatbot with FastAPI and SQLModel",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router with authentication endpoints
# DISABLED: Better Auth temporarily turned OFF - commented out to disable auth functionality
# app.include_router(auth.router, prefix="/api", tags=["auth"])

# Include the tasks router with all task-related endpoints
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

# Include the chat router with all chat-related endpoints
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    Returns a simple welcome message.
    """
    return {"message": "Todo AI Chatbot Backend API - Ready to manage your tasks with AI!"}


# If running this file directly, start the Uvicorn server
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))  # Allow PORT environment variable to override
    uvicorn.run(app, host="0.0.0.0", port=port)