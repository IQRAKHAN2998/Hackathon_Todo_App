export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  chat_metadata?: any; // Optional metadata field
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  intent: string;
  task_result: any; // Task object or null
  success: boolean;
}

export interface SendMessageRequest {
  message: string;
  conversation_id?: string;
}