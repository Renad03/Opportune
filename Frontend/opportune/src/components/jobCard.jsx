const JobCard = ({ job }) => {
  return (
    <div className="card border-0 shadow-sm h-100 hover-card">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <div>
            <h5 className="card-title mb-1">{job.title}</h5>
            <p className="text-muted mb-0">
              <i className="bi bi-building me-1"></i>
              {job.company}
            </p>
          </div>
          <span className="badge badge-navy fs-6">
            {job.matchScore}% Match
          </span>
        </div>

        <p className="text-muted mb-2">
          <i className="bi bi-geo-alt me-1"></i>
          {job.location}
        </p>

        <p className="text-muted mb-3">
          <i className="bi bi-cash me-1"></i>
          {job.salary} • {job.type}
        </p>

        <div className="mb-3">
          {job.skills.map((skill, idx) => (
            <span
              key={idx}
              className="badge badge-navy me-2 mb-2"
            >
              {skill}
            </span>
          ))}
        </div>

        <button className="btn btn-outline-navy w-100">
          <i className="bi bi-eye me-1"></i> View Details
        </button>
      </div>
    </div>
  );
};

export default JobCard;
