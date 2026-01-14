'use client';

import React from 'react';
import AuthNavbar from './AuthNavbar';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Todo App' }) => {
  return (
    <header className="bg-primary-600 text-white shadow">
      <div className="container mx-auto px-4 py-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold">{title}</h1>
        <AuthNavbar />
      </div>
    </header>
  );
};

export default Header;