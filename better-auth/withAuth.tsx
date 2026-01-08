'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { TokenUtils } from './tokenUtils';

// Higher-order component to protect routes
export function withAuth<P extends object>(
  Component: React.ComponentType<P>
): React.FC<P> {
  const AuthenticatedComponent: React.FC<P> = (props: P) => {
    const router = useRouter();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Check if user is authenticated
      if (!TokenUtils.isAuthenticated()) {
        // If not authenticated, redirect to login
        router.push('/auth/login');
      } else {
        // If authenticated, continue loading the component
        setLoading(false);
      }
    }, [router]);

    if (loading) {
      // Show loading state while checking authentication
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Checking authentication...</p>
          </div>
        </div>
      );
    }

    // If authenticated, render the component
    return <Component {...props} />;
  };

  return AuthenticatedComponent;
}

// Hook for checking authentication in components
export const useAuth = () => {
  const router = useRouter();

  const checkAuth = () => {
    if (!TokenUtils.isAuthenticated()) {
      router.push('/auth/login');
      return false;
    }
    return true;
  };

  const logout = () => {
    TokenUtils.removeToken();
    router.push('/auth/login');
  };

  return {
    isAuthenticated: TokenUtils.isAuthenticated(),
    checkAuth,
    logout,
    getToken: TokenUtils.getToken
  };
};