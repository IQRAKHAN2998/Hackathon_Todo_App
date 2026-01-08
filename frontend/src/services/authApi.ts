import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Create axios instance for auth requests
const authApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authApiService = {
  // Signup a new user
  signup: async (email: string, password: string) => {
    try {
      const response = await authApi.post('/auth/signup', {
        email,
        password,
      });
      return response.data;
    } catch (error: any) {
      throw {
        error: error.response?.data?.detail || error.response?.data?.error || 'Signup failed',
        code: error.response?.status,
        details: error.response?.data
      };
    }
  },

  // Login an existing user
  login: async (email: string, password: string) => {
    try {
      const response = await authApi.post('/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error: any) {
      throw {
        error: error.response?.data?.detail || error.response?.data?.error || 'Login failed',
        code: error.response?.status,
        details: error.response?.data
      };
    }
  },
};