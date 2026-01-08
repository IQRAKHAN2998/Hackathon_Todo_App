import axios from 'axios';
import { LoginCredentials, SignupData, AuthResponse, ErrorResponse } from './types';

// Get the API base URL from environment or use default
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Create axios instance for auth requests
const authApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authService = {
  // Signup a new user
  signup: async (email: string, password: string): Promise<AuthResponse> => {
    try {
      const response = await authApi.post('/auth/signup', {
        email,
        password,
      });
      return response.data;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Signup failed';
      const errorCode = error.response?.status;
      const errorDetails = error.response?.data;

      throw {
        error: errorMessage,
        code: errorCode,
        details: errorDetails
      } as ErrorResponse;
    }
  },

  // Login an existing user
  login: async (email: string, password: string): Promise<AuthResponse> => {
    try {
      const response = await authApi.post('/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Login failed';
      const errorCode = error.response?.status;
      const errorDetails = error.response?.data;

      throw {
        error: errorMessage,
        code: errorCode,
        details: errorDetails
      } as ErrorResponse;
    }
  },
};