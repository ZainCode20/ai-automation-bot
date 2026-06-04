"""Conversation Memory Management"""

from datetime import datetime
from typing import List, Dict, Any


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 50):
        """Initialize memory.
        
        Args:
            max_history: Maximum number of messages to store
        """
        self.messages: List[Dict[str, Any]] = []
        self.max_history = max_history
        self.user_preferences = {}
    
    def add_user_message(self, content: str):
        """Add a user message to memory.
        
        Args:
            content: Message content
        """
        self.messages.append({
            "role": "user",
            "content": content,
            "timestamp": datetime.now()
        })
        self._maintain_size()
    
    def add_bot_message(self, content: str):
        """Add a bot message to memory.
        
        Args:
            content: Message content
        """
        self.messages.append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now()
        })
        self._maintain_size()
    
    def get_recent_messages(self, count: int = 5) -> List[Dict[str, str]]:
        """Get recent messages.
        
        Args:
            count: Number of recent messages
            
        Returns:
            List of recent messages
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages[-count:]
        ]
    
    def get_history_summary(self) -> str:
        """Get a summary of conversation history.
        
        Returns:
            Summary string
        """
        if not self.messages:
            return "No conversation history."
        
        user_msgs = sum(1 for m in self.messages if m["role"] == "user")
        bot_msgs = sum(1 for m in self.messages if m["role"] == "assistant")
        
        return f"Conversation: {user_msgs} user messages, {bot_msgs} bot responses"
    
    def clear(self):
        """Clear all conversation history."""
        self.messages = []
        self.user_preferences = {}
    
    def _maintain_size(self):
        """Maintain maximum history size."""
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def set_preference(self, key: str, value: Any):
        """Store user preference.
        
        Args:
            key: Preference key
            value: Preference value
        """
        self.user_preferences[key] = value
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference.
        
        Args:
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value
        """
        return self.user_preferences.get(key, default)
