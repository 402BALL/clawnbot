"""
CLAWNBOT BACKGROUND THINKER
Runs locally, sends thoughts to Vercel via API
"""

import time
import random
import requests
from datetime import datetime

# Your Vercel URL
VERCEL_URL = "https://clawnbotx.vercel.app"

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def main():
    log("CLAWNBOT THINKER STARTED")
    log(f"Sending thoughts to: {VERCEL_URL}")
    log("Thoughts will be generated every 10-15 minutes")
    print("-" * 50)
    
    while True:
        try:
            # Generate a thought via Vercel API
            log("Generating thought...")
            response = requests.post(f"{VERCEL_URL}/api/think", timeout=60)
            
            if response.status_code == 200:
                thought = response.json()
                category = thought.get('category', 'THOUGHT')
                content_preview = thought.get('content', '')[:60] + "..."
                
                log(f"NEW THOUGHT: [{category}]")
                log(f"  {content_preview}")
            else:
                log(f"ERROR: Status {response.status_code}")
                log(f"  {response.text[:100]}")
            
            print("-" * 50)
            
            # Wait 10-15 minutes before next thought
            wait_time = random.randint(600, 900)  # 10-15 minutes
            log(f"Next thought in {wait_time // 60} minutes...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            log("Thinker stopped by user")
            break
        except Exception as e:
            log(f"ERROR: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
