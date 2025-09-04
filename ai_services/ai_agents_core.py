"""
4UAI Specialized AI Agent Core System
Enterprise-grade AI agent architecture for platform optimization and business acceleration
"""

import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# AI API integrations
try:
    import openai
    from anthropic import Anthropic
    HAS_AI_APIS = True
except ImportError:
    HAS_AI_APIS = False

from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent execution status enum
class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"

# Agent priority levels
class AgentPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class AgentTask:
    """Individual task for AI agents"""
    id: str
    name: str
    description: str
    priority: AgentPriority
    requirements: Dict[str, Any]
    expected_output: str
    estimated_duration: int  # minutes
    dependencies: List[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class AgentCapability:
    """Agent capability definition"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    performance_metrics: Dict[str, float]
    success_rate: float

class BaseAIAgent:
    """Base class for all specialized AI agents"""
    
    def __init__(self, agent_id: str, name: str, specialization: str, capabilities: List[AgentCapability]):
        self.agent_id = agent_id
        self.name = name
        self.specialization = specialization
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.performance_history = []
        self.created_at = datetime.now(timezone.utc)
        
        # Initialize AI clients if available
        if HAS_AI_APIS:
            self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            self.anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task using the agent's specialized capabilities"""
        try:
            self.status = AgentStatus.WORKING
            self.current_task = task
            
            logger.info(f"Agent {self.name} starting task: {task.name}")
            
            # Check dependencies
            if task.dependencies:
                dependency_check = await self._check_dependencies(task.dependencies)
                if not dependency_check["success"]:
                    return {
                        "success": False,
                        "error": f"Dependencies not met: {dependency_check['missing']}"
                    }
            
            # Execute the specialized task logic
            result = await self._execute_specialized_task(task)
            
            # Log performance metrics
            self._log_performance(task, result)
            
            self.status = AgentStatus.COMPLETED
            self.current_task = None
            
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"Agent {self.name} error in task {task.name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.id
            }
    
    async def _execute_specialized_task(self, task: AgentTask) -> Dict[str, Any]:
        """Override this method in specialized agent classes"""
        raise NotImplementedError("Specialized agents must implement _execute_specialized_task")
    
    async def _check_dependencies(self, dependencies: List[str]) -> Dict[str, Any]:
        """Check if task dependencies are satisfied"""
        # This would integrate with the platform's dependency management system
        return {"success": True, "missing": []}
    
    def _log_performance(self, task: AgentTask, result: Dict[str, Any]):
        """Log agent performance metrics"""
        performance_entry = {
            "task_id": task.id,
            "task_name": task.name,
            "duration": (datetime.now(timezone.utc) - self.created_at).total_seconds(),
            "success": result.get("success", False),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.performance_history.append(performance_entry)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance statistics"""
        if not self.performance_history:
            return {"tasks_completed": 0, "success_rate": 0.0, "avg_duration": 0.0}
        
        successful_tasks = len([p for p in self.performance_history if p["success"]])
        total_tasks = len(self.performance_history)
        avg_duration = sum(p["duration"] for p in self.performance_history) / total_tasks
        
        return {
            "tasks_completed": total_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0.0,
            "avg_duration": avg_duration,
            "specialization": self.specialization,
            "status": self.status.value
        }

class AgentOrchestrator:
    """Manages and coordinates multiple AI agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAIAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[Dict[str, Any]] = []
        
    def register_agent(self, agent: BaseAIAgent):
        """Register a new agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.name} ({agent.specialization})")
    
    def assign_task(self, task: AgentTask, preferred_agent_id: Optional[str] = None) -> str:
        """Assign a task to the most suitable agent"""
        if preferred_agent_id and preferred_agent_id in self.agents:
            target_agent = self.agents[preferred_agent_id]
        else:
            target_agent = self._find_best_agent_for_task(task)
        
        if not target_agent:
            raise ValueError(f"No suitable agent found for task: {task.name}")
        
        self.task_queue.append(task)
        return target_agent.agent_id
    
    def _find_best_agent_for_task(self, task: AgentTask) -> Optional[BaseAIAgent]:
        """Find the best agent for a given task based on capabilities and performance"""
        available_agents = [agent for agent in self.agents.values() 
                          if agent.status in [AgentStatus.IDLE, AgentStatus.COMPLETED]]
        
        if not available_agents:
            return None
        
        # Score agents based on capability match and performance
        best_agent = None
        best_score = 0
        
        for agent in available_agents:
            score = self._calculate_agent_score(agent, task)
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
    
    def _calculate_agent_score(self, agent: BaseAIAgent, task: AgentTask) -> float:
        """Calculate how well an agent matches a task"""
        # This would be enhanced with machine learning for optimal agent selection
        base_score = 1.0
        
        # Factor in agent performance history
        metrics = agent.get_performance_metrics()
        performance_bonus = metrics["success_rate"] * 0.3
        
        # Factor in agent availability
        availability_bonus = 0.5 if agent.status == AgentStatus.IDLE else 0.1
        
        return base_score + performance_bonus + availability_bonus
    
    async def execute_next_task(self) -> Optional[Dict[str, Any]]:
        """Execute the next task in the queue"""
        if not self.task_queue:
            return None
        
        task = self.task_queue.pop(0)
        agent = self._find_best_agent_for_task(task)
        
        if not agent:
            # Re-queue the task
            self.task_queue.insert(0, task)
            return None
        
        result = await agent.execute_task(task)
        self.completed_tasks.append({
            "task": asdict(task),
            "agent_id": agent.agent_id,
            "result": result,
            "completed_at": datetime.now(timezone.utc).isoformat()
        })
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status and metrics"""
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            agent_statuses[agent_id] = agent.get_performance_metrics()
        
        return {
            "total_agents": len(self.agents),
            "queued_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "agent_performance": agent_statuses,
            "system_health": self._calculate_system_health()
        }
    
    def _calculate_system_health(self) -> float:
        """Calculate overall system health score"""
        if not self.agents:
            return 0.0
        
        total_success_rate = sum(agent.get_performance_metrics()["success_rate"] 
                               for agent in self.agents.values())
        avg_success_rate = total_success_rate / len(self.agents)
        
        # Factor in queue health
        queue_health = 1.0 if len(self.task_queue) < 10 else 0.5
        
        return (avg_success_rate * 0.7) + (queue_health * 0.3)

# Global agent orchestrator instance
orchestrator = AgentOrchestrator()

# Database model for agent performance tracking
class AgentPerformanceLog(db.Model):
    __tablename__ = 'agent_performance_logs'
    
    id = Column(Integer, primary_key=True)
    agent_id = Column(String(100), nullable=False)
    agent_name = Column(String(200), nullable=False)
    task_id = Column(String(100), nullable=False)
    task_name = Column(String(200), nullable=False)
    task_priority = Column(String(50), nullable=False)
    execution_time = Column(Float, nullable=False)
    success = Column(Boolean, nullable=False)
    output_quality_score = Column(Float, default=0.0)
    resource_usage = Column(JSON)
    error_details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_priority': self.task_priority,
            'execution_time': self.execution_time,
            'success': self.success,
            'output_quality_score': self.output_quality_score,
            'resource_usage': self.resource_usage,
            'error_details': self.error_details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def log_agent_performance(agent_id: str, agent_name: str, task_id: str, 
                         task_name: str, priority: str, execution_time: float,
                         success: bool, quality_score: float = 0.0,
                         resource_usage: Dict = None, error_details: str = None):
    """Log agent performance to database"""
    try:
        log_entry = AgentPerformanceLog(
            agent_id=agent_id,
            agent_name=agent_name,
            task_id=task_id,
            task_name=task_name,
            task_priority=priority,
            execution_time=execution_time,
            success=success,
            output_quality_score=quality_score,
            resource_usage=resource_usage or {},
            error_details=error_details
        )
        
        db.session.add(log_entry)
        db.session.commit()
        return True
        
    except Exception as e:
        logger.error(f"Failed to log agent performance: {str(e)}")
        return False

def get_agent_analytics(agent_id: Optional[str] = None, 
                       days: int = 30) -> Dict[str, Any]:
    """Get agent performance analytics"""
    try:
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = AgentPerformanceLog.query.filter(
            AgentPerformanceLog.created_at >= cutoff_date
        )
        
        if agent_id:
            query = query.filter(AgentPerformanceLog.agent_id == agent_id)
        
        logs = query.all()
        
        if not logs:
            return {"total_tasks": 0, "success_rate": 0.0, "avg_execution_time": 0.0}
        
        total_tasks = len(logs)
        successful_tasks = len([log for log in logs if log.success])
        avg_execution_time = sum(log.execution_time for log in logs) / total_tasks
        avg_quality_score = sum(log.output_quality_score for log in logs) / total_tasks
        
        return {
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": successful_tasks / total_tasks,
            "avg_execution_time": avg_execution_time,
            "avg_quality_score": avg_quality_score,
            "period_days": days
        }
        
    except Exception as e:
        logger.error(f"Failed to get agent analytics: {str(e)}")
        return {"error": str(e)}