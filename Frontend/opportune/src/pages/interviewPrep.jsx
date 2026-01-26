import React, { useState } from 'react';
import { interviewQuestions } from '../data/mockJobs';
import { HeroSection } from '../components/heroSection';
const InterviewPrep = () => {
  const [practiced, setPracticed] = useState({});
  const [expanded, setExpanded] = useState({});
  
  const togglePracticed = (category, index) => {
    const key = `${category}-${index}`;
    setPracticed(prev => ({...prev, [key]: !prev[key]}));
  };
  
  const toggleExpanded = (category, index) => {
    const key = `${category}-${index}`;
    setExpanded(prev => ({...prev, [key]: !prev[key]}));
  };
  
  const QuestionSection = ({ title, questions, category }) => (
    <div className="mb-4">
      <h4 className="mb-3">{title}</h4>
      <div>
        {questions.map((question, idx) => {
          const key = `${category}-${idx}`;
          const isExpanded = expanded[key];
          
          return (
            <div key={idx} className="card border-0 shadow-sm mb-2">
              <div className="card-header bg-white border-0">
                <button 
                  className="btn btn-link text-decoration-none text-dark w-100 text-start p-0 d-flex align-items-center justify-content-between"
                  onClick={() => toggleExpanded(category, idx)}
                >
                  <span>{question}</span>
                  <div className="d-flex align-items-center gap-2">
                    {practiced[key] && (
                      <i className="bi bi-check-circle-fill text-success"></i>
                    )}
                    <i className={`bi bi-chevron-${isExpanded ? 'up' : 'down'}`}></i>
                  </div>
                </button>
              </div>
              {isExpanded && (
                <div className="card-body pt-0">
                  <p className="text-muted mb-3">Practice your answer here and prepare talking points.</p>
                  <button 
                    className={`btn btn-sm ${practiced[key] ? 'btn-success' : 'btn-outline-success'}`}
                    onClick={() => togglePracticed(category, idx)}
                  >
                    <i className={`bi ${practiced[key] ? 'bi-check-circle-fill' : 'bi-circle'} me-1`}></i>
                    {practiced[key] ? 'Practiced' : 'Mark as Practiced'}
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
  
  return (
    <>
      <HeroSection 
        title="Ace Your Interviews"
        subtitle="Practice common questions and build confidence"
      />
      
      <div className="container my-5">
        <QuestionSection title="Technical Questions" questions={interviewQuestions.technical} category="technical" />
        <QuestionSection title="Behavioral Questions" questions={interviewQuestions.behavioral} category="behavioral" />
        <QuestionSection title="Common Questions" questions={interviewQuestions.common} category="common" />
      </div>
    </>
  );
};
export default InterviewPrep;