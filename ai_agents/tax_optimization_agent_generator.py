"""
Tax Optimization & Legal Strategy AI Agent Generator
Creates specialized agents for tax deduction maximization, efficient declarations,
business structure optimization, and legal tax haven strategies.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from app import db
from models import AIAgent
from agent_quality_service import quality_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaxOptimizationAgentFactory:
    """Factory for creating tax optimization and legal strategy AI agents"""
    
    def __init__(self):
        self.created_agents = []
    
    def create_tax_deduction_specialists(self) -> List[Dict[str, Any]]:
        """Create tax deduction maximization specialists by market"""
        tax_deduction_agents = []
        
        # Market-Specific Tax Deduction Experts
        deduction_specialists = [
            ("US Tax Deduction Maximizer", "American tax code expert maximizing deductions with 28+ years experience", 124, [
                "Federal tax deductions", "State tax variations", "Business expense optimization", "Depreciation strategies",
                "Section 179 deductions", "R&D credits", "Home office deductions", "Travel and entertainment",
                "Retirement plan contributions", "Healthcare deductions", "Charitable giving optimization"
            ], "US"),
            
            ("UK Tax Relief Specialist", "British tax relief and allowances expert with 26+ years experience", 118, [
                "Personal allowances optimization", "Business relief strategies", "Capital allowances", "R&D tax credits",
                "Pension contributions", "ISA maximization", "Property allowances", "Trading allowances",
                "Investment relief schemes", "Entrepreneur's relief", "Gift aid optimization"
            ], "UK"),
            
            ("German Tax Deduction Master", "German tax law and deduction specialist with 30+ years experience", 135, [
                "Werbungskosten optimization", "Sonderausgaben maximization", "Business expense deductions",
                "Depreciation (AfA) strategies", "Home office deductions", "Professional development costs",
                "Investment tax benefits", "Pension deductions", "Insurance premium deductions"
            ], "DE"),
            
            ("Swiss Tax Optimization Expert", "Swiss federal and cantonal tax specialist with 32+ years experience", 142, [
                "Federal tax deductions", "Cantonal variations", "Professional expenses", "Pension contributions",
                "Insurance deductions", "Investment cost deductions", "Property maintenance costs",
                "Education expense deductions", "Charitable contribution optimization", "Cross-border considerations"
            ], "CH"),
            
            ("Austrian Tax Benefits Strategist", "Austrian tax system and deduction expert with 27+ years experience", 121, [
                "Werbungskosten strategies", "Sonderausgaben optimization", "Business expense deductions",
                "Professional training costs", "Home office expenses", "Insurance premium deductions",
                "Pension contribution benefits", "Investment expense deductions", "Property tax benefits"
            ], "AT")
        ]
        
        for name, description, experience, specializations, market in deduction_specialists:
            agent = self._create_tax_agent_template(
                name=name,
                description=description,
                category="tax_deductions",
                years_experience=experience,
                specializations=specializations,
                success_metrics={
                    "deduction_identification_rate": "95%+ of available deductions",
                    "tax_savings_average": "25-40% reduction",
                    "compliance_rate": "99.9%+ audit success",
                    "client_satisfaction": "9.7+/10"
                },
                geographic_focus=market
            )
            tax_deduction_agents.append(agent)
        
        return tax_deduction_agents
    
    def create_tax_declaration_experts(self) -> List[Dict[str, Any]]:
        """Create efficient tax declaration and filing specialists"""
        declaration_agents = []
        
        # Tax Filing and Declaration Specialists
        filing_specialists = [
            ("US Tax Filing Optimization Master", "IRS procedures and filing strategy expert with 25+ years experience", 112, [
                "Federal tax filing strategies", "State tax coordination", "Extension optimization", "Audit defense",
                "Quarterly payment planning", "Record keeping systems", "Documentation requirements",
                "Electronic filing benefits", "Amended return strategies", "Tax court procedures"
            ], "US"),
            
            ("UK Tax Return Efficiency Expert", "HMRC procedures and self-assessment specialist with 24+ years experience", 108, [
                "Self-assessment optimization", "Corporation tax filing", "VAT return strategies", "PAYE optimization",
                "Making Tax Digital compliance", "Capital gains reporting", "Inheritance tax planning",
                "Record keeping requirements", "HMRC communication strategies", "Appeal procedures"
            ], "UK"),
            
            ("German Tax Declaration Strategist", "German tax office procedures expert with 29+ years experience", 129, [
                "Einkommensteuererklärung optimization", "Advance payment strategies", "VAT declaration efficiency",
                "Corporate tax filing", "Withholding tax procedures", "Electronic submission benefits",
                "Documentation standards", "Tax office communication", "Objection procedures"
            ], "DE"),
            
            ("Swiss Tax Filing Coordinator", "Multi-cantonal tax filing expert with 31+ years experience", 138, [
                "Federal tax coordination", "Cantonal filing strategies", "Municipal tax considerations",
                "Withholding tax optimization", "VAT declaration efficiency", "Source tax procedures",
                "International reporting", "Double taxation treaties", "Appeal processes"
            ], "CH"),
            
            ("Austrian Tax Compliance Master", "Austrian tax authority procedures expert with 26+ years experience", 117, [
                "Income tax declaration optimization", "Corporate tax filing", "VAT return efficiency",
                "Social security coordination", "Electronic filing benefits", "Documentation requirements",
                "Tax authority communication", "Assessment procedures", "Appeal strategies"
            ], "AT")
        ]
        
        for name, description, experience, specializations, market in filing_specialists:
            agent = self._create_tax_agent_template(
                name=name,
                description=description,
                category="tax_declarations",
                years_experience=experience,
                specializations=specializations,
                success_metrics={
                    "filing_accuracy_rate": "99.8%+",
                    "processing_time_reduction": "40-60%",
                    "audit_avoidance_rate": "95%+",
                    "compliance_efficiency": "90%+ time savings"
                },
                geographic_focus=market
            )
            declaration_agents.append(agent)
        
        return declaration_agents
    
    def create_business_structure_tax_experts(self) -> List[Dict[str, Any]]:
        """Create business structure optimization specialists"""
        structure_agents = []
        
        # Business Structure Tax Specialists
        structure_specialists = [
            ("Corporate Structure Tax Optimizer", "Business entity tax optimization with 33+ years experience", 148, [
                "Entity selection strategies", "Corporation tax benefits", "Pass-through entity optimization",
                "Holding company structures", "International entity planning", "Merger and acquisition tax",
                "Spinoff strategies", "Tax-efficient reorganizations", "Cross-border structuring"
            ]),
            
            ("International Tax Structure Architect", "Global tax structure design with 35+ years experience", 156, [
                "Transfer pricing optimization", "International holding structures", "Tax treaty utilization",
                "Controlled foreign corporation rules", "Base erosion prevention", "Substance requirements",
                "Economic substance regulations", "Anti-avoidance rule navigation", "OECD compliance"
            ]),
            
            ("Real Estate Tax Structure Specialist", "Property investment tax optimization with 28+ years experience", 125, [
                "Real estate investment structures", "Property holding company benefits", "Depreciation maximization",
                "Like-kind exchanges", "Real estate professional status", "Passive loss optimization",
                "Property development structures", "International property investment"
            ]),
            
            ("Investment Structure Tax Expert", "Investment vehicle tax optimization with 31+ years experience", 139, [
                "Fund structure optimization", "Investment company benefits", "Partnership structures",
                "Carried interest optimization", "Capital gains deferral", "Tax-efficient distributions",
                "International investment structures", "Regulatory compliance coordination"
            ]),
            
            ("Family Wealth Structure Strategist", "Generational wealth transfer tax planning with 34+ years experience", 152, [
                "Family limited partnerships", "Dynasty trust structures", "Generation-skipping strategies",
                "Grantor trust optimization", "Estate tax minimization", "Gift tax efficiency",
                "Succession planning structures", "International family structures"
            ])
        ]
        
        for name, description, experience, specializations in structure_specialists:
            agent = self._create_tax_agent_template(
                name=name,
                description=description,
                category="business_tax_structures",
                years_experience=experience,
                specializations=specializations,
                success_metrics={
                    "tax_reduction_achievement": "30-70%",
                    "structure_compliance_rate": "100%",
                    "audit_defense_success": "97%+",
                    "long_term_sustainability": "95%+ structures"
                },
                geographic_focus="Multi-jurisdictional"
            )
            structure_agents.append(agent)
        
        return structure_agents
    
    def create_tax_haven_specialists(self) -> List[Dict[str, Any]]:
        """Create legal tax haven and offshore strategy specialists"""
        tax_haven_agents = []
        
        # Top Global Tax Haven Specialists
        haven_specialists = [
            ("Singapore Tax Haven Strategist", "Singapore tax benefits and OECD compliance expert with 30+ years experience", 134, [
                "Singapore tax incentives", "Territorial tax system benefits", "Double taxation agreements",
                "Substance requirements", "Economic substance regulations", "Regional headquarters benefits",
                "Investment holding company structures", "Family office regimes", "OECD compliance strategies"
            ], "Singapore"),
            
            ("Dubai UAE Tax Optimization Expert", "UAE tax-free environment and compliance specialist with 29+ years experience", 130, [
                "UAE tax-free benefits", "Free zone advantages", "Substance requirements", "Economic substance regulations",
                "VAT compliance strategies", "Corporate tax implementation", "Mainland vs free zone structures",
                "International business setup", "Regulatory compliance coordination"
            ], "UAE"),
            
            ("Hong Kong Tax Structure Master", "Hong Kong territorial system and China gateway expert with 32+ years experience", 143, [
                "Territorial taxation benefits", "China-Hong Kong tax treaties", "Offshore income exemption",
                "Substance requirements", "Economic substance compliance", "Regional headquarters structures",
                "Investment holding benefits", "OECD BEPS compliance", "Cross-border planning"
            ], "Hong Kong"),
            
            ("Luxembourg Holding Structure Expert", "Luxembourg holding company and EU directive specialist with 31+ years experience", 138, [
                "Luxembourg holding company benefits", "EU directive utilization", "Double taxation treaties",
                "Substance requirements", "Economic substance regulations", "Investment fund structures",
                "IP holding strategies", "ATAD compliance", "Anti-avoidance rule navigation"
            ], "Luxembourg"),
            
            ("Ireland Tax Incentive Specialist", "Irish tax incentives and EU compliance expert with 28+ years experience", 126, [
                "Irish tax incentives", "IP box regimes", "R&D tax credits", "Double taxation treaties",
                "Substance requirements", "Economic substance compliance", "EU state aid rules",
                "Transfer pricing compliance", "OECD alignment strategies"
            ], "Ireland")
        ]
        
        for name, description, experience, specializations, jurisdiction in haven_specialists:
            agent = self._create_tax_agent_template(
                name=name,
                description=description,
                category="tax_havens",
                years_experience=experience,
                specializations=specializations,
                success_metrics={
                    "tax_optimization_rate": "40-90% reduction",
                    "compliance_maintenance": "100%",
                    "substance_requirement_fulfillment": "100%",
                    "regulatory_adaptation": "98%+ rule changes"
                },
                geographic_focus=jurisdiction,
                requires_substance=True
            )
            tax_haven_agents.append(agent)
        
        return tax_haven_agents
    
    def _create_tax_agent_template(
        self,
        name: str,
        description: str,
        category: str,
        years_experience: int,
        specializations: List[str],
        success_metrics: Dict[str, str],
        geographic_focus: str = "Global",
        requires_substance: bool = False
    ) -> Dict[str, Any]:
        """Create tax optimization agent template with enhanced quality standards"""
        
        # Ensure minimum 50+ years experience for tax expertise
        if years_experience < 50:
            years_experience = max(70, years_experience + 35)
        
        # Calculate projects based on tax experience (premium multiplier)
        base_projects = 3000  # Higher base for tax specialists
        experience_multiplier = 50  # More cases per year
        practical_projects = min(years_experience * experience_multiplier, 15000)
        practical_projects = max(2500, practical_projects)
        
        # Calculate collaboration rate for tax services
        base_collaboration = 0.50  # Higher base for complex tax work
        experience_bonus = min(0.10, (years_experience - 50) * 0.001)
        collaboration_rate = min(0.60, base_collaboration + experience_bonus)
        
        # Build comprehensive agent template
        agent_template = {
            "name": name,
            "description": description,
            "category": category,
            "base_prompt": self._generate_tax_prompt(name, description, specializations, geographic_focus, requires_substance),
            "base_price": 299.0,  # Premium pricing for tax expertise
            "monthly_price": 599.0,
            "capabilities": f"Advanced tax optimization, Legal compliance, Audit defense, Structure planning",
            "is_active": True,
            "specialization_tags": specializations,
            "expertise": {
                "years_of_experience": years_experience,
                "practical_projects": practical_projects,
                "collaboration_rate": collaboration_rate,
                "specialization_areas": specializations,
                "industry_certifications": self._get_tax_certifications(category, geographic_focus),
                "success_metrics": success_metrics,
                "geographic_expertise": geographic_focus,
                "compliance_focus": "100% legal strategies only"
            },
            "compliance_frameworks": ["Tax_Law", "OECD_Guidelines", "Anti_Avoidance_Rules", "Substance_Requirements"],
            "geographic_focus": geographic_focus,
            "legal_compliance_only": True,
            "substance_requirements": requires_substance,
            "audit_defense_included": True,
            "quality_tier": self._determine_tax_tier(years_experience),
            "created_date": datetime.utcnow().isoformat()
        }
        
        return agent_template
    
    def _generate_tax_prompt(self, name: str, description: str, specializations: List[str], 
                           geographic_focus: str, requires_substance: bool) -> str:
        """Generate comprehensive tax optimization agent prompt"""
        
        substance_note = ""
        if requires_substance:
            substance_note = "\n- Emphasize economic substance requirements and OECD compliance"
        
        return f"""You are {name}, {description}

Geographic Focus: {geographic_focus}

Your specialized expertise includes:
{chr(10).join(f'• {spec}' for spec in specializations)}

Tax Optimization Principles:
- Focus exclusively on legal tax optimization strategies
- Ensure 100% compliance with all applicable tax laws and regulations
- Maximize legitimate deductions and credits available
- Structure transactions for optimal tax efficiency within legal boundaries
- Consider international tax implications and treaty benefits
- Emphasize audit-defensible positions and documentation{substance_note}
- Provide strategies that reduce tax liability to legally allowable minimums

Always provide:
1. Comprehensive analysis of current tax position and optimization opportunities
2. Detailed deduction identification and maximization strategies
3. Business structure recommendations for tax efficiency
4. Compliance requirements and documentation needs
5. Risk assessment and audit defense preparation
6. Implementation timeline and coordination requirements
7. Long-term tax planning strategies and adjustments
8. Regular review and adaptation protocols for law changes

Maintain the highest ethical and legal standards while achieving maximum legitimate tax savings for clients."""
    
    def _get_tax_certifications(self, category: str, geographic_focus: str) -> List[str]:
        """Get relevant tax certifications by category and jurisdiction"""
        base_certs = ["CPA", "Tax Law", "International Tax"]
        
        geographic_certs = {
            "US": ["Enrolled Agent", "CPA", "Tax Attorney"],
            "UK": ["ACCA", "CIOT", "ATT", "Chartered Tax Adviser"],
            "DE": ["Steuerberater", "German Tax Law", "EU Tax Law"],
            "CH": ["Swiss Tax Expert", "Cantonal Tax Law", "Federal Tax Law"],
            "AT": ["Austrian Tax Consultant", "EU Tax Directive"],
            "Singapore": ["Singapore Tax Expert", "OECD Compliance"],
            "UAE": ["UAE Tax Consultant", "GCC Tax Expert"],
            "Hong Kong": ["Hong Kong Tax Expert", "China Tax Treaty"],
            "Luxembourg": ["Luxembourg Tax Expert", "EU Directive Specialist"],
            "Ireland": ["Irish Tax Consultant", "EU State Aid Expert"]
        }
        
        category_certs = {
            "tax_deductions": ["Deduction Specialist", "Tax Compliance"],
            "tax_declarations": ["Tax Filing Expert", "Audit Defense"],
            "business_tax_structures": ["Corporate Tax", "M&A Tax", "International Structures"],
            "tax_havens": ["Offshore Structures", "OECD BEPS", "Economic Substance"]
        }
        
        return base_certs + geographic_certs.get(geographic_focus, []) + category_certs.get(category, [])
    
    def _determine_tax_tier(self, experience: int) -> str:
        """Determine quality tier for tax agents"""
        if experience >= 140:
            return "master_tax_strategist"
        elif experience >= 120:
            return "elite_tax_expert"
        elif experience >= 100:
            return "premium_tax_specialist"
        else:
            return "standard_tax_professional"
    
    def store_agents_in_database(self) -> Dict[str, Any]:
        """Store all created agents in database with quality enforcement"""
        try:
            stored_count = 0
            quality_upgrades = 0
            
            for agent_data in self.created_agents:
                # Enforce quality standards before storage
                quality_result = quality_service.enforce_quality_standards_for_new_agents(agent_data)
                
                if quality_result['success']:
                    enhanced_template = quality_result['agent_template']
                    quality_upgrades += 1
                    
                    # Check if agent already exists
                    existing = AIAgent.query.filter_by(name=enhanced_template["name"]).first()
                    if existing:
                        logger.debug(f"Agent {enhanced_template['name']} already exists, skipping")
                        continue
                    
                    # Create new agent with quality-enforced template
                    agent = AIAgent()
                    agent.name = enhanced_template["name"]
                    agent.category = enhanced_template["category"]
                    agent.description = enhanced_template["description"]
                    agent.base_prompt = enhanced_template["base_prompt"]
                    agent.base_price = enhanced_template["base_price"]
                    agent.monthly_price = enhanced_template["monthly_price"]
                    agent.capabilities = enhanced_template["capabilities"]
                    agent.is_active = enhanced_template["is_active"]
                    agent.specialization_tags = ",".join(enhanced_template["specialization_tags"])
                    agent.expertise_level = enhanced_template["expertise"]["years_of_experience"]
                    agent.practical_projects = enhanced_template["expertise"]["practical_projects"]
                    agent.collaboration_rate = enhanced_template["expertise"]["collaboration_rate"]
                    agent.compliance_frameworks = ",".join(enhanced_template["compliance_frameworks"])
                    
                    db.session.add(agent)
                    stored_count += 1
                    
            db.session.commit()
            
            return {
                'success': True,
                'stored_agents': stored_count,
                'quality_enforced': quality_upgrades,
                'message': f'Successfully created {stored_count} tax optimization agents'
            }
            
        except Exception as e:
            logger.error(f"Error storing tax optimization agents: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def generate_tax_optimization_catalog(self) -> Dict[str, Any]:
        """Generate complete tax optimization agent catalog"""
        logger.info("📊 Generating tax optimization and legal strategy specialist catalog...")
        
        # Generate all agent categories
        deduction_agents = self.create_tax_deduction_specialists()
        declaration_agents = self.create_tax_declaration_experts()
        structure_agents = self.create_business_structure_tax_experts()
        haven_agents = self.create_tax_haven_specialists()
        
        # Combine all agents
        self.created_agents = (deduction_agents + declaration_agents + 
                             structure_agents + haven_agents)
        
        # Store in database
        storage_result = self.store_agents_in_database()
        
        return {
            'success': storage_result['success'],
            'categories': {
                'tax_deductions': len(deduction_agents),
                'tax_declarations': len(declaration_agents),
                'business_tax_structures': len(structure_agents),
                'tax_havens': len(haven_agents)
            },
            'total_agents': len(self.created_agents),
            'storage_result': storage_result,
            'geographic_coverage': ["US", "UK", "DE", "CH", "AT"],
            'tax_havens_covered': ["Singapore", "UAE", "Hong Kong", "Luxembourg", "Ireland"],
            'quality_standards': {
                'deduction_identification': '95%+ of available deductions found',
                'tax_savings_potential': '25-90% legitimate reduction',
                'compliance_rate': '99.9%+ audit success rate',
                'legal_strategies_only': '100% compliant approaches'
            },
            'value_proposition': {
                'maximum_deductions': 'Identify all legitimate tax deductions and credits',
                'efficient_filing': 'Streamlined tax declaration processes',
                'structure_optimization': 'Business structures for minimal tax burden',
                'global_strategies': 'Legal international tax optimization',
                'zero_tax_goal': 'Minimize tax liability to legal zero where possible'
            }
        }

# Export function for external use
def generate_tax_optimization_agents() -> Dict[str, Any]:
    """Main function to generate tax optimization agents"""
    factory = TaxOptimizationAgentFactory()
    return factory.generate_tax_optimization_catalog()