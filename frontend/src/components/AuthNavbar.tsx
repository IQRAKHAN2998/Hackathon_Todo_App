'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const AuthNavbar: React.FC = () => {
  const router = useRouter();
  const [isClient, setIsClient] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Set isClient to true on mount to ensure we're on the client
    setIsClient(true);

    // Check if user is authenticated
    const token = localStorage.getItem('token');
    setIsAuthenticated(token !== null);
  }, []);

  const handleLogout = () => {
    // Remove token from localStorage
    localStorage.removeItem('token');
    // Update state
    setIsAuthenticated(false);
    // Redirect to login page
    router.push('/auth/login');
    router.refresh();
  };

  // Render nothing on the server, and a loading state on the client until we know the auth status
  if (!isClient) {
    return <div />; // Empty div to satisfy SSR
  }

  if (isAuthenticated) {
    return (
      <button
        onClick={handleLogout}
        className="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-md transition-colors"
      >
        Logout
      </button>
    );
  }

  return (
    <div className="flex space-x-4">
      <a
        href="/auth/login"
        className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
      >
        Login
      </a>
      <a
        href="/auth/signup"
        className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
      >
        Sign Up
      </a>
    </div>
  );
};

export default AuthNavbar;