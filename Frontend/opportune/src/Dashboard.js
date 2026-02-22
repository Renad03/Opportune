// src/Dashboard.js
import React, { useState } from "react";
import "./App.css"; 

import RecommendedJobs from "./pages/recommendedJobs";
import RecommendedCourses from "./pages/recommendedCourses";
import InterviewPrep from "./pages/interviewPrep";
import ApplicationsTracking from "./pages/applicationsTracking";
import Profile from "./profile";


import { Navbar } from "./components/navbar";
import Footer from "./components/footer";

const Dashboard = () => {
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
      
      // 2. ADD THE CASE FOR PROFILE (This was missing)
      case "profile":
        return <Profile />;
        
      default:
        return <RecommendedJobs />;
    }
  };

  return (
    <div className="app">
      {/* Navbar */}
      <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />
      
      {/* Page Content */}
      {renderPage()}
      
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Dashboard;