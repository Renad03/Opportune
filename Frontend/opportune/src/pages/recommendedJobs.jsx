import React from 'react';
import {mockJobs} from '../data/mockJobs';
import  JobCard  from '../components/jobCard';
import { HeroSection } from '../components/heroSection';
const RecommendedJobs = () => {
  return (
    <>
      <HeroSection 
        title="Find Your Perfect Job Match"
        subtitle="AI-powered recommendations tailored to your skills and experience"
      />
      
      <div className="container my-5">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2 className="mb-0">Recommended for You</h2>
          <span className="text-muted">{mockJobs.length} jobs found</span>
        </div>
        
        <div className="row g-4">
          {mockJobs.map(job => (
            <div key={job.id} className="col-md-6 col-lg-6">
              <JobCard job={job} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default RecommendedJobs;