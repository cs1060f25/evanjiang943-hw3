import React from 'react';

interface LoginPageProps {
  onLogin: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>AI-Assisted Grading Platform</h1>
          <p>Streamline your grading process with AI assistance</p>
        </div>
        
        <div className="login-options">
          <div className="login-card">
            <h2>Teaching Assistant</h2>
            <p>Grade student submissions with AI assistance</p>
            <button className="login-btn primary" onClick={onLogin}>
              Login as TA
            </button>
          </div>
          
          <div className="login-card disabled">
            <h2>Instructor</h2>
            <p>Manage courses and review TA work</p>
            <button className="login-btn secondary" disabled>
              Coming Soon
            </button>
          </div>
        </div>
        
        <div className="login-footer">
          <p>This is a prototype for demonstration purposes</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
