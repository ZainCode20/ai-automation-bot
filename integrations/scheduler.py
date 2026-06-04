"""Task Scheduling Handler"""

from typing import Dict, Any, Callable
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class TaskScheduler:
    """Handles task scheduling and reminders."""
    
    def __init__(self):
        """Initialize task scheduler."""
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.tasks: Dict[str, Any] = {}
    
    def schedule_task(self, task_name: str, func: Callable, trigger: str, **kwargs) -> str:
        """Schedule a task.
        
        Args:
            task_name: Name of the task
            func: Function to execute
            trigger: Trigger type (cron, date, interval)
            **kwargs: Trigger parameters
            
        Returns:
            Confirmation message
        """
        try:
            self.scheduler.add_job(
                func,
                trigger,
                id=task_name,
                **kwargs
            )
            self.tasks[task_name] = {
                "created": datetime.now(),
                "status": "active"
            }
            return f"Task '{task_name}' scheduled successfully"
        except Exception as e:
            return f"Error scheduling task: {str(e)}"
    
    def cancel_task(self, task_name: str) -> bool:
        """Cancel a scheduled task.
        
        Args:
            task_name: Name of the task
            
        Returns:
            Success status
        """
        try:
            self.scheduler.remove_job(task_name)
            if task_name in self.tasks:
                del self.tasks[task_name]
            return True
        except:
            return False
