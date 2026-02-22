import React from 'react';

const JobCard = ({ job, isSelected, isCompact, onBack }) => {
  
  // --- MODE 1: COMPACT VIEW (For Sidebar List) ---
  if (isCompact) {
    return (
      <div 
        className={`card border-0 transition-all ${
          isSelected ? 'bg-white border-start border-4 border-primary shadow-sm' : 'bg-transparent hover-bg-light'
        }`}
        style={{ borderBottom: '1px solid #e0e0e0', cursor: 'pointer' }}
      >
        <div className="card-body p-3">
          <div className="d-flex align-items-center">
            
            {/* Logo */}
            <div className="flex-shrink-0 me-3">
               <div className="rounded bg-white border d-flex align-items-center justify-content-center" style={{width: '48px', height: '48px'}}>
                  {/* Using Bootstrap Icons as placeholder logos */}
                  <i className={`bi ${job.logo || 'bi-building'} fs-4 text-primary`}></i> 
               </div>
            </div>
            
            {/* Text Content */}
            <div className="flex-grow-1">
              <h6 className="card-title mb-1 fw-bold text-dark">{job.title}</h6>
              <div className="text-muted small">{job.company}</div>
            </div>

            {/* --- THE BLUE ARROW BUTTON (Only when Selected) --- */}
            {isSelected && (
                <div className="ms-2">
                    <button 
                        className="btn btn-link p-0 text-decoration-none"
                        onClick={(e) => {
                            e.stopPropagation(); // Stop click from bubbling to parent div
                            if(onBack) onBack(); // Trigger "Back" function
                        }}
                        title="Back to full list"
                    >
                        <i className="bi bi-arrow-left-circle-fill fs-3 text-primary"></i>
                    </button>
                </div>
            )}

          </div>
        </div>
      </div>
    );
  }

  // --- MODE 2: STANDARD VIEW (Big "Tesla" Style Card) ---
  return (
    <div className="card border-0 shadow-sm hover-card bg-white mb-3">
      <div className="card-body p-4">
        <div className="row">
            
          {/* Logo */}
          <div className="col-auto">
            <div className="bg-light rounded p-2 d-flex align-items-center justify-content-center" style={{width: '64px', height: '64px'}}>
               <i className={`bi ${job.logo || 'bi-building'} fs-3 text-secondary`}></i>
            </div>
          </div>

          {/* Main Details */}
          <div className="col ps-2">
            <div className="d-flex justify-content-between align-items-start mb-2">
                 <div>
                    <h5 className="card-title mb-1 fw-bold text-dark">{job.title}</h5>
                    <p className="text-muted mb-0 small text-uppercase fw-bold">{job.company}</p>
                 </div>
                 <div className="d-flex align-items-center gap-2">
                    <span className="badge bg-light text-secondary border fw-normal px-3 py-2 rounded-pill">Intermediate</span>
                    <button className="btn btn-light rounded-circle text-muted border-0"><i className="bi bi-bookmark"></i></button>
                 </div>
            </div>
            
            {/* Description truncated to 2 lines */}
            <p className="card-text text-secondary mb-3" style={{
                display: '-webkit-box',
                WebkitLineClamp: '2',
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
                lineHeight: '1.6',
                fontSize: '0.95rem'
            }}>
               {job.description}
            </p>

            {/* Footer */}
            <div className="d-flex flex-wrap align-items-center justify-content-between pt-2">
                <div className="d-flex gap-4 text-muted small">
                    <span><i className="bi bi-clock me-1"></i> 15 minutes ago</span>
                    <span><i className="bi bi-briefcase me-1"></i> {job.type}</span>
                    <span><i className="bi bi-people me-1"></i> 0 applied</span>
                </div>
                
                <div className="fw-bold fs-5 text-dark">
                    {job.salary} <span className="text-muted fs-6 fw-normal">/year</span>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobCard;