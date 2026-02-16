// import React from 'react';
// import { mockJobs } from '../data/mockJobs';
// import JobCard from '../components/jobCard';
// import { HeroSection } from '../components/heroSection';

// const RecommendedJobs = () => {
//   return (
//     <>
//       <style>{`
//         .section-title {
//           color: #5C7E8F;
//           font-weight: 700;
//           position: relative;
//           padding-bottom: 10px;
//         }
//         .section-title::after {
//           content: "";
//           position: absolute;
//           left: 0;
//           bottom: 0;
//           width: 50px;
//           height: 3px;
//           background-color: #5C7E8F;
//           border-radius: 2px;
//         }
//         .job-count {
//           background-color: #D4DDE2;
//           color: #5C7E8F;
//           padding: 4px 12px;
//           border-radius: 20px;
//           font-size: 0.85rem;
//           font-weight: 600;
//         }
//       `}</style>

//       <HeroSection 
//         title="Find Your Perfect Job Match"
//         subtitle="AI-powered recommendations tailored to your skills and experience"
//       />
      
//       <div className="container my-5">
//         <div className="d-flex justify-content-between align-items-center mb-5">
//           <h2 className="mb-0 section-title text-uppercase tracking-wider">Recommended for You</h2>
//           <span className="job-count">{mockJobs.length} jobs found</span>
//         </div>
        
//         <div className="row g-4">
//           {mockJobs.map(job => (
//             <div key={job.id} className="col-md-6 col-lg-6">
//               <JobCard job={job} />
//             </div>
//           ))}
//         </div>
//       </div>
//     </>
//   );
// };

// export default RecommendedJobs;
import React, { useState } from 'react';
import { mockJobs } from '../data/mockJobs';
import JobCard from '../components/jobCard';
import { HeroSection } from '../components/heroSection';
import JobDetailView from '../components/jobDetailView'; // The right side panel

const RecommendedJobs = () => {
  const [selectedJob, setSelectedJob] = useState(null);

  return (
    <>
      {/* Show Hero only when no job is selected to save space */}
      {!selectedJob && (
        <HeroSection 
          title="Find Your Perfect Job Match"
          subtitle="AI-powered recommendations tailored to your skills and experience"
        />
      )}
      
      <div className="container my-5 px-4">
        <div className="row g-4">
          
          {/* LEFT SIDE: The Job List */}
          <div className={selectedJob ? "col-lg-4 overflow-auto" : "col-12"} 
               style={selectedJob ? { maxHeight: '80vh' } : {}}>
            
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2 className="h4 mb-0 fw-bold" style={{ color: '#5C7E8F' }}>
                {selectedJob ? "Jobs" : "Recommended for You"}
              </h2>
              <span className="badge rounded-pill" style={{ backgroundColor: '#D4DDE2', color: '#5C7E8F' }}>
                {mockJobs.length} found
              </span>
            </div>

            <div className={selectedJob ? "d-flex flex-column gap-3" : "row g-4"}>
              {mockJobs.map(job => (
                <div key={job.id} className={selectedJob ? "w-100" : "col-md-6 col-lg-6"}>
                  <JobCard 
                    job={job} 
                    isActive={selectedJob?.id === job.id}
                    // Pass the click handler to the button
                    onViewDetails={() => setSelectedJob(job)} 
                  />
                </div>
              ))}
            </div>
          </div>

          {/* RIGHT SIDE: The Details Panel */}
          {selectedJob && (
            <div className="col-lg-8 sticky-top" style={{ top: '100px', height: '80vh' }}>
              {/* Back button to close details and return to full grid */}
              <button 
                className="btn btn-sm mb-3 text-secondary"
                onClick={() => setSelectedJob(null)}
              >
                <i className="bi bi-x-lg me-2"></i> Close Details
              </button>
              
              <JobDetailView job={selectedJob} />
            </div>
          )}

        </div>
      </div>
    </>
  );
};

export default RecommendedJobs;