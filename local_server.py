#!/usr/bin/env python3
"""
Local development server for AI-Assisted Grading Platform
This simulates the Vercel serverless functions locally
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse, parse_qs
import sys

# Import the API logic from our serverless function
sys.path.append('./api')
from grade import RUBRICS, STUDENT_SUBMISSIONS, simulate_ai_grading

class LocalAPIHandler(BaseHTTPRequestHandler):
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

def run_server(port=5001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, LocalAPIHandler)
    print(f"🚀 Local API server running on http://localhost:{port}")
    print(f"📡 API endpoints available at http://localhost:{port}/api/")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
