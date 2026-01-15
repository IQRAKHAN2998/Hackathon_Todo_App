from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import uuid


class MessageRole(str, Enum):
    """Enum for the role of the message sender."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(SQLModel, table=True):
    """ChatMessage model to store conversation history."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", nullable=False)  # Link to the conversation
    role: MessageRole = Field(nullable=False)  # Who sent this message (user, assistant, system)
    content: str = Field(nullable=False)  # The actual message content
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Creation timestamp
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Update timestamp
    chat_metadata: Optional[str] = Field(default=None)  # Optional metadata (like task IDs, intent, etc.)


class ChatMessageCreate(SQLModel):
    conversation_id: str
    role: MessageRole
    content: str
    chat_metadata: Optional[str] = None


class ChatMessageRead(SQLModel):
    id: str
    conversation_id: str
    role: MessageRole
    content: str
    created_at: datetime
    updated_at: datetime
    chat_metadata: Optional[str]