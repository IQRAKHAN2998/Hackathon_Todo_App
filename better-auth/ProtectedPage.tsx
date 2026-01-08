'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { TokenUtils } from './tokenUtils';

// A protected page example that can only be accessed when logged in
export default function ProtectedPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is authenticated
    if (!TokenUtils.isAuthenticated()) {
      // If not authenticated, redirect to login
      router.push('/auth/login');
      return;
    }

    // If authenticated, we can decode the token to get user info
    const token = TokenUtils.getToken();
    if (token) {
      const decoded = TokenUtils.decodeToken(token);
      if (decoded && decoded.email) {
        setUserEmail(decoded.email);
      }
    }

    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const handleLogout = () => {
    TokenUtils.removeToken();
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Welcome to Protected Area</h1>

          <div className="mb-6">
            <p className="text-gray-700">
              You are logged in as: <span className="font-semibold">{userEmail || 'Unknown'}</span>
            </p>
          </div>

          <div className="space-y-4">
            <button
              onClick={handleLogout}
              className="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Logout
            </button>

            <button
              onClick={() => router.push('/tasks')}
              className="w-full py-2 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Go to Tasks
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}