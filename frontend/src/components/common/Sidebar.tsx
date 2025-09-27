
import React from 'react';
import './Sidebar.css';

interface SidebarProps {
  activeModule: string;
  onModuleChange: (module: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeModule, onModuleChange }) => {
  const modules = [
    { id: 'dashboard', name: 'Dashboard', icon: '📊' },
    { id: 'customers', name: 'Customers', icon: '👥' },
    { id: 'leads', name: 'Leads', icon: '🎯' },
    { id: 'employees', name: 'Employees', icon: '👤' },
    { id: 'departments', name: 'Departments', icon: '🏢' },
    { id: 'attendance', name: 'Attendance', icon: '⏰' },
    { id: 'leave', name: 'Leave Requests', icon: '📅' },
  ];

  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <h2>CRM + HRMS</h2>
      </div>
      <ul className="sidebar-menu">
        {modules.map((module) => (
          <li key={module.id}>
            <button
              className={`sidebar-item ${activeModule === module.id ? 'active' : ''}`}
              onClick={() => onModuleChange(module.id)}
            >
              <span className="sidebar-icon">{module.icon}</span>
              <span className="sidebar-text">{module.name}</span>
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Sidebar;
