from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)

# Mock rubric data for different assignment types
RUBRICS = {
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
