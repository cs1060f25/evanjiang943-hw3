import React from 'react';

interface TADashboardProps {
  onUpload: () => void;
}

const TADashboard: React.FC<TADashboardProps> = ({ onUpload }) => {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>TA Dashboard</h1>
        <div className="user-info">
          <span>Welcome, Teaching Assistant</span>
        </div>
      </div>
      
      <div className="dashboard-content">
        <div className="dashboard-card">
          <h2>Grade New Submission</h2>
          <p>Upload a student's homework file to begin AI-assisted grading</p>
          <button className="action-btn primary" onClick={onUpload}>
            Upload Submission
          </button>
        </div>
        
        <div className="dashboard-card">
          <h2>Recent Grading Activity</h2>
          <div className="activity-list">
            <div className="activity-item">
              <span className="filename">math_homework_1.pdf</span>
              <span className="status completed">Completed</span>
              <span className="score">18/25 (72%)</span>
            </div>
            <div className="activity-item">
              <span className="filename">essay_draft_2.pdf</span>
              <span className="status completed">Completed</span>
              <span className="score">32/40 (80%)</span>
            </div>
            <div className="activity-item">
              <span className="filename">problem_set_3.pdf</span>
              <span className="status pending">Pending Review</span>
              <span className="score">-</span>
            </div>
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Quick Stats</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-number">15</span>
              <span className="stat-label">Submissions Graded</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">3.2</span>
              <span className="stat-label">Avg. Time (min)</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">78%</span>
              <span className="stat-label">Avg. Score</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TADashboard;
