"""Chat Engine - Natural Language Understanding and Response Generation"""

import os
import requests
from typing import Dict, Any, List
from datetime import datetime
from .memory import ConversationMemory
from .task_executor import TaskExecutor


class ChatEngine:
    """Main chat engine for processing user input and generating responses."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the chat engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.memory = ConversationMemory()
        
        # Setup OpenRouter
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Verify API key exists
        if not self.api_key:
            raise ValueError(
                "❌ OPENROUTER_API_KEY not found!\n"
                "Please add it to your .env file:\n"
                "OPENROUTER_API_KEY=sk-or-your_key_here"
            )
        
        # Initialize task executor (do this after all validations)
        try:
            self.task_executor = TaskExecutor(config)
        except Exception as e:
            print(f"⚠️  Warning: Task executor initialization failed: {e}")
            self.task_executor = None
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response.
        
        Args:
            user_input: Raw user input text
            
        Returns:
            Response string
        """
        # Add to memory
        self.memory.add_user_message(user_input)
        
        # Extract intent and entities
        intent, entities = self._extract_intent(user_input)
        
        # Execute task based on intent (if task executor is available)
        response = None
        if self.task_executor:
            try:
                if intent == 'send_email':
                    response = self.task_executor.send_email(entities)
                elif intent == 'schedule_task':
                    response = self.task_executor.schedule_task(entities)
                elif intent == 'web_search':
                    response = self.task_executor.search_web(entities)
                elif intent == 'get_tasks':
                    response = self.task_executor.get_scheduled_tasks()
                elif intent == 'complete_task':
                    response = self.task_executor.complete_task(entities)
            except Exception as e:
                print(f"⚠️  Task execution error: {e}")
                response = None
        
        # If no task response, use general response
        if response is None:
            response = self._generate_response(user_input)
        
        # Add to memory
        self.memory.add_bot_message(response)
        
        return response
    
    def _extract_intent(self, user_input: str) -> tuple:
        """Extract intent and entities from user input.
        
        Args:
            user_input: User input text
            
        Returns:
            Tuple of (intent, entities)
        """
        input_lower = user_input.lower()
        
        # Simple intent recognition (can be enhanced with ML)
        if any(word in input_lower for word in ['email', 'send', 'mail']):
            return 'send_email', {'message': user_input}
        elif any(word in input_lower for word in ['schedule', 'remind', 'task', 'reminder']):
            return 'schedule_task', {'message': user_input}
        elif any(word in input_lower for word in ['search', 'find', 'what', 'tell']):
            return 'web_search', {'query': user_input}
        elif any(word in input_lower for word in ['tasks', 'scheduled', 'upcoming']):
            return 'get_tasks', {}
        elif any(word in input_lower for word in ['complete', 'done', 'finish']):
            return 'complete_task', {'message': user_input}
        
        return 'general', {'message': user_input}
    
    def _generate_response(self, user_input: str) -> str:
        """Generate a response using OpenRouter API.
        
        Args:
            user_input: User input text
            
        Returns:
            Generated response
        """
        try:
            # Verify API key is available
            if not self.api_key:
                return "❌ Error: OPENROUTER_API_KEY is not configured. Please set it in your .env file."
            
            # Prepare conversation history for context
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI automation assistant. Help users automate their tasks and manage their time efficiently."
                }
            ]
            
            # Add recent conversation history (last 5 exchanges)
            for msg in self.memory.get_recent_messages(5):
                messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user_input})
            
            # Call OpenRouter API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/ZainCode20/ai-automation-bot",
                "X-Title": "AI Automation Bot",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 0.9,
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            else:
                return "Sorry, I couldn't generate a response. Please try again."
        
        except requests.exceptions.Timeout:
            return "⏱️ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "🔌 Connection error. Please check your internet connection and try again."
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return "🔐 Authentication failed. Please check your OPENROUTER_API_KEY in .env file."
            elif e.response.status_code == 429:
                return "⚠️ Rate limit exceeded. Please wait a moment and try again."
            elif e.response.status_code == 404:
                return f"❌ Model not found: {self.model}. Please check your OPENROUTER_MODEL setting."
            else:
                return f"❌ API Error ({e.response.status_code}): {str(e)}"
        except Exception as e:
            return f"❌ Error: {str(e)}. Please try again."
    
    def get_status(self) -> str:
        """Get current bot status.
        
        Returns:
            Status message
        """
        task_count = 0
        if self.task_executor:
            task_count = len(self.task_executor.get_all_tasks())
        return f"✓ Bot is running | Using {self.model} | {task_count} scheduled tasks | Ready to help!"
    
    def get_conversation_history(self) -> str:
        """Get conversation history summary.
        
        Returns:
            History summary
        """
        history = self.memory.get_history_summary()
        return history if history else "No conversation history yet."
    
    def clear_history(self):
        """Clear conversation history."""
        self.memory.clear()
