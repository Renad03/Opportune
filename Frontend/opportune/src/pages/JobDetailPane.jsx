// components/JobDetailPane.js
import React from 'react';

const JobDetailPane = ({ job }) => {
  if (!job) return <div className="p-5 text-center text-muted">Select a job to view details</div>;

  return (
    // Updated styling for better scrolling and sticky behavior
    <div className="card border-0 shadow-sm sticky-top" style={{ top: '20px', maxHeight: 'calc(100vh - 40px)', overflowY: 'auto' }}>
      
      {/* Header Image / Banner */}
      <div className="bg-light w-100" style={{ height: '120px', background: 'linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%)' }}></div>
      
      <div className="card-body p-4 pt-0">
        
        {/* Logo & Title Section */}
        <div className="d-flex align-items-end mb-4" style={{ marginTop: '-40px' }}>
            <div className="bg-white p-3 rounded shadow-sm me-3 border">
                 {/* Dynamic Logo based on job data */}
                 <i className={`bi ${job.logo || 'bi-building'} fs-1 text-primary`}></i> 
            </div>
            <div className="mb-1">
                <h3 className="fw-bold mb-0 text-dark">{job.title}</h3>
                <p className="text-muted mb-0 fw-medium">
                    {job.company} <span className="mx-1">•</span> {job.location}
                </p>
            </div>
        </div>

        {/* Action Buttons */}
        <div className="d-flex gap-2 mb-4 pb-3 border-bottom">
            <button className="btn btn-primary px-4 rounded-pill fw-bold shadow-sm">
                Apply Now <i className="bi bi-box-arrow-up-right ms-2"></i>
            </button>
            <button className="btn btn-outline-secondary rounded-pill px-4 fw-bold">
                Save
            </button>
            <button className="btn btn-outline-light text-secondary border rounded-circle">
                <i className="bi bi-share-fill"></i>
            </button>
        </div>

        {/* Job Description */}
        <div className="mb-4">
            <h5 className="fw-bold mb-3 text-dark">About the job</h5>
            <div className="text-secondary lh-lg" style={{ fontSize: '0.95rem' }}>
                <p>{job.description}</p>
                <p>We are looking for a driven individual who wants to make a significant impact on our product and users.</p>
                
                {/* Kept Responsibilities List */}
                <h6 className="fw-bold text-dark mt-4">Responsibilities:</h6>
                <ul className="ps-3">
                    <li className="mb-2">Collaborate with cross-functional teams to define, design, and ship new features.</li>
                    <li className="mb-2">Work on bug fixing and improving application performance.</li>
                    <li className="mb-2">Discover, evaluate, and implement new technologies to maximize development efficiency.</li>
                    <li className="mb-2">Maintain code quality, organization, and automation.</li>
                </ul>
            </div>
        </div>

        {/* Skills */}
        <div className="mb-4">
            <h5 className="fw-bold mb-3 text-dark">Skills & Qualifications</h5>
            <div className="d-flex flex-wrap gap-2">
                {job.skills && job.skills.map((skill, i) => (
                    <span key={i} className="badge bg-light text-dark border px-3 py-2 fw-normal rounded-pill">
                        {skill}
                    </span>
                ))}
            </div>
        </div>
        
        {/* Footer Info */}
        <div className="card bg-light border-0 p-3 rounded-3 mt-auto">
            <div className="d-flex justify-content-between text-muted small fw-bold">
                <div className="d-flex align-items-center">
                    <i className="bi bi-clock me-2"></i> Posted 2 weeks ago
                </div>
                <div className="d-flex align-items-center">
                    <i className="bi bi-people me-2"></i> {job.applicants || "10"} applicants
                </div>
            </div>
        </div>

      </div>
    </div>
  );
};

export default JobDetailPane;