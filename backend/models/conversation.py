from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from .base import TimestampMixin


class Conversation(SQLModel, table=True):
    """Conversation model to track chat sessions."""
    id: str = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)  # Link to the user who owns the conversation
    title: str = Field(max_length=255, nullable=False)  # Brief title for the conversation
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Creation timestamp
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Update timestamp
    is_active: bool = Field(default=True)  # Whether this conversation is currently active


class ConversationCreate(SQLModel):
    title: str
    user_id: str


class ConversationUpdate(SQLModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class ConversationRead(SQLModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool