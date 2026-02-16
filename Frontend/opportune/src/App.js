import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";

// Pages
import RecommendedJobs from "./pages/recommendedJobs";
import RecommendedCourses from "./pages/recommendedCourses";
import ApplicationsTracking from "./pages/applicationsTracking";
import Signup from "./pages/signup";
import LoginPage from "./pages/login";
import ForgotPassword from "./pages/forgotPassword";
import JobDetailsPage from "./pages/jobDetailsPage";
import MockInterview from "./pages/mockInterview";

// Components
import { Navbar } from "./components/navbar";
import Footer from "./components/footer";

const AppContent = () => {
  const location = useLocation();
  
  // Define routes where we DON'T want the Navbar and Footer (Auth pages)
  const authRoutes = ["/login", "/signup", "/forgot-password", "/logout"];
  const isAuthPage = authRoutes.includes(location.pathname);

  return (
    <div className="app">
      {/* 1. Global Styles (Bootstrap Injection) */}
      <style>{`
        @import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
        @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css');
        
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
          background-color: #F5F7FA;
          color: #102A43;
        }
        
        /* ... Keep all your existing CSS here ... */
      `}</style>

      {/* 2. Conditionally render Navbar */}
      {!isAuthPage && <Navbar />}

      {/* 3. Page Routes */}
      <Routes>
        <Route path="/" element={<RecommendedJobs />} />
        <Route path="/jobs" element={<RecommendedJobs />} />
        <Route path="/courses" element={<RecommendedCourses />} />
        <Route path="/applications" element={<ApplicationsTracking />} />
        <Route path="/job/:id" element={<JobDetailsPage />} /> 
        <Route path="/mock-interview" element={<MockInterview />} />
        
        {/* Auth Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/logout" element={<LoginPage />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />

        {/* Default Fallback */}
        <Route path="*" element={<RecommendedJobs />} />
      </Routes>

      {/* 4. Conditionally render Footer */}
      {!isAuthPage && <Footer />}
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;