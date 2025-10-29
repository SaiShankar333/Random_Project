import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Layout/Navbar';
import Footer from './components/Layout/Footer';
import Dashboard from './pages/Dashboard';
import Detector from './pages/Detector';
import BulkAnalysis from './pages/BulkAnalysis';
import Performance from './pages/Performance';

function App() {
  useEffect(() => {
    // Set dark mode by default
    document.documentElement.classList.add('dark');
  }, []);

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/detector" element={<Detector />} />
            <Route path="/bulk-analysis" element={<BulkAnalysis />} />
            <Route path="/performance" element={<Performance />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;

