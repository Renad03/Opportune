import React, { useState } from 'react';
import './App.css'; 

function MultiStepSignup() {
  // 1. Track which step the user is on (Starts at 1)
  const [step, setStep] = useState(1);

  // 2. Hold ALL the data matching your Spring Boot DTO
  const [formData, setFormData] = useState({
    username: '',
    name: '',
    email: '',
    password: '',
    role: 'JOBSEEKER', // Default role
    profilePicLink: '',
    location: '',
    cvLink: '',
    // Arrays for your complex DTO types
    workExperiences: [], 
    skills: [] 
  });

  // 3. Navigation functions
  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  // 4. Standard input handler
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 5. Final submission to your backend
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Sending this to Spring Boot:', formData);
    // Add your fetch/axios POST request here
  };

  // 6. Conditional Rendering: Show different inputs based on the 'step' state
  return (
    <div className="wizard-container">
      <h2>Create Account - Step {step} of 3</h2>
      
      <form onSubmit={handleSubmit}>
        
        {/* --- STEP 1: ACCOUNT --- */}
        {step === 1 && (
          <div className="form-group">
            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="JOBSEEKER">Job Seeker</option>
              <option value="RECRUITER">Recruiter</option>
            </select>
            <input name="username" placeholder="Username" onChange={handleChange} value={formData.username} />
            <input type="email" name="email" placeholder="Email" onChange={handleChange} value={formData.email} />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} value={formData.password} />
          </div>
        )}

        {/* --- STEP 2: PROFILE --- */}
        {step === 2 && (
          <div className="form-group">
            <input name="name" placeholder="Full Name" onChange={handleChange} value={formData.name} />
            <input name="location" placeholder="City, Country" onChange={handleChange} value={formData.location} />
            <input name="profilePicLink" placeholder="Profile Picture URL" onChange={handleChange} value={formData.profilePicLink} />
          </div>
        )}

        {/* --- STEP 3: PROFESSIONAL --- */}
        {step === 3 && (
          <div className="form-group">
            <input name="cvLink" placeholder="Link to CV/Resume" onChange={handleChange} value={formData.cvLink} />
            {/* Note: Skills and Work Experience require special handling since they are arrays */}
            <p className="note">Add Skills and Experience components here.</p>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="button-group">
          {step > 1 && <button type="button" onClick={prevStep}>Back</button>}
          {step < 3 && <button type="button" onClick={nextStep}>Next</button>}
          {step === 3 && <button type="submit">Complete Signup</button>}
        </div>

      </form>
    </div>
  );
}

export default MultiStepSignup;