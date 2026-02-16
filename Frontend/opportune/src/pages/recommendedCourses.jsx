import React from 'react';
import { mockCourses } from '../data/mockJobs';
import { CourseCard } from '../components/courseCard';
import { HeroSection } from '../components/heroSection';

const RecommendedCourses = () => {
  return (
    <>
      <style>{`
        .section-title {
          color: #5C7E8F;
          font-weight: 700;
          position: relative;
          padding-bottom: 10px;
        }
        .section-title::after {
          content: "";
          position: absolute;
          left: 0;
          bottom: 0;
          width: 50px;
          height: 3px;
          background-color: #5C7E8F;
          border-radius: 2px;
        }
        .item-count {
          background-color: #D4DDE2;
          color: #5C7E8F;
          padding: 4px 12px;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
        }
      `}</style>

      <HeroSection 
        title="Boost Your Skills"
        subtitle="Personalized course recommendations to advance your career"
      />
      
      <div className="container my-5">
        <div className="d-flex justify-content-between align-items-end mb-5">
          <div>
            <h2 className="mb-1 section-title text-uppercase tracking-wider">Recommended Courses</h2>
            <p className="text-muted mb-0">Based on skills gaps in your target roles</p>
          </div>
          <span className="item-count">{mockCourses.length} courses available</span>
        </div>
        
        {/* Added justify-content-center to keep the grid balanced */}
        <div className="row g-4 justify-content-center">
          {mockCourses.map(course => (
            <div key={course.id} className="col-md-6 col-lg-4 col-xl-3">
              <CourseCard course={course} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default RecommendedCourses;