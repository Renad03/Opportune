import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="py-5 mt-5" style={{ backgroundColor: '#3e5663', color: '#D4DDE2' }}>
      <style>{`
        .footer-link {
          color: #D4DDE2;
          opacity: 0.7;
          text-decoration: none;
          transition: all 0.3s ease;
        }
        .footer-link:hover {
          color: #FFFFFF;
          opacity: 1;
          padding-left: 5px;
        }
        .social-icon {
          color: #D4DDE2;
          transition: transform 0.3s ease, color 0.3s ease;
          cursor: pointer;
        }
        .social-icon:hover {
          color: #FFFFFF;
          transform: translateY(-3px);
        }
      `}</style>

      <div className="container">
        <div className="row g-4">
          {/* Brand Section */}
          <div className="col-md-6">
            <h5 className="mb-3 fw-bold text-white text-uppercase tracking-wider">
              <i className="bi bi-briefcase-fill me-2" style={{ color: '#D4DDE2' }}></i>
              Opportune
            </h5>
            <p className="small lh-lg" style={{ maxWidth: '400px', opacity: 0.8 }}>
              Your AI-powered career companion. We help you navigate the job market with 
              smart recommendations, skill development, and expert interview preparation.
            </p>
          </div>

          {/* Quick Links Section */}
          <div className="col-md-3">
            <h6 className="mb-3 fw-bold text-white text-uppercase small tracking-widest">Platform</h6>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link to="/jobs" className="footer-link small">Recommended Jobs</Link>
              </li>
              <li className="mb-2">
                <Link to="/courses" className="footer-link small">Skill Courses</Link>
              </li>
              <li className="mb-2">
                <Link to="/interview" className="footer-link small">Interview Prep</Link>
              </li>
              <li className="mb-2">
                <Link to="/applications" className="footer-link small">Track Applications</Link>
              </li>
            </ul>
          </div>

          {/* Connect Section */}
          <div className="col-md-3">
            <h6 className="mb-3 fw-bold text-white text-uppercase small tracking-widest">Connect With Us</h6>
            <div className="d-flex gap-3">
              <i className="bi bi-linkedin fs-5 social-icon"></i>
              <i className="bi bi-twitter-x fs-5 social-icon"></i>
              <i className="bi bi-github fs-5 social-icon"></i>
              <i className="bi bi-discord fs-5 social-icon"></i>
            </div>
            <div className="mt-4">
              <p className="small mb-1" style={{ opacity: 0.6 }}>Support Email:</p>
              <a href="mailto:hello@opportune.com" className="footer-link small">hello@opportune.com</a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <hr className="my-4" style={{ backgroundColor: '#D4DDE2', opacity: 0.1 }} />
        <div className="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3">
          <p className="x-small mb-0" style={{ opacity: 0.5, fontSize: '0.8rem' }}>
            &copy; {new Date().getFullYear()} Opportune AI. All rights reserved.
          </p>
          <div className="d-flex gap-4">
            <Link to="#" className="footer-link" style={{ fontSize: '0.75rem' }}>Privacy Policy</Link>
            <Link to="#" className="footer-link" style={{ fontSize: '0.75rem' }}>Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;