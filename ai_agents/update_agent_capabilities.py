#!/usr/bin/env python3
"""
Update existing AI agents with proper emoji-compatible capabilities
"""

import json
from app import app, db
from models import AIAgent

def update_agent_capabilities():
    """Update existing agents with structured capabilities for emoji system"""
    
    capability_mapping = {
        'automation': [
            'Process Automation',
            'Workflow Optimization', 
            'Task Management',
            'Quality Control',
            'Resource Allocation'
        ],
        'analytics': [
            'Data Analytics',
            'Business Intelligence',
            'Performance Monitoring',
            'Predictive Analytics',
            'Market Research'
        ],
        'marketing': [
            'Lead Generation',
            'Content Creation',
            'Social Media Management',
            'Email Marketing',
            'Brand Strategy'
        ],
        'optimization': [
            'Revenue Optimization',
            'Cost Reduction',
            'Performance Tuning',
            'Conversion Optimization',
            'Resource Allocation'
        ],
        'platform': [
            'API Integration',
            'Cloud Management',
            'System Monitoring',
            'Infrastructure',
            'Database Optimization'
        ],
        'consulting': [
            'Strategic Planning',
            'Business Intelligence',
            'Market Research',
            'Risk Management',
            'Decision Support'
        ],
        'intelligence': [
            'Machine Learning',
            'Natural Language Processing',
            'Predictive Analytics',
            'Pattern Recognition',
            'Decision Support'
        ],
        'performance': [
            'Performance Monitoring',
            'System Optimization',
            'Performance Tuning',
            'Scalability Management',
            'Resource Allocation'
        ],
        'customer': [
            'Customer Support',
            'User Experience',
            'Personalization',
            'Customer Success',
            'Feedback Management'
        ],
        'leadership': [
            'Strategic Planning',
            'Team Management',
            'Business Intelligence',
            'Decision Support',
            'Performance Monitoring'
        ],
        'revenue': [
            'Revenue Optimization',
            'Lead Generation',
            'Customer Acquisition',
            'Business Intelligence',
            'Financial Analysis'
        ],
        'executive': [
            'Strategic Planning',
            'Business Intelligence',
            'Decision Support',
            'Performance Monitoring',
            'Risk Management'
        ]
    }
    
    with app.app_context():
        agents = AIAgent.query.filter_by(is_active=True).all()
        
        updated_count = 0
        for agent in agents:
            category = agent.category.lower()
            
            if category in capability_mapping:
                # Get capabilities for this category
                capabilities = capability_mapping[category]
                
                # Update agent capabilities
                agent.capabilities = json.dumps(capabilities)
                updated_count += 1
                
                print(f"Updated {agent.name} with {len(capabilities)} capabilities")
        
        try:
            db.session.commit()
            print(f"\n✅ Successfully updated {updated_count} agents with emoji-compatible capabilities")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error updating agents: {e}")
            return False

if __name__ == "__main__":
    success = update_agent_capabilities()
    if success:
        print("🎉 All agents now have emoji-compatible capability tags!")
    else:
        print("❌ Failed to update agent capabilities")