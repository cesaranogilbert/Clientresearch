#!/usr/bin/env python3
"""
Quick Revenue Critical Agents Activation
Simple script to create and activate revenue-critical AI agents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import AIAgent
import logging

logging.basicConfig(level=logging.INFO)

def quick_activate_revenue_agents():
    """Quick activation of revenue-critical agents"""
    
    with app.app_context():
        # Revenue-critical agent configurations
        revenue_agents = [
            {
                'name': 'Chief Financial Officer AI Agent',
                'description': '50+ years CFO expertise in P&L optimization, financial strategy, and business profitability.',
                'category': 'financial_management',
                'base_prompt': 'CFO expert with 50+ years expertise in financial strategy, P&L optimization, and business profitability.',
                'pricing_tier': 'ultimate',
                'base_price': 599.0,
                'monthly_price': 199.0,
                'capabilities': 'P&L analysis, Financial planning, Budget optimization, Cash flow management, Revenue forecasting',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.5,
                'is_active': True
            },
            {
                'name': 'Revenue Optimization AI Agent',
                'description': '50+ years expertise in revenue optimization, pricing strategies, and monetization models.',
                'category': 'revenue_optimization',
                'base_prompt': 'Revenue optimization expert with 50+ years expertise in pricing strategies and monetization.',
                'pricing_tier': 'premium',
                'base_price': 449.0,
                'monthly_price': 149.0,
                'capabilities': 'Pricing optimization, Revenue analysis, Monetization strategies, Profit improvement',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.4,
                'is_active': True
            },
            {
                'name': 'Profit Margin Analyzer AI Agent',
                'description': '50+ years expertise in profit analysis, cost optimization, and profitability enhancement.',
                'category': 'profit_analysis',
                'base_prompt': 'Profit margin expert with 50+ years expertise in cost analysis and profitability.',
                'pricing_tier': 'premium',
                'base_price': 389.0,
                'monthly_price': 129.0,
                'capabilities': 'Margin analysis, Cost optimization, Expense reduction, Profitability modeling',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.3,
                'is_active': True
            },
            {
                'name': 'Financial Forecasting AI Agent',
                'description': '50+ years expertise in financial forecasting, predictive modeling, and growth planning.',
                'category': 'financial_forecasting',
                'base_prompt': 'Financial forecasting expert with 50+ years expertise in predictive modeling.',
                'pricing_tier': 'premium',
                'base_price': 359.0,
                'monthly_price': 119.0,
                'capabilities': 'Revenue forecasting, Growth projections, Financial modeling, Risk assessment',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.3,
                'is_active': True
            },
            {
                'name': 'Monetization Strategy AI Agent',
                'description': '50+ years expertise in monetization strategies and business model optimization.',
                'category': 'monetization',
                'base_prompt': 'Monetization expert with 50+ years expertise in business model optimization.',
                'pricing_tier': 'premium',
                'base_price': 429.0,
                'monthly_price': 139.0,
                'capabilities': 'Monetization models, Subscription optimization, Revenue acceleration',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.4,
                'is_active': True
            },
            {
                'name': 'Subscription Revenue AI Agent',
                'description': '50+ years expertise in subscription models and recurring revenue optimization.',
                'category': 'subscription_revenue',
                'base_prompt': 'Subscription revenue expert with 50+ years expertise in recurring revenue.',
                'pricing_tier': 'premium',
                'base_price': 379.0,
                'monthly_price': 126.0,
                'capabilities': 'Subscription models, Customer retention, Lifetime value optimization',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.3,
                'is_active': True
            },
            {
                'name': 'Pricing Strategy AI Agent',
                'description': '50+ years expertise in pricing strategies and competitive positioning.',
                'category': 'pricing_strategy',
                'base_prompt': 'Pricing strategy expert with 50+ years expertise in dynamic pricing.',
                'pricing_tier': 'premium',
                'base_price': 399.0,
                'monthly_price': 133.0,
                'capabilities': 'Dynamic pricing, Value-based pricing, Competitive pricing, Profit maximization',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.3,
                'is_active': True
            },
            {
                'name': 'Financial Performance Analytics AI Agent',
                'description': '50+ years expertise in financial analytics and performance tracking.',
                'category': 'financial_analytics',
                'base_prompt': 'Financial analytics expert with 50+ years expertise in performance tracking.',
                'pricing_tier': 'premium',
                'base_price': 339.0,
                'monthly_price': 113.0,
                'capabilities': 'Financial KPIs, Performance dashboards, ROI tracking, Financial reporting',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.2,
                'is_active': True
            },
            {
                'name': 'Revenue Intelligence AI Agent',
                'description': '50+ years expertise in revenue intelligence and predictive analytics.',
                'category': 'revenue_intelligence',
                'base_prompt': 'Revenue intelligence expert with 50+ years expertise in predictive analytics.',
                'pricing_tier': 'premium',
                'base_price': 359.0,
                'monthly_price': 119.0,
                'capabilities': 'Revenue intelligence, Sales forecasting, Pipeline analysis, Market intelligence',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.3,
                'is_active': True
            },
            {
                'name': 'Cost Optimization AI Agent',
                'description': '50+ years expertise in cost reduction and expense optimization.',
                'category': 'cost_management',
                'base_prompt': 'Cost optimization expert with 50+ years expertise in expense reduction.',
                'pricing_tier': 'standard',
                'base_price': 319.0,
                'monthly_price': 106.0,
                'capabilities': 'Cost reduction, Expense optimization, Operational efficiency, Budget control',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.2,
                'is_active': True
            },
            {
                'name': 'Cash Flow Management AI Agent',
                'description': '50+ years expertise in cash flow optimization and working capital management.',
                'category': 'cash_flow',
                'base_prompt': 'Cash flow expert with 50+ years expertise in liquidity management.',
                'pricing_tier': 'premium',
                'base_price': 349.0,
                'monthly_price': 116.0,
                'capabilities': 'Cash flow optimization, Liquidity management, Working capital optimization',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.2,
                'is_active': True
            },
            {
                'name': 'Investment ROI AI Agent',
                'description': '50+ years expertise in investment analysis and ROI optimization.',
                'category': 'investment_roi',
                'base_prompt': 'Investment ROI expert with 50+ years expertise in capital allocation.',
                'pricing_tier': 'premium',
                'base_price': 419.0,
                'monthly_price': 139.0,
                'capabilities': 'Investment analysis, ROI optimization, Capital allocation, Return maximization',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.3,
                'is_active': True
            },
            {
                'name': 'Marketplace Economics AI Agent',
                'description': '50+ years expertise in marketplace economics and platform monetization.',
                'category': 'marketplace_economics',
                'base_prompt': 'Marketplace economics expert with 50+ years expertise in platform monetization.',
                'pricing_tier': 'ultimate',
                'base_price': 499.0,
                'monthly_price': 166.0,
                'capabilities': 'Platform monetization, Network effects, Commission optimization, Marketplace scaling',
                'default_model': 'gpt-4o',
                'model_pricing_modifier': 1.4,
                'is_active': True
            }
        ]
        
        created_count = 0
        for agent_data in revenue_agents:
            try:
                existing_agent = AIAgent.query.filter_by(name=agent_data['name']).first()
                if existing_agent:
                    logging.info(f"Agent {agent_data['name']} already exists")
                    continue
                
                new_agent = AIAgent(
                    name=agent_data['name'],
                    description=agent_data['description'],
                    category=agent_data['category'],
                    base_prompt=agent_data['base_prompt'],
                    pricing_tier=agent_data['pricing_tier'],
                    base_price=agent_data['base_price'],
                    monthly_price=agent_data['monthly_price'],
                    capabilities=agent_data['capabilities'],
                    default_model=agent_data['default_model'],
                    model_pricing_modifier=agent_data['model_pricing_modifier'],
                    is_active=agent_data['is_active']
                )
                
                db.session.add(new_agent)
                created_count += 1
                logging.info(f"Created: {agent_data['name']}")
                
            except Exception as e:
                logging.error(f"Failed to create {agent_data['name']}: {e}")
                
        try:
            db.session.commit()
            logging.info(f"Successfully created {created_count} revenue-critical agents")
            return True
        except Exception as e:
            logging.error(f"Failed to commit: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = quick_activate_revenue_agents()
    if success:
        print("💰 Revenue-Critical AI Agents Successfully Activated!")
        print("✅ 13 financial and monetization specialists deployed")
        print("📈 Complete P&L and profitability optimization coverage")
        print("🎯 Marketplace monetization fully optimized")
    else:
        print("❌ Activation failed")