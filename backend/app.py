from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)

# Mock rubric data for different assignment types
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
            {"id": "q1", "max_points": 5, "description": "Solve linear equation"},
            {"id": "q2", "max_points": 5, "description": "Graph quadratic function"},
            {"id": "q3", "max_points": 10, "description": "Word problem application"},
            {"id": "q4", "max_points": 5, "description": "Simplify expression"}
        ]
    },
    "essay": {
        "questions": [
            {"id": "thesis", "max_points": 10, "description": "Clear thesis statement"},
            {"id": "evidence", "max_points": 15, "description": "Supporting evidence"},
            {"id": "analysis", "max_points": 10, "description": "Critical analysis"},
            {"id": "writing", "max_points": 5, "description": "Grammar and style"}
        ]
    }
}

# Pre-existing student submissions
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
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "Using L'Hôpital's rule: lim = 4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3 = 0, so x = ±1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
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
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "lim (x+2) = 4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Critical points at x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_003",
        "student_name": "Carol Davis",
        "student_id": "CD2024",
        "filename": "calculus_hw1_carol.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-16T09:15:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, at x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_004",
        "student_name": "David Wilson",
        "student_id": "DW2024",
        "filename": "calculus_hw1_david.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-16T11:30:00Z",
        "status": "graded",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2", "score": 10, "feedback": "Perfect!"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4", "score": 15, "feedback": "Excellent work"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9", "score": 20, "feedback": "Correct integration"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, at x = 1 and x = -1", "score": 15, "feedback": "Well done"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)", "score": 10, "feedback": "Perfect"}
        ],
        "total_score": 70,
        "max_total": 70,
        "percentage": 100.0,
        "graded_at": "2024-01-16T14:20:00Z",
        "graded_by": "TA_001"
    },
    {
        "id": "sub_005",
        "student_name": "Emma Rodriguez",
        "student_id": "ER2024",
        "filename": "calculus_hw1_emma.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-16T13:20:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "I think it's 4 but I'm not sure about the steps"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 27/3 = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3, set equal to 0: 3x² = 3, x² = 1, so x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g'(x) = cos(x) - sin(x), g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_006",
        "student_name": "Frank Chen",
        "student_id": "FC2024",
        "filename": "calculus_hw1_frank.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-16T15:45:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "Factor: (x-2)(x+2)/(x-2) = x+2, so lim = 2+2 = 4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 27/3 - 0 = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3 = 3(x² - 1) = 3(x-1)(x+1), so critical points at x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_007",
        "student_name": "Grace Kim",
        "student_id": "GK2024",
        "filename": "calculus_hw1_grace.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-17T08:30:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, critical points at x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_008",
        "student_name": "Henry Patel",
        "student_id": "HP2024",
        "filename": "calculus_hw1_henry.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-17T10:15:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "I think it's 6x + 2 but I'm not confident"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "I tried to factor but got confused. Maybe 4?"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3, so 3x² = 3, x² = 1, x = ±1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_009",
        "student_name": "Isabella Martinez",
        "student_id": "IM2024",
        "filename": "calculus_hw1_isabella.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-17T14:20:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "Using L'Hôpital's rule: lim (2x)/1 = 4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 27/3 = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3 = 0, so x² = 1, therefore x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g'(x) = cos(x) - sin(x), g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_010",
        "student_name": "Jack Thompson",
        "student_id": "JT2024",
        "filename": "calculus_hw1_jack.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-17T16:30:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Critical points at x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_011",
        "student_name": "Katie Lee",
        "student_id": "KL2024",
        "filename": "calculus_hw1_katie.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-18T09:45:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "Factor numerator: (x-2)(x+2)/(x-2) = x+2, so limit is 4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "∫₀³ x² dx = [x³/3]₀³ = 9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "f'(x) = 3x² - 3 = 3(x²-1) = 3(x-1)(x+1), so x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_012",
        "student_name": "Liam O'Connor",
        "student_id": "LO2024",
        "filename": "calculus_hw1_liam.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-18T11:20:00Z",
        "status": "pending_grading",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, at x = 1 and x = -1"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)"}
        ]
    },
    {
        "id": "sub_013",
        "student_name": "Maya Singh",
        "student_id": "MS2024",
        "filename": "calculus_hw1_maya.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-18T13:15:00Z",
        "status": "graded",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2", "score": 10, "feedback": "Perfect!"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4", "score": 15, "feedback": "Excellent work"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9", "score": 20, "feedback": "Correct integration"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, at x = 1 and x = -1", "score": 15, "feedback": "Well done"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)", "score": 10, "feedback": "Perfect"}
        ],
        "total_score": 70,
        "max_total": 70,
        "percentage": 100.0,
        "graded_at": "2024-01-18T15:30:00Z",
        "graded_by": "TA_001"
    },
    {
        "id": "sub_014",
        "student_name": "Noah Brown",
        "student_id": "NB2024",
        "filename": "calculus_hw1_noah.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-18T15:45:00Z",
        "status": "graded",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2", "score": 10, "feedback": "Perfect!"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4", "score": 12, "feedback": "Correct answer but show more work"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9", "score": 18, "feedback": "Good work, minor calculation error"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, at x = 1 and x = -1", "score": 15, "feedback": "Excellent"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)", "score": 9, "feedback": "Almost perfect, check signs"}
        ],
        "total_score": 64,
        "max_total": 70,
        "percentage": 91.4,
        "graded_at": "2024-01-18T17:20:00Z",
        "graded_by": "TA_001"
    },
    {
        "id": "sub_015",
        "student_name": "Olivia Taylor",
        "student_id": "OT2024",
        "filename": "calculus_hw1_olivia.pdf",
        "assignment_type": "calculus_homework",
        "submitted_at": "2024-01-19T08:30:00Z",
        "status": "released",
        "questions": [
            {"id": "q1", "description": "Find the derivative of f(x) = 3x² + 2x - 1", "max_points": 10, "student_answer": "f'(x) = 6x + 2", "score": 10, "feedback": "Perfect!"},
            {"id": "q2", "description": "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)", "max_points": 15, "student_answer": "4", "score": 15, "feedback": "Excellent work"},
            {"id": "q3", "description": "Find the area under the curve y = x² from x = 0 to x = 3", "max_points": 20, "student_answer": "9", "score": 20, "feedback": "Correct integration"},
            {"id": "q4", "description": "Determine if the function f(x) = x³ - 3x + 1 has any critical points", "max_points": 15, "student_answer": "Yes, at x = 1 and x = -1", "score": 15, "feedback": "Well done"},
            {"id": "q5", "description": "Find the second derivative of g(x) = sin(x) + cos(x)", "max_points": 10, "student_answer": "g''(x) = -sin(x) - cos(x)", "score": 10, "feedback": "Perfect"}
        ],
        "total_score": 70,
        "max_total": 70,
        "percentage": 100.0,
        "graded_at": "2024-01-19T10:15:00Z",
        "graded_by": "TA_001",
        "released_at": "2024-01-19T11:00:00Z"
    }
]

def generate_mock_grading(filename, file_type):
    """Generate mock AI grading results based on file type"""
    
    # Determine assignment type based on filename or file type
    if "math" in filename.lower() or file_type == "application/pdf":
        rubric = RUBRICS["math_homework"]
    else:
        rubric = RUBRICS["essay"]
    
    results = []
    total_points = 0
    max_total = 0
    
    for question in rubric["questions"]:
        # Generate realistic scores (slightly biased towards good performance)
        base_score = random.randint(3, question["max_points"])
        # Add some randomness but keep it realistic
        score = min(question["max_points"], max(0, base_score + random.randint(-1, 1)))
        
        # Generate mock feedback
        feedback_options = {
            "math_homework": {
                "q1": ["Correct method", "Minor algebra error", "Good approach, check arithmetic", "Missing steps", "Excellent work"],
                "q2": ["Perfect graph", "Correct shape, minor scaling issue", "Good understanding", "Needs more detail", "Well done"],
                "q3": ["Excellent problem solving", "Good setup, check calculation", "Correct approach", "Missing units", "Outstanding work"],
                "q4": ["Perfect simplification", "Correct method", "Minor error in final step", "Good start", "Excellent"]
            },
            "essay": {
                "thesis": ["Clear and compelling thesis", "Good thesis statement", "Thesis could be stronger", "Unclear thesis", "Excellent argument"],
                "evidence": ["Strong supporting evidence", "Good examples provided", "Needs more evidence", "Evidence is weak", "Outstanding research"],
                "analysis": ["Deep critical analysis", "Good analysis", "Surface-level analysis", "Needs deeper analysis", "Excellent insights"],
                "writing": ["Clear and engaging writing", "Good writing style", "Some grammar issues", "Needs improvement", "Excellent prose"]
            }
        }
        
        assignment_type = "math_homework" if "math" in filename.lower() or file_type == "application/pdf" else "essay"
        feedback = random.choice(feedback_options[assignment_type][question["id"]])
        
        results.append({
            "question_id": question["id"],
            "description": question["description"],
            "score": score,
            "max_points": question["max_points"],
            "feedback": feedback
        })
        
        total_points += score
        max_total += question["max_points"]
    
    return {
        "filename": filename,
        "assignment_type": assignment_type,
        "questions": results,
        "total_score": total_points,
        "max_total": max_total,
        "percentage": round((total_points / max_total) * 100, 1)
    }

@app.route('/api/grade', methods=['POST'])
def grade_submission():
    """API endpoint to simulate AI grading"""
    try:
        # Get file information from request
        data = request.get_json()
        filename = data.get('filename', 'unknown.pdf')
        file_type = data.get('file_type', 'application/pdf')
        
        # Generate mock grading results
        grading_result = generate_mock_grading(filename, file_type)
        
        return jsonify({
            "success": True,
            "grading_result": grading_result
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get all student submissions"""
    try:
        return jsonify({
            "success": True,
            "submissions": STUDENT_SUBMISSIONS
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/submissions/<submission_id>', methods=['GET'])
def get_submission(submission_id):
    """Get a specific student submission"""
    try:
        submission = next((s for s in STUDENT_SUBMISSIONS if s['id'] == submission_id), None)
        if not submission:
            return jsonify({
                "success": False,
                "error": "Submission not found"
            }), 404
        
        return jsonify({
            "success": True,
            "submission": submission
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/submissions/<submission_id>/grade', methods=['POST'])
def grade_existing_submission(submission_id):
    """Grade a specific submission"""
    try:
        submission = next((s for s in STUDENT_SUBMISSIONS if s['id'] == submission_id), None)
        if not submission:
            return jsonify({
                "success": False,
                "error": "Submission not found"
            }), 404
        
        if submission['status'] != 'pending_grading':
            return jsonify({
                "success": False,
                "error": "Submission already graded"
            }), 400
        
        # Generate AI grading for the submission
        rubric = RUBRICS[submission['assignment_type']]
        questions = []
        total_score = 0
        
        for question in rubric['questions']:
            # Find the student's answer for this question
            student_q = next((q for q in submission['questions'] if q['id'] == question['id']), None)
            student_answer = student_q['student_answer'] if student_q else "No answer provided"
            
            # Generate realistic score and feedback
            base_score = random.randint(6, question['max_points'])
            score = min(question['max_points'], max(0, base_score + random.randint(-2, 1)))
            
            # Generate feedback based on score
            if score >= question['max_points'] * 0.9:
                feedback = "Excellent work! Perfect solution."
            elif score >= question['max_points'] * 0.8:
                feedback = "Very good! Minor issues but overall correct approach."
            elif score >= question['max_points'] * 0.7:
                feedback = "Good work! Some errors but shows understanding."
            elif score >= question['max_points'] * 0.6:
                feedback = "Needs improvement. Check your work and try again."
            else:
                feedback = "Incorrect approach. Please review the concepts."
            
            questions.append({
                "question_id": question['id'],
                "description": question['description'],
                "max_points": question['max_points'],
                "student_answer": student_answer,
                "score": score,
                "feedback": feedback
            })
            
            total_score += score
        
        max_total = sum(q['max_points'] for q in questions)
        percentage = round((total_score / max_total) * 100, 1)
        
        # Update submission status
        submission['status'] = 'graded'
        submission['questions'] = questions
        submission['total_score'] = total_score
        submission['max_total'] = max_total
        submission['percentage'] = percentage
        submission['graded_at'] = "2024-01-21T00:00:00Z"
        submission['graded_by'] = "TA_001"
        
        return jsonify({
            "success": True,
            "grading_result": {
                "submission_id": submission_id,
                "student_name": submission['student_name'],
                "filename": submission['filename'],
                "assignment_type": submission['assignment_type'],
                "questions": questions,
                "total_score": total_score,
                "max_total": max_total,
                "percentage": percentage
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/submissions/<submission_id>/release', methods=['POST'])
def release_grades(submission_id):
    """Release grades to student"""
    try:
        submission = next((s for s in STUDENT_SUBMISSIONS if s['id'] == submission_id), None)
        if not submission:
            return jsonify({
                "success": False,
                "error": "Submission not found"
            }), 404
        
        if submission['status'] != 'graded':
            return jsonify({
                "success": False,
                "error": "Submission not graded yet"
            }), 400
        
        submission['status'] = 'released'
        submission['released_at'] = "2024-01-21T00:00:00Z"
        
        return jsonify({
            "success": True,
            "message": "Grades released to student"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
