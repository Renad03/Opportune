export const CourseCard = ({ course }) => {
  const getDifficultyClass = (difficulty) => {
    switch (difficulty) {
      case 'Beginner': return 'badge-beginner';
      case 'Intermediate': return 'badge-intermediate';
      case 'Advanced': return 'badge-advanced';
      default: return 'badge-navy';
    }
  };

  return (
    <div className="card border-0 shadow-sm h-100 hover-card">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <h5 className="card-title text-navy">{course.title}</h5>
          <span className={`badge ${getDifficultyClass(course.difficulty)}`}>
            {course.difficulty}
          </span>
        </div>

        <p className="text-muted mb-2">
          <i className="bi bi-award me-1"></i>
          <strong>Skill:</strong> {course.skill}
        </p>

        <p className="text-muted mb-2">
          <i className="bi bi-laptop me-1"></i>
          <strong>Platform:</strong> {course.platform}
        </p>

        <p className="text-muted mb-3">
          <i className="bi bi-clock me-1"></i>
          <strong>Duration:</strong> {course.duration}
        </p>

        <div className="d-flex justify-content-between align-items-center">
          <div>
            <i className="bi bi-star-fill text-warning me-1"></i>
            <span className="fw-bold">{course.rating}</span>
          </div>
          <button className="btn btn-navy btn-sm">
            <i className="bi bi-box-arrow-up-right me-1"></i> Enroll
          </button>
        </div>
      </div>
    </div>
  );
};
