// Type definitions for authentication

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ErrorResponse {
  error: string;
  code?: number;
  details?: any;
}

export interface User {
  id: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}