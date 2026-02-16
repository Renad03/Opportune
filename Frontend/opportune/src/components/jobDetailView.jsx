import React from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
const JobDetailView = ({ job, onClose }) => {
  const navigate = useNavigate(); // 2. Initialize the navigate function
  if (!job) return null;

  const handleStartInterview = () => {
    // 3. This is how you navigate programmatically and pass data (state)
    navigate('/mock-interview', { state: { job } });
  };
  return (
    <div className="bg-white rounded-4 shadow-sm h-100 overflow-hidden d-flex flex-column border border-light">
      {/* Themed Header Strip - Swapped from blue to Slate Gradient */}
      <div 
        style={{ 
          height: '100px', 
          background: 'linear-gradient(135deg, #5C7E8F 0%, #3e5663 100%)' 
        }}
      ></div>
      
      <div className="p-4 pt-0" style={{ marginTop: '-40px' }}>
        {/* Floating Logo Container */}
        <div 
          className="bg-white rounded-4 p-3 shadow-sm d-inline-block mb-3 border" 
          style={{ width: '85px', height: '85px' }}
        >
          <div 
            className="rounded-3 w-100 h-100 d-flex align-items-center justify-content-center text-white"
            style={{ backgroundColor: '#5C7E8F' }}
          >
             <i className="bi bi-briefcase-fill fs-2"></i>
          </div>
        </div>

        {/* Title and Meta Info */}
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <h3 className="fw-bold mb-1" style={{ color: '#3e5663' }}>{job.title}</h3>
            <p className="text-muted mb-4">
              <span className="fw-semibold" style={{ color: '#5C7E8F' }}>{job.company}</span> 
              <span className="mx-2">•</span> 
              {job.location}
            </p>
          </div>
          {/* Close Details Button for mobile/small views */}
          <button onClick={onClose} className="btn btn-link text-muted d-lg-none">
            <i className="bi bi-x-lg"></i>
          </button>
        </div>

        {/* Action Buttons */}
        <div className="d-flex flex-wrap gap-2 mb-4">
          <button 
            className="btn rounded-pill px-4 py-2 fw-bold shadow-sm"
            style={{ backgroundColor: '#5C7E8F', color: 'white', border: 'none' }}
          >
            Apply Now <i className="bi bi-box-arrow-up-right ms-1"></i>
          </button>

          <button 
            onClick={handleStartInterview}
            className="btn rounded-pill px-4 py-2 fw-bold shadow-sm"
            style={{ backgroundColor: '#5C7E8F', color: 'white', border: 'none' }}
          >
            Try Mock Interview <i className="bi bi-chat-dots ms-1"></i>
          </button>
          
          <button 
            className="btn btn-outline-secondary rounded-pill px-4"
            style={{ borderColor: '#D4DDE2', color: '#5C7E8F' }}
          >
            <i className="bi bi-bookmark me-1"></i> Save
          </button>
          
          <button 
            className="btn btn-outline-secondary rounded-circle"
            style={{ borderColor: '#D4DDE2', color: '#5C7E8F' }}
          >
            <i className="bi bi-share"></i>
          </button>
        </div>

        <hr className="my-4" style={{ opacity: '0.1' }} />

        {/* Job Content - Scrollable Area */}
        <div className="overflow-auto pe-2" style={{ maxHeight: 'calc(80vh - 300px)' }}>
          <h5 className="fw-bold mb-3" style={{ color: '#3e5663' }}>About the job</h5>
          <p className="text-secondary lh-lg">
            Looking for an experienced {job.title} to join our growing team. 
            You will be working with cutting-edge technologies to solve complex problems 
            and deliver high-quality software solutions.
          </p>
          
          <h5 className="fw-bold mt-4 mb-3" style={{ color: '#3e5663' }}>Responsibilities:</h5>
          <ul className="text-secondary ps-3 lh-lg">
            <li className="mb-2">Collaborate with cross-functional teams to define and ship new features.</li>
            <li className="mb-2">Maintain code quality, organization, and automation.</li>
            <li className="mb-2">Work on bug fixing and improving application performance.</li>
            <li className="mb-2">Discover and implement new technologies to maximize efficiency.</li>
          </ul>

          <h5 className="fw-bold mt-4 mb-3" style={{ color: '#3e5663' }}>Requirements:</h5>
          <div className="d-flex flex-wrap gap-2 mb-5">
            {['React', 'TypeScript', 'Node.js', 'Tailwind CSS'].map(skill => (
              <span 
                key={skill}
                className="badge rounded-pill px-3 py-2"
                style={{ backgroundColor: '#D4DDE2', color: '#5C7E8F', fontWeight: '600' }}
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetailView;