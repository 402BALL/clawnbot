"""
CLAWNBOT BACKGROUND THINKER
Runs in background, generates thoughts every 10-15 minutes
"""

import time
import random
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from lib.brain import get_brain
from lib.memory import ClawnMemory

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def main():
    log("CLAWNBOT THINKER STARTED")
    log("Thoughts will be generated every 10-15 minutes")
    print("-" * 50)
    
    brain = get_brain()
    memory = ClawnMemory()
    
    while True:
        try:
            # Generate a thought
            log("Generating thought...")
            thought = brain.think()
            memory.save_thought(thought)
            
            category = thought.get('category', 'THOUGHT')
            content_preview = thought.get('content', '')[:50] + "..."
            
            log(f"NEW THOUGHT: [{category}]")
            log(f"  {content_preview}")
            print("-" * 50)
            
            # Wait 10-15 minutes before next thought
            wait_time = random.randint(600, 900)  # 10-15 minutes in seconds
            log(f"Next thought in {wait_time // 60} minutes...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            log("Thinker stopped by user")
            break
        except Exception as e:
            log(f"ERROR: {e}")
            time.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    main()

