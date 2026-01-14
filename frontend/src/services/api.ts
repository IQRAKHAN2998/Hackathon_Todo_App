import axios from 'axios';
import { ChatResponse, SendMessageRequest } from '../types/chat';

// Get the API base URL from environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to requests
// Modified: Better Auth temporarily turned OFF - simplified to add mock token
api.interceptors.request.use(
  (config) => {
    // Add mock token from localStorage (for compatibility with backend expecting auth header)
    // Default to mock token if localStorage is not available
    let token = 'mock-jwt-token-for-development';
    if (typeof window !== 'undefined' && window.localStorage) {
      token = localStorage.getItem('token') || token;
    }
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle authentication errors
// DISABLED: Better Auth temporarily turned OFF - commented out to bypass auth redirects
/*
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.removeItem('token');
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);
*/

// Chat API functions
export const chatAPI = {
  // Send a message to the chatbot
  sendMessage: async (message: string, conversationId?: string): Promise<ChatResponse> => {
    try {
      const response = await api.post<ChatResponse>('/api/chat', {
        message,
        conversation_id: conversationId,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Get all conversations for the current user
  getConversations: async (): Promise<any[]> => {
    try {
      const response = await api.get('/api/chat/conversations');
      return response.data;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  },

  // Get messages for a specific conversation
  getConversationMessages: async (conversationId: string): Promise<any[]> => {
    try {
      const response = await api.get(`/api/chat/conversations/${conversationId}/messages`);
      return response.data;
    } catch (error) {
      console.error('Error fetching conversation messages:', error);
      throw error;
    }
  },
};

// Task API functions
export const taskAPI = {
  // Get all tasks
  getTasks: async (): Promise<any[]> => {
    try {
      const response = await api.get('/api/tasks');
      return response.data;
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Create a new task
  createTask: async (taskData: any): Promise<any> => {
    try {
      const response = await api.post('/api/tasks', taskData);
      return response.data;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Update a task
  updateTask: async (taskId: string, taskData: any): Promise<any> => {
    try {
      const response = await api.put(`/api/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Delete a task
  deleteTask: async (taskId: string): Promise<any> => {
    try {
      const response = await api.delete(`/api/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  },
};

// Authentication API functions
export const authAPI = {
  // Login user
  login: async (email: string, password: string): Promise<any> => {
    try {
      // DISABLED: Better Auth temporarily turned OFF - returning mock success
      // const response = await api.post('/api/auth/login', { email, password });
      // return response.data;

      // Mock successful login response
      const mockToken = 'mock-jwt-token-for-development';
      localStorage.setItem('token', mockToken);
      return {
        access_token: mockToken,
        token_type: 'bearer',
        success: true
      };
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  // Signup user
  signup: async (email: string, password: string): Promise<any> => {
    try {
      // DISABLED: Better Auth temporarily turned OFF - returning mock success
      // const response = await api.post('/api/auth/signup', { email, password });
      // return response.data;

      // Mock successful signup response
      const mockToken = 'mock-jwt-token-for-development';
      localStorage.setItem('token', mockToken);
      return {
        access_token: mockToken,
        token_type: 'bearer',
        success: true
      };
    } catch (error) {
      console.error('Error signing up:', error);
      throw error;
    }
  },
};

export default api;