'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const HomePage = () => {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated by looking for token in localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      // If not authenticated, redirect to login page
      router.push('/auth/login');
    } else {
      // If authenticated, redirect to tasks page
      router.push('/tasks');
    }
  }, [router]);

  // Show a simple loading message while redirecting
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Redirecting...</p>
      </div>
    </div>
  );
};

export default HomePage;