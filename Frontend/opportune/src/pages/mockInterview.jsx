import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const MockInterviewPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const job = location.state?.job;
  
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef(null);

  // Redirect if no job data
  useEffect(() => {
    if (!job) {
      navigate('/');
    } else {
      // Initial AI greeting
      setMessages([
        { 
          role: 'ai', 
          text: `Hello! I'm your AI interviewer for the ${job.title} position at ${job.company}. I've analyzed the job description. Whenever you're ready, tell me a bit about your background and why you're interested in this role.` 
        }
      ]);
    }
  }, [job, navigate]);

  // Auto-scroll to latest message
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI thinking and responding
    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, { 
        role: 'ai', 
        text: `That's a great start. Given the requirements for ${job.title}, can you walk me through a specific project where you used React or similar technologies to solve a complex problem?` 
      }]);
    }, 1500);
  };

  if (!job) return null;

  return (
  /* Main Container: Fixed at 100% screen height, no body scrolling */
  <div className="d-flex flex-column vh-100 bg-light" style={{ overflow: 'hidden' }}>
    
    {/* 1. Header: Stays at the top */}
    <nav className="navbar bg-white border-bottom px-4 flex-shrink-0 shadow-sm">
      <div className="container-fluid">
        <div>
          <span className="text-muted small">Interviewing for:</span>
          <h6 className="mb-0 fw-bold" style={{ color: '#3e5663' }}>{job?.title}</h6>
        </div>
        <button className="btn btn-sm btn-outline-danger rounded-pill px-3" onClick={() => navigate('/')}>
          End Interview
        </button>
      </div>
    </nav>

    {/* 2. Message Area: The only part that scrolls */}
    <div className="flex-grow-1 overflow-auto p-4" ref={scrollRef}>
      <div className="container" style={{ maxWidth: '850px' }}>
        {messages.map((msg, i) => (
          <div key={i} className={`d-flex mb-4 ${msg.role === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
            <div className="d-flex align-items-end" style={{ maxWidth: '80%' }}>
              {msg.role === 'ai' && (
                <div className="bg-dark text-white rounded-circle d-flex align-items-center justify-content-center me-2 mb-1" style={{ width: '30px', height: '30px', flexShrink: 0 }}>
                  <i className="bi bi-robot small"></i>
                </div>
              )}
              <div 
                className={`p-3 shadow-sm ${msg.role === 'user' ? 'rounded-4 rounded-bottom-end-0 text-white' : 'rounded-4 rounded-bottom-start-0 bg-white border'}`}
                style={{ backgroundColor: msg.role === 'user' ? '#5C7E8F' : '#fff' }}
              >
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="d-flex align-items-center text-muted small ms-5 italic">
            <span className="spinner-border spinner-border-sm me-2" role="status"></span>
            AI is thinking...
          </div>
        )}
      </div>
    </div>

    {/* 3. Input Box: Always stuck at the very bottom */}
    <div className="bg-white border-top p-3 flex-shrink-0 shadow-lg">
      <div className="container" style={{ maxWidth: '850px' }}>
        <form onSubmit={handleSendMessage} className="input-group input-group-lg border rounded-pill overflow-hidden bg-light">
          <input 
            type="text" 
            className="form-control border-0 bg-light px-4 py-3" 
            placeholder="Type your response..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isTyping}
            style={{ fontSize: '1rem', boxShadow: 'none' }}
          />
          <button 
            className="btn border-0 px-4" 
            style={{ backgroundColor: '#5C7E8F', color: 'white' }}
            type="submit"
          >
            <i className="bi bi-send-fill"></i>
          </button>
        </form>
      </div>
    </div>
  </div>
);
};

export default MockInterviewPage;