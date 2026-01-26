import "./App.css";
import React, { useState } from "react";
import RecommendedJobs from "./pages/recommendedJobs";
import RecommendedCourses from "./pages/recommendedCourses";
import InterviewPrep from "./pages/interviewPrep";
import ApplicationsTracking from "./pages/applicationsTracking";
import { Navbar } from "./components/navbar";
import Footer from "./components/footer";

const App = () => {
  const [currentPage, setCurrentPage] = useState("jobs");

  const renderPage = () => {
    switch (currentPage) {
      case "jobs":
        return <RecommendedJobs />;
      case "courses":
        return <RecommendedCourses />;
      case "interview":
        return <InterviewPrep />;
      case "applications":
        return <ApplicationsTracking />;
      default:
        return <RecommendedJobs />;
    }
  };

  return (
    <div className="app">
      <style>{`
  @import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
  @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css');

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #F5F7FA;
    color: #102A43;
  }

  /* Hero Section */
 /* Hero gradient (Option 2) */
.hero-section {
  background: linear-gradient(to right, #0B1C2D, #102A43);
  min-height: 320px;
  display: flex;
  align-items: center;
}

/* Hero subtitle */
.text-white-75 {
  color: rgba(255, 255, 255, 0.75);
}

/* Hero inputs */
.hero-input {
  border: none;
  background-color: #F5F7FA;
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
}

.hero-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(11, 28, 45, 0.15);
  background-color: #ffffff;
}



  /* Search Bar */
  .search-bar {
    max-width: 900px;
    margin: 0 auto;
  }

  /* Cards */
  .card {
    border-radius: 14px;
    border: none;
    background-color: #ffffff;
  }

  .hover-card {
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }

  .hover-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 1rem 2rem rgba(11, 28, 45, 0.15) !important;
  }

  /* Buttons */
  .btn {
    border-radius: 10px;
    font-weight: 500;
  }

  .btn-primary {
    background-color: #0B1C2D;
    border-color: #0B1C2D;
  }

  .btn-primary:hover {
    background-color: #102A43;
    border-color: #102A43;
  }

  .btn-outline-primary {
    color: #0B1C2D;
    border-color: #0B1C2D;
  }

  .btn-outline-primary:hover {
    background-color: #0B1C2D;
    color: #ffffff;
  }

  /* Badges */
  .badge {
    padding: 0.45em 0.85em;
    border-radius: 8px;
    font-weight: 500;
    background-color: #E6EDF5;
    color: #0B1C2D;
  }

  /* Navbar */
  .navbar {
    background-color: #ffffff;
    border-bottom: 1px solid #E5E7EB;
  }

  .navbar-brand {
    font-weight: 700;
    color: #0B1C2D !important;
    cursor: pointer;
  }

  .nav-link {
    font-weight: 500;
    color: #6B7280;
    transition: color 0.2s ease;
    cursor: pointer;
  }

  .nav-link:hover,
  .nav-link.active {
    color: #0B1C2D;
  }

  /* Footer */
  footer {
    background-color: #0B1C2D;
    color: #CBD5E1;
  }

  /* ===== Navy Palette ===== */
:root {
  --navy-900: #0B1C2D;
  --navy-800: #102A43;
  --navy-700: #1E3A5F;
  --navy-100: #E6EDF5;
  --navy-muted: #6B7280;
}

/* Badges */
.badge-navy {
  background-color: var(--navy-100);
  color: var(--navy-900);
}

/* Difficulty badges */
.badge-beginner {
  background-color: #E6EDF5;
  color: #0B1C2D;
}

.badge-intermediate {
  background-color: #DBEAFE;
  color: #1E3A5F;
}

.badge-advanced {
  background-color: #E0E7FF;
  color: #312E81;
}

/* Buttons */
.btn-navy {
  background-color: var(--navy-900);
  border-color: var(--navy-900);
  color: #fff;
}

.btn-navy:hover {
  background-color: var(--navy-800);
  border-color: var(--navy-800);
  color: #fff;
}

.btn-outline-navy {
  color: var(--navy-900);
  border-color: var(--navy-900);
}

.btn-outline-navy:hover {
  background-color: var(--navy-900);
  color: #fff;
}

/* Muted text override */
.text-muted {
  color: var(--navy-muted) !important;
}

/* ===== Application Status (Navy System) ===== */
.status-applied {
  background-color: #E6EDF5;
  color: #0B1C2D;
}

.status-interview {
  background-color: #DBEAFE;
  color: #1E3A5F;
}

.status-offer {
  background-color: #DCFCE7;
  color: #065F46;
}

.status-rejected {
  background-color: #FEE2E2;
  color: #7F1D1D;
}

/* Small select styling */
.status-select {
  border: none;
  border-radius: 8px;
  font-weight: 500;
}

/* Danger delete (soft) */
.btn-outline-delete {
  border-color: #CBD5E1;
  color: #64748B;
}

.btn-outline-delete:hover {
  background-color: #FEE2E2;
  color: #7F1D1D;
  border-color: #FCA5A5;
}


`}</style>

      <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />
      {renderPage()}
      <Footer />
    </div>
  );
};

export default App;
