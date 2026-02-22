// src/Login.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; //  useNavigate 
import { FcGoogle } from 'react-icons/fc';
import { FaGithub } from 'react-icons/fa';
import './App.css'; 

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  
  const navigate = useNavigate();
  

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login:', email, password);
    navigate('/dashboard'); 
  };

  const handleSocialLogin = (provider) => {
    console.log(`Logging in with ${provider}`);
    navigate('/dashboard');
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="email"
          placeholder="Email Address"
          className="auth-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="auth-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="auth-button">Login</button>
      </form>

      <div className="separator">
        <span>OR</span>
      </div>

      <button onClick={() => handleSocialLogin('Google')} className="social-btn google-btn">
        <FcGoogle className="social-icon" /> Continue with Google
      </button>

      <button onClick={() => handleSocialLogin('GitHub')} className="social-btn github-btn">
        <FaGithub className="social-icon" /> Continue with GitHub
      </button>

      <div className="auth-link">
        Don't have an account? <Link to="/signup">Sign up</Link>
      </div>
    </div>
  );
}


export default Login;