"""
Automated Agent Consistency System
Permanent automated system for ensuring agent generation consistency and quality
"""

import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from threading import Thread
import threading

from app import app, db
from models import AIAgent
from ai_agent_generation_service import generate_agents_for_topic, validate_agent_ecosystem
from qa_agent_management_service import run_qa_validation, auto_fix_agent_issues


class AutomatedConsistencyChecker:
    """Automated system for continuous agent consistency checking"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.last_check = None
        self.check_thread = None
        self.monitoring_active = False
        
    def start_monitoring(self):
        """Start automated monitoring and consistency checking"""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        self.logger.info("🚀 Starting automated consistency monitoring")
        self.monitoring_active = True
        
        # Schedule regular checks
        schedule.every(6).hours.do(self._run_comprehensive_check)
        schedule.every(24).hours.do(self._run_milestone_check)
        schedule.every(12).hours.do(self._run_auto_fix)
        schedule.every(1).hours.do(self._run_quick_validation)
        
        # Start scheduler thread
        self.check_thread = Thread(target=self._scheduler_loop, daemon=True)
        self.check_thread.start()
        
        # Run initial check
        self._run_comprehensive_check()
        
        self.logger.info("✅ Automated consistency monitoring started")
    
    def stop_monitoring(self):
        """Stop automated monitoring"""
        self.monitoring_active = False
        schedule.clear()
        self.logger.info("⏹️ Automated consistency monitoring stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.monitoring_active:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
    
    def _run_comprehensive_check(self):
        """Run comprehensive consistency and quality check"""
        self.logger.info("🔍 Running comprehensive consistency check")
        
        try:
            with app.app_context():
                # Run QA validation
                qa_result = run_qa_validation()
                
                # Log results
                self.logger.info(f"QA Status: {qa_result['validation_status']}")
                self.logger.info(f"Issues Found: {len(qa_result['issues_found'])}")
                self.logger.info(f"Agents Validated: {qa_result['total_agents_validated']}")
                
                # Store check result
                self.last_check = {
                    'timestamp': datetime.now(),
                    'type': 'comprehensive',
                    'status': qa_result['validation_status'],
                    'issues_count': len(qa_result['issues_found']),
                    'agent_count': qa_result['total_agents_validated']
                }
                
                # Generate alerts if needed
                if qa_result['validation_status'] in ['CRITICAL', 'NEEDS_ATTENTION']:
                    self._generate_alert(qa_result)
                
        except Exception as e:
            self.logger.error(f"Comprehensive check failed: {e}")
    
    def _run_milestone_check(self):
        """Check milestone progress and auto-complete if needed"""
        self.logger.info("🎯 Running milestone progress check")
        
        try:
            with app.app_context():
                total_agents = AIAgent.query.filter_by(is_active=True).count()
                
                if total_agents < 1000:
                    missing = 1000 - total_agents
                    self.logger.warning(f"Milestone incomplete: {missing} agents missing")
                    
                    # Auto-generate missing agents if reasonable amount
                    if missing <= 50:
                        self._auto_complete_milestone(missing)
                else:
                    self.logger.info(f"✅ Milestone achieved: {total_agents} agents")
                
        except Exception as e:
            self.logger.error(f"Milestone check failed: {e}")
    
    def _run_auto_fix(self):
        """Run automatic issue fixing"""
        self.logger.info("🔧 Running automatic issue resolution")
        
        try:
            with app.app_context():
                fix_result = auto_fix_agent_issues()
                
                if fix_result['issues_fixed'] > 0:
                    self.logger.info(f"✅ Auto-fixed {fix_result['issues_fixed']} issues")
                
                if fix_result['issues_remaining'] > 0:
                    self.logger.warning(f"⚠️ {fix_result['issues_remaining']} issues remain")
                
        except Exception as e:
            self.logger.error(f"Auto-fix failed: {e}")
    
    def _run_quick_validation(self):
        """Run quick validation check"""
        try:
            with app.app_context():
                ecosystem_status = validate_agent_ecosystem()
                total_agents = ecosystem_status.get('total_agents', 0)
                
                if total_agents < 1000:
                    self.logger.warning(f"Quick check: {total_agents}/1000 agents")
                else:
                    self.logger.info(f"Quick check: {total_agents} agents - milestone maintained")
                
        except Exception as e:
            self.logger.error(f"Quick validation failed: {e}")
    
    def _auto_complete_milestone(self, missing_count: int):
        """Automatically complete milestone by generating missing agents"""
        self.logger.info(f"Auto-completing milestone: generating {missing_count} agents")
        
        try:
            # Generate diverse agents to complete milestone
            topics = [
                ('business_intelligence', 'analytics', min(missing_count, 20)),
                ('customer_analytics', 'business', min(missing_count, 15)),
                ('performance_optimization', 'technology', min(missing_count, 15)),
                ('strategic_consulting', 'business', min(missing_count, 10))
            ]
            
            total_created = 0
            for topic, category, count in topics:
                if total_created >= missing_count:
                    break
                
                result = generate_agents_for_topic(
                    topic=topic,
                    category=category,
                    count=count,
                    pricing_tier='professional'
                )
                
                if result['success']:
                    total_created += result['created_count']
                    self.logger.info(f"Generated {result['created_count']} {topic} agents")
            
            # Verify completion
            final_count = AIAgent.query.filter_by(is_active=True).count()
            if final_count >= 1000:
                self.logger.info(f"🎯 Milestone auto-completed: {final_count} agents")
            else:
                self.logger.warning(f"Auto-completion partial: {final_count}/1000 agents")
            
        except Exception as e:
            self.logger.error(f"Auto-completion failed: {e}")
    
    def _generate_alert(self, qa_result: Dict):
        """Generate alert for critical issues"""
        alert_message = f"QA Alert: {qa_result['validation_status']} - {len(qa_result['issues_found'])} issues detected"
        self.logger.warning(alert_message)
        
        # Could extend to send notifications, emails, etc.
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            'monitoring_active': self.monitoring_active,
            'last_check': self.last_check,
            'scheduler_running': self.check_thread and self.check_thread.is_alive() if self.check_thread else False
        }


class AgentGenerationTrigger:
    """Automated trigger for agent generation based on conditions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.generation_rules = self._initialize_generation_rules()
    
    def _initialize_generation_rules(self) -> List[Dict]:
        """Initialize rules for automatic agent generation"""
        return [
            {
                'name': 'milestone_completion',
                'condition': lambda: self._check_milestone_incomplete(),
                'action': self._complete_milestone,
                'priority': 'high',
                'max_agents': 100
            },
            {
                'name': 'category_balance',
                'condition': lambda: self._check_category_imbalance(),
                'action': self._balance_categories,
                'priority': 'medium',
                'max_agents': 50
            },
            {
                'name': 'quality_enhancement',
                'condition': lambda: self._check_low_quality_count(),
                'action': self._enhance_quality,
                'priority': 'low',
                'max_agents': 25
            }
        ]
    
    def evaluate_and_trigger(self) -> Dict:
        """Evaluate rules and trigger generation if needed"""
        results = []
        
        try:
            with app.app_context():
                for rule in self.generation_rules:
                    if rule['condition']():
                        self.logger.info(f"Triggering rule: {rule['name']}")
                        result = rule['action'](rule['max_agents'])
                        results.append({
                            'rule': rule['name'],
                            'triggered': True,
                            'result': result
                        })
                    else:
                        results.append({
                            'rule': rule['name'],
                            'triggered': False,
                            'result': None
                        })
        
        except Exception as e:
            self.logger.error(f"Rule evaluation failed: {e}")
            results.append({'error': str(e)})
        
        return {'evaluations': results}
    
    def _check_milestone_incomplete(self) -> bool:
        """Check if milestone is incomplete"""
        total_agents = AIAgent.query.filter_by(is_active=True).count()
        return total_agents < 1000
    
    def _check_category_imbalance(self) -> bool:
        """Check if categories are imbalanced"""
        categories = db.session.query(AIAgent.category, db.func.count(AIAgent.id))\
            .filter_by(is_active=True)\
            .group_by(AIAgent.category)\
            .all()
        
        if len(categories) < 5:
            return True
        
        counts = [count for _, count in categories]
        if max(counts) / min(counts) > 3:  # If largest category is 3x bigger than smallest
            return True
        
        return False
    
    def _check_low_quality_count(self) -> bool:
        """Check if there are too few high-quality agents"""
        high_quality_count = AIAgent.query.filter(
            AIAgent.is_active == True,
            AIAgent.expertise_level >= 80,
            AIAgent.practical_projects >= 1500
        ).count()
        
        total_agents = AIAgent.query.filter_by(is_active=True).count()
        
        if total_agents > 0:
            quality_ratio = high_quality_count / total_agents
            return quality_ratio < 0.3  # Less than 30% high quality
        
        return True
    
    def _complete_milestone(self, max_agents: int) -> Dict:
        """Complete milestone by generating missing agents"""
        total_agents = AIAgent.query.filter_by(is_active=True).count()
        missing = min(1000 - total_agents, max_agents)
        
        if missing <= 0:
            return {'action': 'milestone_already_complete', 'agents_created': 0}
        
        # Generate diverse agents
        result = generate_agents_for_topic(
            topic='strategic_excellence',
            category='business',
            count=missing,
            pricing_tier='professional'
        )
        
        return {
            'action': 'milestone_completion',
            'agents_created': result.get('created_count', 0),
            'success': result.get('success', False)
        }
    
    def _balance_categories(self, max_agents: int) -> Dict:
        """Balance categories by adding to underrepresented ones"""
        categories = db.session.query(AIAgent.category, db.func.count(AIAgent.id))\
            .filter_by(is_active=True)\
            .group_by(AIAgent.category)\
            .all()
        
        if not categories:
            return {'action': 'no_categories_found', 'agents_created': 0}
        
        # Find smallest category
        min_category, min_count = min(categories, key=lambda x: x[1])
        
        # Generate agents for smallest category
        result = generate_agents_for_topic(
            topic=f'{min_category}_expansion',
            category=min_category,
            count=min(max_agents, 20),
            pricing_tier='professional'
        )
        
        return {
            'action': 'category_balance',
            'target_category': min_category,
            'agents_created': result.get('created_count', 0),
            'success': result.get('success', False)
        }
    
    def _enhance_quality(self, max_agents: int) -> Dict:
        """Enhance quality by generating high-expertise agents"""
        result = generate_agents_for_topic(
            topic='excellence_enhancement',
            category='premium',
            count=min(max_agents, 15),
            pricing_tier='elite',
            expertise_level_range=(85, 100),
            base_price_range=(899.0, 1299.0)
        )
        
        return {
            'action': 'quality_enhancement',
            'agents_created': result.get('created_count', 0),
            'success': result.get('success', False)
        }


class PermanentAgentManagementSystem:
    """Comprehensive permanent system for agent management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.consistency_checker = AutomatedConsistencyChecker()
        self.generation_trigger = AgentGenerationTrigger()
        self.system_active = False
    
    def start_system(self):
        """Start the complete automated system"""
        self.logger.info("🚀 Starting Permanent Agent Management System")
        
        # Start consistency monitoring
        self.consistency_checker.start_monitoring()
        
        # Schedule trigger evaluations
        schedule.every(3).hours.do(self._evaluate_triggers)
        
        self.system_active = True
        self.logger.info("✅ Permanent Agent Management System active")
    
    def stop_system(self):
        """Stop the automated system"""
        self.logger.info("⏹️ Stopping Permanent Agent Management System")
        
        self.consistency_checker.stop_monitoring()
        self.system_active = False
        
        self.logger.info("✅ Permanent Agent Management System stopped")
    
    def _evaluate_triggers(self):
        """Evaluate generation triggers"""
        self.logger.info("🔄 Evaluating generation triggers")
        
        try:
            with app.app_context():
                result = self.generation_trigger.evaluate_and_trigger()
                
                triggered_count = sum(1 for eval in result['evaluations'] if eval.get('triggered'))
                self.logger.info(f"Trigger evaluation complete: {triggered_count} rules triggered")
                
        except Exception as e:
            self.logger.error(f"Trigger evaluation failed: {e}")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        try:
            with app.app_context():
                ecosystem_status = validate_agent_ecosystem()
                consistency_status = self.consistency_checker.get_system_status()
                
                return {
                    'system_active': self.system_active,
                    'total_agents': ecosystem_status.get('total_agents', 0),
                    'milestone_status': ecosystem_status.get('milestone_status', 'UNKNOWN'),
                    'consistency_monitoring': consistency_status,
                    'last_update': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'system_active': self.system_active,
                'error': str(e),
                'last_update': datetime.now().isoformat()
            }
    
    def manual_trigger_generation(self, topic: str, category: str, count: int) -> Dict:
        """Manually trigger agent generation"""
        self.logger.info(f"Manual trigger: {count} {topic} agents")
        
        try:
            with app.app_context():
                result = generate_agents_for_topic(
                    topic=topic,
                    category=category,
                    count=count,
                    pricing_tier='professional'
                )
                
                return {
                    'manual_trigger': True,
                    'topic': topic,
                    'category': category,
                    'requested_count': count,
                    'result': result
                }
                
        except Exception as e:
            return {
                'manual_trigger': False,
                'error': str(e)
            }


# Global system instance
_permanent_system = None

def start_permanent_system():
    """Start the permanent agent management system"""
    global _permanent_system
    if _permanent_system is None:
        _permanent_system = PermanentAgentManagementSystem()
    
    _permanent_system.start_system()
    return _permanent_system

def stop_permanent_system():
    """Stop the permanent agent management system"""
    global _permanent_system
    if _permanent_system:
        _permanent_system.stop_system()

def get_permanent_system_status() -> Dict:
    """Get status of permanent system"""
    global _permanent_system
    if _permanent_system:
        return _permanent_system.get_system_status()
    else:
        return {'system_active': False, 'error': 'System not initialized'}

def manual_generate_agents(topic: str, category: str, count: int) -> Dict:
    """Manually trigger agent generation through permanent system"""
    global _permanent_system
    if _permanent_system:
        return _permanent_system.manual_trigger_generation(topic, category, count)
    else:
        return {'error': 'System not initialized'}