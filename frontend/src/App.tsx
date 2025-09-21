import { useState, useRef } from 'react';
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
  const dashboardUpdateRef = useRef<((submissionId: string, updatedGrades: any) => void) | null>(null);

  const handleLogin = () => {
    setCurrentState('dashboard');
  };


  const handleGradeSubmission = (gradingResult: GradingResult) => {
    console.log('Received grading result:', gradingResult);
    setGradingResult(gradingResult);
    setEditedGrades({ ...gradingResult, questions: gradingResult.questions.map(q => ({ ...q, edited: false })) });
    setCurrentState('review');
  };


  const handleReviewComplete = (finalGrades: EditedGrades) => {
    setEditedGrades(finalGrades);
    setCurrentState('student');
  };


  const handleRegisterUpdateFunction = (updateFn: (submissionId: string, updatedGrades: any) => void) => {
    dashboardUpdateRef.current = updateFn;
  };

  const handleGradesSaved = (submissionId: string, grades: any) => {
    // This will be called when grades are saved from the review page
    console.log('Grades saved for submission:', submissionId, grades);
    // Update the dashboard with the new grades
    if (dashboardUpdateRef.current) {
      dashboardUpdateRef.current(submissionId, grades);
    }
    setEditedGrades(grades);
  };

  const handleBackToDashboard = () => {
    setCurrentState('dashboard');
    // Don't clear the data so it persists when navigating back
  };

  const handleNewSubmission = () => {
    setGradingResult(null);
    setEditedGrades(null);
    setCurrentState('dashboard');
  };

  return (
    <div className="App">
      {currentState === 'login' && <LoginPage onLogin={handleLogin} />}
      {currentState === 'dashboard' && <TADashboard onGradeSubmission={handleGradeSubmission} onRegisterUpdateFunction={handleRegisterUpdateFunction} />}
      {currentState === 'review' && gradingResult && (
        <ReviewGrades 
          gradingResult={gradingResult}
          editedGrades={editedGrades}
          onReviewComplete={handleReviewComplete}
          onBack={handleBackToDashboard}
          onGradesSaved={handleGradesSaved}
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