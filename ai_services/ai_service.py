import os
import json
import logging
from openai import OpenAI

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def safe_json_loads(content):
    """Safely parse JSON content with None checking"""
    if content is None:
        return None
    try:
        return json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return None

def generate_app_template(app_name, description, category, features):
    """Generate a basic app template using AI"""
    if not openai_client:
        logging.error("OpenAI API key not configured")
        return None
    
    try:
        prompt = f"""
        Generate a basic web application template for:
        App Name: {app_name}
        Description: {description}
        Category: {category}
        Features: {features}
        
        Create a simple HTML/CSS/JavaScript template structure with:
        1. Basic HTML structure
        2. CSS styling
        3. JavaScript functionality placeholders
        4. Integration points for the requested features
        
        Return the response as JSON with keys: 'html', 'css', 'javascript', 'config'
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return safe_json_loads(response.choices[0].message.content)
        
    except Exception as e:
        logging.error(f"Error generating app template: {e}")
        return None

def get_app_recommendations(user_preferences, existing_apps):
    """Get AI-powered app recommendations"""
    if not openai_client:
        return []
    
    try:
        prompt = f"""
        Based on user preferences: {user_preferences}
        And existing apps: {existing_apps}
        
        Recommend 5 apps that would be most valuable for this user.
        Consider their business needs, technical requirements, and market trends.
        
        Return as JSON array with keys: 'name', 'reason', 'category', 'estimated_value'
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = safe_json_loads(response.choices[0].message.content)
        return result.get('recommendations', []) if result else []
        
    except Exception as e:
        logging.error(f"Error getting recommendations: {e}")
        return []

def generate_custom_branding(brand_name, colors, style_preferences):
    """Generate custom branding CSS and configuration"""
    if not openai_client:
        return None
    
    try:
        prompt = f"""
        Generate custom branding for:
        Brand Name: {brand_name}
        Colors: {colors}
        Style Preferences: {style_preferences}
        
        Create CSS variables and styling that can be applied to white-label apps.
        Include logo placement, color scheme, typography, and component styling.
        
        Return as JSON with keys: 'css_variables', 'custom_styles', 'brand_config'
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return safe_json_loads(response.choices[0].message.content)
        
    except Exception as e:
        logging.error(f"Error generating branding: {e}")
        return None

def analyze_market_pricing(app_category, features, competitors):
    """Analyze market pricing for dynamic pricing suggestions"""
    if not openai_client:
        return {"base_price": 99, "monthly_price": 19}
    
    try:
        prompt = f"""
        Analyze market pricing for:
        App Category: {app_category}
        Features: {features}
        Competitors: {competitors}
        
        Suggest optimal pricing strategy including:
        - Base license price
        - Monthly subscription price
        - Pricing tiers
        - Market positioning
        
        Return as JSON with keys: 'base_price', 'monthly_price', 'tiers', 'strategy'
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = safe_json_loads(response.choices[0].message.content)
        return result if result else {"base_price": 99, "monthly_price": 19}
        
    except Exception as e:
        logging.error(f"Error analyzing pricing: {e}")
        return {"base_price": 99, "monthly_price": 19}
