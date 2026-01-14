from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from passlib.context import CryptContext
from .base import TimestampMixin
import uuid


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    """User model for authentication with email and password."""
    id: str = Field(default_factory=generate_uuid, primary_key=True, nullable=False)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password: str = Field(nullable=False)  # Hashed password
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using bcrypt"""
        # Bcrypt has a 72 character limit, so truncate if necessary
        if len(password) > 72:
            password = password[:72]
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify the provided password against the stored hash"""
        return pwd_context.verify(plain_password, self.password)


class UserCreate(SQLModel):
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: str
    email: str
    created_at: datetime
    updated_at: datetime


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None