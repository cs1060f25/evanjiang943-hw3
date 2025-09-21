import { useState } from 'react';
import './App.css';
import LoginPage from './components/LoginPage';
import TADashboard from './components/TADashboard';
import ReviewGrades from './components/ReviewGrades';
import StudentView from './components/StudentView';

export interface GradingResult {
  submission_id?: string;
  student_name?: string;
  filename: string;
  assignment_type: string;
  questions: Array<{
    question_id: string;
    description: string;
    score: number;
    max_points: number;
    feedback: string;
    student_answer?: string;
  }>;
  total_score: number;
  max_total: number;
  percentage: number;
}

export interface EditedGrades extends GradingResult {
  questions: Array<{
    question_id: string;
    description: string;
    score: number;
    max_points: number;
    feedback: string;
    student_answer?: string;
    edited?: boolean;
  }>;
}

type AppState = 'login' | 'dashboard' | 'review' | 'student';

function App() {
  const [currentState, setCurrentState] = useState<AppState>('login');
  const [gradingResult, setGradingResult] = useState<GradingResult | null>(null);
  const [editedGrades, setEditedGrades] = useState<EditedGrades | null>(null);

  const handleLogin = () => {
    setCurrentState('dashboard');
  };


  const handleGradeSubmission = async (submission: any) => {
    try {
      // Call the API to grade the submission
      const response = await fetch(`http://localhost:5001/api/submissions/${submission.id}/grade`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const gradingResult = await response.json();
        console.log('Grading result from API:', gradingResult);
        setGradingResult(gradingResult);
        setEditedGrades({ ...gradingResult, questions: gradingResult.questions.map(q => ({ ...q, edited: false })) });
        setCurrentState('review');
      } else {
        console.error('Failed to grade submission');
        // Fallback to mock data
        const mockGradingResult: GradingResult = {
          submission_id: submission.id,
          student_name: submission.student_name,
          filename: submission.filename,
          assignment_type: submission.assignment_type,
          questions: submission.questions.map((q: any) => ({
            question_id: q.id,
            description: q.description,
            score: Math.floor(Math.random() * q.max_points * 0.8) + q.max_points * 0.2,
            max_points: q.max_points,
            feedback: "Mock feedback for demonstration",
            student_answer: q.student_answer
          })),
          total_score: 0,
          max_total: submission.questions.reduce((sum: number, q: any) => sum + q.max_points, 0),
          percentage: 0
        };
        mockGradingResult.total_score = mockGradingResult.questions.reduce((sum, q) => sum + q.score, 0);
        mockGradingResult.percentage = (mockGradingResult.total_score / mockGradingResult.max_total) * 100;
        
        setGradingResult(mockGradingResult);
        setEditedGrades({ ...mockGradingResult, questions: mockGradingResult.questions.map(q => ({ ...q, edited: false })) });
        setCurrentState('review');
      }
    } catch (error) {
      console.error('Error grading submission:', error);
    }
  };


  const handleReviewComplete = (finalGrades: EditedGrades) => {
    setEditedGrades(finalGrades);
    setCurrentState('student');
  };

  const handleBackToDashboard = () => {
    setCurrentState('dashboard');
    setGradingResult(null);
    setEditedGrades(null);
  };

  const handleNewSubmission = () => {
    setGradingResult(null);
    setEditedGrades(null);
    setCurrentState('dashboard');
  };

  return (
    <div className="App">
      {currentState === 'login' && <LoginPage onLogin={handleLogin} />}
      {currentState === 'dashboard' && <TADashboard onGradeSubmission={handleGradeSubmission} />}
      {currentState === 'review' && gradingResult && (
        <ReviewGrades 
          gradingResult={gradingResult}
          editedGrades={editedGrades}
          onGradesUpdated={setEditedGrades}
          onReviewComplete={handleReviewComplete}
          onBack={handleBackToDashboard}
        />
      )}
      {currentState === 'student' && editedGrades && (
        <StudentView 
          finalGrades={editedGrades}
          onNewSubmission={handleNewSubmission}
          onBack={handleBackToDashboard}
        />
      )}
    </div>
  );
}

export default App;