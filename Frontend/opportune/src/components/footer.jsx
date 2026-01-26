const Footer = () => {
  return (
    <footer className="bg-dark text-white py-4 mt-5">
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <h5 className="mb-3">
              <i className="bi bi-briefcase-fill me-2"></i>
              Opportune
            </h5>
            <p className="text-white-50">Your AI-powered career companion for job search, skill development, and interview preparation.</p>
          </div>
          <div className="col-md-3">
            <h6 className="mb-3">Quick Links</h6>
            <ul className="list-unstyled">
              <li className="mb-2 text-white-50">Jobs</li>
              <li className="mb-2 text-white-50">Courses</li>
              <li className="mb-2 text-white-50">Interview Prep</li>
              <li className="mb-2 text-white-50">Applications</li>
            </ul>
          </div>
          <div className="col-md-3">
            <h6 className="mb-3">Connect</h6>
            <div className="d-flex gap-3">
              <i className="bi bi-linkedin fs-4"></i>
              <i className="bi bi-twitter fs-4"></i>
              <i className="bi bi-github fs-4"></i>
            </div>
          </div>
        </div>
        <hr className="my-4 bg-white-50" />
        <p className="text-center text-white-50 mb-0">&copy; 2024 Opportune. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;