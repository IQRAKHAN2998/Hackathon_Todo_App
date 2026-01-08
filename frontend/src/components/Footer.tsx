import React from 'react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-100 border-t border-gray-200 py-6">
      <div className="container mx-auto px-4 text-center text-gray-600">
        <p>© {currentYear} Todo App. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;