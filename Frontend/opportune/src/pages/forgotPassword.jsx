import React from 'react';
import { Link } from 'react-router-dom';

const ForgotPassword = () => {
  return (
    <div className="d-flex flex-column align-items-center justify-content-center min-vh-100 p-4" 
         style={{ background: 'linear-gradient(135deg, #c1d5e0 0%, #3e5663 100%)' }}>
      
      {/* Icon Avatar */}
      <div className="rounded-circle d-flex align-items-center justify-content-center shadow-lg"
           style={{ width: '90px', height: '90px', background: 'rgba(212, 221, 226, 0.2)', 
                    backdropFilter: 'blur(10px)', border: '1px solid rgba(212, 221, 226, 0.3)', 
                    marginBottom: '-45px', zIndex: 10 }}>
        <i className="bi bi-shield-lock-fill text-white" style={{ fontSize: '2.5rem' }}></i>
      </div>

      {/* Reset Card */}
      <div className="p-5 shadow-lg text-center" 
           style={{ background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(15px)', 
                    border: '1px solid rgba(212, 221, 226, 0.2)', borderRadius: '2rem', 
                    width: '100%', maxWidth: '400px' }}>
        
        <h2 className="h4 fw-bold text-white mb-2 mt-4 text-uppercase tracking-widest">Reset Password</h2>
        <p className="small mb-4" style={{ color: '#D4DDE2', opacity: 0.8 }}>
          Enter your email and we'll send you instructions to reset your password.
        </p>

        <form onSubmit={(e) => e.preventDefault()}>
          <input type="email" className="form-control mb-4 text-center py-2" 
                 placeholder="Email Address"
                 style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid #D4DDE2', color: 'white' }} 
                 required />

          <button type="submit" className="btn w-100 rounded-pill py-2 fw-bold text-uppercase shadow-sm mb-2"
                  style={{ backgroundColor: '#D4DDE2', color: '#5C7E8F' }}>
            Send Reset Link
          </button>
        </form>
      </div>

      {/* Back Link */}
      <div className="mt-4 text-center">
        <Link to="/login" className="text-white-50 text-decoration-none d-flex align-items-center justify-content-center">
          <i className="bi bi-arrow-left me-2"></i> Back to Login
        </Link>
      </div>
    </div>
  );
};

export default ForgotPassword;