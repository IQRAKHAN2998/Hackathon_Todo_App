from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from datetime import datetime, timezone
import uuid
from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    """
    User model for authentication with email and password.
    Also serves as the base user for task association.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password: str = Field(nullable=False)  # Hashed password
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @staticmethod
    def hash_password(password: str):
        """Hash the password using bcrypt"""
        # Bcrypt has a 72 character limit, so truncate if necessary
        if len(password) > 72:
            password = password[:72]
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify the provided password against the stored hash"""
        return pwd_context.verify(plain_password, self.password)


class Task(SQLModel, table=True):
    """
    Task model representing a user's to-do item.
    Each task is associated with a specific user via user_id.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(max_length=255, nullable=False)  # Title is required
    description: Optional[str] = Field(default=None, max_length=1000)  # Optional description
    completed: bool = Field(default=False)  # Whether the task is completed
    priority: str = Field(default="medium", regex="^(low|medium|high)$")  # Priority level
    tags: Optional[str] = Field(default=None)  # Optional tags for the task (stored as JSON string)
    due_date: Optional[datetime] = None  # Optional due date
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Creation timestamp
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Update timestamp
    user_id: str = Field(foreign_key="user.id", nullable=False)  # Link to the user who owns the task