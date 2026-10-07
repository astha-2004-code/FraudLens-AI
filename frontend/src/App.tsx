import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import InvestigationDetail from './pages/InvestigationDetail';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-slate-950 font-sans">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/investigations/:id" element={<InvestigationDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
