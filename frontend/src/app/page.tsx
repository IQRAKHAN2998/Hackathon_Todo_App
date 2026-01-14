'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const HomePage = () => {
  const router = useRouter();

  useEffect(() => {
    // Redirect to signup page as per requirements
    router.push('/auth/signup');
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <p className="text-lg text-gray-600">Redirecting to signup...</p>
      </div>
    </div>
  );
};

export default HomePage;