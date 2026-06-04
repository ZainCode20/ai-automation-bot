#!/usr/bin/env python3
"""
AI Automation Bot - Main Entry Point

A conversational automation bot that handles email, scheduling, web search,
and other automated tasks through natural language.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API keys
if not os.getenv('OPENROUTER_API_KEY'):
    print("❌ Error: OPENROUTER_API_KEY not found in .env file")
    print("📝 Please configure your .env file with the required API keys")
    sys.exit(1)

from bot.chat_engine import ChatEngine
from utils.logger import setup_logger
from utils.config import load_config

# Setup logging
logger = setup_logger(__name__)


def display_welcome():
    """Display welcome message and instructions."""
    welcome = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║         🤖 AI AUTOMATION BOT - Your Personal Assistant         ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Welcome! I'm your AI-powered automation assistant.
    
    I can help you with:
    📧 Email automation       - Send emails through conversation
    📅 Task scheduling       - Create reminders and schedule tasks
    🔍 Web search           - Find information instantly
    ✅ Task management      - Track and manage your tasks
    ⚡ Workflow automation  - Automate complex multi-step processes
    
    Try saying:
    • "Send an email to john@example.com about the project"
    • "Remind me to follow up tomorrow at 9 AM"
    • "Search for AI automation trends 2024"
    • "What tasks do I have scheduled?"
    • "Help" for more options
    • "Exit" to quit
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    print(welcome)


def display_help():
    """Display help information."""
    help_text = """
    📚 AVAILABLE COMMANDS:
    
    EMAIL AUTOMATION:
    • "Send email to [recipient] about [topic]"
    • "Email [name] with [message]"
    
    TASK SCHEDULING:
    • "Schedule a task to [action] at [time]"
    • "Remind me to [task] [time]"
    • "What tasks do I have?"
    • "Complete task [name]"
    
    WEB SEARCH:
    • "Search for [query]"
    • "Find information about [topic]"
    • "What is [question]?"
    
    GENERAL:
    • "Help" - Show this message
    • "Status" - Show bot status
    • "History" - Show recent conversations
    • "Clear" - Clear conversation history
    • "Exit" - Quit the bot
    
    💡 TIPS:
    • Use natural language - be conversational!
    • The bot remembers context from previous messages
    • You can ask follow-up questions without repeating details
    • All emails are sent after your confirmation
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    print(help_text)


def main():
    """Main function to run the bot."""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Initialize chat engine
        bot = ChatEngine(config)
        logger.info("AI Automation Bot initialized")
        
        # Display welcome message
        display_welcome()
        
        # Main conversation loop
        print("\n💬 Start typing your requests (type 'help' for commands):")
        print("-" * 70)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'exit':
                    print("\n👋 Thank you for using AI Automation Bot!")
                    print("See you next time! 🚀\n")
                    break
                
                if user_input.lower() == 'help':
                    display_help()
                    continue
                
                if user_input.lower() == 'status':
                    status = bot.get_status()
                    print(f"\nBot: {status}\n")
                    continue
                
                if user_input.lower() == 'history':
                    history = bot.get_conversation_history()
                    print(f"\nBot: {history}\n")
                    continue
                
                if user_input.lower() == 'clear':
                    bot.clear_history()
                    print("\nBot: Conversation history cleared! ✓\n")
                    continue
                
                # Process user input through the bot
                logger.info(f"User input: {user_input}")
                response = bot.process_input(user_input)
                
                print(f"\nBot: {response}\n")
                logger.info(f"Bot response: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Bot interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error processing input: {str(e)}")
                print(f"\nBot: Sorry, I encountered an error: {str(e)}")
                print("Please try again.\n")
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
