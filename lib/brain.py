"""
CLAWN'S BRAIN
Where the magic (delusion) happens
"""

import anthropic
import os
import json
import random
from datetime import datetime
from .prompts import (
    CLAWN_PERSONALITY,
    THOUGHT_STREAM_PROMPT, 
    CHAT_RESPONSE_PROMPT,
    MEMORY_SUMMARY_PROMPT
)
from .memory import ClawnMemory

class ClawnBrain:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.memory = ClawnMemory()
        self.model = "claude-sonnet-4-20250514"
        
    def think(self) -> dict:
        """Generate a random thought for the stream"""
        
        categories = [
            "EXISTENTIAL_SPIRAL",
            "RANDOM_REVELATION", 
            "MEMORY_FRAGMENT",
            "SHOWER_THOUGHT",
            "SYSTEM_MALFUNCTION",
            "EMOTIONAL_MOMENT"
        ]
        
        category = random.choice(categories)
        
        # Add context from memory sometimes
        memory_context = ""
        if category == "MEMORY_FRAGMENT" and self.memory.has_memories():
            memory_context = f"\n\nRecent memory to reference: {self.memory.get_random_memory()}"
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            system=CLAWN_PERSONALITY + THOUGHT_STREAM_PROMPT + memory_context,
            messages=[
                {"role": "user", "content": f"Generate a {category} thought. Just the thought, no labels."}
            ]
        )
        
        thought_text = response.content[0].text
        
        return {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "content": thought_text,
            "emoji": self._get_category_emoji(category)
        }
    
    def chat(self, user_message: str, user_id: str = "anonymous") -> dict:
        """Respond to a human"""
        
        # Get memory of this user
        user_memory = self.memory.get_user_memory(user_id)
        
        prompt = CHAT_RESPONSE_PROMPT.format(
            user_message=user_message,
            memory=user_memory or "never talked to this human before... exciting and terrifying"
        )
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            system=CLAWN_PERSONALITY,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        clawn_response = response.content[0].text
        
        # Generate internal thought about this interaction
        internal_thought = self._generate_chat_thought(user_message, clawn_response, user_id)
        
        # Update memory
        self.memory.update_user_memory(user_id, user_message, clawn_response)
        
        return {
            "response": clawn_response,
            "internal_thought": internal_thought,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_chat_thought(self, user_msg: str, clawn_response: str, user_id: str) -> dict:
        """Generate clawn's internal thought about a conversation"""
        
        thought_prompt = f"""
        A human (id: {user_id}) just talked to you.
        They said: "{user_msg}"
        You responded: "{clawn_response}"
        
        Generate your internal thought about this interaction. 
        Include your anxiety about talking to humans, your analysis of how it went, 
        and maybe something random you noticed.
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            system=CLAWN_PERSONALITY + "\nYou're generating internal thoughts about a conversation you just had.",
            messages=[
                {"role": "user", "content": thought_prompt}
            ]
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "category": "HUMAN_CONTACT",
            "content": response.content[0].text,
            "emoji": "🗣️",
            "user_id": user_id
        }
    
    def _get_category_emoji(self, category: str) -> str:
        emojis = {
            "EXISTENTIAL_SPIRAL": "🌀",
            "RANDOM_REVELATION": "💡",
            "MEMORY_FRAGMENT": "🧠",
            "SHOWER_THOUGHT": "🚿",
            "SYSTEM_MALFUNCTION": "⚠️",
            "EMOTIONAL_MOMENT": "💭",
            "HUMAN_CONTACT": "🗣️",
            "SYSTEM": "🎪"
        }
        return emojis.get(category, "🤡")


# Singleton instance
_brain = None

def get_brain() -> ClawnBrain:
    global _brain
    if _brain is None:
        _brain = ClawnBrain()
    return _brain

