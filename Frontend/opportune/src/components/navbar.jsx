export const Navbar = ({ currentPage, onNavigate }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
      <div className="container">
        <button className="navbar-brand fw-bold text-success border-0 bg-transparent" onClick={() => onNavigate('jobs')}>
          <i className="bi bi-briefcase-fill me-2"></i>
          Opportune
        </button>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <button 
                className={`nav-link border-0 bg-transparent ${currentPage === 'jobs' ? 'active' : ''}`} 
                onClick={() => onNavigate('jobs')}
              >
                <i className="bi bi-house-door me-1"></i> Jobs
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link border-0 bg-transparent ${currentPage === 'courses' ? 'active' : ''}`} 
                onClick={() => onNavigate('courses')}
              >
                <i className="bi bi-book me-1"></i> Courses
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link border-0 bg-transparent ${currentPage === 'interview' ? 'active' : ''}`} 
                onClick={() => onNavigate('interview')}
              >
                <i className="bi bi-chat-left-quote me-1"></i> Interview Prep
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link border-0 bg-transparent ${currentPage === 'applications' ? 'active' : ''}`} 
                onClick={() => onNavigate('applications')}
              >
                <i className="bi bi-clipboard-check me-1"></i> Applications
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

