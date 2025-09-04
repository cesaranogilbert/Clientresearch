"""
AI Agent Generation & Validation Service
Permanent system for consistent, high-quality AI agent creation and management
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from app import db
from models import AIAgent


@dataclass
class AgentGenerationRequest:
    """Request structure for generating new AI agents"""
    topic: str
    category: str
    count: int
    expertise_level_range: Tuple[int, int] = (50, 100)
    pricing_tier: str = 'professional'
    base_price_range: Tuple[float, float] = (399.0, 899.0)
    monthly_price_range: Tuple[float, float] = (299.0, 699.0)
    specialization_areas: Optional[List[str]] = None


@dataclass
class AgentValidationResult:
    """Result of agent validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    agent_data: Optional[Dict] = None


class AIAgentGenerationService:
    """
    Comprehensive AI Agent Generation & Validation Service
    Ensures consistent, high-quality agent creation with automatic validation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_rules = self._initialize_validation_rules()
        self.quality_thresholds = self._initialize_quality_thresholds()
        
    def _initialize_validation_rules(self) -> Dict:
        """Initialize comprehensive validation rules"""
        return {
            'name_length': {'min': 10, 'max': 100},
            'description_length': {'min': 50, 'max': 500},
            'expertise_level': {'min': 50, 'max': 100},
            'practical_projects': {'min': 1000, 'max': 5000},
            'collaboration_rate': {'min': 0.80, 'max': 1.0},
            'required_fields': ['name', 'description', 'category', 'base_prompt', 
                              'pricing_tier', 'base_price', 'monthly_price'],
            'pricing_tiers': ['basic', 'professional', 'enterprise', 'elite'],
            'valid_categories': ['wealth_generation', 'healthcare', 'technology', 
                               'creative', 'business', 'enterprise', 'marketing',
                               'finance', 'operations', 'analytics']
        }
    
    def _initialize_quality_thresholds(self) -> Dict:
        """Initialize quality thresholds for agent generation"""
        return {
            'minimum_expertise_years': 50,
            'minimum_projects': 1000,
            'minimum_collaboration_rate': 0.80,
            'maximum_duplicate_similarity': 0.30,
            'required_approval_status': 'approved',
            'required_active_status': True
        }
    
    def generate_agents_for_topic(self, request: AgentGenerationRequest) -> List[Dict]:
        """
        Generate comprehensive AI agents for a specific topic
        
        Args:
            request: AgentGenerationRequest with topic details
            
        Returns:
            List of validated agent data dictionaries
        """
        self.logger.info(f"🚀 Generating {request.count} agents for topic: {request.topic}")
        
        try:
            # Generate agent variations
            agent_variations = self._generate_agent_variations(request)
            
            # Validate each agent
            validated_agents = []
            for agent_data in agent_variations:
                validation_result = self._validate_agent_data(agent_data)
                
                if validation_result.is_valid:
                    validated_agents.append(validation_result.agent_data)
                else:
                    self.logger.warning(f"Agent validation failed: {validation_result.errors}")
            
            self.logger.info(f"✅ Generated {len(validated_agents)} validated agents")
            return validated_agents
            
        except Exception as e:
            self.logger.error(f"❌ Agent generation failed: {e}")
            return []
    
    def _generate_agent_variations(self, request: AgentGenerationRequest) -> List[Dict]:
        """Generate agent variations based on topic and requirements"""
        topic_keywords = self._extract_topic_keywords(request.topic)
        specialization_areas = request.specialization_areas or self._generate_specializations(request.topic)
        
        agents = []
        for i in range(request.count):
            # Create unique agent variation
            agent_name = self._generate_agent_name(request.topic, topic_keywords, i)
            description = self._generate_agent_description(request.topic, specialization_areas[i % len(specialization_areas)])
            
            # Calculate pricing based on tier and expertise
            base_price = self._calculate_price(request.base_price_range, request.pricing_tier, i)
            monthly_price = self._calculate_price(request.monthly_price_range, request.pricing_tier, i)
            
            # Calculate expertise metrics
            expertise_level = self._calculate_expertise_level(request.expertise_level_range, i)
            practical_projects = self._calculate_projects(expertise_level)
            collaboration_rate = self._calculate_collaboration_rate(expertise_level)
            
            agent_data = {
                'name': agent_name,
                'description': description,
                'category': request.category,
                'base_prompt': f'You are a {agent_name} with {expertise_level} years of experience in {request.topic}. {description}',
                'pricing_tier': request.pricing_tier,
                'base_price': base_price,
                'monthly_price': monthly_price,
                'capabilities': f'{request.topic} specialist with advanced expertise',
                'default_model': 'gpt-4o',
                'is_featured': True,
                'approval_status': 'approved',
                'is_active': True,
                'expertise_level': expertise_level,
                'practical_projects': practical_projects,
                'collaboration_rate': collaboration_rate,
                'specialization_tags': ', '.join(specialization_areas[:3])
            }
            
            agents.append(agent_data)
        
        return agents
    
    def _extract_topic_keywords(self, topic: str) -> List[str]:
        """Extract relevant keywords from topic"""
        # Convert topic to keywords
        keywords = topic.replace('_', ' ').replace('-', ' ').split()
        
        # Add relevant variations
        keyword_variations = []
        for keyword in keywords:
            keyword_variations.extend([
                keyword.capitalize(),
                keyword.upper(),
                keyword + ' Expert',
                keyword + ' Specialist',
                keyword + ' Master',
                keyword + ' Pro'
            ])
        
        return keyword_variations
    
    def _generate_specializations(self, topic: str) -> List[str]:
        """Generate specialization areas for the topic"""
        base_specializations = [
            f'{topic} strategy',
            f'{topic} optimization',
            f'{topic} analysis',
            f'{topic} implementation',
            f'{topic} consulting',
            f'{topic} management',
            f'{topic} development',
            f'{topic} research',
            f'{topic} innovation',
            f'{topic} excellence'
        ]
        
        # Add advanced specializations
        advanced_specializations = [
            f'Advanced {topic}',
            f'{topic} automation',
            f'{topic} intelligence',
            f'{topic} transformation',
            f'{topic} leadership'
        ]
        
        return base_specializations + advanced_specializations
    
    def _generate_agent_name(self, topic: str, keywords: List[str], index: int) -> str:
        """Generate unique agent name"""
        name_patterns = [
            f'{topic.title()} {keywords[index % len(keywords)]}',
            f'Elite {topic.title()} AI',
            f'{topic.title()} Mastery Expert',
            f'Advanced {topic.title()} Specialist',
            f'{topic.title()} Excellence AI'
        ]
        
        base_name = name_patterns[index % len(name_patterns)]
        
        # Ensure uniqueness
        if index > 0:
            base_name += f' {index + 1}'
        
        return base_name
    
    def _generate_agent_description(self, topic: str, specialization: str) -> str:
        """Generate comprehensive agent description"""
        return f'Elite specialist in {specialization} with advanced expertise in {topic}. Provides comprehensive solutions, strategic insights, and proven methodologies for optimal results. Combines deep theoretical knowledge with practical implementation experience.'
    
    def _calculate_price(self, price_range: Tuple[float, float], tier: str, index: int) -> float:
        """Calculate price based on tier and variation"""
        min_price, max_price = price_range
        
        # Tier multipliers
        tier_multipliers = {
            'basic': 0.7,
            'professional': 1.0,
            'enterprise': 1.3,
            'elite': 1.6
        }
        
        base_price = min_price + (max_price - min_price) * (index % 10) / 10
        return round(base_price * tier_multipliers.get(tier, 1.0), 2)
    
    def _calculate_expertise_level(self, range_tuple: Tuple[int, int], index: int) -> int:
        """Calculate expertise level with variation"""
        min_exp, max_exp = range_tuple
        return min_exp + (index % (max_exp - min_exp + 1))
    
    def _calculate_projects(self, expertise_level: int) -> int:
        """Calculate practical projects based on expertise level"""
        return max(1000, expertise_level * 20 + (expertise_level % 10) * 50)
    
    def _calculate_collaboration_rate(self, expertise_level: int) -> float:
        """Calculate collaboration rate based on expertise"""
        base_rate = 0.80
        bonus = min(0.15, (expertise_level - 50) / 100 * 0.15)
        return round(base_rate + bonus, 2)
    
    def _validate_agent_data(self, agent_data: Dict) -> AgentValidationResult:
        """Comprehensive validation of agent data"""
        errors = []
        warnings = []
        
        # Check required fields
        for field in self.validation_rules['required_fields']:
            if field not in agent_data or not agent_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate field lengths
        if len(agent_data.get('name', '')) < self.validation_rules['name_length']['min']:
            errors.append("Agent name too short")
        
        if len(agent_data.get('description', '')) < self.validation_rules['description_length']['min']:
            errors.append("Agent description too short")
        
        # Validate numeric ranges
        expertise = agent_data.get('expertise_level', 0)
        if not (self.validation_rules['expertise_level']['min'] <= expertise <= self.validation_rules['expertise_level']['max']):
            errors.append("Expertise level out of valid range")
        
        projects = agent_data.get('practical_projects', 0)
        if not (self.validation_rules['practical_projects']['min'] <= projects <= self.validation_rules['practical_projects']['max']):
            errors.append("Practical projects count out of valid range")
        
        collaboration = agent_data.get('collaboration_rate', 0)
        if not (self.validation_rules['collaboration_rate']['min'] <= collaboration <= self.validation_rules['collaboration_rate']['max']):
            errors.append("Collaboration rate out of valid range")
        
        # Validate categories and tiers
        if agent_data.get('pricing_tier') not in self.validation_rules['pricing_tiers']:
            errors.append("Invalid pricing tier")
        
        if agent_data.get('category') not in self.validation_rules['valid_categories']:
            warnings.append("Category not in standard list")
        
        # Check for duplicates
        if self._check_duplicate_agent(agent_data.get('name', '')):
            errors.append("Agent with similar name already exists")
        
        is_valid = len(errors) == 0
        
        return AgentValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            agent_data=agent_data if is_valid else None
        )
    
    def _check_duplicate_agent(self, name: str) -> bool:
        """Check if agent with similar name already exists"""
        try:
            existing = AIAgent.query.filter_by(name=name, is_active=True).first()
            return existing is not None
        except Exception:
            return False
    
    def create_agents_in_database(self, validated_agents: List[Dict]) -> Tuple[int, List[str]]:
        """
        Create validated agents in database with transaction safety
        
        Returns:
            Tuple of (created_count, error_messages)
        """
        created_count = 0
        errors = []
        
        try:
            for agent_data in validated_agents:
                # Double-check for duplicates
                existing = AIAgent.query.filter_by(name=agent_data['name']).first()
                if existing:
                    errors.append(f"Skipped duplicate: {agent_data['name']}")
                    continue
                
                # Create new agent
                if agent_data:
                    agent = AIAgent(**agent_data)
                    db.session.add(agent)
                    created_count += 1
                
                # Commit in batches of 20
                if created_count % 20 == 0:
                    db.session.commit()
                    self.logger.info(f"Batch committed: {created_count} agents created")
            
            # Final commit
            db.session.commit()
            
            self.logger.info(f"✅ Successfully created {created_count} agents in database")
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Database creation failed: {e}"
            self.logger.error(error_msg)
            errors.append(error_msg)
        
        return created_count, errors
    
    def generate_and_create_agents(self, request: AgentGenerationRequest) -> Dict:
        """
        Complete workflow: Generate, validate, and create agents in database
        
        Returns:
            Status dictionary with results
        """
        start_time = datetime.now()
        
        # Get current agent count
        initial_count = AIAgent.query.filter_by(is_active=True).count()
        
        # Generate validated agents
        validated_agents = self.generate_agents_for_topic(request)
        
        if not validated_agents:
            return {
                'success': False,
                'message': 'No valid agents generated',
                'initial_count': initial_count,
                'final_count': initial_count,
                'created_count': 0,
                'errors': ['Agent generation failed']
            }
        
        # Create agents in database
        created_count, errors = self.create_agents_in_database(validated_agents)
        
        # Get final count
        final_count = AIAgent.query.filter_by(is_active=True).count()
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return {
            'success': created_count > 0,
            'message': f'Successfully created {created_count} agents for {request.topic}',
            'initial_count': initial_count,
            'final_count': final_count,
            'created_count': created_count,
            'requested_count': request.count,
            'topic': request.topic,
            'category': request.category,
            'duration_seconds': duration,
            'errors': errors,
            'validation_passed': len(validated_agents),
            'milestone_progress': f'{final_count}/1000 agents ({(final_count/1000)*100:.1f}% complete)'
        }


# Convenience function for easy access
def generate_agents_for_topic(topic: str, category: str, count: int, **kwargs) -> Dict:
    """
    Convenience function to generate agents for a specific topic
    
    Args:
        topic: The topic/subject area for the agents
        category: The category to assign the agents to
        count: Number of agents to generate
        **kwargs: Additional parameters for AgentGenerationRequest
        
    Returns:
        Generation result dictionary
    """
    service = AIAgentGenerationService()
    request = AgentGenerationRequest(
        topic=topic,
        category=category,
        count=count,
        **kwargs
    )
    
    return service.generate_and_create_agents(request)


# Quality assurance function
def validate_agent_ecosystem() -> Dict:
    """
    Comprehensive validation of the entire agent ecosystem
    
    Returns:
        Validation report
    """
    service = AIAgentGenerationService()
    
    try:
        total_agents = AIAgent.query.filter_by(is_active=True).count()
        
        # Category distribution
        categories = db.session.query(AIAgent.category, db.func.count(AIAgent.id))\
            .filter_by(is_active=True)\
            .group_by(AIAgent.category)\
            .all()
        
        # Quality metrics
        avg_expertise = db.session.query(db.func.avg(AIAgent.expertise_level))\
            .filter_by(is_active=True).scalar() or 0
        
        avg_projects = db.session.query(db.func.avg(AIAgent.practical_projects))\
            .filter_by(is_active=True).scalar() or 0
        
        avg_collaboration = db.session.query(db.func.avg(AIAgent.collaboration_rate))\
            .filter_by(is_active=True).scalar() or 0
        
        return {
            'total_agents': total_agents,
            'milestone_status': 'COMPLETED' if total_agents >= 1000 else 'IN_PROGRESS',
            'milestone_progress': f'{total_agents}/1000 ({(total_agents/1000)*100:.1f}%)',
            'category_distribution': dict(categories),
            'quality_metrics': {
                'average_expertise_years': round(avg_expertise, 1),
                'average_projects': round(avg_projects),
                'average_collaboration_rate': round(avg_collaboration, 2)
            },
            'validation_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'error': f'Validation failed: {e}',
            'validation_timestamp': datetime.now().isoformat()
        }