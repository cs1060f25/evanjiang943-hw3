# AI-Assisted Grading Platform

A rapid prototype of an AI-assisted grading platform designed to help instructors and TAs grade homework faster and more consistently with the help of AI.

## Project Information

- **Student Name:** Evan Jiang
- **GitHub Username:** evanjiang943
- **Deployed App URL:** [https://ai-grading-platform.vercel.app](https://ai-grading-platform.vercel.app)
- **Team PRD:** [Google Drive Link](https://drive.google.com/drive/folders/your-prd-link-here)

## Overview

This prototype demonstrates a simplified version of the Teaching Assistant (TA) user journey for an AI-assisted grading platform. The system includes **15 pre-existing student submissions** with calculus homework problems, allowing TAs to immediately start the grading workflow without needing to upload files. The platform simulates AI-powered grading with rubric-based scoring, TA review and editing, and final feedback delivery to students.

## Features

### Primary User Journey (Teaching Assistant)

1. **Login / Dashboard**
   - Simple login interface with "Login as TA" option
   - Dashboard showing pre-existing student submissions
   - Three submission categories: Pending Grading, Graded, Released
   - Quick stats showing total submissions and grading progress

2. **Manage Pre-existing Submissions**
   - **15 mock student submissions** with calculus homework problems
   - **12 pending submissions** ready for AI grading
   - **2 graded submissions** ready for review and release
   - **1 released submission** already sent to student
   - Realistic student answers with varying quality levels

3. **AI Grading Workflow**
   - Click "Grade with AI" on any pending submission
   - Automated grading with rubric-based scoring
   - Calculus problems: derivatives, limits, integrals, critical points
   - Realistic score generation with detailed feedback

4. **TA Review & Edit**
   - Interactive table showing AI-generated grades
   - **Student answers displayed** for each question
   - Editable scores and feedback for each question
   - Visual indicators for edited items
   - Real-time total score calculation

5. **Release Grades to Students**
   - Review and approve final grades
   - Click "Release to Student" to send feedback
   - Track submission status: pending → graded → released
   - Professional student-facing interface with detailed feedback

## Technical Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling and development server
- **CSS3** with modern styling and responsive design
- **Fetch API** for backend communication

### Backend
- **Vercel Serverless Functions** (Python)
- **Mock data generation** for AI grading simulation
- **RESTful API** design

## Project Structure

```
ai-grading-platform/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── LoginPage.tsx
│   │   │   ├── TADashboard.tsx
│   │   │   ├── ReviewGrades.tsx
│   │   │   └── StudentView.tsx
│   │   ├── App.tsx          # Main application component
│   │   ├── App.css          # Application styles
│   │   └── main.tsx         # Application entry point
│   ├── package.json
│   └── vite.config.ts
├── api/                     # Vercel serverless functions
│   └── grade.py             # Main API handler
├── vercel.json              # Vercel configuration
└── README.md
```

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- Python 3.8 or higher
- Git

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

5. The backend will be available at `http://localhost:5001`

## Usage

1. **Start the application** by opening the frontend in your browser
2. **Login as TA** by clicking the "Login as TA" button
3. **View pre-existing submissions** in three categories:
   - **Pending Grading**: 12 submissions ready for AI grading
   - **Graded**: 2 submissions ready for review and release
   - **Released**: 1 submission already sent to student
4. **Grade submissions** by clicking "Grade with AI" on any pending submission
5. **Review and edit grades** in the review interface, making any necessary adjustments
6. **Release grades** by clicking "Release to Student" when ready
7. **View student feedback** to see the final graded report

## Mock Data

The system includes **15 pre-existing student submissions** with realistic mock data:

### **Student Submissions**
- **Alice Johnson, Bob Smith, Carol Davis** - Confident answers with good understanding
- **Emma Rodriguez, Frank Chen, Grace Kim** - Detailed work with step-by-step solutions
- **Henry Patel** - Struggling student showing honest uncertainty
- **Isabella Martinez, Jack Thompson, Katie Lee** - Advanced techniques and clear explanations
- **Liam O'Connor, Maya Singh, Noah Brown, Olivia Taylor** - Various performance levels

### **Calculus Problems**
All submissions contain the same 5 calculus problems:
1. **Derivatives**: f(x) = 3x² + 2x - 1 (10 points)
2. **Limits**: lim(x→2) (x²-4)/(x-2) (15 points)  
3. **Integration**: Area under y = x² from 0 to 3 (20 points)
4. **Critical Points**: f(x) = x³ - 3x + 1 (15 points)
5. **Second Derivatives**: g(x) = sin(x) + cos(x) (10 points)

### **Submission States**
- **12 Pending**: Ready for AI grading
- **2 Graded**: Ready for review and release
- **1 Released**: Already sent to student

## Deployment

The frontend is deployed on Vercel and can be accessed at the URL provided above. The backend can be run locally or deployed to a cloud service like Heroku or Railway.

## Constraints

- **No real AI integration** - Uses mock data for demonstration
- **No authentication** - Simplified login for prototype
- **Happy path only** - No complex error handling
- **Mock OCR** - File processing is simulated

## Future Enhancements

- Real AI/LLM integration for actual grading
- OCR integration for handwritten submissions
- User authentication and authorization
- Database integration for persistent data
- Real-time collaboration features
- Advanced analytics and reporting

## License

This project is created for educational purposes as part of a CS1060 assignment.

## Contact

For questions or issues, please contact Evan Jiang at [your-email@example.com].
