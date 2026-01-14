from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone
from models.conversation import Conversation, ConversationCreate, ConversationUpdate
from models.chat_message import ChatMessage, ChatMessageCreate, MessageRole


class ConversationService:
    """Service class for handling conversation operations."""

    @staticmethod
    def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
        """Get all conversations for a specific user."""
        conversations = session.exec(select(Conversation).where(Conversation.user_id == user_id)).all()
        return conversations

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """Get a specific conversation by ID for a specific user."""
        conversation = session.get(Conversation, conversation_id)
        if conversation and conversation.user_id == user_id:
            return conversation
        return None

    @staticmethod
    def create_conversation(session: Session, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title,
            is_active=True
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def update_conversation(session: Session, conversation_id: str, conversation_data: ConversationUpdate, user_id: str) -> Optional[Conversation]:
        """Update an existing conversation for a user."""
        conversation = session.get(Conversation, conversation_id)
        if conversation and conversation.user_id == user_id:
            # Update the conversation with provided values (only non-None values)
            for key, value in conversation_data.dict(exclude_unset=True).items():
                setattr(conversation, key, value)
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation
        return None

    @staticmethod
    def deactivate_conversation(session: Session, conversation_id: str, user_id: str) -> bool:
        """Deactivate a conversation."""
        conversation = session.get(Conversation, conversation_id)
        if conversation and conversation.user_id == user_id:
            conversation.is_active = False
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)
            session.commit()
            return True
        return False

    @staticmethod
    def get_messages_for_conversation(session: Session, conversation_id: str, user_id: str) -> List[ChatMessage]:
        """Get all messages for a specific conversation."""
        # First verify the user has access to this conversation
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            return []

        # Get all messages for this conversation
        messages = session.exec(
            select(ChatMessage)
            .where(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.created_at)
        ).all()
        return messages

    @staticmethod
    def add_message_to_conversation(session: Session, message_data: ChatMessageCreate, user_id: str) -> Optional[ChatMessage]:
        """Add a message to a conversation after verifying user access."""
        # Verify the user has access to this conversation
        conversation = session.get(Conversation, message_data.conversation_id)
        if not conversation or conversation.user_id != user_id:
            return None

        message = ChatMessage(
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content,
            chat_metadata=message_data.chat_metadata
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message