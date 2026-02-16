const JobSidebarItem = ({ job, isActive, onClick }) => {
  return (
    <div 
      onClick={onClick}
      className={`p-3 mb-2 rounded-4 border transition cursor-pointer ${
        isActive ? 'border-primary bg-light shadow-sm' : 'border-transparent bg-white'
      }`}
      style={{ cursor: 'pointer', transition: '0.2s' }}
    >
      <div className="d-flex align-items-center justify-content-between">
        <div className="d-flex align-items-center gap-3">
          <div className="bg-primary rounded-3 p-2 text-white shadow-sm" style={{ width: '45px', height: '45px' }}>
            <i className="bi bi-briefcase-fill fs-4"></i>
          </div>
          <div>
            <h6 className="mb-0 fw-bold text-dark">{job.title}</h6>
            <small className="text-muted">{job.company}</small>
          </div>
        </div>
        {isActive && <i className="bi bi-arrow-left-circle-fill text-primary fs-5"></i>}
      </div>
    </div>
  );
};

export default JobSidebarItem;