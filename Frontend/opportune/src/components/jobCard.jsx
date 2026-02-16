import React from "react";

// Add onViewDetails and isActive to the props destructuring
const JobCard = ({ job, onViewDetails, isActive }) => {
  return (
    <div 
      className={`card h-100 border-0 shadow-sm transition hover-card ${isActive ? 'ring-slate' : ''}`}
      style={{ 
        borderRadius: '1.5rem', 
        border: isActive ? '2px solid #5C7E8F' : '1px solid transparent',
        backgroundColor: isActive ? '#f8fafb' : '#fff',
        transition: 'all 0.3s ease',
        cursor: 'pointer'
      }}
      // Optional: Clicking the whole card also triggers the details
      onClick={onViewDetails}
    >
      <div className="card-body p-4">
        <div className="d-flex justify-content-between mb-3">
          <div>
            <h5 className="card-title fw-bold mb-1" style={{ color: '#3e5663' }}>
              {job.title}
            </h5>
            <p className="text-muted small mb-0">
              <i className="bi bi-building me-1"></i> {job.company}
            </p>
          </div>
          <div 
            className="badge" 
            style={{ backgroundColor: '#D4DDE2', color: '#5C7E8F', alignSelf: 'start' }}
          >
            95% Match
          </div>
        </div>
        
        <div className="d-flex flex-wrap gap-3 mb-4 text-muted small">
          <span>
            <i className="bi bi-geo-alt me-1" style={{ color: '#5C7E8F' }}></i> 
            {job.location}
          </span>
          <span>
            <i className="bi bi-cash-stack me-1" style={{ color: '#5C7E8F' }}></i> 
            {job.salary}
          </span>
          <span>
            <i className="bi bi-clock me-1" style={{ color: '#5C7E8F' }}></i> 
            {job.type}
          </span>
        </div>

        <button 
          className="btn w-100 rounded-pill py-2 fw-bold"
          style={{ 
            backgroundColor: isActive ? '#5C7E8F' : 'transparent',
            color: isActive ? '#fff' : '#5C7E8F',
            border: '2px solid #5C7E8F'
          }}
          onClick={(e) => {
            e.stopPropagation(); // Prevents double-triggering if you click the button
            onViewDetails();
          }}
        >
          View Details <i className={`bi ${isActive ? 'bi-arrow-left' : 'bi-arrow-right'} ms-2`}></i>
        </button>
      </div>
    </div>
  );
};

export default JobCard;