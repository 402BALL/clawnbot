"""
THOUGHTS API ENDPOINT
"""

from http.server import BaseHTTPRequestHandler
import json
import os

# Direct Supabase REST API call (no SDK needed)
import urllib.request

def get_thoughts():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        return []
    
    api_url = f"{url}/rest/v1/thoughts?select=*&order=timestamp.asc&limit=100"
    
    req = urllib.request.Request(api_url)
    req.add_header("apikey", key)
    req.add_header("Authorization", f"Bearer {key}")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error: {e}")
        return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            thoughts = get_thoughts()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(thoughts).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
