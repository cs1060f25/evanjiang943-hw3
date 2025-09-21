import React, { useState } from 'react';
import './App.css';
import LoginPage from './components/LoginPage';
import TADashboard from './components/TADashboard';
import UploadSubmission from './components/UploadSubmission';
import ReviewGrades from './components/ReviewGrades';
import StudentView from './components/StudentView';

export interface GradingResult {
  filename: string;
  assignment_type: string;
  questions: Array<{
    question_id: string;
    description: string;
    score: number;
    max_points: number;
    feedback: string;
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
    edited?: boolean;
  }>;
}

type AppState = 'login' | 'dashboard' | 'upload' | 'review' | 'student';

function App() {
  const [currentState, setCurrentState] = useState<AppState>('login');
  const [gradingResult, setGradingResult] = useState<GradingResult | null>(null);
  const [editedGrades, setEditedGrades] = useState<EditedGrades | null>(null);

  const handleLogin = () => {
    setCurrentState('dashboard');
  };

  const handleUpload = () => {
    setCurrentState('upload');
  };

  const handleGradingComplete = (result: GradingResult) => {
    setGradingResult(result);
    setEditedGrades({ ...result, questions: result.questions.map(q => ({ ...q, edited: false })) });
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
    setCurrentState('upload');
  };

  return (
    <div className="App">
      {currentState === 'login' && <LoginPage onLogin={handleLogin} />}
      {currentState === 'dashboard' && <TADashboard onUpload={handleUpload} />}
      {currentState === 'upload' && (
        <UploadSubmission 
          onGradingComplete={handleGradingComplete}
          onBack={handleBackToDashboard}
        />
      )}
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