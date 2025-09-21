import React, { useState, useEffect } from 'react';

interface Submission {
  id: string;
  student_name: string;
  student_id: string;
  filename: string;
  assignment_type: string;
  submitted_at: string;
  status: 'pending_grading' | 'graded' | 'released';
  total_score?: number;
  max_total?: number;
  percentage?: number;
  graded_at?: string;
  released_at?: string;
}

interface TADashboardProps {
  onGradeSubmission: (submission: Submission) => void;
}

const TADashboard: React.FC<TADashboardProps> = ({ onGradeSubmission }) => {
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const fetchSubmissions = async () => {
    try {
      const response = await fetch('/api/submissions');
      if (response.ok) {
        const data = await response.json();
        setSubmissions(data);
      } else {
        // Fallback to mock data if backend is not available
        setSubmissions([
          {
            id: 'sub_001',
            student_name: 'Alice Johnson',
            student_id: 'AJ2024',
            filename: 'calculus_hw1_alice.pdf',
            assignment_type: 'calculus_homework',
            submitted_at: '2024-01-15T14:30:00Z',
            status: 'pending_grading'
          },
          {
            id: 'sub_002',
            student_name: 'Bob Smith',
            student_id: 'BS2024',
            filename: 'calculus_hw1_bob.pdf',
            assignment_type: 'calculus_homework',
            submitted_at: '2024-01-15T16:45:00Z',
            status: 'pending_grading'
          },
          {
            id: 'sub_003',
            student_name: 'Carol Davis',
            student_id: 'CD2024',
            filename: 'calculus_hw1_carol.pdf',
            assignment_type: 'calculus_homework',
            submitted_at: '2024-01-16T09:15:00Z',
            status: 'pending_grading'
          },
          {
            id: 'sub_004',
            student_name: 'David Wilson',
            student_id: 'DW2024',
            filename: 'calculus_hw1_david.pdf',
            assignment_type: 'calculus_homework',
            submitted_at: '2024-01-16T11:30:00Z',
            status: 'graded',
            total_score: 70,
            max_total: 70,
            percentage: 100.0,
            graded_at: '2024-01-16T14:20:00Z'
          }
        ]);
      }
    } catch (error) {
      console.error('Error fetching submissions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGradeSubmission = async (submission: Submission) => {
    try {
      const response = await fetch(`/api/submissions/${submission.id}/grade`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const data = await response.json();
        onGradeSubmission(data.grading_result);
      } else {
        // Fallback to mock grading
        onGradeSubmission({
          submission_id: submission.id,
          student_name: submission.student_name,
          filename: submission.filename,
          assignment_type: submission.assignment_type,
          questions: [
            { question_id: 'q1', description: 'Find the derivative', max_points: 10, score: 8, feedback: 'Good work!' },
            { question_id: 'q2', description: 'Calculate the limit', max_points: 15, score: 12, feedback: 'Minor error' },
            { question_id: 'q3', description: 'Find the area', max_points: 20, score: 18, feedback: 'Excellent!' },
            { question_id: 'q4', description: 'Critical points', max_points: 15, score: 14, feedback: 'Well done' },
            { question_id: 'q5', description: 'Second derivative', max_points: 10, score: 9, feedback: 'Perfect' }
          ],
          total_score: 61,
          max_total: 70,
          percentage: 87.1
        });
      }
    } catch (error) {
      console.error('Error grading submission:', error);
    }
  };

  const handleReleaseGrades = async (submission: Submission) => {
    try {
      const response = await fetch(`/api/submissions/${submission.id}/release`, {
        method: 'POST'
      });
      
      if (response.ok) {
        // Update local state
        setSubmissions(prev => prev.map(sub => 
          sub.id === submission.id ? { ...sub, status: 'released' as const } : sub
        ));
      }
    } catch (error) {
      console.error('Error releasing grades:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending_grading': return 'status-pending';
      case 'graded': return 'status-graded';
      case 'released': return 'status-released';
      default: return 'status-pending';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending_grading': return 'Pending Grading';
      case 'graded': return 'Graded';
      case 'released': return 'Released';
      default: return 'Unknown';
    }
  };

  const pendingSubmissions = submissions.filter(s => s.status === 'pending_grading');
  const gradedSubmissions = submissions.filter(s => s.status === 'graded');
  const releasedSubmissions = submissions.filter(s => s.status === 'released');
  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>TA Dashboard</h1>
        </div>
        <div className="loading">Loading submissions...</div>
      </div>
    );
  }

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
          <h2>Pending Grading ({pendingSubmissions.length})</h2>
          <div className="submissions-list">
            {pendingSubmissions.length === 0 ? (
              <p className="no-submissions">No submissions pending grading</p>
            ) : (
              pendingSubmissions.map(submission => (
                <div key={submission.id} className="submission-item">
                  <div className="submission-info">
                    <div className="student-name">{submission.student_name}</div>
                    <div className="filename">{submission.filename}</div>
                    <div className="submitted-at">
                      Submitted: {new Date(submission.submitted_at).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="submission-actions">
                    <button 
                      className="action-btn primary small"
                      onClick={() => handleGradeSubmission(submission)}
                    >
                      Grade with AI
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Graded Submissions ({gradedSubmissions.length})</h2>
          <div className="submissions-list">
            {gradedSubmissions.length === 0 ? (
              <p className="no-submissions">No graded submissions</p>
            ) : (
              gradedSubmissions.map(submission => (
                <div key={submission.id} className="submission-item">
                  <div className="submission-info">
                    <div className="student-name">{submission.student_name}</div>
                    <div className="filename">{submission.filename}</div>
                    <div className="score-info">
                      Score: {submission.total_score}/{submission.max_total} ({submission.percentage}%)
                    </div>
                  </div>
                  <div className="submission-actions">
                    <button 
                      className="action-btn secondary small"
                      onClick={() => onGradeSubmission(submission as any)}
                    >
                      Review
                    </button>
                    <button 
                      className="action-btn primary small"
                      onClick={() => handleReleaseGrades(submission)}
                    >
                      Release to Student
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Released Grades ({releasedSubmissions.length})</h2>
          <div className="submissions-list">
            {releasedSubmissions.length === 0 ? (
              <p className="no-submissions">No released grades</p>
            ) : (
              releasedSubmissions.map(submission => (
                <div key={submission.id} className="submission-item">
                  <div className="submission-info">
                    <div className="student-name">{submission.student_name}</div>
                    <div className="filename">{submission.filename}</div>
                    <div className="score-info">
                      Score: {submission.total_score}/{submission.max_total} ({submission.percentage}%)
                    </div>
                  </div>
                  <div className="submission-actions">
                    <span className="status-badge released">Released</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Quick Stats</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-number">{submissions.length}</span>
              <span className="stat-label">Total Submissions</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{gradedSubmissions.length + releasedSubmissions.length}</span>
              <span className="stat-label">Graded</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{releasedSubmissions.length}</span>
              <span className="stat-label">Released</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TADashboard;
