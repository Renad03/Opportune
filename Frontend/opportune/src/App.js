// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './login';
import Signup from './Signup';
import Dashboard from './Dashboard'; // We import the file we just created

function App() {
  return (
    <Router>
      <Routes>
        {/* Route 1: The Login Page (Default) */}
        <Route path="/" element={<Login />} />
        
        {/* Route 2: The Signup Page */}
        <Route path="/signup" element={<Signup />} />
        
        {/* Route 3: The Main Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;