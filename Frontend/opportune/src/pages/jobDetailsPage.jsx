import React, { useState } from 'react';
import { mockJobs } from '../data/mockJobs';
import JobDetailView from '../components/jobDetailView';
import JobSidebarItem from '../components/jobSidebarItem';
const RecommendedJobs = () => {
  const [activeJob, setActiveJob] = useState(mockJobs[0]); // Default to first job

  return (
    <div className="min-vh-100 bg-light">
      {/* Simplified Page Header */}
      <div className="container py-4">
        <div className="mb-4">
          <h2 className="fw-bold" style={{ color: '#0B1C2D' }}>Job Details</h2>
          <p className="text-muted small">Viewing job details</p>
        </div>

        <div className="row g-4" style={{ height: 'calc(100vh - 200px)' }}>
          {/* Left Sidebar: List of Jobs */}
          <div className="col-lg-4 col-md-5 h-100 overflow-auto pe-3">
            {mockJobs.map(job => (
              <JobSidebarItem 
                key={job.id} 
                job={job} 
                isActive={activeJob?.id === job.id}
                onClick={() => setActiveJob(job)}
              />
            ))}
          </div>

          {/* Right Panel: Job Details */}
          <div className="col-lg-8 col-md-7 h-100">
            <JobDetailView job={activeJob} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendedJobs;