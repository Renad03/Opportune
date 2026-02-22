// src/pages/profile.jsx
import React from 'react';
import { BiMap, BiCalendar, BiLink, BiBriefcase, BiDownload, BiEnvelope } from "react-icons/bi"; 

const Profile = () => {
  const user = {
    name: "Ahmed Mohamed",
    handle: "@ahmed_dev",
    role: "Senior Frontend Developer",
    location: "Cairo, Egypt",
    joined: "Joined January 2024",
    website: "github.com/ahmed",
    following: 142,
    followers: 1250,
    about: "Passionate Frontend Developer with 5+ years of experience building responsive, user-friendly web applications using React and Tailwind CSS. Dedicated to optimizing performance and ensuring accessibility. Currently looking for new opportunities in Fintech or EdTech.",
    skills: ["React.js", "TypeScript", "Next.js", "Redux", "Node.js", "Tailwind CSS", "Figma", "Git"],
    experience: [
      { role: "Frontend Team Lead", company: "Tech Solutions", year: "2021 - Present" },
      { role: "Junior Web Developer", company: "Creative Agency", year: "2019 - 2021" }
    ]
  };

  return (
    <div className="profile-container">
      {/* 1. Full Width Cover */}
      <div className="cover-photo"></div>
      
      {/* 2. Wrapper to center content (Max Width 1200px) */}
      <div className="profile-content-wrapper">
        
        {/* Navigation & Avatar */}
        <div className="profile-nav">
          <div className="profile-pic-container">
            <img 
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" 
              alt="Profile" 
              className="profile-pic"
            />
          </div>
          
          <div className="action-btns d-flex gap-3">
             <button className="btn btn-outline-dark rounded-pill fw-bold px-4">
                <BiDownload className="me-2"/> Resume
             </button>
             <button className="btn btn-dark rounded-pill fw-bold px-4" style={{backgroundColor: '#0B1C2D'}}>
                <BiEnvelope className="me-2"/> Message
             </button>
          </div>
        </div>

        {/* Basic Info */}
        <div className="profile-info">
          <h2 className="fw-bold mb-1 text-dark">{user.name}</h2>
          <p className="text-muted mb-2 fs-5">{user.handle}</p>
          <p className="text-primary fw-bold fs-5 mb-3">{user.role}</p>

          <div className="profile-meta d-flex flex-wrap text-muted my-3">
            <span><BiMap /> {user.location}</span>
            <span><BiLink /> <a href="#">{user.website}</a></span>
            <span><BiCalendar /> {user.joined}</span>
          </div>

          <div className="follow-stats d-flex gap-4 border-bottom pb-4 mb-4">
            <span><span className="fw-bold text-dark">{user.following}</span> <span className="text-muted">Following</span></span>
            <span><span className="fw-bold text-dark">{user.followers}</span> <span className="text-muted">Followers</span></span>
          </div>
        </div>

        {/* 3. Main Content Sections (Grid Layout) */}
        <div className="profile-section-card">
            
            {/* Open to Work Badge */}
            <div className="alert alert-light border d-flex align-items-center mb-5 shadow-sm p-4" role="alert">
                <BiBriefcase className="fs-3 me-3 text-success"/>
                <div>
                    <h5 className="mb-1 fw-bold">Open to Work</h5>
                    <div className="text-muted">Actively looking for Full-time roles.</div>
                </div>
            </div>

            <div className="row">
                {/* Left Column: About & Skills */}
                <div className="col-md-7 pe-md-5">
                    <div className="mb-5">
                        <h4 className="fw-bold mb-3">About</h4>
                        <p className="text-secondary fs-5" style={{lineHeight: '1.8'}}>
                            {user.about}
                        </p>
                    </div>

                    <div className="mb-5">
                        <h4 className="fw-bold mb-3">Skills</h4>
                        <div className="d-flex flex-wrap gap-2">
                            {user.skills.map((skill, index) => (
                                <span key={index} className="badge bg-light text-dark border p-2 fs-6">
                                    {skill}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Column: Experience */}
                <div className="col-md-5">
                    <h4 className="fw-bold mb-3">Experience</h4>
                    {user.experience.map((exp, index) => (
                        <div key={index} className="d-flex align-items-start mb-4 p-3 border rounded hover-bg-light">
                            <div className="bg-light p-3 rounded me-3 text-secondary">
                                <BiBriefcase size={28} />
                            </div>
                            <div>
                                <h5 className="fw-bold mb-1">{exp.role}</h5>
                                <div className="text-dark fw-medium">{exp.company}</div>
                                <div className="text-muted small mt-1">{exp.year}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

        </div>
      </div>
    </div>
  );
};

export default Profile;