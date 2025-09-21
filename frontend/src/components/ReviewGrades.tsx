import React, { useState } from 'react';
import type { GradingResult, EditedGrades } from '../App';

interface ReviewGradesProps {
  gradingResult: GradingResult;
  editedGrades: EditedGrades | null;
  onGradesUpdated: (grades: EditedGrades) => void;
  onReviewComplete: (finalGrades: EditedGrades) => void;
  onBack: () => void;
}

const ReviewGrades: React.FC<ReviewGradesProps> = ({ 
  gradingResult, 
  editedGrades, 
  onGradesUpdated, 
  onReviewComplete, 
  onBack 
}) => {
  console.log('ReviewGrades received gradingResult:', gradingResult);
  console.log('ReviewGrades received editedGrades:', editedGrades);
  
  const [currentGrades, setCurrentGrades] = useState<EditedGrades>(
    editedGrades || { ...gradingResult, questions: gradingResult.questions.map(q => ({ ...q, edited: false })) }
  );

  const handleScoreChange = (questionId: string, newScore: number) => {
    const updatedGrades = {
      ...currentGrades,
      questions: currentGrades.questions.map(q => 
        q.question_id === questionId 
          ? { ...q, score: Math.max(0, Math.min(q.max_points, newScore)), edited: true }
          : q
      )
    };
    
    // Recalculate total
    const newTotal = updatedGrades.questions.reduce((sum, q) => sum + q.score, 0);
    updatedGrades.total_score = newTotal;
    updatedGrades.percentage = Math.round((newTotal / updatedGrades.max_total) * 100 * 10) / 10;
    
    setCurrentGrades(updatedGrades);
    onGradesUpdated(updatedGrades);
  };

  const handleFeedbackChange = (questionId: string, newFeedback: string) => {
    const updatedGrades = {
      ...currentGrades,
      questions: currentGrades.questions.map(q => 
        q.question_id === questionId 
          ? { ...q, feedback: newFeedback, edited: true }
          : q
      )
    };
    
    setCurrentGrades(updatedGrades);
    onGradesUpdated(updatedGrades);
  };

  const handleSubmit = () => {
    onReviewComplete(currentGrades);
  };

  console.log('ReviewGrades rendering with currentGrades:', currentGrades);
  
  if (!gradingResult || !gradingResult.questions) {
    return (
      <div className="review-page">
        <div className="review-container">
          <div className="review-header">
            <button className="back-btn" onClick={onBack}>
              ← Back to Dashboard
            </button>
            <h1>Review AI-Generated Grades</h1>
            <p>Loading grading data...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="review-page">
      <div className="review-container">
        <div className="review-header">
          <button className="back-btn" onClick={onBack}>
            ← Back to Dashboard
          </button>
          <h1>Review AI-Generated Grades</h1>
          <p>Review and adjust the AI-generated grades before sending feedback to the student</p>
        </div>

        <div className="review-content">
        <div className="submission-info">
          <h2>{gradingResult.filename}</h2>
          {gradingResult.student_name && (
            <div className="student-info">
              Student: <strong>{gradingResult.student_name}</strong>
            </div>
          )}
          <div className="assignment-type">
            Assignment Type: <span className="type-badge">{gradingResult.assignment_type}</span>
          </div>
        </div>

          <div className="grades-summary">
            <div className="summary-card">
              <div className="summary-item">
                <span className="summary-label">Total Score</span>
                <span className="summary-value">
                  {currentGrades.total_score} / {currentGrades.max_total}
                </span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Percentage</span>
                <span className="summary-value">{currentGrades.percentage}%</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Grade</span>
                <span className="summary-value">
                  {currentGrades.percentage >= 90 ? 'A' : 
                   currentGrades.percentage >= 80 ? 'B' : 
                   currentGrades.percentage >= 70 ? 'C' : 
                   currentGrades.percentage >= 60 ? 'D' : 'F'}
                </span>
              </div>
            </div>
          </div>

          <div className="grades-table">
            <h3>Question-by-Question Review</h3>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Question</th>
                    <th>Description</th>
                    <th>Student Answer</th>
                    <th>Score</th>
                    <th>Max Points</th>
                    <th>Feedback</th>
                  </tr>
                </thead>
                <tbody>
                  {currentGrades.questions.map((question) => (
                    <tr key={question.question_id} className={question.edited ? 'edited' : ''}>
                      <td className="question-id">{question.question_id.toUpperCase()}</td>
                      <td className="question-desc">{question.description}</td>
                      <td className="student-answer">
                        {question.student_answer || 'No answer provided'}
                      </td>
                      <td className="score-cell">
                        <input
                          type="number"
                          min="0"
                          max={question.max_points}
                          value={question.score}
                          onChange={(e) => handleScoreChange(question.question_id, parseInt(e.target.value) || 0)}
                          className="score-input"
                        />
                        {question.edited && <span className="edited-indicator">*</span>}
                      </td>
                      <td className="max-points">{question.max_points}</td>
                      <td className="feedback-cell">
                        <textarea
                          value={question.feedback}
                          onChange={(e) => handleFeedbackChange(question.question_id, e.target.value)}
                          className="feedback-input"
                          rows={2}
                        />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="review-actions">
            <button className="action-btn secondary" onClick={onBack}>
              Cancel
            </button>
            <button className="action-btn primary" onClick={handleSubmit}>
              Send Feedback to Student
            </button>
          </div>

          <div className="review-notes">
            <p><strong>Note:</strong> Items marked with * have been edited from the AI's original assessment.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewGrades;
