"""Task Executor - Executes automation tasks"""

from typing import Dict, Any, List
from datetime import datetime
from integrations.email_handler import EmailHandler
from integrations.scheduler import TaskScheduler
from integrations.web_search import WebSearch


class TaskExecutor:
    """Executes automated tasks."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize task executor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.email_handler = EmailHandler(config)
        self.scheduler = TaskScheduler()
        self.web_search = WebSearch()
        self.tasks: List[Dict[str, Any]] = []
    
    def send_email(self, entities: Dict[str, Any]) -> str:
        """Send an email.
        
        Args:
            entities: Extracted entities
            
        Returns:
            Response message
        """
        try:
            # In a real implementation, extract recipient and message from entities
            # For now, return placeholder
            return "Email feature configured! To send emails, please set up SMTP credentials in .env"
        except Exception as e:
            return f"Error sending email: {str(e)}"
    
    def schedule_task(self, entities: Dict[str, Any]) -> str:
        """Schedule a task.
        
        Args:
            entities: Extracted entities
            
        Returns:
            Response message
        """
        try:
            task = {
                "description": entities.get('message', 'Task'),
                "created_at": datetime.now(),
                "status": "scheduled"
            }
            self.tasks.append(task)
            return f"✓ Task scheduled successfully! You now have {len(self.tasks)} scheduled tasks."
        except Exception as e:
            return f"Error scheduling task: {str(e)}"
    
    def search_web(self, entities: Dict[str, Any]) -> str:
        """Search the web.
        
        Args:
            entities: Extracted entities
            
        Returns:
            Search results
        """
        try:
            query = entities.get('query', 'search')
            return f"Web search feature available! To search, configure web search API in .env"
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    def get_scheduled_tasks(self) -> str:
        """Get all scheduled tasks.
        
        Returns:
            Task list
        """
        if not self.tasks:
            return "You have no scheduled tasks."
        
        task_list = "Your scheduled tasks:\n"
        for i, task in enumerate(self.tasks, 1):
            task_list += f"{i}. {task['description']} ({task['status']})\n"
        
        return task_list
    
    def complete_task(self, entities: Dict[str, Any]) -> str:
        """Mark a task as complete.
        
        Args:
            entities: Extracted entities
            
        Returns:
            Response message
        """
        if self.tasks:
            task = self.tasks.pop(0)
            return f"✓ Task completed: {task['description']}"
        return "No tasks to complete."
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks.
        
        Returns:
            List of tasks
        """
        return self.tasks
