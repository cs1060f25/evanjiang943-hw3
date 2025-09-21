from http.server import BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse, parse_qs

# Mock rubric data
RUBRICS = {
    "calculus_homework": {
        "questions": [
            {"id": "q1", "max_points": 10, "description": "Find the derivative of f(x) = 3x² + 2x - 1"},
            {"id": "q2", "max_points": 15, "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)"},
            {"id": "q3", "max_points": 20, "description": "Find the area under the curve y = x² from x = 0 to x = 3"},
            {"id": "q4", "max_points": 15, "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points"},
            {"id": "q5", "max_points": 10, "description": "Find the second derivative of g(x) = sin(x) + cos(x)"}
        ]
    },
    "math_homework": {
        "questions": [
            {"id": "q1", "max_points": 20, "description": "Solve the quadratic equation x² - 5x + 6 = 0"},
            {"id": "q2", "max_points": 15, "description": "Find the slope of the line passing through points (2,3) and (5,9)"},
            {"id": "q3", "max_points": 25, "description": "Graph the function f(x) = 2x + 1 and identify its domain and range"}
        ]
    },
    "essay": {
        "questions": [
            {"id": "q1", "max_points": 30, "description": "Thesis statement and argument structure"},
            {"id": "q2", "max_points": 25, "description": "Evidence and examples used"},
            {"id": "q3", "max_points": 20, "description": "Writing quality and grammar"},
            {"id": "q4", "max_points": 25, "description": "Conclusion and overall coherence"}
        ]
    }
}

# Mock student submissions
STUDENT_SUBMISSIONS = [
    {
        "id": "sub_001",
        "student_name": "Alice Johnson",
        "student_id": "AJ2024",
        "filename": "calculus_hw1_alice.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-15T14:30:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "Using L'Hôpital's rule: lim(x→2) (2x)/1 = 4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 27/3 - 0 = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3 = 3(x² - 1) = 3(x-1)(x+1). Critical points at x = ±1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g'(x) = cos(x) - sin(x), g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_002",
        "student_name": "Bob Smith",
        "student_id": "BS2024",
        "filename": "calculus_hw1_bob.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-15T16:45:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "-sin(x) - cos(x)"}
        ]
    }
]

def generate_feedback(score, max_points, question_id):
    """Generate realistic feedback based on score"""
    percentage = (score / max_points) * 100
    
    if percentage >= 90:
        return "Excellent work! Clear understanding demonstrated."
    elif percentage >= 80:
        return "Good work with minor issues. Well done overall."
    elif percentage >= 70:
        return "Decent attempt but some concepts need clarification."
    elif percentage >= 60:
        return "Shows some understanding but needs improvement."
    else:
        return "Needs significant improvement. Review the concepts."

def simulate_ai_grading(assignment_type, questions):
    """Simulate AI grading with realistic score distribution"""
    rubric = RUBRICS.get(assignment_type, RUBRICS["calculus_homework"])
    graded_questions = []
    total_score = 0
    max_total = 0
    
    for question in questions:
        max_points = question["max_points"]
        max_total += max_points
        
        # Simulate realistic grading with some variation
        base_score = max_points * random.uniform(0.6, 0.95)
        score = round(base_score, 1)
        score = min(score, max_points)  # Cap at max points
        
        total_score += score
        
        feedback = generate_feedback(score, max_points, question["id"])
        
        graded_questions.append({
            "question_id": question["id"],
            "description": question["description"],
            "score": score,
            "max_points": max_points,
            "feedback": feedback,
            "student_answer": question.get("student_answer", "")
        })
    
    percentage = round((total_score / max_total) * 100, 1)
    
    return {
        "questions": graded_questions,
        "total_score": round(total_score, 1),
        "max_total": max_total,
        "percentage": percentage
    }

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        if path_parts[0] == 'api':
            if len(path_parts) == 2 and path_parts[1] == 'submissions':
                # GET /api/submissions
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(STUDENT_SUBMISSIONS).encode())
                return
            elif len(path_parts) == 3 and path_parts[1] == 'submissions':
                # GET /api/submissions/{id}
                submission_id = path_parts[2]
                submission = next((s for s in STUDENT_SUBMISSIONS if s['id'] == submission_id), None)
                if submission:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(submission).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Submission not found"}).encode())
                return
        
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        if path_parts[0] == 'api':
            if len(path_parts) == 4 and path_parts[1] == 'submissions' and path_parts[3] == 'grade':
                # POST /api/submissions/{id}/grade
                submission_id = path_parts[2]
                submission = next((s for s in STUDENT_SUBMISSIONS if s['id'] == submission_id), None)
                
                if submission:
                    result = simulate_ai_grading(submission['assignment_type'], submission['questions'])
                    result['submission_id'] = submission_id
                    result['student_name'] = submission['student_name']
                    result['filename'] = submission['filename']
                    result['assignment_type'] = submission['assignment_type']
                    
                    # Update submission status
                    submission['status'] = 'graded'
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Submission not found"}).encode())
                return
            elif len(path_parts) == 4 and path_parts[1] == 'submissions' and path_parts[3] == 'release':
                # POST /api/submissions/{id}/release
                submission_id = path_parts[2]
                submission = next((s for s in STUDENT_SUBMISSIONS if s['id'] == submission_id), None)
                
                if submission:
                    submission['status'] = 'released'
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "Grades released successfully"}).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Submission not found"}).encode())
                return
        
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())
