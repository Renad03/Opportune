import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Signup = () => {
  const navigate = useNavigate();
  
  // State for toggling visibility
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Common style for inputs
  const inputStyle = {
    background: 'rgba(255, 255, 255, 0.05)',
    border: '1px solid #D4DDE2',
    color: 'white',
    borderRight: 'none', // Remove right border to merge with icon
  };

  // Common style for the icon button
  const iconButtonStyle = {
    background: 'rgba(255, 255, 255, 0.05)',
    border: '1px solid #D4DDE2',
    borderLeft: 'none', // Remove left border to merge with input
    color: '#D4DDE2',
  };

  return (
    <div className="d-flex flex-column align-items-center justify-content-center min-vh-100 p-4" 
         style={{ background: 'linear-gradient(135deg, #c1d5e0 0%, #3e5663 100%)' }}>
      
      {/* Icon Avatar */}
      <div className="rounded-circle d-flex align-items-center justify-content-center shadow-lg"
           style={{ width: '90px', height: '90px', background: 'rgba(212, 221, 226, 0.2)', 
                    backdropFilter: 'blur(10px)', border: '1px solid rgba(212, 221, 226, 0.3)', 
                    marginBottom: '-45px', zIndex: 10 }}>
        <i className="bi bi-person-plus-fill text-white" style={{ fontSize: '2.5rem' }}></i>
      </div>

      {/* Signup Card */}
      <div className="p-5 shadow-lg" 
           style={{ background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(15px)', 
                    border: '1px solid rgba(212, 221, 226, 0.2)', borderRadius: '2rem', 
                    width: '100%', maxWidth: '450px' }}>
        
        <h2 className="h4 fw-bold text-white text-center mb-4 mt-4 text-uppercase tracking-widest">Create Account</h2>

        <form onSubmit={(e) => { e.preventDefault(); navigate('/jobs'); }}>
          <div className="mb-3">
            <input type="text" className="form-control text-center py-2" 
                   placeholder="User Name"
                   style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid #D4DDE2', color: 'white' }} />
          </div>
          
          <div className="mb-3">
            <input type="email" className="form-control text-center py-2" 
                   placeholder="Email Address"
                   style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid #D4DDE2', color: 'white' }} />
          </div>

          {/* Password Field using Input Group */}
          <div className="input-group mb-3">
            <input 
              type={showPassword ? "text" : "password"} 
              className="form-control text-center py-2 ps-5" // ps-5 to keep text centered despite icon
              placeholder="Password"
              style={inputStyle} 
            />
            <button 
              className="btn btn-outline-secondary" 
              type="button"
              style={iconButtonStyle}
              onClick={() => setShowPassword(!showPassword)}
            >
              <i className={`bi ${showPassword ?'bi-eye' : 'bi-eye-slash' }`}></i>
            </button>
          </div>

          {/* Confirm Password Field using Input Group */}
          <div className="input-group mb-4">
            <input 
              type={showConfirmPassword ? "text" : "password"} 
              className="form-control text-center py-2 ps-5"
              placeholder="Confirm Password"
              style={inputStyle} 
            />
            <button 
              className="btn btn-outline-secondary" 
              type="button"
              style={iconButtonStyle}
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              <i className={`bi ${showConfirmPassword ? 'bi-eye' : 'bi-eye-slash'}`}></i>
            </button>
          </div>
  
          <button type="submit" className="btn w-100 rounded-pill py-2 fw-bold text-uppercase shadow-sm"
                  style={{ backgroundColor: '#D4DDE2', color: '#5C7E8F' }}>
            Register Now
          </button>
        </form>

        <div className="text-center pt-4 mt-3 border-top border-white-25">
          <p className="small text-white-50">
            Already have an account? <Link to="/login" className="fw-bold text-white text-decoration-none text-uppercase ms-1">Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;