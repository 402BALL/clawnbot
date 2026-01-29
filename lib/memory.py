"""
CLAWN'S MEMORY
Where clawn stores important information like "that guy likes pizza"
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

# For local dev
DATA_DIR = Path(__file__).parent.parent / "data"

class ClawnMemory:
    def __init__(self):
        self.memory_file = DATA_DIR / "memory.json"
        self.thoughts_file = DATA_DIR / "thoughts.json"
        self._ensure_files()
        
    def _ensure_files(self):
        """Make sure our memory files exist"""
        DATA_DIR.mkdir(exist_ok=True)
        
        if not self.memory_file.exists():
            self._save_memory({"users": {}, "general": []})
            
        if not self.thoughts_file.exists():
            self._save_thoughts([])
    
    def _load_memory(self) -> dict:
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": {}, "general": []}
    
    def _save_memory(self, data: dict):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_thoughts(self) -> list:
        try:
            with open(self.thoughts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_thoughts(self, data: list):
        with open(self.thoughts_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # === User Memory ===
    
    def get_user_memory(self, user_id: str) -> str | None:
        """Get what clawn remembers about a user"""
        memory = self._load_memory()
        user_data = memory["users"].get(user_id)
        if user_data:
            return user_data.get("summary", None)
        return None
    
    def update_user_memory(self, user_id: str, user_msg: str, clawn_response: str):
        """Update memory about a user after conversation"""
        memory = self._load_memory()
        
        if user_id not in memory["users"]:
            memory["users"][user_id] = {
                "first_contact": datetime.now().isoformat(),
                "interactions": 0,
                "summary": "",
                "facts": []
            }
        
        user_data = memory["users"][user_id]
        user_data["interactions"] += 1
        user_data["last_contact"] = datetime.now().isoformat()
        
        # Store recent exchange
        if "recent_messages" not in user_data:
            user_data["recent_messages"] = []
        
        user_data["recent_messages"].append({
            "user": user_msg,
            "clawn": clawn_response,
            "time": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages
        user_data["recent_messages"] = user_data["recent_messages"][-10:]
        
        self._save_memory(memory)
    
    def set_user_summary(self, user_id: str, summary: str):
        """Set the summary for a user (called after AI generates it)"""
        memory = self._load_memory()
        if user_id in memory["users"]:
            memory["users"][user_id]["summary"] = summary
            self._save_memory(memory)
    
    # === General Memory ===
    
    def has_memories(self) -> bool:
        """Check if clawn has any memories"""
        memory = self._load_memory()
        return len(memory["users"]) > 0 or len(memory["general"]) > 0
    
    def get_random_memory(self) -> str:
        """Get a random memory for thought generation"""
        memory = self._load_memory()
        
        memories = []
        
        # Add user summaries
        for user_id, data in memory["users"].items():
            if data.get("summary"):
                memories.append(f"User {user_id}: {data['summary']}")
        
        # Add general memories
        memories.extend(memory["general"])
        
        if memories:
            return random.choice(memories)
        return "i dont remember anything... is that normal?"
    
    def add_general_memory(self, memory_text: str):
        """Add a general memory"""
        memory = self._load_memory()
        memory["general"].append({
            "text": memory_text,
            "time": datetime.now().isoformat()
        })
        # Keep only last 50 general memories
        memory["general"] = memory["general"][-50:]
        self._save_memory(memory)
    
    # === Thoughts Log ===
    
    def save_thought(self, thought: dict):
        """Save a thought to the log"""
        thoughts = self._load_thoughts()
        thoughts.append(thought)
        
        # Keep last 500 thoughts
        thoughts = thoughts[-500:]
        self._save_thoughts(thoughts)
    
    def get_thoughts(self, limit: int = 50) -> list:
        """Get recent thoughts"""
        thoughts = self._load_thoughts()
        return thoughts[-limit:]
    
    def get_all_thoughts(self) -> list:
        """Get all thoughts"""
        return self._load_thoughts()

