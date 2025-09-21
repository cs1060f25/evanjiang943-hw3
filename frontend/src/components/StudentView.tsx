import React from 'react';
import { EditedGrades } from '../App';

interface StudentViewProps {
  finalGrades: EditedGrades;
  onNewSubmission: () => void;
  onBack: () => void;
}

const StudentView: React.FC<StudentViewProps> = ({ finalGrades, onNewSubmission, onBack }) => {
  const getGradeLetter = (percentage: number) => {
    if (percentage >= 90) return 'A';
    if (percentage >= 80) return 'B';
    if (percentage >= 70) return 'C';
    if (percentage >= 60) return 'D';
    return 'F';
  };

  const getGradeColor = (percentage: number) => {
    if (percentage >= 90) return 'grade-a';
    if (percentage >= 80) return 'grade-b';
    if (percentage >= 70) return 'grade-c';
    if (percentage >= 60) return 'grade-d';
    return 'grade-f';
  };

  return (
    <div className="student-view-page">
      <div className="student-container">
        <div className="student-header">
          <button className="back-btn" onClick={onBack}>
            ← Back to Dashboard
          </button>
          <h1>Student Feedback Report</h1>
          <p>Final graded report for student review</p>
        </div>

        <div className="student-content">
          <div className="report-header">
            <h2>{finalGrades.filename}</h2>
            <div className="assignment-info">
              <span className="assignment-type">Assignment Type: {finalGrades.assignment_type}</span>
              <span className="graded-date">Graded on: {new Date().toLocaleDateString()}</span>
            </div>
          </div>

          <div className="grade-summary">
            <div className="summary-card">
              <div className="grade-display">
                <div className={`grade-letter ${getGradeColor(finalGrades.percentage)}`}>
                  {getGradeLetter(finalGrades.percentage)}
                </div>
                <div className="grade-details">
                  <div className="grade-percentage">{finalGrades.percentage}%</div>
                  <div className="grade-points">
                    {finalGrades.total_score} / {finalGrades.max_total} points
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="detailed-feedback">
            <h3>Detailed Feedback</h3>
            <div className="feedback-list">
              {finalGrades.questions.map((question, index) => (
                <div key={question.question_id} className="feedback-item">
                  <div className="feedback-header">
                    <div className="question-info">
                      <span className="question-id">{question.question_id.toUpperCase()}</span>
                      <span className="question-desc">{question.description}</span>
                    </div>
                    <div className="question-score">
                      <span className="score">{question.score}</span>
                      <span className="max-points">/ {question.max_points}</span>
                    </div>
                  </div>
                  <div className="feedback-content">
                    <p>{question.feedback}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="overall-comments">
            <h3>Overall Comments</h3>
            <div className="comments-card">
              <p>
                {finalGrades.percentage >= 90 
                  ? "Excellent work! You demonstrated a strong understanding of the concepts and provided clear, well-reasoned solutions."
                  : finalGrades.percentage >= 80
                  ? "Good work overall! You showed solid understanding with room for improvement in some areas."
                  : finalGrades.percentage >= 70
                  ? "Satisfactory work. Consider reviewing the feedback below to strengthen your understanding."
                  : finalGrades.percentage >= 60
                  ? "Your work shows effort, but there are several areas that need improvement. Please review the feedback carefully."
                  : "This submission needs significant improvement. Please review the feedback and consider seeking additional help."
                }
              </p>
            </div>
          </div>

          <div className="next-steps">
            <h3>Next Steps</h3>
            <div className="steps-list">
              <div className="step-item">
                <span className="step-number">1</span>
                <span className="step-text">Review the detailed feedback for each question</span>
              </div>
              <div className="step-item">
                <span className="step-number">2</span>
                <span className="step-text">Identify areas for improvement</span>
              </div>
              <div className="step-item">
                <span className="step-number">3</span>
                <span className="step-text">Consider attending office hours if you have questions</span>
              </div>
              <div className="step-item">
                <span className="step-number">4</span>
                <span className="step-text">Apply feedback to future assignments</span>
              </div>
            </div>
          </div>

          <div className="student-actions">
            <button className="action-btn secondary" onClick={onBack}>
              Back to Dashboard
            </button>
            <button className="action-btn primary" onClick={onNewSubmission}>
              Grade Another Submission
            </button>
          </div>

          <div className="regrade-notice">
            <p>
              <strong>Need a regrade?</strong> If you believe there was an error in grading, 
              please contact your TA within 48 hours of receiving this feedback.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentView;
