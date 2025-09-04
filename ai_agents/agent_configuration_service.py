#!/usr/bin/env python3
"""
AI Agent Configuration Service for 4UAI
Handles "Subway-style" agent customization with optimal conversion focus
"""

import json
import logging

# AI Model Configuration Options
AI_MODEL_OPTIONS = {
    'gpt-4o': {
        'name': 'OpenAI GPT-4o',
        'description': 'Most powerful general AI - Best for complex reasoning and analysis',
        'provider': 'OpenAI',
        'pricing_modifier': 1.0,
        'best_for': ['Business Analysis', 'Creative Writing', 'Problem Solving', 'General Tasks'],
        'tag': 'Most Popular',
        'icon': '🚀'
    },
    'claude-sonnet-4': {
        'name': 'Anthropic Claude 4.0',
        'description': 'Superior reasoning and safety - Ideal for professional and technical work',
        'provider': 'Anthropic', 
        'pricing_modifier': 1.2,
        'best_for': ['Technical Analysis', 'Research', 'Professional Writing', 'Code Review'],
        'tag': 'Premium Choice',
        'icon': '🧠'
    },
    'gpt-4o-mini': {
        'name': 'OpenAI GPT-4o Mini',
        'description': 'Fast and cost-effective - Perfect for routine tasks and quick responses',
        'provider': 'OpenAI',
        'pricing_modifier': 0.7,
        'best_for': ['Customer Service', 'Quick Analysis', 'Data Processing', 'Routine Tasks'],
        'tag': 'Cost Efficient',
        'icon': '⚡'
    }
}

# Response Style Options
RESPONSE_STYLE_OPTIONS = {
    'professional': {
        'name': 'Professional',
        'description': 'Formal, business-focused communication style',
        'icon': '👔',
        'prompt_modifier': 'Respond in a professional, business-appropriate tone with clear structure and formal language.'
    },
    'creative': {
        'name': 'Creative',
        'description': 'Innovative, out-of-the-box thinking and expression',
        'icon': '🎨', 
        'prompt_modifier': 'Be creative, innovative, and think outside the box. Use engaging language and creative approaches.'
    },
    'analytical': {
        'name': 'Analytical', 
        'description': 'Data-driven, logical, and systematic approach',
        'icon': '📊',
        'prompt_modifier': 'Focus on data-driven analysis, logical reasoning, and systematic problem-solving approaches.'
    },
    'casual': {
        'name': 'Conversational',
        'description': 'Friendly, approachable, and easy-to-understand',
        'icon': '💬',
        'prompt_modifier': 'Use a friendly, conversational tone that is approachable and easy to understand.'
    }
}

# Expertise Focus Options  
EXPERTISE_FOCUS_OPTIONS = {
    'general': {
        'name': 'General Business',
        'description': 'Broad business knowledge across all industries',
        'icon': '🏢'
    },
    'finance': {
        'name': 'Financial Services',
        'description': 'Banking, investment, accounting, and financial analysis',
        'icon': '💰'
    },
    'healthcare': {
        'name': 'Healthcare & Medical',
        'description': 'Medical practices, healthcare operations, patient care',
        'icon': '⚕️'
    },
    'technology': {
        'name': 'Technology & Software',
        'description': 'Software development, IT operations, tech consulting',
        'icon': '💻'
    },
    'legal': {
        'name': 'Legal Services',
        'description': 'Law practice, legal research, compliance, contracts',
        'icon': '⚖️'
    },
    'marketing': {
        'name': 'Marketing & Sales',
        'description': 'Digital marketing, sales strategy, customer acquisition',
        'icon': '📈'
    }
}

# Interaction Mode Options
INTERACTION_MODE_OPTIONS = {
    'detailed': {
        'name': 'Comprehensive',
        'description': 'Thorough, detailed responses with full explanations',
        'icon': '📋',
        'prompt_modifier': 'Provide comprehensive, detailed responses with thorough explanations and examples.'
    },
    'concise': {
        'name': 'Quick & Direct',
        'description': 'Brief, to-the-point answers for fast decisions',
        'icon': '⚡',
        'prompt_modifier': 'Keep responses concise, direct, and focused on key points for quick decision-making.'
    },
    'interactive': {
        'name': 'Interactive Guide',
        'description': 'Ask follow-up questions to provide personalized help',
        'icon': '🗣️',
        'prompt_modifier': 'Engage interactively by asking relevant follow-up questions to provide personalized assistance.'
    }
}

# Language Preference Options
LANGUAGE_OPTIONS = {
    'english': {'name': 'English', 'icon': '🇺🇸'},
    'spanish': {'name': 'Español', 'icon': '🇪🇸'}, 
    'french': {'name': 'Français', 'icon': '🇫🇷'},
    'german': {'name': 'Deutsch', 'icon': '🇩🇪'},
    'chinese': {'name': '中文', 'icon': '🇨🇳'},
    'japanese': {'name': '日本語', 'icon': '🇯🇵'}
}

def get_agent_configuration_options():
    """Get all available configuration options for agent customization"""
    return {
        'ai_models': AI_MODEL_OPTIONS,
        'response_styles': RESPONSE_STYLE_OPTIONS,
        'expertise_focus': EXPERTISE_FOCUS_OPTIONS,
        'interaction_modes': INTERACTION_MODE_OPTIONS,
        'languages': LANGUAGE_OPTIONS
    }

def calculate_customization_pricing(agent_id, selected_model='gpt-4o'):
    """Calculate pricing based on selected AI model and customizations"""
    try:
        from models import AIAgent
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return None
            
        base_monthly_price = agent.monthly_price
        base_one_time_price = agent.base_price
        
        # Get model pricing modifier
        model_modifier = AI_MODEL_OPTIONS.get(selected_model, {}).get('pricing_modifier', 1.0)
        
        # Apply agent-specific model pricing modifier (if available)
        agent_modifier = getattr(agent, 'model_pricing_modifier', 1.0) or 1.0
        total_modifier = model_modifier * agent_modifier
        
        return {
            'base_monthly': base_monthly_price,
            'base_one_time': base_one_time_price,
            'customized_monthly': base_monthly_price * total_modifier,
            'customized_one_time': base_one_time_price * total_modifier,
            'model_modifier': model_modifier,
            'savings_or_premium': (total_modifier - 1.0) * base_monthly_price,
            'selected_model': selected_model,
            'model_name': AI_MODEL_OPTIONS.get(selected_model, {}).get('name', selected_model)
        }
        
    except Exception as e:
        logging.error(f"Error calculating customization pricing: {e}")
        return None

def create_customized_agent(user_id, agent_id, customization_options):
    """Create a fully customized agent based on user preferences"""
    try:
        from models import AIAgent, AgentCustomization, db
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return None
            
        # Extract customization preferences
        ai_model = customization_options.get('ai_model', 'gpt-4o')
        response_style = customization_options.get('response_style', 'professional')
        expertise_focus = customization_options.get('expertise_focus', 'general')
        interaction_mode = customization_options.get('interaction_mode', 'detailed')
        language_preference = customization_options.get('language_preference', 'english')
        custom_name = customization_options.get('custom_name', f"Custom {agent.name}")
        
        # Build enhanced prompt with customizations
        enhanced_prompt = build_enhanced_prompt(
            agent.base_prompt,
            response_style,
            expertise_focus, 
            interaction_mode,
            language_preference
        )
        
        # Generate unique API key
        import uuid
        api_key = str(uuid.uuid4())
        
        # Create customization record
        customization = AgentCustomization(
            user_id=user_id,
            agent_id=agent_id,
            custom_name=custom_name,
            custom_prompt=enhanced_prompt,
            ai_model=ai_model,
            response_style=response_style,
            expertise_focus=expertise_focus,
            interaction_mode=interaction_mode,
            language_preference=language_preference,
            api_key=api_key,
            branding_config=json.dumps(customization_options.get('branding', {}))
        )
        
        db.session.add(customization)
        db.session.commit()
        
        return {
            'id': customization.id,
            'custom_name': custom_name,
            'api_key': api_key,
            'ai_model': ai_model,
            'configuration': {
                'response_style': response_style,
                'expertise_focus': expertise_focus,
                'interaction_mode': interaction_mode,
                'language': language_preference
            }
        }
        
    except Exception as e:
        logging.error(f"Error creating customized agent: {e}")
        db.session.rollback()
        return None

def build_enhanced_prompt(base_prompt, response_style, expertise_focus, interaction_mode, language):
    """Build enhanced prompt incorporating all customization options"""
    
    enhanced_prompt = base_prompt or "You are a helpful AI assistant."
    
    # Add response style modifier
    style_modifier = RESPONSE_STYLE_OPTIONS.get(response_style, {}).get('prompt_modifier', '')
    if style_modifier:
        enhanced_prompt += f"\n\nCommunication Style: {style_modifier}"
    
    # Add expertise focus
    if expertise_focus != 'general':
        focus_info = EXPERTISE_FOCUS_OPTIONS.get(expertise_focus, {})
        enhanced_prompt += f"\n\nExpertise Focus: Specialize in {focus_info.get('description', expertise_focus)} with deep knowledge in this domain."
    
    # Add interaction mode modifier
    mode_modifier = INTERACTION_MODE_OPTIONS.get(interaction_mode, {}).get('prompt_modifier', '')
    if mode_modifier:
        enhanced_prompt += f"\n\nInteraction Approach: {mode_modifier}"
    
    # Add language preference
    if language != 'english':
        lang_name = LANGUAGE_OPTIONS.get(language, {}).get('name', language)
        enhanced_prompt += f"\n\nLanguage: Always respond in {lang_name} unless specifically asked to use another language."
    
    return enhanced_prompt

def get_agent_customization_summary(customization_id):
    """Get a user-friendly summary of agent customization"""
    try:
        from models import AIAgent, AgentCustomization
        customization = AgentCustomization.query.get(customization_id)
        if not customization:
            return None
            
        agent = AIAgent.query.get(customization.agent_id)
        
        # Get configuration details
        model_info = AI_MODEL_OPTIONS.get(customization.ai_model, {})
        style_info = RESPONSE_STYLE_OPTIONS.get(customization.response_style, {})
        focus_info = EXPERTISE_FOCUS_OPTIONS.get(customization.expertise_focus, {})
        mode_info = INTERACTION_MODE_OPTIONS.get(customization.interaction_mode, {})
        lang_info = LANGUAGE_OPTIONS.get(customization.language_preference, {})
        
        return {
            'agent_name': agent.name if agent else 'Unknown',
            'custom_name': customization.custom_name,
            'configuration': {
                'ai_model': {
                    'name': model_info.get('name', customization.ai_model),
                    'icon': model_info.get('icon', '🤖'),
                    'tag': model_info.get('tag', '')
                },
                'response_style': {
                    'name': style_info.get('name', customization.response_style),
                    'icon': style_info.get('icon', '💬')
                },
                'expertise_focus': {
                    'name': focus_info.get('name', customization.expertise_focus),
                    'icon': focus_info.get('icon', '🎯')
                },
                'interaction_mode': {
                    'name': mode_info.get('name', customization.interaction_mode),
                    'icon': mode_info.get('icon', '🔧')
                },
                'language': {
                    'name': lang_info.get('name', customization.language_preference),
                    'icon': lang_info.get('icon', '🌐')
                }
            },
            'created_at': customization.created_at,
            'api_key': customization.api_key
        }
        
    except Exception as e:
        logging.error(f"Error getting customization summary: {e}")
        return None

def update_agent_supported_models():
    """Update all agents to support the new AI model options"""
    try:
        from models import AIAgent, db
        agents = AIAgent.query.all()
        supported_models = list(AI_MODEL_OPTIONS.keys())
        
        for agent in agents:
            agent.supported_models = json.dumps(supported_models)
            agent.default_model = 'gpt-4o'
            agent.model_pricing_modifier = 1.0
            
        db.session.commit()
        logging.info(f"Updated {len(agents)} agents with AI model support")
        return True
        
    except Exception as e:
        logging.error(f"Error updating agent model support: {e}")
        db.session.rollback()
        return False