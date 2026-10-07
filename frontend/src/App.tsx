import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-slate-950 font-sans">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          {/* We will add other routes here in subsequent commits */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
