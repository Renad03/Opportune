export const HeroSection = ({ title, subtitle }) => {
  return (
    <div className="hero-section py-5">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-lg-8 mx-auto text-center text-white">
            <h1 className="display-4 fw-bold mb-3">{title}</h1>
            <p className="lead mb-4 text-white-75">{subtitle}</p>

            <div className="search-bar bg-white rounded-3 shadow p-2">
              <div className="row g-2 align-items-center">
                <div className="col-md-4">
                  <input
                    type="text"
                    className="form-control hero-input"
                    placeholder="Skills (e.g., React, Python)"
                  />
                </div>
                <div className="col-md-3">
                  <input
                    type="text"
                    className="form-control hero-input"
                    placeholder="Experience"
                  />
                </div>
                <div className="col-md-3">
                  <input
                    type="text"
                    className="form-control hero-input"
                    placeholder="Location"
                  />
                </div>
                <div className="col-md-2">
                  <button className="btn btn-navy w-100">
                    <i className="bi bi-search me-1"></i> Search
                  </button>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};
