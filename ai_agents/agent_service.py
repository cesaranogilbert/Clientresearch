import json
import logging
import uuid
from datetime import datetime
from models import db, AIAgent, AgentCustomization, AgentConversation, User, Revenue
from ai_service import openai_client

def get_all_agents():
    """Get all active AI agents"""
    try:
        agents = AIAgent.query.all()
        return [{
            'id': agent.id,
            'name': agent.name,
            'description': agent.description,
            'category': agent.category,
            'pricing_tier': agent.pricing_tier or 'standard',
            'base_price': agent.base_price,
            'monthly_price': agent.monthly_price,
            'capabilities': agent.capabilities.split(', ') if agent.capabilities else []
        } for agent in agents]
    except Exception as e:
        logging.error(f"Error getting agents: {e}")
        return []

def get_agent_by_id(agent_id):
    """Get specific agent details"""
    try:
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return None
            
        return {
            'id': agent.id,
            'name': agent.name,
            'description': agent.description,
            'category': agent.category,
            'pricing_tier': agent.pricing_tier,
            'base_price': agent.base_price,
            'monthly_price': agent.monthly_price,
            'capabilities': agent.capabilities.split(', ') if agent.capabilities else [],
            'base_prompt': agent.base_prompt
        }
    except Exception as e:
        logging.error(f"Error getting agent {agent_id}: {e}")
        return None

def get_agents_by_category(category):
    """Get agents filtered by category"""
    try:
        agents = AIAgent.query.filter_by(category=category).all()
        return [get_agent_by_id(agent.id) for agent in agents]
    except Exception as e:
        logging.error(f"Error getting agents for category {category}: {e}")
        return []

def create_agent_customization(user_id, agent_id, custom_name, custom_prompt=None, branding_config=None):
    """Create a customized instance of an AI agent for a user"""
    try:
        agent = AIAgent.query.get(agent_id)
        user = User.query.get(user_id)
        
        if not agent or not user:
            return None
            
        # Generate unique API key for this customization
        api_key = str(uuid.uuid4())
        
        # Create customization record
        customization = AgentCustomization(
            user_id=user_id,
            agent_id=agent_id,
            custom_name=custom_name or agent.name,
            custom_prompt=custom_prompt or agent.base_prompt,
            branding_config=json.dumps(branding_config) if branding_config else None,
            api_key=api_key
        )
        
        db.session.add(customization)
        db.session.commit()
        
        return {
            'id': customization.id,
            'api_key': api_key,
            'custom_name': customization.custom_name,
            'deployment_url': f"/api/agents/{customization.id}/chat"
        }
        
    except Exception as e:
        logging.error(f"Error creating agent customization: {e}")
        db.session.rollback()
        return None

def get_user_agent_customizations(user_id):
    """Get all agent customizations for a user"""
    try:
        customizations = AgentCustomization.query.filter_by(user_id=user_id).all()
        result = []
        
        for custom in customizations:
            agent = AIAgent.query.get(custom.agent_id)
            result.append({
                'id': custom.id,
                'agent_name': agent.name if agent else 'Unknown',
                'custom_name': custom.custom_name,
                'api_key': custom.api_key,
                'deployment_url': f"/api/agents/{custom.id}/chat",
                'created_at': custom.created_at.strftime('%Y-%m-%d %H:%M'),
                'conversation_count': len(custom.conversations)
            })
            
        return result
    except Exception as e:
        logging.error(f"Error getting user customizations: {e}")
        return []

def chat_with_agent(customization_id, user_message, conversation_id=None):
    """Handle chat conversation with a customized agent"""
    try:
        customization = AgentCustomization.query.get(customization_id)
        if not customization:
            return None
            
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            
        # Get the custom prompt or fall back to base prompt
        system_prompt = customization.custom_prompt
        
        # Make OpenAI API call
        if not openai_client:
            return {
                'response': 'AI service is currently unavailable. Please check API configuration.',
                'conversation_id': conversation_id
            }
            
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        agent_response = response.choices[0].message.content
        
        # Save conversation to database
        conversation = AgentConversation(
            customization_id=customization_id,
            conversation_id=conversation_id,
            user_message=user_message,
            agent_response=agent_response
        )
        db.session.add(conversation)
        db.session.commit()
        
        return {
            'response': agent_response,
            'conversation_id': conversation_id
        }
        
    except Exception as e:
        logging.error(f"Error in agent chat: {e}")
        return {
            'response': 'Sorry, I encountered an error processing your message. Please try again.',
            'conversation_id': conversation_id or str(uuid.uuid4())
        }

def get_conversation_history(customization_id, limit=50):
    """Get conversation history for an agent customization"""
    try:
        conversations = AgentConversation.query.filter_by(
            customization_id=customization_id
        ).order_by(AgentConversation.created_at.desc()).limit(limit).all()
        
        return [{
            'user_message': conv.user_message,
            'agent_response': conv.agent_response,
            'timestamp': conv.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for conv in reversed(conversations)]
        
    except Exception as e:
        logging.error(f"Error getting conversation history: {e}")
        return []

def process_agent_purchase(agent_id, user_id, stripe_payment_id):
    """Process successful agent license purchase"""
    try:
        agent = AIAgent.query.get(agent_id)
        user = User.query.get(user_id)
        
        if not agent or not user:
            return False
            
        # Create revenue record
        revenue = Revenue(
            user_id=user_id,
            app_id=None,  # Agent purchase, not app
            amount=agent.base_price,
            transaction_type='agent_license',
            stripe_payment_id=stripe_payment_id
        )
        db.session.add(revenue)
        
        # Create default customization for the user
        customization = create_agent_customization(
            user_id=user_id,
            agent_id=agent_id,
            custom_name=f"{user.username}'s {agent.name}"
        )
        
        db.session.commit()
        logging.info(f"Agent purchase processed: User {user_id}, Agent {agent_id}")
        return customization
        
    except Exception as e:
        logging.error(f"Error processing agent purchase: {e}")
        db.session.rollback()
        return False

def get_agent_analytics():
    """Get analytics for agent performance"""
    try:
        # Get agent purchase stats
        agent_revenues = Revenue.query.filter_by(transaction_type='agent_license').all()
        total_agent_revenue = sum(r.amount for r in agent_revenues)
        total_agent_sales = len(agent_revenues)
        
        # Get conversation stats
        total_conversations = AgentConversation.query.count()
        active_customizations = AgentCustomization.query.count()
        
        # Get category breakdown
        category_stats = {}
        agents = AIAgent.query.filter_by(is_active=True).all()
        for agent in agents:
            if agent.category not in category_stats:
                category_stats[agent.category] = 0
            category_stats[agent.category] += len(agent.customizations)
        
        return {
            'total_agent_revenue': total_agent_revenue,
            'total_agent_sales': total_agent_sales,
            'average_agent_value': total_agent_revenue / max(total_agent_sales, 1),
            'total_conversations': total_conversations,
            'active_customizations': active_customizations,
            'category_breakdown': category_stats
        }
    except Exception as e:
        logging.error(f"Error getting agent analytics: {e}")
        return {}

def update_agent_branding(customization_id, branding_config):
    """Update branding configuration for an agent customization"""
    try:
        customization = AgentCustomization.query.get(customization_id)
        if not customization:
            return False
            
        customization.branding_config = json.dumps(branding_config)
        db.session.commit()
        return True
        
    except Exception as e:
        logging.error(f"Error updating agent branding: {e}")
        db.session.rollback()
        return False