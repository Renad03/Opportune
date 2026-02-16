// components/heroSection.js
export const HeroSection = ({ title, subtitle }) => {
  return (
    <div className="py-5 text-center text-white shadow-sm" 
         style={{ background: 'linear-gradient(135deg, #c1d5e0 0%, #3e5663 100%)', minHeight: '300px', display: 'flex', alignItems: 'center' }}>
      <div className="container">
        <h1 className="display-4 fw-bold mb-3 text-uppercase tracking-widest">{title}</h1>
        <p className="lead opacity-75 mx-auto" style={{ maxWidth: '700px', color: '#D4DDE2' }}>
          {subtitle}
        </p>
        
        {/* Themed Search Bar Container */}
        <div className="mt-4 p-2 rounded-pill bg-white shadow-lg mx-auto d-flex align-items-center" style={{ maxWidth: '800px' }}>
            <div className="input-group border-0">
                <span className="input-group-text bg-transparent border-0"><i className="bi bi-search text-muted"></i></span>
                <input type="text" className="form-control border-0 shadow-none" placeholder="Skills (e.g., React, Python)" />
                <button className="btn rounded-pill px-4 ms-2 fw-bold" style={{ backgroundColor: '#5C7E8F', color: 'white' }}>
                    Search
                </button>
            </div>
        </div>
      </div>
    </div>
  );
};