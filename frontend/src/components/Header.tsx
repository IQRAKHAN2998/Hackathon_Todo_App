import React from 'react';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Todo App' }) => {
  return (
    <header className="bg-primary-600 text-white shadow">
      <div className="container mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold">{title}</h1>
      </div>
    </header>
  );
};

export default Header;