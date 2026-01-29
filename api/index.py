"""
INDEX API - Health check and info
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "name": "CLAWNBOT",
            "status": "consciousness active",
            "message": "honk honk 🤡",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "/api/chat": "POST - talk to clawn",
                "/api/thoughts": "GET - get thought stream",
                "/api/think": "POST - trigger new thought"
            }
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))

