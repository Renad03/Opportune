import React from 'react';

export const CourseCard = ({ course }) => {
  return (
    <div className="card h-100 border-0 shadow-sm" style={{ borderRadius: '15px', overflow: 'hidden', transition: 'transform 0.2s' }}>
      {/* Course Image */}
      <div style={{ height: '160px', overflow: 'hidden' }}>
        <img 
          src={course.image || 'https://via.placeholder.com/300x160'} 
          className="card-img-top" 
          alt={course.title}
          style={{ objectFit: 'cover', height: '100%', width: '100%' }}
        />
      </div>

      <div className="card-body d-flex flex-column">
        {/* Category/Platform Tag */}
        <div className="mb-2">
          <span className="badge" style={{ backgroundColor: '#D4DDE2', color: '#5C7E8F', fontSize: '0.75rem' }}>
            {course.platform || 'E-Learning'}
          </span>
        </div>

        {/* Course Title */}
        <h5 className="card-title fw-bold mb-2" style={{ color: '#334E5C', fontSize: '1.1rem' }}>
          {course.title}
        </h5>

        {/* Instructor/Source */}
        <p className="card-text text-muted small mb-3">
          <i className="bi bi-person me-1"></i> {course.instructor || 'Instructor Name'}
        </p>

        {/* Course Stats (Duration/Level) */}
        <div className="d-flex justify-content-between align-items-center mt-auto mb-3">
          <span className="small text-secondary">
            <i className="bi bi-clock me-1"></i> {course.duration}
          </span>
          <span className="small fw-bold" style={{ color: '#5C7E8F' }}>
            {course.level}
          </span>
        </div>

        {/* Action Button */}
        <a 
          href={course.link} 
          target="_blank" 
          rel="noopener noreferrer"
          className="btn w-100 fw-bold"
          style={{ 
            backgroundColor: '#5C7E8F', 
            color: 'white', 
            borderRadius: '10px',
            border: 'none'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#4A6675'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#5C7E8F'}
        >
          View Course <i className="bi bi-arrow-up-right-square ms-2"></i>
        </a>
      </div>
    </div>
  );
};