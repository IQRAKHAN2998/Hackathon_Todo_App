from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
import json

from database import get_session
from models.user import User
from models.conversation import Conversation, ConversationCreate, ConversationRead
from models.chat_message import ChatMessage, ChatMessageCreate, ChatMessageRead, MessageRole
from routes.auth import get_current_user

import uuid

# Fixed UUID for the dummy user to ensure consistency across requests
# Must match the one in tasks.py for consistency
DUMMY_USER_ID = "11111111-1111-1111-1111-111111111111"

# Simple function to return the dummy user directly
def get_current_user_bypass():
    """Bypass authentication for development - returns the dummy user"""
    # Create a dummy user with the consistent UUID
    dummy_user = User()
    dummy_user.id = DUMMY_USER_ID
    dummy_user.email = "dev@example.com"
    dummy_user.password = "dummy_hash"
    return dummy_user
from services.ai_processor import ai_processor, IntentType
from services.conversation_service import ConversationService
from mcp_tools.task_operations import add_task, list_tasks, complete_task, delete_task, update_task

# Create a router for chat-related endpoints
router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=dict)
def process_chat_message(
    message_data: dict,
    current_user: User = Depends(get_current_user_bypass),
    session: Session = Depends(get_session)
):
    """
    Process a chat message from the user and return an AI-generated response.

    The message_data should contain:
    - 'message': The user's message text
    - 'conversation_id': Optional conversation ID (will create new if not provided)
    """
    user_message = message_data.get("message", "")
    conversation_id = message_data.get("conversation_id")

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    # If no conversation ID provided, create a new one
    if not conversation_id:
        conv_title = user_message[:50] + "..." if len(user_message) > 50 else user_message
        conversation_data = ConversationCreate(user_id=current_user.id, title=conv_title)
        conversation = ConversationService.create_conversation(session, conversation_data)
        conversation_id = conversation.id
    else:
        # Verify user has access to this conversation
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, current_user.id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found or access denied")

    # Add user message to conversation
    user_msg_data = ChatMessageCreate(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=user_message
    )
    ConversationService.add_message_to_conversation(session, user_msg_data, current_user.id)

    # Process the message with AI to determine intent
    intent, entities = ai_processor.extract_intent_and_entities(user_message, current_user.id)

    # Process based on intent using MCP tools
    ai_response = ""
    task_result = None

    if intent == IntentType.CREATE_TASK:
        created_task = add_task(user_message, current_user.id, session)
        if created_task:
            ai_response = f"I've created a task for you: '{created_task.title}'"
            task_result = created_task
        else:
            ai_response = "Sorry, I couldn't create that task. Could you please rephrase?"

    elif intent == IntentType.LIST_TASKS:
        user_tasks = list_tasks(user_message, current_user.id, session)
        if user_tasks:
            task_titles = [task.title for task in user_tasks]
            ai_response = f"Here are your tasks: {', '.join(task_titles)}"
        else:
            ai_response = "You don't have any tasks right now."

    elif intent == IntentType.COMPLETE_TASK:
        completed_task = complete_task(user_message, current_user.id, session)
        if completed_task:
            ai_response = f"I've marked '{completed_task.title}' as complete!"
        else:
            ai_response = "Sorry, I couldn't find or complete that task. Could you be more specific?"

    elif intent == IntentType.DELETE_TASK:
        success = delete_task(user_message, current_user.id, session)
        if success:
            ai_response = "I've deleted that task for you."
        else:
            ai_response = "Sorry, I couldn't find that task to delete. Could you be more specific?"

    elif intent == IntentType.UPDATE_TASK:
        updated_task = update_task(user_message, current_user.id, session)
        if updated_task:
            ai_response = f"I've updated your task: '{updated_task.title}'"
        else:
            ai_response = "Sorry, I couldn't find or update that task. Could you be more specific?"

    else:
        # For general chat or unrecognized intents
        ai_response = ai_processor.generate_response(intent, entities)

    # Add AI response to conversation
    ai_msg_data = ChatMessageCreate(
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
        content=ai_response
    )
    ConversationService.add_message_to_conversation(session, ai_msg_data, current_user.id)

    return {
        "conversation_id": conversation_id,
        "response": ai_response,
        "intent": intent.value,
        "task_result": task_result.dict() if task_result else None,
        "success": True
    }


@router.get("/chat/conversations", response_model=List[ConversationRead])
def get_user_conversations(
    current_user: User = Depends(get_current_user_bypass),
    session: Session = Depends(get_session)
):
    """Get all conversations for the authenticated user."""
    conversations = ConversationService.get_conversations_by_user(session, current_user.id)
    return conversations


@router.get("/chat/conversations/{conversation_id}/messages", response_model=List[ChatMessageRead])
def get_conversation_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user_bypass),
    session: Session = Depends(get_session)
):
    """Get all messages for a specific conversation."""
    messages = ConversationService.get_messages_for_conversation(session, conversation_id, current_user.id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")
    return messages


@router.delete("/chat/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user_bypass),
    session: Session = Depends(get_session)
):
    """Delete a conversation and all its messages."""
    # In a real implementation, you'd want to delete the messages as well
    # For now, we'll just deactivate the conversation
    success = ConversationService.deactivate_conversation(session, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")
    return {"success": True, "message": "Conversation deactivated successfully"}