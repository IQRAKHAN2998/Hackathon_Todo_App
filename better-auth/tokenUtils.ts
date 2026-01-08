// Utility functions for handling JWT tokens

export const TokenUtils = {
  // Store token in localStorage
  setToken: (token: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  },

  // Get token from localStorage
  getToken: (): string | null => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  },

  // Remove token from localStorage
  removeToken: (): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  },

  // Check if user is authenticated
  isAuthenticated: (): boolean => {
    const token = TokenUtils.getToken();
    return token !== null && token !== undefined && token !== '';
  },

  // Decode JWT token to get user info (basic implementation)
  decodeToken: (token: string): any | null => {
    try {
      if (!token) return null;

      // Remove 'Bearer ' prefix if present
      const cleanToken = token.startsWith('Bearer ') ? token.substring(7) : token;

      // Split the token to get the payload
      const parts = cleanToken.split('.');
      if (parts.length !== 3) {
        return null;
      }

      // Decode the payload (second part)
      const payload = parts[1];
      // Add padding if needed
      const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
      const decodedPayload = atob(paddedPayload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  },
};