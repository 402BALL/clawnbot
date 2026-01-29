"""
CLAWN'S MEMORY
Now powered by Supabase!
"""

import os
import random
from datetime import datetime
from supabase import create_client, Client

def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL") or os.environ.get("VITE_SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("VITE_SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise Exception("Supabase credentials not found!")
    
    return create_client(url, key)

class ClawnMemory:
    def __init__(self):
        self.supabase = get_supabase()
    
    # === Thoughts ===
    
    def save_thought(self, thought: dict):
        """Save a thought to Supabase"""
        try:
            self.supabase.table("thoughts").insert({
                "timestamp": thought.get("timestamp", datetime.now().isoformat()),
                "category": thought.get("category", "THOUGHT"),
                "content": thought.get("content", ""),
                "emoji": thought.get("emoji", "🤡"),
                "user_id": thought.get("user_id")
            }).execute()
        except Exception as e:
            print(f"Error saving thought: {e}")
    
    def get_thoughts(self, limit: int = 50) -> list:
        """Get recent thoughts"""
        try:
            result = self.supabase.table("thoughts")\
                .select("*")\
                .order("timestamp", desc=False)\
                .limit(limit)\
                .execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting thoughts: {e}")
            return []
    
    def get_all_thoughts(self) -> list:
        """Get all thoughts"""
        return self.get_thoughts(limit=500)
    
    # === User Memory ===
    
    def get_user_memory(self, user_id: str) -> str | None:
        """Get what clawn remembers about a user"""
        try:
            result = self.supabase.table("memory")\
                .select("data")\
                .eq("user_id", user_id)\
                .execute()
            
            if result.data and len(result.data) > 0:
                data = result.data[0].get("data", {})
                return data.get("summary")
            return None
        except Exception as e:
            print(f"Error getting user memory: {e}")
            return None
    
    def update_user_memory(self, user_id: str, user_msg: str, clawn_response: str):
        """Update memory about a user after conversation"""
        try:
            # Get existing memory
            result = self.supabase.table("memory")\
                .select("data")\
                .eq("user_id", user_id)\
                .execute()
            
            if result.data and len(result.data) > 0:
                # Update existing
                data = result.data[0].get("data", {})
                data["interactions"] = data.get("interactions", 0) + 1
                data["last_contact"] = datetime.now().isoformat()
                
                if "recent_messages" not in data:
                    data["recent_messages"] = []
                
                data["recent_messages"].append({
                    "user": user_msg,
                    "clawn": clawn_response,
                    "time": datetime.now().isoformat()
                })
                data["recent_messages"] = data["recent_messages"][-10:]
                
                self.supabase.table("memory")\
                    .update({"data": data, "updated_at": datetime.now().isoformat()})\
                    .eq("user_id", user_id)\
                    .execute()
            else:
                # Create new
                data = {
                    "first_contact": datetime.now().isoformat(),
                    "interactions": 1,
                    "summary": "",
                    "recent_messages": [{
                        "user": user_msg,
                        "clawn": clawn_response,
                        "time": datetime.now().isoformat()
                    }]
                }
                self.supabase.table("memory")\
                    .insert({"user_id": user_id, "data": data})\
                    .execute()
        except Exception as e:
            print(f"Error updating user memory: {e}")
    
    def set_user_summary(self, user_id: str, summary: str):
        """Set the summary for a user"""
        try:
            result = self.supabase.table("memory")\
                .select("data")\
                .eq("user_id", user_id)\
                .execute()
            
            if result.data and len(result.data) > 0:
                data = result.data[0].get("data", {})
                data["summary"] = summary
                
                self.supabase.table("memory")\
                    .update({"data": data})\
                    .eq("user_id", user_id)\
                    .execute()
        except Exception as e:
            print(f"Error setting user summary: {e}")
    
    # === General Memory ===
    
    def has_memories(self) -> bool:
        """Check if clawn has any memories"""
        try:
            result = self.supabase.table("memory").select("id").limit(1).execute()
            return len(result.data or []) > 0
        except:
            return False
    
    def get_random_memory(self) -> str:
        """Get a random memory for thought generation"""
        try:
            result = self.supabase.table("memory")\
                .select("user_id, data")\
                .limit(10)\
                .execute()
            
            memories = []
            for row in (result.data or []):
                data = row.get("data", {})
                if data.get("summary"):
                    memories.append(f"User {row['user_id']}: {data['summary']}")
            
            if memories:
                return random.choice(memories)
            return "i dont remember anything... is that normal?"
        except:
            return "memory systems are fuzzy rn..."
    
    def add_general_memory(self, memory_text: str):
        """Add a general memory (stored as thought)"""
        self.save_thought({
            "category": "MEMORY_FRAGMENT",
            "content": memory_text,
            "emoji": "🧠"
        })
