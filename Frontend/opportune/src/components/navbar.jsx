import React from 'react';
import { Link, NavLink } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top py-3">
      <style>{`
        /* Branding Color */
        .navbar-brand {
          color: #5C7E8F !important;
          letter-spacing: 0.5px;
        }

        /* Nav Link Transitions */
        .nav-link {
          color: #A2A2A2 !important; /* Medium Gray */
          font-weight: 500;
          transition: all 0.3s ease;
          position: relative;
          padding: 0.5rem 1rem !important;
        }

        /* Hover & Active States */
        .nav-link:hover, 
        .nav-link.active {
          color: #5C7E8F !important; /* Primary Slate */
        }

        /* Active Underline Effect */
        .nav-link.active::after {
          content: "";
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 20px;
          height: 3px;
          background-color: #5C7E8F;
          border-radius: 2px;
        }

        /* Logout Specific Style */
        .nav-logout {
          color: #dc3545 !important;
          opacity: 0.8;
        }
        .nav-logout:hover {
          opacity: 1;
        }
      `}</style>

      <div className="container">
        {/* Brand Link with Slate Theme */}
        <Link className="navbar-brand fw-bold d-flex align-items-center" to="/jobs">
          <i className="bi bi-briefcase-fill me-2" style={{ fontSize: '1.4rem' }}></i>
          OPPORTUNE
        </Link>

        <button 
          className="navbar-toggler border-0" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto align-items-center">
            <li className="nav-item">
              <NavLink 
                to="/jobs" 
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                <i className="bi bi-house-door me-1"></i> Jobs
              </NavLink>
            </li>

            <li className="nav-item">
              <NavLink 
                to="/courses" 
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                <i className="bi bi-book me-1"></i> Courses
              </NavLink>
            </li>

            <li className="nav-item">
              <NavLink 
                to="/applications" 
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                <i className="bi bi-clipboard-check me-1"></i> Applications
              </NavLink>
            </li>

            <li className="nav-item me-lg-2">
              <NavLink 
                to="/profile" 
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                <i className="bi bi-person-circle me-1"></i> Profile
              </NavLink>
            </li>

            {/* Styled Logout Button */}
            <li className="nav-item ms-lg-3 border-start ps-lg-3">
              <NavLink to="/login" className="nav-link nav-logout">
                <i className="bi bi-box-arrow-right me-1"></i> Logout
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};