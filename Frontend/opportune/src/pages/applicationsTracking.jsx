import React, { useState } from "react";
import { HeroSection } from "../components/heroSection";

const ApplicationsTracking = () => {
  const [applications, setApplications] = useState([
    {
      id: 1,
      jobTitle: "Senior Frontend Developer",
      company: "TechCorp Inc.",
      date: "2024-01-15",
      status: "Interview",
    },
    {
      id: 2,
      jobTitle: "Full Stack Engineer",
      company: "StartupXYZ",
      date: "2024-01-10",
      status: "Applied",
    },
  ]);

  const [showForm, setShowForm] = useState(false);
  const [newApp, setNewApp] = useState({
    jobTitle: "",
    company: "",
    date: "",
    status: "Applied",
  });

  const statusClasses = {
    Applied: "status-applied",
    Interview: "status-interview",
    Offer: "status-offer",
    Rejected: "status-rejected",
  };

  const handleStatusChange = (id, newStatus) => {
    setApplications((apps) =>
      apps.map((app) => (app.id === id ? { ...app, status: newStatus } : app)),
    );
  };

  const handleAddApplication = () => {
    if (newApp.jobTitle && newApp.company && newApp.date) {
      const app = {
        ...newApp,
        id: Date.now(),
      };
      setApplications([app, ...applications]);
      setNewApp({ jobTitle: "", company: "", date: "", status: "Applied" });
      setShowForm(false);
    }
  };

  const handleDelete = (id) => {
    setApplications((apps) => apps.filter((app) => app.id !== id));
  };

  return (
    <>
      <HeroSection
        title="Track Your Applications"
        subtitle="Stay organized and never miss a follow-up"
      />

      <div className="container my-5">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2 className="mb-0">My Applications</h2>
          <button
            className="btn btn-navy"
            onClick={() => setShowForm(!showForm)}
          >
            <i className="bi bi-plus-circle me-1"></i> Add Application
          </button>
        </div>

        {showForm && (
          <div className="card shadow-sm mb-4">
            <div className="card-body">
              <h5 className="card-title mb-3">Add New Application</h5>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label">Job Title</label>
                  <input
                    type="text"
                    className="form-control"
                    value={newApp.jobTitle}
                    onChange={(e) =>
                      setNewApp({ ...newApp, jobTitle: e.target.value })
                    }
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Company</label>
                  <input
                    type="text"
                    className="form-control"
                    value={newApp.company}
                    onChange={(e) =>
                      setNewApp({ ...newApp, company: e.target.value })
                    }
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Application Date</label>
                  <input
                    type="date"
                    className="form-control"
                    value={newApp.date}
                    onChange={(e) =>
                      setNewApp({ ...newApp, date: e.target.value })
                    }
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Status</label>
                  <select
                    className="form-select"
                    value={newApp.status}
                    onChange={(e) =>
                      setNewApp({ ...newApp, status: e.target.value })
                    }
                  >
                    <option value="Applied">Applied</option>
                    <option value="Interview">Interview</option>
                    <option value="Offer">Offer</option>
                    <option value="Rejected">Rejected</option>
                  </select>
                </div>
                <div className="col-12">
                  <button
                    className="btn btn-navy me-2"
                    onClick={handleAddApplication}
                  >
                    Save
                  </button>
                  <button
                    className="btn btn-outline-secondary"
                    onClick={() => setShowForm(false)}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="row g-3">
          {applications.map((app) => (
            <div key={app.id} className="col-12">
              <div className="card border-0 shadow-sm">
                <div className="card-body">
                  <div className="row align-items-center">
                    <div className="col-md-4">
                      <h5 className="mb-1">{app.jobTitle}</h5>
                      <p className="text-muted mb-0">
                        <i className="bi bi-building me-1"></i>
                        {app.company}
                      </p>
                    </div>
                    <div className="col-md-3">
                      <small className="text-muted">Applied on</small>
                      <p className="mb-0">
                        {new Date(app.date).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="col-md-3">
                      <small className="text-muted d-block mb-1">Status</small>
                      <select
                        className={`form-select form-select-sm status-select ${statusClasses[app.status]}`}
                        value={app.status}
                        onChange={(e) =>
                          handleStatusChange(app.id, e.target.value)
                        }
                      >
                        <option value="Applied">Applied</option>
                        <option value="Interview">Interview</option>
                        <option value="Offer">Offer</option>
                        <option value="Rejected">Rejected</option>
                      </select>
                    </div>
                    <div className="col-md-2 text-end">
                      <button
                        className="btn btn-sm btn-outline-delete"
                        onClick={() => handleDelete(app.id)}
                      >
                        <i className="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};
export default ApplicationsTracking;
