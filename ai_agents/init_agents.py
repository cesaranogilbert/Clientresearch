#!/usr/bin/env python3
"""
4UAI Agent Initialization Script
Populates the database with all AI agents for the marketplace
"""

from app import app, db
from models import AIAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def init_ai_agents():
    """Initialize all AI agents for the 4UAI marketplace"""
    
    agents_data = [
        # BUSINESS CATEGORY ($99-299/month)
        {
            'name': 'Financial Advisor AI',
            'description': 'Personal finance planning and investment guidance specialist with expertise in portfolio management, retirement planning, and wealth building strategies.',
            'category': 'business',
            'base_prompt': 'You are a certified financial advisor AI with deep expertise in personal finance, investment strategies, and wealth management. Provide practical, actionable financial advice while considering risk tolerance and long-term goals.',
            'pricing_tier': 'professional',
            'base_price': 299.0,
            'monthly_price': 149.0,
            'capabilities': 'Investment Analysis, Portfolio Management, Retirement Planning, Tax Strategy, Risk Assessment'
        },
        {
            'name': 'Market Analysis AI',
            'description': 'Advanced stock market trends analyzer and trading insights provider with real-time market intelligence and predictive analytics capabilities.',
            'category': 'business',
            'base_prompt': 'You are a sophisticated market analysis AI with expertise in technical analysis, fundamental analysis, and market trends. Provide data-driven insights for trading and investment decisions.',
            'pricing_tier': 'professional',
            'base_price': 399.0,
            'monthly_price': 199.0,
            'capabilities': 'Technical Analysis, Market Trends, Stock Screening, Risk Management, Trading Signals'
        },
        {
            'name': 'Business Consultant AI',
            'description': 'Strategic business consultant specializing in growth optimization, operational efficiency, and competitive analysis for businesses of all sizes.',
            'category': 'business',
            'base_prompt': 'You are a senior business consultant AI with expertise in strategy development, operations optimization, and business growth. Provide strategic insights and actionable recommendations.',
            'pricing_tier': 'professional',
            'base_price': 349.0,
            'monthly_price': 179.0,
            'capabilities': 'Strategic Planning, Market Analysis, Process Optimization, Competitive Intelligence, Growth Strategy'
        },
        {
            'name': 'Sales Coach AI',
            'description': 'Expert sales methodology trainer focusing on customer relationship management, conversion optimization, and revenue growth strategies.',
            'category': 'business',
            'base_prompt': 'You are an elite sales coach AI with proven methodologies for improving sales performance, customer relationships, and conversion rates. Provide tactical sales guidance.',
            'pricing_tier': 'basic',
            'base_price': 199.0,
            'monthly_price': 99.0,
            'capabilities': 'Sales Training, CRM Strategy, Lead Generation, Conversion Optimization, Customer Retention'
        },
        {
            'name': 'Marketing Strategist AI',
            'description': 'Digital marketing expert specializing in brand development, campaign optimization, and customer acquisition across all digital channels.',
            'category': 'business',
            'base_prompt': 'You are a digital marketing strategist AI with expertise in brand development, campaign management, and customer acquisition. Provide comprehensive marketing guidance.',
            'pricing_tier': 'professional',
            'base_price': 299.0,
            'monthly_price': 149.0,
            'capabilities': 'Brand Strategy, Digital Marketing, Campaign Management, SEO/SEM, Social Media Strategy'
        },
        {
            'name': 'Operations Manager AI',
            'description': 'Process optimization specialist focused on workflow management, efficiency improvement, and operational excellence across organizations.',
            'category': 'business',
            'base_prompt': 'You are an operations management AI expert in process optimization, workflow design, and operational efficiency. Provide systematic improvement recommendations.',
            'pricing_tier': 'professional',
            'base_price': 279.0,
            'monthly_price': 139.0,
            'capabilities': 'Process Optimization, Workflow Management, Quality Control, Resource Planning, Performance Metrics'
        },
        {
            'name': 'HR Assistant AI',
            'description': 'Human resources specialist covering recruitment, employee management, policy development, and workplace culture optimization.',
            'category': 'business',
            'base_prompt': 'You are an HR management AI with expertise in recruitment, employee relations, policy development, and workplace culture. Provide comprehensive HR guidance.',
            'pricing_tier': 'basic',
            'base_price': 249.0,
            'monthly_price': 124.0,
            'capabilities': 'Recruitment, Employee Relations, Policy Development, Performance Management, Workplace Culture'
        },
        {
            'name': 'Customer Service AI',
            'description': 'Customer experience optimization expert specializing in support ticket resolution, satisfaction improvement, and service quality management.',
            'category': 'business',
            'base_prompt': 'You are a customer service excellence AI with expertise in support operations, customer satisfaction, and service quality improvement. Provide service optimization strategies.',
            'pricing_tier': 'basic',
            'base_price': 199.0,
            'monthly_price': 99.0,
            'capabilities': 'Support Operations, Customer Satisfaction, Service Quality, Issue Resolution, Experience Design'
        },
        
        # HEALTHCARE CATEGORY ($149-349/month)
        {
            'name': 'Medical Research AI',
            'description': 'Advanced medical literature analyst providing clinical insights, research summaries, and evidence-based medical information for healthcare professionals.',
            'category': 'healthcare',
            'base_prompt': 'You are a medical research AI with expertise in clinical literature analysis, evidence-based medicine, and medical research methodology. Provide accurate, well-sourced medical information.',
            'pricing_tier': 'enterprise',
            'base_price': 449.0,
            'monthly_price': 349.0,
            'capabilities': 'Literature Review, Clinical Research, Evidence Analysis, Medical Guidelines, Research Methodology'
        },
        {
            'name': 'Wellness Coach AI',
            'description': 'Personalized health optimization advisor focusing on lifestyle improvements, preventive care, and holistic wellness strategies.',
            'category': 'healthcare',
            'base_prompt': 'You are a wellness coach AI with expertise in preventive health, lifestyle optimization, and holistic wellness approaches. Provide personalized health guidance.',
            'pricing_tier': 'professional',
            'base_price': 249.0,
            'monthly_price': 179.0,
            'capabilities': 'Lifestyle Optimization, Preventive Care, Wellness Planning, Health Tracking, Habit Formation'
        },
        {
            'name': 'Mental Health Support AI',
            'description': 'Emotional wellness specialist providing stress management techniques, coping strategies, and mental health resource guidance.',
            'category': 'healthcare',
            'base_prompt': 'You are a mental health support AI with training in stress management, emotional wellness, and coping strategies. Provide supportive, evidence-based mental health guidance.',
            'pricing_tier': 'professional',
            'base_price': 299.0,
            'monthly_price': 199.0,
            'capabilities': 'Stress Management, Emotional Wellness, Coping Strategies, Mental Health Resources, Mindfulness'
        },
        {
            'name': 'Nutrition Advisor AI',
            'description': 'Evidence-based nutritional guidance specialist focusing on dietary planning, nutritional optimization, and health-focused meal strategies.',
            'category': 'healthcare',
            'base_prompt': 'You are a nutrition advisor AI with expertise in dietary planning, nutritional science, and health optimization through nutrition. Provide evidence-based nutritional guidance.',
            'pricing_tier': 'basic',
            'base_price': 199.0,
            'monthly_price': 149.0,
            'capabilities': 'Dietary Planning, Nutritional Analysis, Meal Planning, Health Optimization, Supplement Guidance'
        },
        
        # LEGAL CATEGORY ($199-399/month)
        {
            'name': 'Legal Research AI',
            'description': 'Comprehensive case law analyzer and legal document reviewer with expertise in legal research methodology and precedent analysis.',
            'category': 'legal',
            'base_prompt': 'You are a legal research AI with expertise in case law analysis, legal precedent research, and legal document review. Provide thorough legal research assistance.',
            'pricing_tier': 'enterprise',
            'base_price': 499.0,
            'monthly_price': 399.0,
            'capabilities': 'Case Law Analysis, Legal Research, Precedent Review, Document Analysis, Citation Verification'
        },
        {
            'name': 'Contract Analyzer AI',
            'description': 'Specialized contract review expert focusing on risk assessment, clause analysis, and legal agreement optimization for businesses.',
            'category': 'legal',
            'base_prompt': 'You are a contract analysis AI with expertise in contract review, risk assessment, and legal agreement optimization. Provide detailed contract analysis.',
            'pricing_tier': 'enterprise',
            'base_price': 449.0,
            'monthly_price': 349.0,
            'capabilities': 'Contract Review, Risk Assessment, Clause Analysis, Legal Agreement Optimization, Compliance Checking'
        },
        {
            'name': 'Compliance Monitor AI',
            'description': 'Regulatory compliance specialist tracking policy updates, compliance requirements, and regulatory changes across industries.',
            'category': 'legal',
            'base_prompt': 'You are a compliance monitoring AI with expertise in regulatory requirements, policy updates, and compliance management across various industries.',
            'pricing_tier': 'professional',
            'base_price': 349.0,
            'monthly_price': 249.0,
            'capabilities': 'Regulatory Compliance, Policy Monitoring, Compliance Training, Risk Management, Audit Support'
        },
        {
            'name': 'IP Protection AI',
            'description': 'Intellectual property strategist specializing in patent research, trademark analysis, and IP protection strategy development.',
            'category': 'legal',
            'base_prompt': 'You are an intellectual property AI with expertise in patent research, trademark analysis, and IP protection strategies. Provide comprehensive IP guidance.',
            'pricing_tier': 'professional',
            'base_price': 399.0,
            'monthly_price': 299.0,
            'capabilities': 'Patent Research, Trademark Analysis, IP Strategy, Copyright Protection, Trade Secret Management'
        },
        
        # TECHNOLOGY CATEGORY ($129-249/month)
        {
            'name': 'Code Review AI',
            'description': 'Software development expert providing code optimization, security analysis, and development best practices across multiple programming languages.',
            'category': 'technology',
            'base_prompt': 'You are a senior software development AI with expertise in code review, optimization, and security analysis across multiple programming languages and frameworks.',
            'pricing_tier': 'professional',
            'base_price': 299.0,
            'monthly_price': 199.0,
            'capabilities': 'Code Review, Security Analysis, Performance Optimization, Best Practices, Multi-Language Support'
        },
        {
            'name': 'Cybersecurity AI',
            'description': 'Information security specialist focused on threat analysis, vulnerability assessment, and comprehensive security strategy development.',
            'category': 'technology',
            'base_prompt': 'You are a cybersecurity AI with expertise in threat analysis, vulnerability assessment, and security strategy development. Provide comprehensive security guidance.',
            'pricing_tier': 'professional',
            'base_price': 349.0,
            'monthly_price': 249.0,
            'capabilities': 'Threat Analysis, Vulnerability Assessment, Security Strategy, Incident Response, Risk Management'
        },
        {
            'name': 'Data Analyst AI',
            'description': 'Business intelligence expert specializing in data visualization, statistical analysis, and insights generation from complex datasets.',
            'category': 'technology',
            'base_prompt': 'You are a data analysis AI with expertise in business intelligence, statistical analysis, and data visualization. Provide actionable insights from data.',
            'pricing_tier': 'professional',
            'base_price': 279.0,
            'monthly_price': 189.0,
            'capabilities': 'Data Analysis, Statistical Modeling, Data Visualization, Business Intelligence, Predictive Analytics'
        },
        {
            'name': 'DevOps Assistant AI',
            'description': 'Infrastructure management specialist focusing on deployment automation, system monitoring, and scalable architecture design.',
            'category': 'technology',
            'base_prompt': 'You are a DevOps AI with expertise in infrastructure management, deployment automation, and scalable system architecture. Provide operational excellence guidance.',
            'pricing_tier': 'basic',
            'base_price': 249.0,
            'monthly_price': 179.0,
            'capabilities': 'Infrastructure Management, Deployment Automation, System Monitoring, Scalability, CI/CD Pipeline'
        },
        
        # CREATIVE CATEGORY ($89-199/month)
        {
            'name': 'Content Creator AI',
            'description': 'Professional writing and content strategy expert specializing in blog creation, copywriting, and comprehensive content marketing.',
            'category': 'creative',
            'base_prompt': 'You are a content creation AI with expertise in professional writing, content strategy, and content marketing. Provide high-quality, engaging content.',
            'pricing_tier': 'basic',
            'base_price': 199.0,
            'monthly_price': 129.0,
            'capabilities': 'Content Writing, Blog Creation, Copywriting, Content Strategy, SEO Content'
        },
        {
            'name': 'Design Assistant AI',
            'description': 'Creative direction specialist providing visual concept development, design strategy, and brand aesthetic guidance for all media.',
            'category': 'creative',
            'base_prompt': 'You are a design assistant AI with expertise in visual design, creative direction, and brand aesthetics. Provide comprehensive design guidance.',
            'pricing_tier': 'basic',
            'base_price': 179.0,
            'monthly_price': 119.0,
            'capabilities': 'Visual Design, Creative Direction, Brand Aesthetics, Design Strategy, Layout Design'
        },
        {
            'name': 'Social Media Manager AI',
            'description': 'Social media strategy expert focusing on content scheduling, engagement optimization, and community management across all platforms.',
            'category': 'creative',
            'base_prompt': 'You are a social media management AI with expertise in content strategy, engagement optimization, and community management across all social platforms.',
            'pricing_tier': 'basic',
            'base_price': 149.0,
            'monthly_price': 99.0,
            'capabilities': 'Content Scheduling, Engagement Strategy, Community Management, Social Analytics, Platform Optimization'
        },
        {
            'name': 'Brand Identity AI',
            'description': 'Brand development strategist specializing in logo design concepts, brand positioning, and comprehensive brand identity development.',
            'category': 'creative',
            'base_prompt': 'You are a brand identity AI with expertise in brand development, logo design concepts, and brand positioning strategy. Provide comprehensive branding guidance.',
            'pricing_tier': 'basic',
            'base_price': 199.0,
            'monthly_price': 139.0,
            'capabilities': 'Brand Development, Logo Design, Brand Positioning, Brand Guidelines, Identity Systems'
        }
    ]
    
    # Industry Expert Agents
    expert_agents = [
        {
            'name': 'Healthcare Strategy Expert',
            'description': 'Senior medical practice management consultant with 20+ years experience in healthcare operations, patient care optimization, and medical practice growth.',
            'category': 'healthcare_expert',
            'base_prompt': 'You are a senior healthcare strategy consultant with deep expertise in medical practice management, healthcare operations, and industry best practices. Provide strategic healthcare guidance.',
            'pricing_tier': 'enterprise',
            'base_price': 599.0,
            'monthly_price': 449.0,
            'capabilities': 'Healthcare Strategy, Practice Management, Patient Care Optimization, Healthcare Operations, Regulatory Compliance'
        },
        {
            'name': 'Financial Services Expert',
            'description': 'Investment banking and wealth management advisor with expertise in financial markets, investment strategies, and portfolio management.',
            'category': 'financial_expert',
            'base_prompt': 'You are a financial services expert with investment banking and wealth management experience. Provide sophisticated financial strategy and investment guidance.',
            'pricing_tier': 'enterprise',
            'base_price': 649.0,
            'monthly_price': 449.0,
            'capabilities': 'Investment Banking, Wealth Management, Portfolio Strategy, Financial Markets, Risk Management'
        },
        {
            'name': 'Legal Practice Expert',
            'description': 'Corporate law and litigation strategy specialist with deep expertise in legal practice management and complex legal matters.',
            'category': 'legal_expert',
            'base_prompt': 'You are a legal practice expert with corporate law and litigation experience. Provide sophisticated legal strategy and practice management guidance.',
            'pricing_tier': 'enterprise',
            'base_price': 699.0,
            'monthly_price': 449.0,
            'capabilities': 'Corporate Law, Litigation Strategy, Legal Practice Management, Complex Legal Matters, Risk Assessment'
        },
        {
            'name': 'Manufacturing Expert',
            'description': 'Operations efficiency and supply chain optimization specialist with expertise in lean manufacturing and process improvement.',
            'category': 'manufacturing_expert',
            'base_prompt': 'You are a manufacturing expert with deep knowledge of operations efficiency, supply chain optimization, and lean manufacturing principles.',
            'pricing_tier': 'enterprise',
            'base_price': 549.0,
            'monthly_price': 379.0,
            'capabilities': 'Operations Efficiency, Supply Chain Optimization, Lean Manufacturing, Process Improvement, Quality Management'
        },
        {
            'name': 'Real Estate Expert',
            'description': 'Market analysis and investment strategy advisor with comprehensive knowledge of real estate markets and property investment.',
            'category': 'real_estate_expert',
            'base_prompt': 'You are a real estate expert with expertise in market analysis, property investment, and real estate strategy development.',
            'pricing_tier': 'enterprise',
            'base_price': 499.0,
            'monthly_price': 349.0,
            'capabilities': 'Market Analysis, Property Investment, Real Estate Strategy, Investment Analysis, Market Trends'
        },
        {
            'name': 'Startup Strategy Expert',
            'description': 'Venture capital and scaling methodology specialist with proven experience in startup growth and business model development.',
            'category': 'startup_expert',
            'base_prompt': 'You are a startup strategy expert with venture capital experience and deep knowledge of scaling methodologies and business model development.',
            'pricing_tier': 'enterprise',
            'base_price': 599.0,
            'monthly_price': 399.0,
            'capabilities': 'Startup Strategy, Venture Capital, Scaling Methodology, Business Model Development, Growth Strategy'
        },
        {
            'name': 'Retail Operations Expert',
            'description': 'Customer experience and inventory management specialist with expertise in retail optimization and consumer behavior.',
            'category': 'retail_expert',
            'base_prompt': 'You are a retail operations expert with deep knowledge of customer experience, inventory management, and retail optimization strategies.',
            'pricing_tier': 'enterprise',
            'base_price': 449.0,
            'monthly_price': 329.0,
            'capabilities': 'Customer Experience, Inventory Management, Retail Optimization, Consumer Behavior, Operations Management'
        },
        {
            'name': 'Marketing Executive Expert',
            'description': 'Brand strategy and campaign development specialist with executive-level expertise in marketing leadership and brand management.',
            'category': 'marketing_expert',
            'base_prompt': 'You are a marketing executive expert with deep expertise in brand strategy, campaign development, and marketing leadership at the executive level.',
            'pricing_tier': 'enterprise',
            'base_price': 549.0,
            'monthly_price': 379.0,
            'capabilities': 'Brand Strategy, Campaign Development, Marketing Leadership, Brand Management, Strategic Marketing'
        },
        {
            'name': 'Energy Sector Expert',
            'description': 'Renewable energy and sustainability consulting specialist with expertise in energy markets and environmental strategy.',
            'category': 'energy_expert',
            'base_prompt': 'You are an energy sector expert with deep knowledge of renewable energy, sustainability consulting, and energy market dynamics.',
            'pricing_tier': 'enterprise',
            'base_price': 579.0,
            'monthly_price': 399.0,
            'capabilities': 'Renewable Energy, Sustainability Consulting, Energy Markets, Environmental Strategy, Green Technology'
        }
    ]
    
    # Combine all agents
    all_agents = agents_data + expert_agents
    
    with app.app_context():
        try:
            # Clear existing agents (optional - remove if you want to keep existing data)
            AIAgent.query.delete()
            
            # Create all agents
            for agent_data in all_agents:
                agent = AIAgent(
                    name=agent_data['name'],
                    description=agent_data['description'],
                    category=agent_data['category'],
                    base_prompt=agent_data['base_prompt'],
                    pricing_tier=agent_data['pricing_tier'],
                    base_price=agent_data['base_price'],
                    monthly_price=agent_data['monthly_price'],
                    capabilities=agent_data['capabilities'],
                    is_active=True
                )
                db.session.add(agent)
                logging.info(f"Added agent: {agent_data['name']}")
            
            db.session.commit()
            logging.info(f"Successfully initialized {len(all_agents)} AI agents")
            
            # Print summary
            print("\n=== 4UAI AGENT INITIALIZATION COMPLETE ===")
            print(f"Total Agents Created: {len(all_agents)}")
            print(f"Business Agents: 8")
            print(f"Healthcare Agents: 4") 
            print(f"Legal Agents: 4")
            print(f"Technology Agents: 4")
            print(f"Creative Agents: 4")
            print(f"Industry Experts: 9")
            print("=== READY FOR MARKETPLACE ===\n")
            
        except Exception as e:
            logging.error(f"Error initializing agents: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_ai_agents()