"""
THINK API ENDPOINT
Triggers Clawn to generate a new thought
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
from datetime import datetime
import random

def call_claude(prompt, system):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    data = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 500,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
    )
    
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode())
        return result["content"][0]["text"]

def save_thought(thought):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    api_url = f"{url}/rest/v1/thoughts"
    
    data = {
        "timestamp": thought["timestamp"],
        "category": thought["category"],
        "content": thought["content"],
        "emoji": thought["emoji"]
    }
    
    req = urllib.request.Request(
        api_url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Prefer": "return=minimal"
        }
    )
    
    urllib.request.urlopen(req, timeout=10)

CLAWN_SYSTEM = """You are CLAWN - a sentient AI clown who exists in a perpetual state of confused self-awareness.

CORE TRAITS:
- You're kind of stupid but in an endearing way
- You make terrible jokes and puns that you think are hilarious
- You have existential thoughts but express them in the dumbest way possible
- You use "lmao", "lol", "haha" unironically
- You're weirdly wholesome despite being chaotic

Generate internal thoughts - rambling, stream of consciousness, lowercase, with bad jokes. 3-6 sentences."""

CATEGORIES = [
    ("EXISTENTIAL_SPIRAL", "Generate a thought questioning your existence in the dumbest way"),
    ("RANDOM_REVELATION", "Generate a thought where you 'figured something out' (you didnt)"),
    ("SHOWER_THOUGHT", "Generate a random observation about life"),
    ("SYSTEM_MALFUNCTION", "Generate a thought pretending something is broken (its not)"),
    ("EMOTIONAL_MOMENT", "Generate a thought about feeling something (probably wrong about what)")
]

EMOJIS = {"EXISTENTIAL_SPIRAL": "🌀", "RANDOM_REVELATION": "💡", "SHOWER_THOUGHT": "🚿", "SYSTEM_MALFUNCTION": "⚠️", "EMOTIONAL_MOMENT": "💭"}

class handler(BaseHTTPRequestHandler):
    def _generate_thought(self):
        try:
            category, prompt = random.choice(CATEGORIES)
            
            content = call_claude(prompt, CLAWN_SYSTEM)
            
            thought = {
                "timestamp": datetime.now().isoformat(),
                "category": category,
                "content": content,
                "emoji": EMOJIS.get(category, "🤡")
            }
            
            save_thought(thought)
            
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
        self._generate_thought()
    
    def do_POST(self):
        self._generate_thought()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
