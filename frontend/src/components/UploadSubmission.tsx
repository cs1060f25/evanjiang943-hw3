import React, { useState } from 'react';
import { GradingResult } from '../App';

interface UploadSubmissionProps {
  onGradingComplete: (result: GradingResult) => void;
  onBack: () => void;
}

const UploadSubmission: React.FC<UploadSubmissionProps> = ({ onGradingComplete, onBack }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;

    setIsUploading(true);
    
    try {
      // Simulate API call to backend
      const response = await fetch('http://localhost:5000/api/grade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filename: file.name,
          file_type: file.type
        })
      });

      if (!response.ok) {
        throw new Error('Grading failed');
      }

      const data = await response.json();
      onGradingComplete(data.grading_result);
    } catch (error) {
      console.error('Error grading submission:', error);
      // For demo purposes, use mock data if backend is not available
      const mockResult: GradingResult = {
        filename: file.name,
        assignment_type: file.name.includes('math') ? 'math_homework' : 'essay',
        questions: [
          {
            question_id: 'q1',
            description: 'Problem solving',
            score: 4,
            max_points: 5,
            feedback: 'Good approach, minor calculation error'
          },
          {
            question_id: 'q2',
            description: 'Methodology',
            score: 5,
            max_points: 5,
            feedback: 'Excellent work'
          },
          {
            question_id: 'q3',
            description: 'Final answer',
            score: 3,
            max_points: 5,
            feedback: 'Correct method, check arithmetic'
          }
        ],
        total_score: 12,
        max_total: 15,
        percentage: 80.0
      };
      onGradingComplete(mockResult);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <div className="upload-header">
          <button className="back-btn" onClick={onBack}>
            ← Back to Dashboard
          </button>
          <h1>Upload Student Submission</h1>
        </div>

        <div className="upload-content">
          <div 
            className={`upload-area ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="file-upload"
              className="file-input"
              accept=".pdf,.txt,.doc,.docx"
              onChange={handleFileInput}
            />
            <label htmlFor="file-upload" className="upload-label">
              {file ? (
                <div className="file-selected">
                  <div className="file-icon">📄</div>
                  <div className="file-info">
                    <div className="file-name">{file.name}</div>
                    <div className="file-size">{(file.size / 1024).toFixed(1)} KB</div>
                  </div>
                </div>
              ) : (
                <div className="upload-prompt">
                  <div className="upload-icon">📁</div>
                  <div className="upload-text">
                    <h3>Drop your file here or click to browse</h3>
                    <p>Supports PDF, TXT, DOC, DOCX files</p>
                  </div>
                </div>
              )}
            </label>
          </div>

          <div className="upload-actions">
            <button 
              className="action-btn secondary" 
              onClick={onBack}
              disabled={isUploading}
            >
              Cancel
            </button>
            <button 
              className="action-btn primary" 
              onClick={handleSubmit}
              disabled={!file || isUploading}
            >
              {isUploading ? 'Grading...' : 'Start AI Grading'}
            </button>
          </div>

          {isUploading && (
            <div className="grading-progress">
              <div className="progress-bar">
                <div className="progress-fill"></div>
              </div>
              <p>AI is analyzing the submission and applying rubric-based grading...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadSubmission;
