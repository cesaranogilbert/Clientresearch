"""
Quality Assurance AI Agent Management Service
Dedicated AI agents for permanent monitoring and validation of agent generation processes
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from app import db
from models import AIAgent
from ai_agent_generation_service import AIAgentGenerationService, validate_agent_ecosystem


class QAAgentType(Enum):
    """Types of QA agents for different validation tasks"""
    VALIDATION_MASTER = "validation_master"
    CONSISTENCY_CHECKER = "consistency_checker"
    QUALITY_MONITOR = "quality_monitor"
    DUPLICATION_DETECTOR = "duplication_detector"
    PERFORMANCE_ANALYZER = "performance_analyzer"
    SYSTEM_COORDINATOR = "system_coordinator"


@dataclass
class QAValidationResult:
    """Result of QA agent validation"""
    agent_type: QAAgentType
    validation_passed: bool
    issues_found: List[str]
    recommendations: List[str]
    timestamp: datetime
    agent_count_validated: int


@dataclass
class QASystemStatus:
    """Overall QA system status"""
    total_agents: int
    validation_status: str
    last_validation: datetime
    issues_detected: int
    recommendations_count: int
    milestone_status: str


class QualityAssuranceAgent:
    """Base class for all QA agents"""
    
    def __init__(self, agent_type: QAAgentType):
        self.agent_type = agent_type
        self.logger = logging.getLogger(f"QA_{agent_type.value}")
        self.last_validation = None
        
    def validate(self) -> QAValidationResult:
        """Override in subclasses"""
        raise NotImplementedError
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of this QA agent"""
        return {
            'agent_type': self.agent_type.value,
            'last_validation': self.last_validation.isoformat() if self.last_validation else None,
            'status': 'active'
        }


class ValidationMasterAgent(QualityAssuranceAgent):
    """Master validation agent - oversees all validation processes"""
    
    def __init__(self):
        super().__init__(QAAgentType.VALIDATION_MASTER)
        self.generation_service = AIAgentGenerationService()
    
    def validate(self) -> QAValidationResult:
        """Comprehensive validation of agent ecosystem"""
        self.logger.info("🔍 Starting comprehensive ecosystem validation")
        
        issues = []
        recommendations = []
        
        try:
            # Get ecosystem status
            ecosystem_status = validate_agent_ecosystem()
            
            total_agents = ecosystem_status.get('total_agents', 0)
            
            # Check milestone progress
            if total_agents < 1000:
                missing = 1000 - total_agents
                issues.append(f"Missing {missing} agents to reach 1000+ milestone")
                recommendations.append(f"Generate {missing} additional agents to complete milestone")
            
            # Validate quality metrics
            quality_metrics = ecosystem_status.get('quality_metrics', {})
            
            avg_expertise = quality_metrics.get('average_expertise_years', 0)
            if avg_expertise < 50:
                issues.append(f"Average expertise ({avg_expertise} years) below minimum threshold (50 years)")
                recommendations.append("Increase expertise levels for new agents")
            
            avg_projects = quality_metrics.get('average_projects', 0)
            if avg_projects < 1000:
                issues.append(f"Average projects ({avg_projects}) below minimum threshold (1000)")
                recommendations.append("Increase project counts for new agents")
            
            avg_collaboration = quality_metrics.get('average_collaboration_rate', 0)
            if avg_collaboration < 0.80:
                issues.append(f"Average collaboration rate ({avg_collaboration}) below minimum (0.80)")
                recommendations.append("Improve collaboration rates for agents")
            
            # Check category distribution
            categories = ecosystem_status.get('category_distribution', {})
            if len(categories) < 5:
                issues.append("Insufficient category diversity")
                recommendations.append("Add agents across more categories")
            
            validation_passed = len(issues) == 0
            
            self.last_validation = datetime.now()
            
            self.logger.info(f"✅ Validation complete: {total_agents} agents, {len(issues)} issues found")
            
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=validation_passed,
                issues_found=issues,
                recommendations=recommendations,
                timestamp=self.last_validation,
                agent_count_validated=total_agents
            )
            
        except Exception as e:
            self.logger.error(f"❌ Validation failed: {e}")
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=False,
                issues_found=[f"Validation error: {e}"],
                recommendations=["Fix validation system errors"],
                timestamp=datetime.now(),
                agent_count_validated=0
            )


class ConsistencyCheckerAgent(QualityAssuranceAgent):
    """Checks for consistency in agent data and structure"""
    
    def __init__(self):
        super().__init__(QAAgentType.CONSISTENCY_CHECKER)
    
    def validate(self) -> QAValidationResult:
        """Check consistency across all agents"""
        self.logger.info("🔧 Checking agent consistency")
        
        issues = []
        recommendations = []
        
        try:
            # Get all active agents
            agents = AIAgent.query.filter_by(is_active=True).all()
            agent_count = len(agents)
            
            # Check for missing required fields
            for agent in agents:
                if not agent.name or len(agent.name.strip()) < 10:
                    issues.append(f"Agent {agent.id}: Invalid name")
                
                if not agent.description or len(agent.description.strip()) < 50:
                    issues.append(f"Agent {agent.id}: Invalid description")
                
                if not agent.base_prompt or len(agent.base_prompt.strip()) < 20:
                    issues.append(f"Agent {agent.id}: Invalid base prompt")
                
                if agent.expertise_level < 50:
                    issues.append(f"Agent {agent.id}: Expertise level too low ({agent.expertise_level})")
                
                if agent.practical_projects < 1000:
                    issues.append(f"Agent {agent.id}: Project count too low ({agent.practical_projects})")
            
            # Check for naming consistency
            name_patterns = {}
            for agent in agents:
                # Extract pattern (remove numbers and common suffixes)
                pattern = agent.name.replace(' AI', '').replace(' Expert', '').replace(' Master', '').replace(' Pro', '')
                pattern = ''.join([c for c in pattern if not c.isdigit()]).strip()
                
                if pattern in name_patterns:
                    name_patterns[pattern] += 1
                else:
                    name_patterns[pattern] = 1
            
            # Check for excessive duplication
            for pattern, count in name_patterns.items():
                if count > 5:
                    issues.append(f"Too many similar agents for pattern: {pattern} ({count} agents)")
                    recommendations.append(f"Diversify agents in {pattern} category")
            
            # Check pricing consistency
            pricing_issues = self._check_pricing_consistency(agents)
            issues.extend(pricing_issues)
            
            validation_passed = len(issues) == 0
            
            if validation_passed:
                recommendations.append("Agent consistency is excellent")
            else:
                recommendations.append("Review and fix consistency issues")
            
            self.last_validation = datetime.now()
            
            self.logger.info(f"✅ Consistency check complete: {len(issues)} issues found")
            
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=validation_passed,
                issues_found=issues,
                recommendations=recommendations,
                timestamp=self.last_validation,
                agent_count_validated=agent_count
            )
            
        except Exception as e:
            self.logger.error(f"❌ Consistency check failed: {e}")
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=False,
                issues_found=[f"Consistency check error: {e}"],
                recommendations=["Fix consistency checking system"],
                timestamp=datetime.now(),
                agent_count_validated=0
            )
    
    def _check_pricing_consistency(self, agents: List[AIAgent]) -> List[str]:
        """Check pricing consistency across agents"""
        issues = []
        
        try:
            # Group by pricing tier
            tier_prices = {}
            for agent in agents:
                tier = agent.pricing_tier
                if tier not in tier_prices:
                    tier_prices[tier] = []
                tier_prices[tier].append((agent.base_price, agent.monthly_price))
            
            # Check for reasonable price ranges within tiers
            for tier, prices in tier_prices.items():
                if len(prices) > 1:
                    base_prices = [p[0] for p in prices]
                    monthly_prices = [p[1] for p in prices]
                    
                    base_range = max(base_prices) - min(base_prices)
                    monthly_range = max(monthly_prices) - min(monthly_prices)
                    
                    # Check for excessive price variation within tier
                    if base_range > 500:
                        issues.append(f"Excessive base price variation in {tier} tier: ${base_range}")
                    
                    if monthly_range > 300:
                        issues.append(f"Excessive monthly price variation in {tier} tier: ${monthly_range}")
            
        except Exception as e:
            issues.append(f"Pricing consistency check error: {e}")
        
        return issues


class QualityMonitorAgent(QualityAssuranceAgent):
    """Monitors overall quality metrics and trends"""
    
    def __init__(self):
        super().__init__(QAAgentType.QUALITY_MONITOR)
    
    def validate(self) -> QAValidationResult:
        """Monitor quality metrics and trends"""
        self.logger.info("📊 Monitoring quality metrics")
        
        issues = []
        recommendations = []
        
        try:
            # Get ecosystem status
            ecosystem_status = validate_agent_ecosystem()
            quality_metrics = ecosystem_status.get('quality_metrics', {})
            
            agent_count = ecosystem_status.get('total_agents', 0)
            
            # Define quality thresholds
            thresholds = {
                'min_expertise': 65,
                'min_projects': 1200,
                'min_collaboration': 0.85,
                'excellence_expertise': 80,
                'excellence_projects': 1800,
                'excellence_collaboration': 0.90
            }
            
            # Check current metrics against thresholds
            avg_expertise = quality_metrics.get('average_expertise_years', 0)
            avg_projects = quality_metrics.get('average_projects', 0)
            avg_collaboration = quality_metrics.get('average_collaboration_rate', 0)
            
            # Quality assessments
            if avg_expertise < thresholds['min_expertise']:
                issues.append(f"Average expertise ({avg_expertise}) below recommended minimum ({thresholds['min_expertise']})")
                recommendations.append("Focus on creating higher-expertise agents")
            elif avg_expertise >= thresholds['excellence_expertise']:
                recommendations.append("Excellent expertise levels maintained")
            
            if avg_projects < thresholds['min_projects']:
                issues.append(f"Average projects ({avg_projects}) below recommended minimum ({thresholds['min_projects']})")
                recommendations.append("Increase project counts for new agents")
            elif avg_projects >= thresholds['excellence_projects']:
                recommendations.append("Excellent project experience levels")
            
            if avg_collaboration < thresholds['min_collaboration']:
                issues.append(f"Average collaboration ({avg_collaboration}) below recommended minimum ({thresholds['min_collaboration']})")
                recommendations.append("Improve collaboration ratings")
            elif avg_collaboration >= thresholds['excellence_collaboration']:
                recommendations.append("Excellent collaboration rates")
            
            # Overall quality assessment
            quality_score = (
                (avg_expertise / 100) * 0.4 +
                (min(avg_projects, 2000) / 2000) * 0.3 +
                avg_collaboration * 0.3
            )
            
            if quality_score >= 0.90:
                recommendations.append(f"Outstanding overall quality score: {quality_score:.2f}")
            elif quality_score >= 0.80:
                recommendations.append(f"Good overall quality score: {quality_score:.2f}")
            else:
                issues.append(f"Quality score needs improvement: {quality_score:.2f}")
                recommendations.append("Focus on improving all quality metrics")
            
            validation_passed = len(issues) == 0
            
            self.last_validation = datetime.now()
            
            self.logger.info(f"✅ Quality monitoring complete: Score {quality_score:.2f}")
            
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=validation_passed,
                issues_found=issues,
                recommendations=recommendations,
                timestamp=self.last_validation,
                agent_count_validated=agent_count
            )
            
        except Exception as e:
            self.logger.error(f"❌ Quality monitoring failed: {e}")
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=False,
                issues_found=[f"Quality monitoring error: {e}"],
                recommendations=["Fix quality monitoring system"],
                timestamp=datetime.now(),
                agent_count_validated=0
            )


class SystemCoordinatorAgent(QualityAssuranceAgent):
    """Coordinates all QA agents and manages the overall system"""
    
    def __init__(self):
        super().__init__(QAAgentType.SYSTEM_COORDINATOR)
        self.qa_agents = [
            ValidationMasterAgent(),
            ConsistencyCheckerAgent(),
            QualityMonitorAgent()
        ]
    
    def validate(self) -> QAValidationResult:
        """Coordinate validation across all QA agents"""
        self.logger.info("🎯 Coordinating comprehensive QA validation")
        
        all_issues = []
        all_recommendations = []
        total_validated = 0
        
        try:
            # Run all QA agents
            for qa_agent in self.qa_agents:
                result = qa_agent.validate()
                all_issues.extend(result.issues_found)
                all_recommendations.extend(result.recommendations)
                total_validated = max(total_validated, result.agent_count_validated)
            
            # System-level checks
            ecosystem_status = validate_agent_ecosystem()
            total_agents = ecosystem_status.get('total_agents', 0)
            
            # Check milestone completion
            if total_agents >= 1000:
                all_recommendations.append("🎯 MILESTONE ACHIEVED: 1000+ agents successfully created!")
            else:
                missing = 1000 - total_agents
                all_issues.append(f"Milestone incomplete: {missing} agents still needed")
                all_recommendations.append(f"Priority: Generate {missing} more agents to reach 1000+ milestone")
            
            # Generate system-wide recommendations
            if len(all_issues) == 0:
                all_recommendations.append("🚀 System operating at optimal quality levels")
                all_recommendations.append("Continue monitoring and maintaining current standards")
            else:
                all_recommendations.append("🔧 System requires attention to maintain quality standards")
                all_recommendations.append("Implement recommended fixes immediately")
            
            validation_passed = len(all_issues) == 0
            
            self.last_validation = datetime.now()
            
            self.logger.info(f"✅ System coordination complete: {len(all_issues)} total issues")
            
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=validation_passed,
                issues_found=all_issues,
                recommendations=all_recommendations,
                timestamp=self.last_validation,
                agent_count_validated=total_validated
            )
            
        except Exception as e:
            self.logger.error(f"❌ System coordination failed: {e}")
            return QAValidationResult(
                agent_type=self.agent_type,
                validation_passed=False,
                issues_found=[f"System coordination error: {e}"],
                recommendations=["Fix QA system coordination"],
                timestamp=datetime.now(),
                agent_count_validated=0
            )


class QAAgentManagementService:
    """Central service for managing all QA agents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.coordinator = SystemCoordinatorAgent()
        
    def run_comprehensive_qa(self) -> Dict[str, Any]:
        """Run comprehensive QA validation across all systems"""
        self.logger.info("🚀 Starting comprehensive QA validation")
        
        start_time = datetime.now()
        
        # Run system coordinator (which runs all other QA agents)
        result = self.coordinator.validate()
        
        duration = (datetime.now() - start_time).total_seconds()
        
        # Determine overall status
        if result.validation_passed:
            status = "EXCELLENT"
        elif len(result.issues_found) <= 3:
            status = "GOOD"
        elif len(result.issues_found) <= 10:
            status = "NEEDS_ATTENTION"
        else:
            status = "CRITICAL"
        
        return {
            'validation_status': status,
            'validation_passed': result.validation_passed,
            'total_agents_validated': result.agent_count_validated,
            'issues_found': result.issues_found,
            'recommendations': result.recommendations,
            'validation_timestamp': result.timestamp.isoformat(),
            'duration_seconds': duration,
            'next_validation_due': (datetime.now() + timedelta(hours=24)).isoformat()
        }
    
    def get_system_status(self) -> QASystemStatus:
        """Get current QA system status"""
        try:
            ecosystem_status = validate_agent_ecosystem()
            
            total_agents = ecosystem_status.get('total_agents', 0)
            milestone_status = "COMPLETED" if total_agents >= 1000 else f"IN_PROGRESS ({total_agents}/1000)"
            
            # Quick validation
            qa_result = self.coordinator.validate()
            
            return QASystemStatus(
                total_agents=total_agents,
                validation_status="PASSED" if qa_result.validation_passed else "FAILED",
                last_validation=qa_result.timestamp,
                issues_detected=len(qa_result.issues_found),
                recommendations_count=len(qa_result.recommendations),
                milestone_status=milestone_status
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return QASystemStatus(
                total_agents=0,
                validation_status="ERROR",
                last_validation=datetime.now(),
                issues_detected=1,
                recommendations_count=0,
                milestone_status="UNKNOWN"
            )
    
    def auto_fix_issues(self) -> Dict[str, Any]:
        """Automatically fix common issues when possible"""
        self.logger.info("🔧 Starting automatic issue resolution")
        
        # Run QA to identify issues
        qa_result = self.coordinator.validate()
        
        fixed_issues = []
        remaining_issues = []
        
        for issue in qa_result.issues_found:
            if "Missing" in issue and "agents" in issue:
                # Try to auto-generate missing agents
                try:
                    # Extract number of missing agents
                    import re
                    match = re.search(r'(\d+)', issue)
                    if match:
                        missing_count = int(match.group(1))
                        
                        # Generate agents to fill the gap
                        from ai_agent_generation_service import generate_agents_for_topic
                        
                        # Generate diverse agents
                        topics = ['digital_marketing', 'data_analytics', 'customer_success', 'product_management']
                        agents_per_topic = max(1, missing_count // len(topics))
                        
                        for topic in topics:
                            if missing_count <= 0:
                                break
                                
                            result = generate_agents_for_topic(
                                topic=topic,
                                category='business',
                                count=min(agents_per_topic, missing_count)
                            )
                            
                            if result['success']:
                                missing_count -= result['created_count']
                                fixed_issues.append(f"Auto-generated {result['created_count']} {topic} agents")
                        
                        if missing_count <= 0:
                            fixed_issues.append(f"Resolved: {issue}")
                        else:
                            remaining_issues.append(issue)
                    else:
                        remaining_issues.append(issue)
                        
                except Exception as e:
                    self.logger.error(f"Auto-fix failed for: {issue} - {e}")
                    remaining_issues.append(issue)
            else:
                remaining_issues.append(issue)
        
        return {
            'auto_fix_completed': True,
            'issues_fixed': len(fixed_issues),
            'issues_remaining': len(remaining_issues),
            'fixed_details': fixed_issues,
            'remaining_issues': remaining_issues,
            'recommendations': qa_result.recommendations
        }


# Convenience functions for easy access
def run_qa_validation() -> Dict[str, Any]:
    """Run comprehensive QA validation"""
    service = QAAgentManagementService()
    return service.run_comprehensive_qa()


def get_qa_status() -> QASystemStatus:
    """Get current QA system status"""
    service = QAAgentManagementService()
    return service.get_system_status()


def auto_fix_agent_issues() -> Dict[str, Any]:
    """Automatically fix agent issues when possible"""
    service = QAAgentManagementService()
    return service.auto_fix_issues()