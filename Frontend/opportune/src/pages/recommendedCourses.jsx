import React from 'react';
import {mockCourses} from '../data/mockJobs';
import { CourseCard } from '../components/courseCard';
import { HeroSection } from '../components/heroSection';
const RecommendedCourses = () => {
  return (
    <>
      <HeroSection 
        title="Boost Your Skills"
        subtitle="Personalized course recommendations to advance your career"
      />
      
      <div className="container my-5">
        <div className="mb-4">
          <h2 className="mb-2">Recommended Courses</h2>
          <p className="text-muted">Based on skills gaps in your target roles</p>
        </div>
        
        <div className="row g-4">
          {mockCourses.map(course => (
            <div key={course.id} className="col-md-6 col-lg-3">
              <CourseCard course={course} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};
export default RecommendedCourses;