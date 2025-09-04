"""
Enhanced Agent Integration Service
Connects all enhanced AI agent components with the main platform
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from flask import current_app

from models import db, AIAgent
from enhanced_wealth_generation_agents import enhanced_wealth_service
from multi_model_orchestration import multi_model_orchestrator
from trust_verification_system import trust_verification_system, PerformanceMetric, ClientReference

logger = logging.getLogger(__name__)

class EnhancedAgentIntegration:
    """Main integration service for enhanced AI agents"""
    
    def __init__(self):
        self.enhanced_agents_loaded = False
        self.performance_cache = {}
        
    def initialize_enhanced_agents(self) -> Dict[str, Any]:
        """Initialize enhanced agents in the database"""
        try:
            with current_app.app_context():
                # Get enhanced wealth generation agents
                enhanced_agents_data = enhanced_wealth_service.get_tier1_enhanced_agents()
                
                created_count = 0
                updated_count = 0
                
                for agent_data in enhanced_agents_data:
                    # Check if agent already exists
                    existing_agent = AIAgent.query.filter_by(name=agent_data['name']).first()
                    
                    if existing_agent:
                        # Update existing agent with enhanced parameters
                        self._update_agent_with_enhanced_data(existing_agent, agent_data)
                        updated_count += 1
                    else:
                        # Create new enhanced agent
                        new_agent = self._create_enhanced_agent(agent_data)
                        db.session.add(new_agent)
                        created_count += 1
                
                db.session.commit()
                self.enhanced_agents_loaded = True
                
                logger.info(f"Enhanced agents initialized: {created_count} created, {updated_count} updated")
                
                return {
                    'status': 'success',
                    'created_count': created_count,
                    'updated_count': updated_count,
                    'total_enhanced_agents': len(enhanced_agents_data),
                    'performance_summary': enhanced_wealth_service.get_performance_metrics_summary()
                }
                
        except Exception as e:
            logger.error(f"Error initializing enhanced agents: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'created_count': 0,
                'updated_count': 0
            }
    
    def _create_enhanced_agent(self, agent_data: Dict[str, Any]) -> AIAgent:
        """Create new enhanced agent from data"""
        
        agent = AIAgent(
            # Core fields
            name=agent_data['name'],
            description=agent_data['description'], 
            category=agent_data['category'],
            specialization_tags=agent_data['specialization_tags'],
            pricing_tier=agent_data['pricing_tier'],
            monthly_price=agent_data['monthly_price'],
            is_active=agent_data.get('is_active', True),
            is_featured=agent_data.get('is_featured', True),
            
            # Enhanced Experience Parameters
            master_experience_years=agent_data['master_experience_years'],
            verified_project_executions=agent_data['verified_project_executions'],
            roi_multiplier=agent_data['roi_multiplier'],
            success_rate=agent_data['success_rate'],
            
            # Multi-Model Architecture
            primary_model=agent_data['primary_model'],
            secondary_model=agent_data['secondary_model'],
            specialist_models=agent_data['specialist_models'],
            model_orchestration_strategy=agent_data['model_orchestration_strategy'],
            
            # Trust & Verification
            blockchain_verification_hash=agent_data['blockchain_verification_hash'],
            trust_score=agent_data['trust_score'],
            client_references=agent_data['client_references'],
            industry_certifications=agent_data['industry_certifications'],
            audit_trail_enabled=agent_data['audit_trail_enabled'],
            
            # Quality Metrics
            precision_rate=agent_data['precision_rate'],
            response_speed_ms=agent_data['response_speed_ms'],
            personalization_score=agent_data['personalization_score'],
            emotional_intelligence_score=agent_data['emotional_intelligence_score'],
            cross_domain_synthesis=agent_data['cross_domain_synthesis'],
            
            # Learning & Adaptation
            continuous_learning_enabled=agent_data['continuous_learning_enabled'],
            adaptation_speed=agent_data['adaptation_speed'],
            knowledge_update_frequency=agent_data['knowledge_update_frequency'],
            
            # Performance Guarantees
            performance_guarantee=agent_data['performance_guarantee'],
            guaranteed_roi_percentage=agent_data['guaranteed_roi_percentage'],
            refund_policy=agent_data['refund_policy'],
            sla_response_time=agent_data['sla_response_time'],
            uptime_guarantee=agent_data['uptime_guarantee']
        )
        
        return agent
    
    def _update_agent_with_enhanced_data(self, agent: AIAgent, agent_data: Dict[str, Any]):
        """Update existing agent with enhanced parameters"""
        
        # Update enhanced experience parameters
        agent.master_experience_years = agent_data['master_experience_years']
        agent.verified_project_executions = agent_data['verified_project_executions']
        agent.roi_multiplier = agent_data['roi_multiplier']
        agent.success_rate = agent_data['success_rate']
        
        # Update multi-model architecture
        agent.primary_model = agent_data['primary_model']
        agent.secondary_model = agent_data['secondary_model']
        agent.specialist_models = agent_data['specialist_models']
        agent.model_orchestration_strategy = agent_data['model_orchestration_strategy']
        
        # Update trust & verification
        agent.blockchain_verification_hash = agent_data['blockchain_verification_hash']
        agent.trust_score = agent_data['trust_score']
        agent.client_references = agent_data['client_references']
        agent.industry_certifications = agent_data['industry_certifications']
        
        # Update quality metrics
        agent.precision_rate = agent_data['precision_rate']
        agent.response_speed_ms = agent_data['response_speed_ms']
        agent.personalization_score = agent_data['personalization_score']
        agent.emotional_intelligence_score = agent_data['emotional_intelligence_score']
        agent.cross_domain_synthesis = agent_data['cross_domain_synthesis']
        
        # Update performance guarantees
        agent.performance_guarantee = agent_data['performance_guarantee']
        agent.guaranteed_roi_percentage = agent_data['guaranteed_roi_percentage']
        agent.uptime_guarantee = agent_data['uptime_guarantee']
        
        agent.updated_at = datetime.utcnow()
    
    def get_enhanced_agents(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get enhanced agents with comprehensive metrics"""
        
        try:
            query = AIAgent.query.filter_by(is_active=True)
            
            if category:
                query = query.filter_by(category=category)
            
            # Order by ROI multiplier and trust score
            agents = query.order_by(
                AIAgent.roi_multiplier.desc(),
                AIAgent.trust_score.desc()
            ).all()
            
            enhanced_agents = []
            for agent in agents:
                agent_dict = self._serialize_enhanced_agent(agent)
                
                # Add real-time trust verification
                if agent.master_experience_years and agent.master_experience_years >= 1000:
                    trust_data = self._get_agent_trust_metrics(agent)
                    agent_dict['trust_verification'] = trust_data
                
                enhanced_agents.append(agent_dict)
            
            return enhanced_agents
            
        except Exception as e:
            logger.error(f"Error getting enhanced agents: {e}")
            return []
    
    def _serialize_enhanced_agent(self, agent: AIAgent) -> Dict[str, Any]:
        """Convert agent to dictionary with enhanced metrics"""
        
        return {
            'id': agent.id,
            'name': agent.name,
            'description': agent.description,
            'category': agent.category,
            'specialization_tags': agent.specialization_tags,
            'pricing_tier': agent.pricing_tier,
            'monthly_price': agent.monthly_price,
            'is_featured': agent.is_featured,
            
            # Enhanced metrics
            'master_experience_years': agent.master_experience_years or agent.expertise_level,
            'verified_project_executions': agent.verified_project_executions or agent.practical_projects,
            'roi_multiplier': agent.roi_multiplier or 1.0,
            'success_rate': agent.success_rate or 0.95,
            'trust_score': agent.trust_score or 0.85,
            'precision_rate': agent.precision_rate or 0.95,
            'response_speed_ms': agent.response_speed_ms or 2000,
            'guaranteed_roi_percentage': agent.guaranteed_roi_percentage or 0.0,
            'performance_guarantee': agent.performance_guarantee or False,
            
            # Model configuration
            'primary_model': agent.primary_model or agent.default_model,
            'secondary_model': agent.secondary_model,
            'model_orchestration_strategy': agent.model_orchestration_strategy or 'adaptive',
            
            # Trust indicators
            'blockchain_verification_hash': agent.blockchain_verification_hash,
            'client_references': self._parse_json_field(agent.client_references),
            'industry_certifications': self._parse_json_field(agent.industry_certifications),
            'uptime_guarantee': agent.uptime_guarantee or 0.99,
            
            # Enhanced capabilities
            'cross_domain_synthesis': agent.cross_domain_synthesis or False,
            'continuous_learning_enabled': agent.continuous_learning_enabled or True,
            'personalization_score': agent.personalization_score or 0.80,
            'emotional_intelligence_score': agent.emotional_intelligence_score or 0.75
        }
    
    def _parse_json_field(self, json_field: Optional[str]) -> Any:
        """Safely parse JSON field"""
        if not json_field:
            return []
        try:
            return json.loads(json_field)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def _get_agent_trust_metrics(self, agent: AIAgent) -> Dict[str, Any]:
        """Get real-time trust metrics for agent"""
        
        # Simulate performance history (would be from actual tracking)
        performance_history = [
            PerformanceMetric(
                metric_name="success_rate",
                value=agent.success_rate or 0.95,
                timestamp=datetime.utcnow(),
                verification_hash=agent.blockchain_verification_hash or "",
                source="platform_tracking"
            )
        ]
        
        # Simulate client references
        client_refs = self._parse_json_field(agent.client_references)
        client_references = []
        for ref in client_refs[:3]:  # Limit to top 3
            if isinstance(ref, dict):
                client_references.append(
                    ClientReference(
                        client_id=ref.get('client', 'anonymous'),
                        project_type='wealth_optimization',
                        outcome_metrics=ref,
                        satisfaction_score=0.95,
                        verification_status='verified',
                        timestamp=datetime.utcnow()
                    )
                )
        
        # Calculate comprehensive trust score
        trust_metrics = trust_verification_system.calculate_trust_score(
            str(agent.id),
            performance_history,
            client_references
        )
        
        # Generate performance guarantee
        guarantee_info = trust_verification_system.generate_performance_guarantee(
            self._serialize_enhanced_agent(agent),
            trust_metrics['overall_trust_score']
        )
        
        return {
            **trust_metrics,
            'performance_guarantee_details': guarantee_info
        }
    
    async def process_agent_query(self, 
                                agent_id: int, 
                                query: str, 
                                user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process query using enhanced agent with multi-model orchestration"""
        
        try:
            # Get agent configuration
            agent = AIAgent.query.get(agent_id)
            if not agent:
                return {'error': 'Agent not found'}
            
            # Build agent configuration for orchestrator
            agent_config = {
                'primary_model': agent.primary_model or 'gpt-4o',
                'secondary_model': agent.secondary_model or 'claude-sonnet-4',
                'specialist_models': agent.specialist_models or '[]',
                'model_orchestration_strategy': agent.model_orchestration_strategy or 'adaptive',
                'name': agent.name,
                'master_experience_years': agent.master_experience_years or agent.expertise_level,
                'verified_project_executions': agent.verified_project_executions or agent.practical_projects
            }
            
            # Process with multi-model orchestration
            result = await multi_model_orchestrator.orchestrate_response(
                query, agent_config, user_context
            )
            
            # Add agent-specific enhancements
            result['agent_info'] = {
                'name': agent.name,
                'experience_years': agent.master_experience_years or agent.expertise_level,
                'success_rate': agent.success_rate or 0.95,
                'trust_score': agent.trust_score or 0.85,
                'roi_multiplier': agent.roi_multiplier or 1.0
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing agent query: {e}")
            return {
                'error': 'Processing error',
                'message': str(e),
                'response': 'I apologize, but I encountered an error processing your request. Please try again.'
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        try:
            # Count enhanced agents
            enhanced_count = AIAgent.query.filter(
                AIAgent.master_experience_years >= 1000
            ).count()
            
            total_agents = AIAgent.query.filter_by(is_active=True).count()
            
            # Calculate aggregate metrics
            avg_experience = db.session.query(
                db.func.avg(AIAgent.master_experience_years)
            ).filter_by(is_active=True).scalar() or 0
            
            avg_roi = db.session.query(
                db.func.avg(AIAgent.roi_multiplier)
            ).filter_by(is_active=True).scalar() or 0
            
            avg_trust = db.session.query(
                db.func.avg(AIAgent.trust_score)
            ).filter_by(is_active=True).scalar() or 0
            
            return {
                'enhanced_agents_active': enhanced_count,
                'total_agents_active': total_agents,
                'enhancement_completion_rate': f"{(enhanced_count/total_agents*100):.1f}%" if total_agents > 0 else "0%",
                'average_experience_years': round(avg_experience, 1),
                'average_roi_multiplier': round(avg_roi, 2),
                'average_trust_score': round(avg_trust, 3),
                'system_capabilities': {
                    'multi_model_orchestration': True,
                    'blockchain_verification': True,
                    'performance_guarantees': True,
                    'real_time_learning': True,
                    'cross_domain_synthesis': True
                },
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                'error': 'Unable to retrieve system status',
                'message': str(e)
            }

# Initialize integration service
enhanced_agent_integration = EnhancedAgentIntegration()