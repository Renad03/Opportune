import React, { useState } from 'react';
import { mockJobs } from '../data/mockJobs';
import JobCard from '../components/jobCard';
// Kept your import path, but usually components are in '../components/JobDetailPane'
import JobDetailPane from '../pages/JobDetailPane'; 
import { HeroSection } from '../components/heroSection';

const Sidebar = ({ onClose }) => (
  <div className="card border-0 shadow-sm h-100" style={{ minHeight: '100vh' }}>
    <div className="card-body p-0">
      
      {/* Header with 3-Slashes Icon */}
      <div className="d-flex justify-content-between align-items-center p-3 border-bottom">
          <span className="fw-bold text-uppercase small text-secondary">Menu</span>
          <button onClick={onClose} className="btn btn-sm btn-outline-secondary border-0 fs-4">
            <i className="bi bi-list"></i> 
          </button>
      </div>

      {/* SECTION: MAIN */}
      <div className="list-group list-group-flush mb-2">
        <div className="list-group-item bg-transparent text-uppercase fw-bold text-muted small border-0 mt-2">
          Main Menu
        </div>
        <a href="#" className="list-group-item list-group-item-action fw-bold text-primary border-0 border-start border-4 border-primary bg-light">
          <i className="bi bi-grid-fill me-3"></i> Dashboard
        </a>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-person me-3"></i> My Profile
        </a>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-briefcase me-3"></i> Recommended Jobs
        </a>
      </div>

      {/* SECTION: JOB HUNT */}
      <div className="list-group list-group-flush mb-2">
        <div className="list-group-item bg-transparent text-uppercase fw-bold text-muted small border-0">
          Job Hunt
        </div>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-bookmark me-3"></i> Saved Jobs
          <span className="badge bg-secondary rounded-pill float-end">12</span>
        </a>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-file-earmark-text me-3"></i> Applications
          <span className="badge bg-success rounded-pill float-end">3</span>
        </a>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-calendar-event me-3"></i> Interviews
        </a>
      </div>

      {/* SECTION: COMMUNITY */}
      <div className="list-group list-group-flush mb-2">
        <div className="list-group-item bg-transparent text-uppercase fw-bold text-muted small border-0">
          Community
        </div>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-people me-3"></i> Networking
        </a>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-chat-dots me-3"></i> Messages
        </a>
      </div>

      {/* SECTION: SETTINGS */}
      <div className="list-group list-group-flush pb-3">
        <div className="list-group-item bg-transparent text-uppercase fw-bold text-muted small border-0">
          Settings
        </div>
        <a href="#" className="list-group-item list-group-item-action text-secondary border-0">
          <i className="bi bi-gear me-3"></i> Account
        </a>
        <a href="#" className="list-group-item list-group-item-action text-danger border-0">
          <i className="bi bi-box-arrow-right me-3"></i> Logout
        </a>
      </div>

    </div>
  </div>
);

const RecommendedJobs = () => {
  const [selectedJob, setSelectedJob] = useState(null); 
  const [showSidebar, setShowSidebar] = useState(false);

  return (
    <div className="container-fluid py-4 bg-light" style={{ minHeight: '100vh' }}>
      <div className="row g-0">
        
        {/* Sidebar */}
        {showSidebar && (
          <div className="col-lg-2 d-none d-lg-block pe-0 transition-all">
             <Sidebar onClose={() => setShowSidebar(false)} />
          </div>
        )}

        {/* Main Content */}
        <div className={`transition-all ${showSidebar ? "col-lg-10" : "col-12"}`}>
          
          {/* Top Bar */}
          <div className="mb-3 px-3">
             {!showSidebar && (
                <button onClick={() => setShowSidebar(true)} className="btn btn-link text-secondary text-decoration-none p-0 mb-2">
                  <i className="bi bi-list fs-4"></i>
                </button>
             )}
             <div className="d-flex justify-content-between align-items-end border-bottom pb-2">
                <div>
                   <h4 className="fw-bold mb-1">
                       {selectedJob ? "Job Details" : "Recommended for You"}
                   </h4>
                   <small className="text-muted">
                       {selectedJob ? "Viewing job details" : "Based on your profile and search history"}
                   </small>
                </div>
                
                {/* REMOVED THE "BACK TO LIST" BUTTON FROM HERE */}
                {/* The functionality is now inside the JobCard arrow */}
             </div>
          </div>

          <div className="row g-0 px-3">
            
            {/* --- CASE 1: NO JOB SELECTED (Show Big List) --- */}
            {!selectedJob ? (
                <div className="col-lg-8 offset-lg-2 col-md-10 offset-md-1">
                    <div className="d-flex flex-column gap-3">
                        {mockJobs.map(job => (
                            <div key={job.id} onClick={() => setSelectedJob(job)} style={{ cursor: 'pointer' }}>
                                <JobCard job={job} isCompact={false} />
                            </div>
                        ))}
                    </div>
                </div>
            ) : (
            /* --- CASE 2: JOB SELECTED (Show Split View) --- */
                <>
                    {/* Left: Compact List */}
                    <div className="col-lg-4 col-md-5 pe-lg-3">
                        <div className="d-flex flex-column gap-2" style={{ maxHeight: '85vh', overflowY: 'auto' }}>
                            {mockJobs.map(job => (
                                <div key={job.id} onClick={() => setSelectedJob(job)} style={{ cursor: 'pointer' }}>
                                    <JobCard 
                                        job={job} 
                                        isSelected={selectedJob?.id === job.id} 
                                        isCompact={true}
                                        // ADDED: Pass the back function here
                                        onBack={() => setSelectedJob(null)} 
                                    />
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Right: Detail Pane */}
                    <div className="col-lg-8 col-md-7 d-none d-md-block ps-lg-2">
                        <div className="sticky-top" style={{ top: '20px' }}>
                            <JobDetailPane job={selectedJob} />
                        </div>
                    </div>
                </>
            )}

          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendedJobs;