"""
Initialize the AI Agent System in the Flask App
Execute this to set up the agent engine integration
"""
import logging
from flask import Flask
from ai_agent_engine import initialize_agent_engine

logger = logging.getLogger(__name__)

def setup_agent_system(app: Flask):
    """Set up the AI agent system with Flask app context"""
    try:
        with app.app_context():
            # Initialize the agent engine
            initialize_agent_engine()
            logger.info("✅ AI Agent System initialized successfully")
            
            # Add navigation menu item for agents
            @app.context_processor
            def inject_agent_menu():
                return {
                    'agent_chat_available': True,
                    'free_agents_count': 2,  # Customer Service + Marketing Content
                    'premium_agents_count': 0  # To be added later
                }
                
            return True
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI Agent System: {e}")
        return False

if __name__ == "__main__":
    # Test initialization
    from app import app
    success = setup_agent_system(app)
    if success:
        print("🚀 AI Agent System ready for production")
    else:
        print("❌ AI Agent System initialization failed")