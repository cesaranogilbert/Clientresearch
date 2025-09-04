"""
AI Agent Orchestration Service
Central service for managing and coordinating all specialized AI agents
"""

import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from enterprise_policy_enforcement import require_dlp_scan, require_permission
from dataclasses import asdict

# Import all agent modules
from ai_agents_core import orchestrator, AgentTask, AgentPriority, log_agent_performance, get_agent_analytics
from enterprise_agents import EnterpriseArchitectureAgent, CodeQualityAssuranceAgent
from developer_ecosystem_agents import SDKDevelopmentAgent, APIArchitectureAgent
from premium_service_agents import EnterpriseOnboardingAgent, CustomAITrainingAgent
from integration_automation_agents import EnterpriseConnectorAgent, WorkflowAutomationAgent
from analytics_intelligence_agents import PredictiveAnalyticsAgent, ExecutiveDashboardAgent
from partnership_revenue_agents import StrategicPartnershipAgent, MarketplaceOperationsAgent

logger = logging.getLogger(__name__)

# Create Flask Blueprint for agent orchestration
agent_orchestration_bp = Blueprint('agent_orchestration', __name__, url_prefix='/agents')

class AgentOrchestrationService:
    """Service class for managing AI agent orchestration and coordination"""
    
    def __init__(self):
        self.orchestrator = orchestrator
        self.task_history = []
        self.performance_metrics = {}
        
    async def execute_agent_task(self, agent_type: str, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the appropriate specialized agent"""
        try:
            # Create task from configuration
            task = AgentTask(
                id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.task_history)}",
                name=task_config.get("name", "Agent Task"),
                description=task_config.get("description", ""),
                priority=AgentPriority(task_config.get("priority", "medium")),
                requirements=task_config.get("requirements", {}),
                expected_output=task_config.get("expected_output", ""),
                estimated_duration=task_config.get("estimated_duration", 30)
            )
            
            # Assign task to appropriate agent
            agent_id = self.orchestrator.assign_task(task, preferred_agent_id=agent_type)
            
            # Execute task
            result = await self.orchestrator.execute_next_task()
            
            # Log performance
            if result and result.get("success"):
                log_agent_performance(
                    agent_id=agent_id,
                    agent_name=task_config.get("agent_name", "Unknown"),
                    task_id=task.id,
                    task_name=task.name,
                    priority=task.priority.value,
                    execution_time=task.estimated_duration,
                    success=result.get("success", False),
                    quality_score=result.get("quality_score", 0.8)
                )
            
            # Store in history
            self.task_history.append({
                "task": asdict(task),
                "result": result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
            return result or {"success": False, "error": "Task execution failed"}
            
        except Exception as e:
            logger.error(f"Agent orchestration error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_available_agents(self) -> Dict[str, Any]:
        """Get list of all available agents and their capabilities"""
        agents_info = {}
        
        for agent_id, agent in self.orchestrator.agents.items():
            agents_info[agent_id] = {
                "name": agent.name,
                "specialization": agent.specialization,
                "status": agent.status.value,
                "capabilities": [
                    {
                        "name": cap.name,
                        "description": cap.description,
                        "input_types": cap.input_types,
                        "output_types": cap.output_types,
                        "success_rate": cap.success_rate
                    }
                    for cap in agent.capabilities
                ],
                "performance_metrics": agent.get_performance_metrics()
            }
        
        return agents_info
    
    def get_system_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive system dashboard data"""
        system_status = self.orchestrator.get_system_status()
        
        dashboard_data = {
            "system_overview": {
                "total_agents": system_status["total_agents"],
                "active_agents": len([agent for agent in self.orchestrator.agents.values() 
                                    if agent.status.value in ["idle", "working"]]),
                "queued_tasks": system_status["queued_tasks"],
                "completed_tasks": system_status["completed_tasks"],
                "system_health": system_status["system_health"]
            },
            "agent_categories": {
                "enterprise_optimization": {
                    "agents": ["enterprise_architect_001", "code_qa_specialist_001"],
                    "description": "System architecture and code quality optimization",
                    "performance": self._get_category_performance(["enterprise_architect_001", "code_qa_specialist_001"])
                },
                "developer_ecosystem": {
                    "agents": ["sdk_developer_001", "api_architect_001"],
                    "description": "SDK development and API optimization",
                    "performance": self._get_category_performance(["sdk_developer_001", "api_architect_001"])
                },
                "premium_services": {
                    "agents": ["enterprise_onboarding_001", "custom_ai_trainer_001"],
                    "description": "Enterprise onboarding and custom AI solutions",
                    "performance": self._get_category_performance(["enterprise_onboarding_001", "custom_ai_trainer_001"])
                },
                "integration_automation": {
                    "agents": ["enterprise_connector_001", "workflow_automation_001"],
                    "description": "Enterprise integration and process automation",
                    "performance": self._get_category_performance(["enterprise_connector_001", "workflow_automation_001"])
                },
                "analytics_intelligence": {
                    "agents": ["predictive_analytics_001", "executive_dashboard_001"],
                    "description": "Predictive analytics and business intelligence",
                    "performance": self._get_category_performance(["predictive_analytics_001", "executive_dashboard_001"])
                },
                "partnership_revenue": {
                    "agents": ["strategic_partnership_001", "marketplace_operations_001"],
                    "description": "Partnership development and revenue optimization",
                    "performance": self._get_category_performance(["strategic_partnership_001", "marketplace_operations_001"])
                }
            },
            "recent_activities": self._get_recent_activities(),
            "performance_trends": self._get_performance_trends(),
            "recommendations": self._get_system_recommendations()
        }
        
        return dashboard_data
    
    def _get_category_performance(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Get performance metrics for a category of agents"""
        category_agents = [self.orchestrator.agents[agent_id] for agent_id in agent_ids 
                          if agent_id in self.orchestrator.agents]
        
        if not category_agents:
            return {"avg_success_rate": 0.0, "total_tasks": 0, "avg_performance": 0.0}
        
        metrics = [agent.get_performance_metrics() for agent in category_agents]
        
        return {
            "avg_success_rate": sum(m["success_rate"] for m in metrics) / len(metrics),
            "total_tasks": sum(m["tasks_completed"] for m in metrics),
            "avg_performance": sum(m["success_rate"] for m in metrics) / len(metrics),
            "agent_count": len(category_agents)
        }
    
    def _get_recent_activities(self) -> List[Dict[str, Any]]:
        """Get recent agent activities"""
        recent_tasks = self.task_history[-10:] if self.task_history else []
        
        activities = []
        for task_entry in reversed(recent_tasks):  # Most recent first
            activities.append({
                "timestamp": task_entry["timestamp"],
                "task_name": task_entry["task"]["name"],
                "agent_type": task_entry["task"]["requirements"].get("agent_type", "unknown"),
                "status": "completed" if task_entry["result"].get("success") else "failed",
                "duration": task_entry["task"]["estimated_duration"]
            })
        
        return activities
    
    def _get_performance_trends(self) -> Dict[str, Any]:
        """Get performance trend data"""
        # This would typically pull from database analytics
        # For now, return mock trend data
        return {
            "success_rate_trend": [0.85, 0.87, 0.89, 0.91, 0.88, 0.92, 0.94],
            "task_volume_trend": [45, 52, 48, 61, 58, 67, 72],
            "response_time_trend": [2.3, 2.1, 2.4, 2.0, 1.9, 2.2, 1.8],
            "trend_period": "last_7_days"
        }
    
    def _get_system_recommendations(self) -> List[Dict[str, Any]]:
        """Get system optimization recommendations"""
        recommendations = []
        
        system_health = self.orchestrator.get_system_status()["system_health"]
        
        if system_health < 0.8:
            recommendations.append({
                "type": "performance",
                "priority": "high",
                "title": "System Health Optimization",
                "description": f"System health is at {system_health:.1%}. Consider agent load balancing.",
                "action": "Review agent workload distribution and optimize task assignment"
            })
        
        queued_tasks = self.orchestrator.get_system_status()["queued_tasks"]
        if queued_tasks > 10:
            recommendations.append({
                "type": "capacity",
                "priority": "medium",
                "title": "Task Queue Management",
                "description": f"{queued_tasks} tasks in queue. Consider scaling agents.",
                "action": "Add more agent instances or optimize task processing"
            })
        
        # Check for underutilized agents
        idle_agents = [agent for agent in self.orchestrator.agents.values() 
                      if agent.status.value == "idle"]
        if len(idle_agents) > 3:
            recommendations.append({
                "type": "optimization",
                "priority": "low",
                "title": "Agent Utilization",
                "description": f"{len(idle_agents)} agents are idle. Consider task redistribution.",
                "action": "Analyze workload patterns and optimize agent allocation"
            })
        
        return recommendations

# Initialize service
orchestration_service = AgentOrchestrationService()

# Flask Routes
@agent_orchestration_bp.route('/dashboard')
def agent_dashboard():
    """Agent orchestration dashboard"""
    try:
        dashboard_data = orchestration_service.get_system_dashboard_data()
        return render_template('agent_orchestration/dashboard.html', data=dashboard_data)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@agent_orchestration_bp.route('/api/agents')
def get_agents():
    """Get list of available agents"""
    try:
        agents = orchestration_service.get_available_agents()
        return jsonify({"success": True, "agents": agents})
    except Exception as e:
        logger.error(f"Get agents error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@agent_orchestration_bp.route('/api/execute', methods=['POST'])
async def execute_agent_task():
    """Execute an agent task"""
    try:
        task_config = request.get_json()
        if not task_config:
            return jsonify({"success": False, "error": "No task configuration provided"}), 400
        
        agent_type = task_config.get("agent_type")
        if not agent_type:
            return jsonify({"success": False, "error": "Agent type is required"}), 400
        
        result = await orchestration_service.execute_agent_task(agent_type, task_config)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Task execution error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@agent_orchestration_bp.route('/api/status')
def get_system_status():
    """Get system status"""
    try:
        status = orchestrator.get_system_status()
        return jsonify({"success": True, "status": status})
    except Exception as e:
        logger.error(f"Status error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@agent_orchestration_bp.route('/api/analytics')
def get_analytics():
    """Get agent performance analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        agent_id = request.args.get('agent_id')
        
        analytics = get_agent_analytics(agent_id=agent_id, days=days)
        return jsonify({"success": True, "analytics": analytics})
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500