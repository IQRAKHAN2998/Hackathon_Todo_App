import axios from 'axios';
import { Task, TaskResponse, ErrorResponse, FilterCriteria, SortCriteria } from '@/types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle authentication errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      localStorage.removeItem('token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

export const taskApi = {
  // Get all tasks with optional filtering and sorting
  getTasks: async (filters?: FilterCriteria, sort?: SortCriteria) => {
    const params: Record<string, any> = {};

    if (filters) {
      if (filters.completed !== undefined && filters.completed !== null) {
        params.completed = filters.completed;
      }
      if (filters.priority) {
        params.priority = filters.priority;
      }
      if (filters.tags && filters.tags.length > 0) {
        params.tag = filters.tags[0]; // Using first tag as query param (backend might need to handle multiple)
      }
      if (filters.searchQuery) {
        params.keyword = filters.searchQuery;
      }
    }

    if (sort) {
      params.sort = sort.field;
      params.reverse = sort.direction === 'desc';
    }

    try {
      // The backend returns raw task data, but we need to wrap it in our expected format
      const response = await api.get<any>(`/api/tasks`, { params }); // Removed userId from URL

      // Wrap the raw response in our expected format
      const wrappedResponse: TaskResponse = {
        success: true,
        data: response.data
      };

      // Process response to convert tags from string to array
      if (wrappedResponse.data && Array.isArray(wrappedResponse.data)) {
        wrappedResponse.data = wrappedResponse.data.map(task => ({
          ...task,
          tags: Array.isArray(task.tags) ? task.tags : (task.tags ? JSON.parse(task.tags) : []),
          dueDate: task.due_date || undefined,
          createdAt: task.created_at,
          updatedAt: task.updated_at
        }));
      }

      return wrappedResponse;
    } catch (error: any) {
      const errorResponse: ErrorResponse = {
        error: error.response?.data?.error || 'Failed to fetch tasks',
        code: error.response?.status.toString() || '500',
        details: error.response?.data
      };
      throw errorResponse;
    }
  },

  // Get a specific task by ID
  getTask: async (id: string) => {
    try {
      // The backend returns raw task data, but we need to wrap it in our expected format
      const response = await api.get<any>(`/api/tasks/${id}`); // Removed userId from URL

      // Wrap the raw response in our expected format
      const wrappedResponse: TaskResponse = {
        success: true,
        data: response.data
      };

      // Process response to convert tags from string to array
      if (wrappedResponse.data) {
        wrappedResponse.data = {
          ...wrappedResponse.data,
          tags: Array.isArray(wrappedResponse.data.tags) ?
            wrappedResponse.data.tags :
            (wrappedResponse.data.tags ? JSON.parse(wrappedResponse.data.tags) : []),
          dueDate: wrappedResponse.data.due_date || undefined,
          createdAt: wrappedResponse.data.created_at,
          updatedAt: wrappedResponse.data.updated_at
        };
      }

      return wrappedResponse;
    } catch (error: any) {
      const errorResponse: ErrorResponse = {
        error: error.response?.data?.error || `Failed to fetch task with ID: ${id}`,
        code: error.response?.status.toString() || '500',
        details: error.response?.data
      };
      throw errorResponse;
    }
  },

  // Create a new task
  createTask: async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      // Convert tags from array to JSON string for backend storage
      const taskDataToSend = {
        ...taskData,
        tags: Array.isArray(taskData.tags) ? JSON.stringify(taskData.tags) : taskData.tags
      };

      // The backend returns raw task data, but we need to wrap it in our expected format
      const response = await api.post<any>(`/api/tasks`, taskDataToSend); // Removed userId from URL

      // Wrap the raw response in our expected format
      const wrappedResponse: TaskResponse = {
        success: true,
        data: response.data
      };

      // Process response to convert tags from string back to array
      if (wrappedResponse.data) {
        wrappedResponse.data = {
          ...wrappedResponse.data,
          tags: Array.isArray(wrappedResponse.data.tags) ?
            wrappedResponse.data.tags :
            (wrappedResponse.data.tags ? JSON.parse(wrappedResponse.data.tags) : []),
          dueDate: wrappedResponse.data.due_date || undefined,
          createdAt: wrappedResponse.data.created_at,
          updatedAt: wrappedResponse.data.updated_at
        };
      }

      return wrappedResponse;
    } catch (error: any) {
      const errorResponse: ErrorResponse = {
        error: error.response?.data?.error || 'Failed to create task',
        code: error.response?.status.toString() || '500',
        details: error.response?.data
      };
      throw errorResponse;
    }
  },

  // Update an existing task
  updateTask: async (id: string, taskData: Partial<Task>) => {
    try {
      // Convert tags from array to JSON string for backend storage if present
      const taskDataToSend = {
        ...taskData,
        tags: taskData.tags !== undefined ?
          (Array.isArray(taskData.tags) ? JSON.stringify(taskData.tags) : taskData.tags) :
          undefined
      };

      // The backend returns raw task data, but we need to wrap it in our expected format
      const response = await api.put<any>(`/api/tasks/${id}`, taskDataToSend); // Removed userId from URL

      // Wrap the raw response in our expected format
      const wrappedResponse: TaskResponse = {
        success: true,
        data: response.data
      };

      // Process response to convert tags from string back to array
      if (wrappedResponse.data) {
        wrappedResponse.data = {
          ...wrappedResponse.data,
          tags: Array.isArray(wrappedResponse.data.tags) ?
            wrappedResponse.data.tags :
            (wrappedResponse.data.tags ? JSON.parse(wrappedResponse.data.tags) : []),
          dueDate: wrappedResponse.data.due_date || undefined,
          createdAt: wrappedResponse.data.created_at,
          updatedAt: wrappedResponse.data.updated_at
        };
      }

      return wrappedResponse;
    } catch (error: any) {
      const errorResponse: ErrorResponse = {
        error: error.response?.data?.error || `Failed to update task with ID: ${id}`,
        code: error.response?.status.toString() || '500',
        details: error.response?.data
      };
      throw errorResponse;
    }
  },

  // Delete a task
  deleteTask: async (id: string) => {
    try {
      // The backend returns a success message, but we need to wrap it in our expected format
      const response = await api.delete<any>(`/api/tasks/${id}`); // Removed userId from URL

      // For delete operations, we'll return a success response with no data
      const wrappedResponse: TaskResponse = {
        success: true,
        data: response.data  // This could be the success message from the backend
      };

      return wrappedResponse;
    } catch (error: any) {
      const errorResponse: ErrorResponse = {
        error: error.response?.data?.error || `Failed to delete task with ID: ${id}`,
        code: error.response?.status.toString() || '500',
        details: error.response?.data
      };
      throw errorResponse;
    }
  },

  // Toggle task completion status
  toggleTaskCompletion: async (id: string, completed: boolean) => {
    try {
      // The backend returns raw task data, but we need to wrap it in our expected format
      const response = await api.patch<any>(`/api/tasks/${id}/complete`, {
        completed
      });

      // Wrap the raw response in our expected format
      const wrappedResponse: TaskResponse = {
        success: true,
        data: response.data
      };

      // Process response to convert tags from string back to array
      if (wrappedResponse.data) {
        wrappedResponse.data = {
          ...wrappedResponse.data,
          tags: Array.isArray(wrappedResponse.data.tags) ?
            wrappedResponse.data.tags :
            (wrappedResponse.data.tags ? JSON.parse(wrappedResponse.data.tags) : []),
          dueDate: wrappedResponse.data.due_date || undefined,
          createdAt: wrappedResponse.data.created_at,
          updatedAt: wrappedResponse.data.updated_at
        };
      }

      return wrappedResponse;
    } catch (error: any) {
      const errorResponse: ErrorResponse = {
        error: error.response?.data?.error || `Failed to update task completion status with ID: ${id}`,
        code: error.response?.status.toString() || '500',
        details: error.response?.data
      };
      throw errorResponse;
    }
  },
};

export default api;