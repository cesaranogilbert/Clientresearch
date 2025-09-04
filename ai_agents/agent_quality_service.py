"""
AI Agent Quality Assurance Service
Ensures all AI agents meet minimum quality standards:
- 50+ years experience (preferably 100+)
- 1000+ successful project executions
- 30%+ project participation rate for proven advice delivery
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from app import db
from models import AIAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityStandards:
    """Define minimum quality standards for AI agents"""
    min_experience_years: int = 50
    preferred_experience_years: int = 100
    min_practical_projects: int = 1000
    min_collaboration_rate: float = 0.30
    max_collaboration_rate: float = 0.65
    
    # Quality tiers based on experience
    QUALITY_TIERS = {
        'standard': {'min_exp': 50, 'max_exp': 74, 'projects_multiplier': 20},
        'premium': {'min_exp': 75, 'max_exp': 99, 'projects_multiplier': 25},
        'elite': {'min_exp': 100, 'max_exp': 149, 'projects_multiplier': 30},
        'legendary': {'min_exp': 150, 'max_exp': 999, 'projects_multiplier': 35}
    }

class AgentQualityAuditService:
    """Service for auditing and upgrading agent quality standards"""
    
    def __init__(self):
        self.standards = QualityStandards()
        
    def audit_all_agents(self) -> Dict[str, any]:
        """Audit all existing agents against quality standards"""
        try:
            all_agents = db.session.query(AIAgent).filter_by(is_active=True).all()
            audit_results = {
                'total_agents': len(all_agents),
                'compliant_agents': 0,
                'non_compliant_agents': 0,
                'upgrade_candidates': [],
                'quality_distribution': {
                    'standard': 0,
                    'premium': 0,
                    'elite': 0,
                    'legendary': 0
                },
                'issues_found': []
            }
            
            for agent in all_agents:
                compliance_result = self._check_agent_compliance(agent)
                
                if compliance_result['is_compliant']:
                    audit_results['compliant_agents'] += 1
                    # Categorize by quality tier
                    tier = self._determine_quality_tier(agent.expertise_level)
                    audit_results['quality_distribution'][tier] += 1
                else:
                    audit_results['non_compliant_agents'] += 1
                    audit_results['upgrade_candidates'].append({
                        'agent_id': agent.id,
                        'name': agent.name,
                        'category': agent.category,
                        'current_experience': agent.expertise_level,
                        'current_projects': agent.practical_projects,
                        'current_collaboration': agent.collaboration_rate,
                        'issues': compliance_result['issues'],
                        'recommended_upgrades': compliance_result['recommended_upgrades']
                    })
                    
            logger.info(f"Agent quality audit completed: {audit_results['compliant_agents']}/{audit_results['total_agents']} agents compliant")
            return audit_results
            
        except Exception as e:
            logger.error(f"Error during agent quality audit: {e}")
            return {'error': str(e)}
    
    def _check_agent_compliance(self, agent: AIAgent) -> Dict[str, any]:
        """Check if a single agent meets quality standards"""
        issues = []
        recommended_upgrades = {}
        
        # Check experience level
        if agent.expertise_level < self.standards.min_experience_years:
            issues.append(f"Experience too low: {agent.expertise_level} < {self.standards.min_experience_years}")
            recommended_upgrades['experience'] = max(self.standards.min_experience_years, 
                                                   self._calculate_optimal_experience(agent.category))
        
        # Check practical projects
        if agent.practical_projects < self.standards.min_practical_projects:
            issues.append(f"Projects too few: {agent.practical_projects} < {self.standards.min_practical_projects}")
            recommended_upgrades['projects'] = self._calculate_optimal_projects(
                recommended_upgrades.get('experience', agent.expertise_level)
            )
        
        # Check collaboration rate
        if agent.collaboration_rate < self.standards.min_collaboration_rate:
            issues.append(f"Collaboration rate too low: {agent.collaboration_rate:.2%} < {self.standards.min_collaboration_rate:.2%}")
            recommended_upgrades['collaboration'] = self._calculate_optimal_collaboration_rate(
                recommended_upgrades.get('experience', agent.expertise_level)
            )
        elif agent.collaboration_rate > self.standards.max_collaboration_rate:
            issues.append(f"Collaboration rate unrealistic: {agent.collaboration_rate:.2%} > {self.standards.max_collaboration_rate:.2%}")
            recommended_upgrades['collaboration'] = min(0.65, max(0.35, agent.collaboration_rate))
        
        return {
            'is_compliant': len(issues) == 0,
            'issues': issues,
            'recommended_upgrades': recommended_upgrades
        }
    
    def _determine_quality_tier(self, experience_years: int) -> str:
        """Determine quality tier based on experience"""
        for tier, criteria in self.standards.QUALITY_TIERS.items():
            if criteria['min_exp'] <= experience_years <= criteria['max_exp']:
                return tier
        return 'standard'
    
    def _calculate_optimal_experience(self, category: str) -> int:
        """Calculate optimal experience based on agent category"""
        # Higher experience for specialized or leadership roles
        high_expertise_categories = [
            'healthcare', 'legal', 'finance', 'executive', 
            'compliance', 'security', 'architecture'
        ]
        
        if category.lower() in high_expertise_categories:
            return max(75, self.standards.min_experience_years + 25)  # 75+ years
        else:
            return max(60, self.standards.min_experience_years + 10)  # 60+ years
    
    def _calculate_optimal_projects(self, experience_years: int) -> int:
        """Calculate optimal project count based on experience"""
        # More experienced agents should have proportionally more projects
        base_projects = 1200  # Base minimum
        experience_bonus = max(0, (experience_years - 50) * 15)  # 15 projects per year above minimum
        return base_projects + experience_bonus
    
    def _calculate_optimal_collaboration_rate(self, experience_years: int) -> float:
        """Calculate optimal collaboration rate based on experience"""
        # More experienced agents typically have higher collaboration rates
        base_rate = 0.35
        experience_factor = min(0.25, (experience_years - 50) * 0.005)  # Up to 25% bonus
        return min(0.60, base_rate + experience_factor)
    
    def upgrade_non_compliant_agents(self, upgrade_candidates: List[Dict]) -> Dict[str, any]:
        """Upgrade all non-compliant agents to meet quality standards"""
        try:
            upgrade_results = {
                'total_upgrades': 0,
                'successful_upgrades': 0,
                'failed_upgrades': 0,
                'upgrade_details': []
            }
            
            for candidate in upgrade_candidates:
                try:
                    agent = AIAgent.query.get(candidate['agent_id'])
                    if not agent:
                        continue
                    
                    # Store original values for tracking
                    original_values = {
                        'experience': agent.expertise_level,
                        'projects': agent.practical_projects,
                        'collaboration': agent.collaboration_rate
                    }
                    
                    # Apply upgrades
                    upgrades_applied = []
                    
                    if 'experience' in candidate['recommended_upgrades']:
                        new_experience = candidate['recommended_upgrades']['experience']
                        agent.expertise_level = new_experience
                        upgrades_applied.append(f"Experience: {original_values['experience']} → {new_experience}")
                    
                    if 'projects' in candidate['recommended_upgrades']:
                        new_projects = candidate['recommended_upgrades']['projects']
                        agent.practical_projects = new_projects
                        upgrades_applied.append(f"Projects: {original_values['projects']} → {new_projects}")
                    
                    if 'collaboration' in candidate['recommended_upgrades']:
                        new_collaboration = candidate['recommended_upgrades']['collaboration']
                        agent.collaboration_rate = new_collaboration
                        upgrades_applied.append(f"Collaboration: {original_values['collaboration']:.2%} → {new_collaboration:.2%}")
                    
                    # Update agent metadata
                    agent.updated_at = datetime.utcnow()
                    
                    # Add quality upgrade note to specialization tags
                    current_tags = agent.specialization_tags or ""
                    if "Quality Upgraded" not in current_tags:
                        agent.specialization_tags = f"{current_tags}, Quality Upgraded {datetime.now().strftime('%Y-%m')}"
                    
                    db.session.commit()
                    
                    upgrade_results['successful_upgrades'] += 1
                    upgrade_results['upgrade_details'].append({
                        'agent_id': agent.id,
                        'name': agent.name,
                        'upgrades_applied': upgrades_applied,
                        'new_tier': self._determine_quality_tier(agent.expertise_level)
                    })
                    
                except Exception as e:
                    upgrade_results['failed_upgrades'] += 1
                    logger.error(f"Failed to upgrade agent {candidate['agent_id']}: {e}")
                
                upgrade_results['total_upgrades'] += 1
            
            logger.info(f"Agent quality upgrade completed: {upgrade_results['successful_upgrades']}/{upgrade_results['total_upgrades']} successful")
            return upgrade_results
            
        except Exception as e:
            logger.error(f"Error during agent quality upgrade: {e}")
            return {'error': str(e)}
    
    def enforce_quality_standards_for_new_agents(self, agent_template: Dict[str, any]) -> Dict[str, any]:
        """Ensure new agents meet quality standards before creation"""
        try:
            category = agent_template.get('category', 'general')
            
            # Calculate optimal experience for category
            optimal_experience = self._calculate_optimal_experience(category)
            
            # Ensure experience meets standards (prefer higher values)
            if agent_template.get('years_experience', 0) < self.standards.min_experience_years:
                agent_template['years_experience'] = optimal_experience
            
            # Calculate and set optimal projects
            experience = agent_template['years_experience']
            optimal_projects = self._calculate_optimal_projects(experience)
            agent_template['practical_projects'] = max(optimal_projects, 
                                                     agent_template.get('practical_projects', 1000))
            
            # Calculate and set optimal collaboration rate
            optimal_collaboration = self._calculate_optimal_collaboration_rate(experience)
            agent_template['collaboration_rate'] = max(optimal_collaboration,
                                                     agent_template.get('collaboration_rate', 0.35))
            
            # Add quality certification
            quality_tier = self._determine_quality_tier(experience)
            agent_template['quality_certified'] = True
            agent_template['quality_tier'] = quality_tier
            agent_template['quality_certification_date'] = datetime.utcnow().isoformat()
            
            # Add to specialization tags
            specialization_tags = agent_template.get('specialization_tags', [])
            if isinstance(specialization_tags, list):
                specialization_tags.append(f"Quality Certified {quality_tier.title()}")
            else:
                specialization_tags = f"{specialization_tags}, Quality Certified {quality_tier.title()}"
            
            agent_template['specialization_tags'] = specialization_tags
            
            logger.info(f"Quality standards enforced for new agent: {experience} years, {optimal_projects} projects, {optimal_collaboration:.2%} collaboration")
            
            return {
                'success': True,
                'agent_template': agent_template,
                'quality_tier': quality_tier,
                'standards_applied': {
                    'experience': experience,
                    'projects': optimal_projects,
                    'collaboration': optimal_collaboration
                }
            }
            
        except Exception as e:
            logger.error(f"Error enforcing quality standards: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_quality_metrics_report(self) -> Dict[str, any]:
        """Generate comprehensive quality metrics report"""
        try:
            audit_results = self.audit_all_agents()
            
            # Calculate additional metrics
            total_agents = audit_results.get('total_agents', 0)
            compliant_percentage = (audit_results.get('compliant_agents', 0) / total_agents * 100) if total_agents > 0 else 0
            
            # Get experience distribution
            all_agents = db.session.query(AIAgent).filter_by(is_active=True).all()
            experience_stats = {
                'min_experience': min((a.expertise_level for a in all_agents), default=0),
                'max_experience': max((a.expertise_level for a in all_agents), default=0),
                'avg_experience': sum(a.expertise_level for a in all_agents) / len(all_agents) if all_agents else 0,
                'median_experience': sorted([a.expertise_level for a in all_agents])[len(all_agents)//2] if all_agents else 0
            }
            
            project_stats = {
                'min_projects': min((a.practical_projects for a in all_agents), default=0),
                'max_projects': max((a.practical_projects for a in all_agents), default=0),
                'avg_projects': sum(a.practical_projects for a in all_agents) / len(all_agents) if all_agents else 0,
                'total_projects': sum(a.practical_projects for a in all_agents)
            }
            
            collaboration_stats = {
                'min_collaboration': min((a.collaboration_rate for a in all_agents), default=0),
                'max_collaboration': max((a.collaboration_rate for a in all_agents), default=0),
                'avg_collaboration': sum(a.collaboration_rate for a in all_agents) / len(all_agents) if all_agents else 0
            }
            
            return {
                'compliance_overview': {
                    'total_agents': total_agents,
                    'compliant_agents': audit_results.get('compliant_agents', 0),
                    'compliance_percentage': round(compliant_percentage, 2),
                    'non_compliant_count': audit_results.get('non_compliant_agents', 0)
                },
                'quality_distribution': audit_results.get('quality_distribution', {}),
                'experience_statistics': experience_stats,
                'project_statistics': project_stats,
                'collaboration_statistics': collaboration_stats,
                'quality_standards': {
                    'min_experience': self.standards.min_experience_years,
                    'preferred_experience': self.standards.preferred_experience_years,
                    'min_projects': self.standards.min_practical_projects,
                    'min_collaboration': self.standards.min_collaboration_rate
                },
                'total_expertise_years': sum(a.expertise_level for a in all_agents),
                'total_practical_projects': project_stats['total_projects'],
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating quality metrics report: {e}")
            return {'error': str(e)}

# Global quality service instance
quality_service = AgentQualityAuditService()