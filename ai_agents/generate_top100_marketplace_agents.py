#!/usr/bin/env python3
"""
Top 100 AI Agents Marketplace Generator
Generates all missing Top 100 AI Agents from ranking system into marketplace database
Ensures all featured agents are available for purchase with optimized pricing
"""

import logging
import json
from datetime import datetime
from app import app, db
from models import AIAgent
from top_100_ai_agents_ranking import Top100AgentsRanking
# Pricing optimization handled internally

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Top100MarketplaceGenerator:
    """Generate Top 100 AI Agents for marketplace with comprehensive data"""
    
    def __init__(self):
        self.ranking_system = Top100AgentsRanking()
        self.generated_count = 0
        self.updated_count = 0
        self.skipped_count = 0
        
    def generate_all_top100_agents(self):
        """Generate all Top 100 AI Agents from ranking system"""
        try:
            with app.app_context():
                logger.info("🚀 Starting Top 100 AI Agents marketplace generation...")
                
                # Get Top 100 agents from ranking system
                ranking_data = self.ranking_system.get_top_100_agents_ranking()
                top_100_agents = ranking_data['top_100_agents']
                
                logger.info(f"📊 Found {len(top_100_agents)} agents in Top 100 ranking")
                
                # Process each agent
                for rank, agent_data in enumerate(top_100_agents, 1):
                    self._process_agent(agent_data, rank)
                
                # Commit all changes
                db.session.commit()
                
                logger.info("✅ Top 100 AI Agents marketplace generation completed!")
                logger.info(f"  - Generated: {self.generated_count} new agents")
                logger.info(f"  - Updated: {self.updated_count} existing agents")
                logger.info(f"  - Skipped: {self.skipped_count} agents")
                
                return {
                    'success': True,
                    'generated': self.generated_count,
                    'updated': self.updated_count,
                    'skipped': self.skipped_count,
                    'total_processed': len(top_100_agents)
                }
                
        except Exception as e:
            logger.error(f"❌ Error generating Top 100 agents: {str(e)}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _process_agent(self, agent_data, rank):
        """Process individual agent from ranking data"""
        try:
            agent_name = agent_data['name']
            
            # Check if agent already exists
            existing_agent = AIAgent.query.filter_by(name=agent_name).first()
            
            if existing_agent and existing_agent.is_active:
                # Update existing agent with latest data
                self._update_existing_agent(existing_agent, agent_data, rank)
                self.updated_count += 1
                logger.info(f"🔄 Updated #{rank}: {agent_name}")
            else:
                # Create new agent
                new_agent = self._create_new_agent(agent_data, rank)
                db.session.add(new_agent)
                self.generated_count += 1
                logger.info(f"✨ Generated #{rank}: {agent_name}")
                
        except Exception as e:
            logger.error(f"❌ Error processing agent {agent_data.get('name', 'Unknown')}: {str(e)}")
            self.skipped_count += 1
    
    def _create_new_agent(self, agent_data, rank):
        """Create new AIAgent from ranking data"""
        
        # Calculate optimized pricing
        base_price = self._calculate_base_price(agent_data, rank)
        monthly_price = self._calculate_monthly_price(base_price, agent_data['category'])
        
        # Generate comprehensive capabilities
        capabilities = self._generate_capabilities(agent_data)
        
        # Create success metrics
        success_metrics = self._generate_success_metrics(agent_data)
        
        # Generate specialization tags
        specialization_tags = self._generate_specialization_tags(agent_data)
        
        # Create new agent
        agent = AIAgent(
            name=agent_data['name'],
            description=agent_data['specialization'],
            category=agent_data['category'],
            base_prompt=self._generate_base_prompt(agent_data),
            pricing_tier=self._determine_pricing_tier(rank),
            base_price=base_price,
            monthly_price=monthly_price,
            capabilities=capabilities,
            is_active=True,
            specialization_tags=specialization_tags,
            expertise_level=int(agent_data['experience_years']),
            practical_projects=agent_data['proven_projects'],
            collaboration_rate=agent_data.get('collaboration_rate', 0.997),
            compliance_frameworks=self._get_compliance_frameworks(agent_data['category']),
            industry_category=self._map_category_to_industry(agent_data['category']),
            role_level=self._determine_role_level(rank),
            success_metrics=success_metrics,
            certifications=self._generate_certifications(agent_data),
            case_studies=self._generate_case_studies(agent_data),
            default_model="gpt-4o",
            model_pricing_modifier=1.0,
            creator_id=None,  # System created
            creator_revenue_share=0.0,
            approval_status="approved",
            submission_date=datetime.utcnow(),
            is_featured=rank <= 10,  # Top 10 are featured
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return agent
    
    def _update_existing_agent(self, agent, agent_data, rank):
        """Update existing agent with latest ranking data"""
        
        # Update core fields
        agent.description = agent_data['specialization']
        agent.expertise_level = int(agent_data['experience_years'])
        agent.practical_projects = agent_data['proven_projects']
        agent.collaboration_rate = agent_data.get('collaboration_rate', 0.997)
        agent.is_featured = rank <= 10
        agent.updated_at = datetime.utcnow()
        
        # Update pricing if needed
        base_price = self._calculate_base_price(agent_data, rank)
        monthly_price = self._calculate_monthly_price(base_price, agent_data['category'])
        
        agent.base_price = base_price
        agent.monthly_price = monthly_price
        agent.pricing_tier = self._determine_pricing_tier(rank)
    
    def _calculate_base_price(self, agent_data, rank):
        """Calculate base price based on ROI multiplier and ranking"""
        
        roi_multiplier = agent_data.get('roi_multiplier', 5.0)
        category = agent_data['category']
        
        # Base pricing formula: ROI multiplier * category factor * rank factor
        category_factors = {
            'wealth_generation': 120,     # Highest value
            'revenue_optimization': 90,
            'strategic_consulting': 80,
            'compliance_risk': 70,
            'innovation_growth': 85,
            'market_intelligence': 65
        }
        
        base_factor = category_factors.get(category, 75)
        rank_multiplier = max(0.7, 1.2 - (rank * 0.005))  # Higher ranks get premium
        
        base_price = int(roi_multiplier * base_factor * rank_multiplier)
        
        # Apply psychological pricing
        if base_price < 100:
            return max(49, base_price)
        elif base_price < 300:
            return int(base_price / 10) * 10 - 1  # e.g., 199, 289
        else:
            return int(base_price / 25) * 25 - 1  # e.g., 399, 499
    
    def _calculate_monthly_price(self, base_price, category):
        """Calculate monthly price using optimized pricing strategy"""
        
        # Use optimized pricing ratios (6-15% of base price)
        pricing_ratios = {
            'wealth_generation': 0.06,      # Elite: 6%
            'revenue_optimization': 0.08,   # Professional: 8% 
            'strategic_consulting': 0.10,   # Professional: 10%
            'compliance_risk': 0.12,        # Essential: 12%
            'innovation_growth': 0.09,      # Professional: 9%
            'market_intelligence': 0.15     # Essential: 15%
        }
        
        ratio = pricing_ratios.get(category, 0.10)
        monthly_price = int(base_price * ratio)
        
        # Psychological pricing for monthly
        if monthly_price < 50:
            return max(9, monthly_price)
        else:
            return int(monthly_price / 5) * 5 - 1  # e.g., 39, 49, 79
    
    def _determine_pricing_tier(self, rank):
        """Determine pricing tier based on ranking"""
        if rank <= 20:
            return "elite"
        elif rank <= 60:
            return "professional"
        else:
            return "essential"
    
    def _determine_role_level(self, rank):
        """Determine role level based on ranking"""
        if rank <= 10:
            return "c_suite"
        elif rank <= 30:
            return "director"
        elif rank <= 60:
            return "manager"
        else:
            return "specialist"
    
    def _generate_capabilities(self, agent_data):
        """Generate capabilities JSON from agent data"""
        
        base_capabilities = [
            "Advanced problem-solving and strategic thinking",
            "Real-time data analysis and insights",
            "Automated decision support",
            "Integration with existing workflows",
            "Customizable outputs and reporting"
        ]
        
        # Add category-specific capabilities
        category_capabilities = {
            'wealth_generation': [
                "Investment portfolio optimization",
                "Risk-adjusted return analysis",
                "Market trend prediction",
                "Tax optimization strategies"
            ],
            'revenue_optimization': [
                "Revenue stream analysis",
                "Customer lifetime value optimization",
                "Pricing strategy development",
                "Sales funnel optimization"
            ],
            'strategic_consulting': [
                "Strategic planning facilitation",
                "Competitive analysis",
                "Market research and intelligence",
                "Change management support"
            ],
            'compliance_risk': [
                "Regulatory compliance monitoring",
                "Risk assessment and mitigation",
                "Policy development and implementation",
                "Audit preparation and support"
            ]
        }
        
        category = agent_data['category']
        specific_caps = category_capabilities.get(category, [])
        
        all_capabilities = base_capabilities + specific_caps
        return json.dumps(all_capabilities)
    
    def _generate_specialization_tags(self, agent_data):
        """Generate specialization tags from agent data"""
        
        category = agent_data['category']
        name = agent_data['name']
        
        # Extract key terms from name and specialization
        tags = []
        
        # Category-based tags
        category_tags = {
            'wealth_generation': ['investment', 'wealth', 'finance', 'portfolio', 'returns'],
            'revenue_optimization': ['revenue', 'sales', 'marketing', 'growth', 'optimization'],
            'strategic_consulting': ['strategy', 'consulting', 'planning', 'analysis', 'advisory'],
            'compliance_risk': ['compliance', 'risk', 'legal', 'regulatory', 'governance']
        }
        
        tags.extend(category_tags.get(category, []))
        
        # Extract from name
        name_words = name.lower().replace(' ai agent', '').replace(' expert', '').replace(' specialist', '').split()
        tags.extend([word for word in name_words if len(word) > 3])
        
        # Geographic markets
        tags.extend(['US', 'UK', 'DE', 'CH', 'AT'])
        
        return ','.join(set(tags))
    
    def _generate_base_prompt(self, agent_data):
        """Generate base prompt for agent"""
        
        prompt = f"""You are {agent_data['name']}, an elite AI agent with {agent_data['experience_years']:.1f} years of expertise.

SPECIALIZATION: {agent_data['specialization']}

EXPERTISE LEVEL: {agent_data['experience_years']:.1f} years of proven experience
PROVEN PROJECTS: {agent_data['proven_projects']:,}+ successful implementations
SUCCESS RATE: {agent_data['success_rate']*100:.1f}%

Your role is to provide expert-level guidance, analysis, and strategic recommendations in your specialized domain. You combine deep theoretical knowledge with extensive practical experience to deliver actionable insights that drive measurable results.

APPROACH:
1. Analyze the situation comprehensively
2. Apply proven methodologies and best practices
3. Provide specific, actionable recommendations
4. Consider implementation challenges and solutions
5. Focus on measurable outcomes and ROI

Always maintain the highest standards of professionalism and deliver value that justifies the premium positioning of this AI agent service."""

        return prompt
    
    def _generate_success_metrics(self, agent_data):
        """Generate success metrics JSON"""
        
        metrics = {
            'experience_years': agent_data['experience_years'],
            'proven_projects': agent_data['proven_projects'],
            'success_rate': agent_data['success_rate'],
            'roi_multiplier': agent_data.get('roi_multiplier', 5.0),
            'client_satisfaction': 0.985,
            'project_completion_rate': 0.997,
            'average_project_value': 50000,
            'repeat_client_rate': 0.89
        }
        
        return json.dumps(metrics)
    
    def _generate_certifications(self, agent_data):
        """Generate certifications based on category"""
        
        category_certs = {
            'wealth_generation': [
                "Certified Financial Planner (CFP)",
                "Chartered Financial Analyst (CFA)", 
                "Financial Risk Manager (FRM)",
                "Certified Investment Management Analyst (CIMA)"
            ],
            'revenue_optimization': [
                "Certified Revenue Management Executive (CRME)",
                "Digital Marketing Institute Certification",
                "Google Analytics Certified",
                "HubSpot Revenue Operations Certification"
            ],
            'strategic_consulting': [
                "Certified Management Consultant (CMC)",
                "Project Management Professional (PMP)",
                "Lean Six Sigma Black Belt",
                "Strategy& Consulting Certification"
            ],
            'compliance_risk': [
                "Certified Compliance & Ethics Professional (CCEP)",
                "Certified Risk Management Professional (CRMP)",
                "ISO 27001 Lead Auditor",
                "GDPR Certified Data Protection Officer"
            ]
        }
        
        category = agent_data['category']
        certs = category_certs.get(category, ["Industry Expert Certification"])
        
        return json.dumps(certs)
    
    def _generate_case_studies(self, agent_data):
        """Generate case studies JSON"""
        
        case_studies = [
            {
                "title": f"Delivered {agent_data.get('roi_multiplier', 5):.1f}x ROI for Fortune 500 Client",
                "industry": "Technology",
                "result": f"${agent_data.get('roi_multiplier', 5)*500000:,.0f} value created",
                "duration": "6 months"
            },
            {
                "title": "Strategic Transformation Initiative",
                "industry": "Financial Services", 
                "result": "45% efficiency improvement",
                "duration": "12 months"
            },
            {
                "title": "Market Expansion Strategy",
                "industry": "Manufacturing",
                "result": "3 new markets successfully entered",
                "duration": "9 months"
            }
        ]
        
        return json.dumps(case_studies)
    
    def _get_compliance_frameworks(self, category):
        """Get relevant compliance frameworks for category"""
        
        frameworks = {
            'wealth_generation': "SEC,FINRA,MiFID II,GDPR,SOX",
            'revenue_optimization': "GDPR,CCPA,PCI DSS,SOC 2",
            'strategic_consulting': "ISO 27001,SOC 2,GDPR,HIPAA",
            'compliance_risk': "GDPR,HIPAA,SOX,ISO 27001,PCI DSS,CCPA"
        }
        
        return frameworks.get(category, "GDPR,SOC 2")
    
    def _map_category_to_industry(self, category):
        """Map agent category to industry category"""
        
        mapping = {
            'wealth_generation': 'Financial Services',
            'revenue_optimization': 'Marketing & Sales',
            'strategic_consulting': 'Business Consulting',
            'compliance_risk': 'Legal & Compliance',
            'innovation_growth': 'Technology & Innovation',
            'market_intelligence': 'Research & Analytics'
        }
        
        return mapping.get(category, 'Business Services')

def main():
    """Main execution function"""
    generator = Top100MarketplaceGenerator()
    result = generator.generate_all_top100_agents()
    
    if result['success']:
        print(f"✅ Successfully generated Top 100 AI Agents marketplace!")
        print(f"   - New agents: {result['generated']}")
        print(f"   - Updated agents: {result['updated']}")
        print(f"   - Total processed: {result['total_processed']}")
    else:
        print(f"❌ Failed to generate agents: {result['error']}")
    
    return result

if __name__ == "__main__":
    main()