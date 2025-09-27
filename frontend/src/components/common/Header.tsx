
import React from 'react';
import './Header.css';

interface HeaderProps {
  title: string;
  user?: {
    name: string;
    email: string;
  };
}

const Header: React.FC<HeaderProps> = ({ title, user }) => {
  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="header-title">{title}</h1>
        {user && (
          <div className="user-info">
            <span className="user-name">{user.name}</span>
            <span className="user-email">{user.email}</span>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
