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


  const handleGradeSubmission = (submission: any) => {
    // Convert submission to grading result format
    const gradingResult: GradingResult = {
      submission_id: submission.submission_id || submission.id,
      student_name: submission.student_name,
      filename: submission.filename,
      assignment_type: submission.assignment_type,
      questions: submission.questions || [],
      total_score: submission.total_score || 0,
      max_total: submission.max_total || 0,
      percentage: submission.percentage || 0
    };
    
    setGradingResult(gradingResult);
    setEditedGrades({ ...gradingResult, questions: gradingResult.questions.map(q => ({ ...q, edited: false })) });
    setCurrentState('review');
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