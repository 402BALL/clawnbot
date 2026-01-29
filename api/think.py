"""
THINK API ENDPOINT
Triggers Clawn to generate a new thought
Supports both GET (for Vercel Cron) and POST
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.brain import get_brain
from lib.memory import ClawnMemory

class handler(BaseHTTPRequestHandler):
    def _generate_thought(self):
        try:
            brain = get_brain()
            thought = brain.think()
            
            # Save thought
            memory = ClawnMemory()
            memory.save_thought(thought)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(thought).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_GET(self):
        """For Vercel Cron"""
        self._generate_thought()
    
    def do_POST(self):
        self._generate_thought()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
