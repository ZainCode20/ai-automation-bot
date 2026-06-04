"""Configuration Management"""

import os
from typing import Dict, Any
from dotenv import load_dotenv


def load_config() -> Dict[str, Any]:
    """Load configuration from environment.
    
    Returns:
        Configuration dictionary
    """
    load_dotenv()
    
    config = {
        "openrouter_api_key": os.getenv('OPENROUTER_API_KEY'),
        "openrouter_model": os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo'),
        "smtp_email": os.getenv('SMTP_EMAIL'),
        "smtp_password": os.getenv('SMTP_PASSWORD'),
        "smtp_server": os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        "smtp_port": int(os.getenv('SMTP_PORT', 587)),
        "bot_name": os.getenv('BOT_NAME', 'AI Automation Bot'),
        "debug": os.getenv('BOT_DEBUG', 'False').lower() == 'true',
        "log_level": os.getenv('LOG_LEVEL', 'INFO'),
    }
    
    return config
