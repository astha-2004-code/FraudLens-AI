import React from 'react';
import { NavLink } from 'react-router-dom';
import { Activity, ShieldAlert, BarChart3, Users, Settings, LogOut } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { icon: <BarChart3 size={20} />, label: 'Dashboard', path: '/' },
    { icon: <ShieldAlert size={20} />, label: 'Investigations', path: '/investigations' },
    { icon: <Activity size={20} />, label: 'Risk Signals', path: '/signals' },
    { icon: <Users size={20} />, label: 'Customers', path: '/customers' },
    { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
  ];

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 text-slate-300 flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
          FraudLens AI
        </h1>
      </div>
      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item, idx) => (
          <NavLink
            key={idx}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive 
                  ? 'bg-blue-500/10 text-blue-400 font-medium' 
                  : 'hover:bg-slate-800 hover:text-slate-100'
              }`
            }
          >
            {item.icon}
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-slate-800">
        <button className="flex items-center space-x-3 px-4 py-3 w-full text-left rounded-xl hover:bg-slate-800 hover:text-rose-400 transition-colors">
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
