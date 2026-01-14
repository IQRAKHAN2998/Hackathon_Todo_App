import openai
from typing import Dict, List, Optional, Tuple
from config.settings import settings
from models.task import TaskCreate, TaskUpdate
from enum import Enum


class IntentType(Enum):
    """Enum for different types of intents that the AI can recognize."""
    CREATE_TASK = "create_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"
    GENERAL_CHAT = "general_chat"


class AIProcessor:
    """Service to handle natural language processing and intent recognition."""

    def __init__(self):
        """Initialize the AI processor with OpenAI API key."""
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        else:
            # For development/testing without API key, create a mock processor
            print("Warning: OpenAI API key not set. Using fallback processor.")

    def extract_intent_and_entities(self, user_input: str, user_id: str) -> Tuple[IntentType, Dict]:
        """
        Extract intent and entities from user input using OpenAI.

        Args:
            user_input: The natural language input from the user
            user_id: The ID of the user making the request

        Returns:
            Tuple containing the intent type and extracted entities
        """
        # Check if API key is available
        if not settings.openai_api_key:
            # Use fallback method when API key is not set
            return self._fallback_intent_detection(user_input)

        # Define the system prompt to guide the AI
        system_prompt = f"""
        You are an AI assistant that helps with task management. Your job is to understand user requests related to tasks and classify them.

        Available intents:
        - create_task: When user wants to create a new task
        - list_tasks: When user wants to see their tasks
        - complete_task: When user wants to mark a task as complete
        - delete_task: When user wants to delete a task
        - update_task: When user wants to modify a task
        - general_chat: When user is having a general conversation

        For create_task, extract these entities:
        - title: The task title
        - description: Optional description
        - priority: Optional priority (low, medium, high)
        - due_date: Optional due date
        - tags: Optional tags

        For complete_task, delete_task, update_task, extract:
        - identifier: What identifies the task (number, title, etc.)

        For update_task, also extract any of the create_task entities that need updating.

        Respond in JSON format with "intent" and "entities" keys.
        """

        try:
            response = openai.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            result = response.choices[0].message.content
            parsed_result = eval(result)  # In production, use json.loads

            intent_str = parsed_result.get("intent", "general_chat")
            entities = parsed_result.get("entities", {})

            # Map string to IntentType enum
            intent_map = {
                "create_task": IntentType.CREATE_TASK,
                "list_tasks": IntentType.LIST_TASKS,
                "complete_task": IntentType.COMPLETE_TASK,
                "delete_task": IntentType.DELETE_TASK,
                "update_task": IntentType.UPDATE_TASK,
                "general_chat": IntentType.GENERAL_CHAT
            }

            intent = intent_map.get(intent_str, IntentType.GENERAL_CHAT)

            return intent, entities

        except Exception as e:
            print(f"Error processing AI request: {e}")
            # Fallback to a simple rule-based approach if API fails
            return self._fallback_intent_detection(user_input)

    def _fallback_intent_detection(self, user_input: str) -> Tuple[IntentType, Dict]:
        """
        Fallback method to detect intent when AI service is unavailable.

        Args:
            user_input: The natural language input from the user

        Returns:
            Tuple containing the intent type and empty entities
        """
        user_input_lower = user_input.lower()

        if any(word in user_input_lower for word in ["add", "create", "new", "make"]):
            return IntentType.CREATE_TASK, {"title": user_input}
        elif any(word in user_input_lower for word in ["list", "show", "see", "my"]):
            return IntentType.LIST_TASKS, {}
        elif any(word in user_input_lower for word in ["complete", "done", "finish", "mark"]):
            return IntentType.COMPLETE_TASK, {}
        elif any(word in user_input_lower for word in ["delete", "remove", "cancel"]):
            return IntentType.DELETE_TASK, {}
        elif any(word in user_input_lower for word in ["update", "change", "modify"]):
            return IntentType.UPDATE_TASK, {}
        else:
            return IntentType.GENERAL_CHAT, {}

    def generate_response(self, intent: IntentType, entities: Dict, task_data: Optional[List] = None) -> str:
        """
        Generate a natural language response based on intent and task data.

        Args:
            intent: The recognized intent
            entities: Extracted entities from the user input
            task_data: Optional task data to include in the response

        Returns:
            A natural language response string
        """
        if intent == IntentType.CREATE_TASK:
            return f"I've created a task for you: '{entities.get('title', 'Unknown')}'"
        elif intent == IntentType.LIST_TASKS:
            if task_data:
                task_titles = [task.title for task in task_data]
                return f"Here are your tasks: {', '.join(task_titles)}"
            else:
                return "You don't have any tasks right now."
        elif intent == IntentType.COMPLETE_TASK:
            return "I've marked that task as complete!"
        elif intent == IntentType.DELETE_TASK:
            return "I've deleted that task for you."
        elif intent == IntentType.UPDATE_TASK:
            return "I've updated your task."
        else:
            return "I understand. How else can I help you with your tasks?"


# Global instance of AI processor
try:
    ai_processor = AIProcessor()
except ValueError:
    # Handle the case where API key is not set during initialization
    from .ai_processor import IntentType

    class MockAIProcessor:
        def extract_intent_and_entities(self, user_input: str, user_id: str):
            # Use fallback method when API key is not set
            user_input_lower = user_input.lower()

            if any(word in user_input_lower for word in ['add', 'create', 'new', 'make']):
                return IntentType.CREATE_TASK, {'title': user_input}
            elif any(word in user_input_lower for word in ['list', 'show', 'see', 'my']):
                return IntentType.LIST_TASKS, {}
            elif any(word in user_input_lower for word in ['complete', 'done', 'finish', 'mark']):
                return IntentType.COMPLETE_TASK, {}
            elif any(word in user_input_lower for word in ['delete', 'remove', 'cancel']):
                return IntentType.DELETE_TASK, {}
            elif any(word in user_input_lower for word in ['update', 'change', 'modify']):
                return IntentType.UPDATE_TASK, {}
            else:
                return IntentType.GENERAL_CHAT, {}

        def generate_response(self, intent, entities, task_data=None):
            if intent == IntentType.CREATE_TASK:
                return f"I've created a task for you: '{entities.get('title', 'Unknown')}'"
            elif intent == IntentType.LIST_TASKS:
                if task_data:
                    task_titles = [task.title for task in task_data]
                    return f"Here are your tasks: {', '.join(task_titles)}"
                else:
                    return "You don't have any tasks right now."
            elif intent == IntentType.COMPLETE_TASK:
                return "I've marked that task as complete!"
            elif intent == IntentType.DELETE_TASK:
                return "I've deleted that task for you."
            elif intent == IntentType.UPDATE_TASK:
                return "I've updated your task."
            else:
                return "I understand. How else can I help you with your tasks?"

    ai_processor = MockAIProcessor()