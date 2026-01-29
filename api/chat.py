"""
CHAT API ENDPOINT
For talking to Clawn
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.brain import get_brain
from lib.memory import ClawnMemory

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '')
            user_id = data.get('user_id', 'anonymous')
            
            if not message:
                self.send_error(400, "No message provided")
                return
            
            # Get Clawn's response
            brain = get_brain()
            result = brain.chat(message, user_id)
            
            # Save the internal thought to log
            memory = ClawnMemory()
            memory.save_thought(result['internal_thought'])
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "response": result['response'],
                "timestamp": result['timestamp']
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

