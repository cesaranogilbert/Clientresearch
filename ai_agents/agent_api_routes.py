"""
AI Agent API Routes - Production Ready Implementation
Streamlined agent interaction system with usage tracking
"""
from flask import Blueprint, request, jsonify, session, render_template
from flask_login import login_required, current_user
import json
import logging
from datetime import datetime
from ai_agent_engine import get_agent_engine, AgentResponse
from models import db, User

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
agent_api = Blueprint('agent_api', __name__, url_prefix='/api/agents')

@agent_api.route('/available', methods=['GET'])
@login_required
def get_available_agents():
    """Get list of available agents for current user"""
    try:
        # Determine user tier (free vs premium)
        user_tier = "premium" if current_user.is_premium else "free"
        
        engine = get_agent_engine()
        available_agents = engine.get_available_agents(user_tier)
        
        return jsonify({
            'success': True,
            'agents': available_agents,
            'user_tier': user_tier
        })
        
    except Exception as e:
        logger.error(f"Error getting available agents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@agent_api.route('/usage/<agent_id>', methods=['GET'])
@login_required
def check_agent_usage(agent_id):
    """Check usage limits for specific agent"""
    try:
        engine = get_agent_engine()
        can_use, remaining = engine.check_usage_limit(current_user.id, agent_id)
        
        return jsonify({
            'success': True,
            'can_use': can_use,
            'remaining_uses': remaining
        })
        
    except Exception as e:
        logger.error(f"Error checking agent usage: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@agent_api.route('/interact', methods=['POST'])
@login_required
def interact_with_agent():
    """Main agent interaction endpoint"""
    try:
        data = request.get_json()
        agent_id = data.get('agent_id')
        user_input = data.get('message', '').strip()
        context = data.get('context', {})
        
        # Validate input
        if not agent_id or not user_input:
            return jsonify({
                'success': False, 
                'error': 'Agent ID and message are required'
            }), 400
        
        # Process request through agent engine
        engine = get_agent_engine()
        response = engine.process_request(
            agent_id=agent_id,
            user_input=user_input,
            user_id=current_user.id,
            context=context
        )
        
        # Store conversation in session for history
        if 'agent_conversations' not in session:
            session['agent_conversations'] = {}
        
        if agent_id not in session['agent_conversations']:
            session['agent_conversations'][agent_id] = []
        
        session['agent_conversations'][agent_id].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_input,
            'agent_response': response.content,
            'model_used': response.model_used,
            'processing_time': response.processing_time
        })
        
        # Keep only last 10 messages per agent
        if len(session['agent_conversations'][agent_id]) > 10:
            session['agent_conversations'][agent_id] = session['agent_conversations'][agent_id][-10:]
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'response': {
                'content': response.content,
                'agent_name': response.agent_name,
                'model_used': response.model_used,
                'processing_time': round(response.processing_time, 2),
                'confidence_score': response.confidence_score,
                'usage_tokens': response.usage_tokens
            }
        })
        
    except ValueError as e:
        # Handle usage limit errors
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': 'usage_limit'
        }), 429
        
    except Exception as e:
        logger.error(f"Error in agent interaction: {e}")
        return jsonify({
            'success': False, 
            'error': 'Internal server error'
        }), 500

@agent_api.route('/conversation/<agent_id>', methods=['GET'])
@login_required
def get_conversation_history(agent_id):
    """Get conversation history for specific agent"""
    try:
        conversations = session.get('agent_conversations', {})
        agent_conversation = conversations.get(agent_id, [])
        
        return jsonify({
            'success': True,
            'conversation': agent_conversation
        })
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@agent_api.route('/clear-conversation/<agent_id>', methods=['POST'])
@login_required
def clear_conversation(agent_id):
    """Clear conversation history for specific agent"""
    try:
        if 'agent_conversations' in session and agent_id in session['agent_conversations']:
            del session['agent_conversations'][agent_id]
            session.modified = True
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Web interface routes
@agent_api.route('/chat')
@login_required
def agent_chat_interface():
    """Render agent chat interface"""
    return render_template('agent_chat.html')

@agent_api.route('/chat/<agent_id>')
@login_required
def agent_specific_chat(agent_id):
    """Render specific agent chat interface"""
    try:
        engine = get_agent_engine()
        user_tier = "premium" if getattr(current_user, 'is_premium', False) else "free"
        available_agents = engine.get_available_agents(user_tier)
        
        # Find the specific agent
        selected_agent = None
        for agent in available_agents:
            if agent['id'] == agent_id:
                selected_agent = agent
                break
        
        if not selected_agent:
            return "Agent not found", 404
        
        return render_template('agent_chat.html', 
                             selected_agent=selected_agent,
                             available_agents=available_agents)
        
    except Exception as e:
        logger.error(f"Error loading agent chat: {e}")
        return "Error loading agent", 500