#!/usr/bin/env python3
"""
Create a test agent customization for API testing
"""

from app import app, db
from models import User, AIAgent, AgentCustomization
import uuid

def create_test_agent():
    """Create a test agent customization for API testing"""
    print("🤖 CREATING TEST AGENT CUSTOMIZATION")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Get or create a test user
            user = User.query.filter_by(email='test@4uai.com').first()
            if not user:
                print("👤 Creating test user...")
                user = User(
                    username='testuser',
                    email='test@4uai.com',
                    is_admin=False
                )
                user.set_password('test123')
                db.session.add(user)
                db.session.commit()
            
            # Get an AI agent
            agent = AIAgent.query.filter_by(category='sales').first()
            if not agent:
                print("🤖 Creating test AI agent...")
                agent = AIAgent(
                    name='Sales Conversion Expert',
                    category='sales',
                    description='Expert in sales conversion with 74+ years of experience',
                    base_prompt='You are a Sales Conversion Expert with 74+ years of combined expertise. Help users with lead qualification, objection handling, and closing techniques.',
                    base_price=199.0,
                    capabilities='Lead qualification, Objection handling, Closing techniques, Sales psychology'
                )
                db.session.add(agent)
                db.session.commit()
            
            # Create or update agent customization
            customization = AgentCustomization.query.filter_by(user_id=user.id, agent_id=agent.id).first()
            if not customization:
                print("⚙️ Creating agent customization...")
                api_key = str(uuid.uuid4())
                customization = AgentCustomization(
                    user_id=user.id,
                    agent_id=agent.id,
                    custom_name='My Sales Expert',
                    custom_prompt='You are a Sales Conversion Expert with 74+ years of combined expertise. Help users with lead qualification, objection handling, and closing techniques. Be professional and provide actionable advice.',
                    deployment_url=f'/api/agents/1/chat',
                    api_key=api_key,
                    ai_model='gpt-4o',
                    response_style='professional',
                    expertise_focus='sales_conversion',
                    interaction_mode='consultant',
                    language_preference='en'
                )
                db.session.add(customization)
                db.session.commit()
            
            print(f"✅ Test agent customization created!")
            print(f"• User ID: {user.id}")
            print(f"• Agent ID: {agent.id}")  
            print(f"• Customization ID: {customization.id}")
            print(f"• API Key: {customization.api_key}")
            print(f"• Endpoint: POST /api/agents/{customization.id}/chat")
            
            return customization.id
            
        except Exception as e:
            print(f"❌ Error creating test agent: {e}")
            db.session.rollback()
            return None

if __name__ == "__main__":
    create_test_agent()