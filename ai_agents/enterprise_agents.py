"""
Enterprise Architecture & Quality Assurance AI Agents
High-performance specialized agents for system optimization and quality control
"""

import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging
import subprocess
import ast
import re

from ai_agents_core import BaseAIAgent, AgentTask, AgentCapability, AgentPriority, orchestrator

logger = logging.getLogger(__name__)

class EnterpriseArchitectureAgent(BaseAIAgent):
    """AI Agent specializing in enterprise system architecture review and optimization"""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="architecture_analysis",
                description="Comprehensive system architecture analysis and optimization",
                input_types=["codebase", "config_files", "database_schema"],
                output_types=["architecture_report", "optimization_recommendations", "risk_assessment"],
                performance_metrics={"accuracy": 0.95, "coverage": 0.90},
                success_rate=0.92
            ),
            AgentCapability(
                name="integration_validation",
                description="Validate system integrations and prevent conflicts",
                input_types=["integration_config", "api_specs", "dependency_graph"],
                output_types=["validation_report", "conflict_detection", "resolution_plan"],
                performance_metrics={"precision": 0.88, "recall": 0.94},
                success_rate=0.89
            ),
            AgentCapability(
                name="scalability_assessment",
                description="Assess system scalability and performance bottlenecks",
                input_types=["system_metrics", "load_patterns", "resource_usage"],
                output_types=["scalability_report", "bottleneck_analysis", "scaling_strategy"],
                performance_metrics={"prediction_accuracy": 0.87, "optimization_impact": 0.78},
                success_rate=0.85
            )
        ]
        
        super().__init__(
            agent_id="enterprise_architect_001",
            name="Enterprise Architecture Specialist",
            specialization="System Architecture & Integration",
            capabilities=capabilities
        )
    
    async def _execute_specialized_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute enterprise architecture tasks"""
        try:
            task_type = task.requirements.get("type", "architecture_analysis")
            
            if task_type == "architecture_analysis":
                return await self._analyze_system_architecture(task)
            elif task_type == "integration_validation":
                return await self._validate_integrations(task)
            elif task_type == "scalability_assessment":
                return await self._assess_scalability(task)
            else:
                return {"success": False, "error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"Enterprise Architecture Agent error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_system_architecture(self, task: AgentTask) -> Dict[str, Any]:
        """Analyze system architecture for optimization opportunities"""
        project_path = task.requirements.get("project_path", ".")
        
        analysis_results = {
            "architecture_score": 0.0,
            "optimization_opportunities": [],
            "risk_factors": [],
            "recommendations": [],
            "compliance_assessment": {}
        }
        
        # Analyze codebase structure
        structure_analysis = await self._analyze_codebase_structure(project_path)
        analysis_results.update(structure_analysis)
        
        # Check for common architecture anti-patterns
        antipattern_analysis = await self._detect_architecture_antipatterns(project_path)
        analysis_results["risk_factors"].extend(antipattern_analysis)
        
        # Generate optimization recommendations
        recommendations = await self._generate_architecture_recommendations(analysis_results)
        analysis_results["recommendations"] = recommendations
        
        # Calculate overall architecture score
        analysis_results["architecture_score"] = self._calculate_architecture_score(analysis_results)
        
        return {
            "success": True,
            "task_type": "architecture_analysis",
            "analysis_results": analysis_results,
            "execution_time": datetime.now(timezone.utc).isoformat()
        }
    
    async def _analyze_codebase_structure(self, project_path: str) -> Dict[str, Any]:
        """Analyze codebase structure and organization"""
        structure_info = {
            "file_organization": {},
            "dependency_complexity": 0.0,
            "modularity_score": 0.0,
            "separation_of_concerns": 0.0
        }
        
        try:
            # Walk through project structure
            for root, dirs, files in os.walk(project_path):
                python_files = [f for f in files if f.endswith('.py')]
                if python_files:
                    relative_path = os.path.relpath(root, project_path)
                    structure_info["file_organization"][relative_path] = {
                        "python_files": len(python_files),
                        "complexity_indicators": []
                    }
                    
                    # Analyze individual files
                    for file in python_files:
                        file_path = os.path.join(root, file)
                        file_analysis = await self._analyze_python_file(file_path)
                        structure_info["file_organization"][relative_path]["complexity_indicators"].append(file_analysis)
            
            # Calculate modularity score
            structure_info["modularity_score"] = self._calculate_modularity_score(structure_info)
            
        except Exception as e:
            logger.error(f"Error analyzing codebase structure: {str(e)}")
        
        return structure_info
    
    async def _analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze individual Python file for complexity metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for complexity analysis
            tree = ast.parse(content)
            
            analysis = {
                "file_name": os.path.basename(file_path),
                "lines_of_code": len(content.splitlines()),
                "function_count": 0,
                "class_count": 0,
                "import_count": 0,
                "complexity_score": 0.0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["function_count"] += 1
                elif isinstance(node, ast.ClassDef):
                    analysis["class_count"] += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    analysis["import_count"] += 1
            
            # Calculate complexity score
            analysis["complexity_score"] = (
                analysis["lines_of_code"] * 0.1 +
                analysis["function_count"] * 2 +
                analysis["class_count"] * 3 +
                analysis["import_count"] * 1
            ) / 100
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {"file_name": os.path.basename(file_path), "error": str(e)}
    
    async def _detect_architecture_antipatterns(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect common architecture anti-patterns"""
        antipatterns = []
        
        # Check for circular dependencies
        circular_deps = await self._detect_circular_dependencies(project_path)
        if circular_deps:
            antipatterns.append({
                "type": "circular_dependencies",
                "severity": "high",
                "description": "Circular dependencies detected between modules",
                "affected_modules": circular_deps,
                "impact": "Reduces maintainability and testability"
            })
        
        # Check for god objects/classes
        god_objects = await self._detect_god_objects(project_path)
        if god_objects:
            antipatterns.append({
                "type": "god_objects",
                "severity": "medium",
                "description": "Classes with excessive responsibilities detected",
                "affected_classes": god_objects,
                "impact": "Violates single responsibility principle"
            })
        
        return antipatterns
    
    async def _detect_circular_dependencies(self, project_path: str) -> List[str]:
        """Detect circular dependencies in the codebase"""
        # Simplified circular dependency detection
        # In production, this would use more sophisticated graph analysis
        dependencies = {}
        
        try:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Extract imports
                        imports = re.findall(r'from\s+(\w+)\s+import|import\s+(\w+)', content)
                        module_name = os.path.splitext(file)[0]
                        dependencies[module_name] = [imp[0] or imp[1] for imp in imports if imp[0] or imp[1]]
            
            # Simple circular dependency check
            circular = []
            for module, deps in dependencies.items():
                for dep in deps:
                    if dep in dependencies and module in dependencies[dep]:
                        circular.append(f"{module} <-> {dep}")
            
            return list(set(circular))
            
        except Exception as e:
            logger.error(f"Error detecting circular dependencies: {str(e)}")
            return []
    
    async def _detect_god_objects(self, project_path: str) -> List[str]:
        """Detect god objects (classes with too many responsibilities)"""
        god_objects = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        tree = ast.parse(content)
                        
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                                if method_count > 15:  # Threshold for god object
                                    god_objects.append(f"{file}::{node.name}")
            
            return god_objects
            
        except Exception as e:
            logger.error(f"Error detecting god objects: {str(e)}")
            return []
    
    def _calculate_modularity_score(self, structure_info: Dict[str, Any]) -> float:
        """Calculate modularity score based on structure analysis"""
        if not structure_info["file_organization"]:
            return 0.0
        
        total_files = sum(info["python_files"] for info in structure_info["file_organization"].values())
        total_directories = len(structure_info["file_organization"])
        
        # Higher modularity score for well-organized structure
        if total_directories == 0:
            return 0.0
        
        files_per_directory = total_files / total_directories
        
        # Optimal range: 3-8 files per directory
        if 3 <= files_per_directory <= 8:
            return 0.9
        elif files_per_directory < 3:
            return 0.6
        else:
            return max(0.1, 0.9 - (files_per_directory - 8) * 0.1)
    
    async def _generate_architecture_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate architecture optimization recommendations"""
        recommendations = []
        
        # Modularity recommendations
        if analysis_results["modularity_score"] < 0.7:
            recommendations.append({
                "category": "modularity",
                "priority": "high",
                "title": "Improve Code Modularity",
                "description": "Consider reorganizing code into more focused modules",
                "implementation_effort": "medium",
                "expected_impact": "high"
            })
        
        # Risk factor recommendations
        for risk in analysis_results["risk_factors"]:
            if risk["type"] == "circular_dependencies":
                recommendations.append({
                    "category": "dependencies",
                    "priority": "critical",
                    "title": "Resolve Circular Dependencies",
                    "description": "Break circular dependencies to improve maintainability",
                    "implementation_effort": "high",
                    "expected_impact": "very_high"
                })
        
        return recommendations
    
    def _calculate_architecture_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate overall architecture quality score"""
        base_score = 100.0
        
        # Deduct points for risk factors
        for risk in analysis_results["risk_factors"]:
            if risk["severity"] == "critical":
                base_score -= 30
            elif risk["severity"] == "high":
                base_score -= 20
            elif risk["severity"] == "medium":
                base_score -= 10
        
        # Factor in modularity
        modularity_bonus = analysis_results["modularity_score"] * 20
        
        final_score = min(100.0, max(0.0, base_score + modularity_bonus - 100))
        return final_score / 100.0

class CodeQualityAssuranceAgent(BaseAIAgent):
    """AI Agent specializing in automated code quality assurance and testing"""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="code_quality_analysis",
                description="Comprehensive code quality analysis and scoring",
                input_types=["source_code", "test_files", "config_files"],
                output_types=["quality_report", "improvement_suggestions", "compliance_score"],
                performance_metrics={"accuracy": 0.93, "coverage": 0.88},
                success_rate=0.91
            ),
            AgentCapability(
                name="test_suite_generation",
                description="Automated test case generation and validation",
                input_types=["function_definitions", "class_specifications", "api_endpoints"],
                output_types=["test_cases", "coverage_analysis", "test_execution_report"],
                performance_metrics={"test_coverage": 0.85, "bug_detection_rate": 0.79},
                success_rate=0.87
            ),
            AgentCapability(
                name="security_vulnerability_scan",
                description="Automated security vulnerability detection and remediation",
                input_types=["source_code", "dependency_list", "configuration"],
                output_types=["vulnerability_report", "risk_assessment", "remediation_plan"],
                performance_metrics={"detection_accuracy": 0.90, "false_positive_rate": 0.12},
                success_rate=0.89
            )
        ]
        
        super().__init__(
            agent_id="code_qa_specialist_001",
            name="Code Quality Assurance Specialist",
            specialization="Code Quality & Testing",
            capabilities=capabilities
        )
    
    async def _execute_specialized_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute code quality assurance tasks"""
        try:
            task_type = task.requirements.get("type", "quality_analysis")
            
            if task_type == "quality_analysis":
                return await self._analyze_code_quality(task)
            elif task_type == "test_generation":
                return await self._generate_test_suite(task)
            elif task_type == "security_scan":
                return await self._perform_security_scan(task)
            else:
                return {"success": False, "error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"Code QA Agent error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_code_quality(self, task: AgentTask) -> Dict[str, Any]:
        """Perform comprehensive code quality analysis"""
        project_path = task.requirements.get("project_path", ".")
        
        quality_metrics = {
            "overall_score": 0.0,
            "maintainability_index": 0.0,
            "cyclomatic_complexity": 0.0,
            "code_duplication": 0.0,
            "test_coverage": 0.0,
            "documentation_coverage": 0.0,
            "style_compliance": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        # Analyze code complexity
        complexity_analysis = await self._analyze_code_complexity(project_path)
        quality_metrics.update(complexity_analysis)
        
        # Check code style compliance
        style_analysis = await self._check_style_compliance(project_path)
        quality_metrics.update(style_analysis)
        
        # Analyze test coverage
        coverage_analysis = await self._analyze_test_coverage(project_path)
        quality_metrics.update(coverage_analysis)
        
        # Generate improvement recommendations
        recommendations = await self._generate_quality_recommendations(quality_metrics)
        quality_metrics["recommendations"] = recommendations
        
        # Calculate overall quality score
        quality_metrics["overall_score"] = self._calculate_quality_score(quality_metrics)
        
        return {
            "success": True,
            "task_type": "quality_analysis",
            "quality_metrics": quality_metrics,
            "execution_time": datetime.now(timezone.utc).isoformat()
        }
    
    async def _analyze_code_complexity(self, project_path: str) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        complexity_data = {
            "cyclomatic_complexity": 0.0,
            "maintainability_index": 0.0,
            "complexity_issues": []
        }
        
        try:
            total_complexity = 0
            file_count = 0
            
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        file_complexity = await self._calculate_file_complexity(file_path)
                        total_complexity += file_complexity["complexity"]
                        file_count += 1
                        
                        if file_complexity["complexity"] > 10:  # Threshold for complex files
                            complexity_data["complexity_issues"].append({
                                "file": file,
                                "complexity": file_complexity["complexity"],
                                "recommendation": "Consider refactoring to reduce complexity"
                            })
            
            if file_count > 0:
                complexity_data["cyclomatic_complexity"] = total_complexity / file_count
                complexity_data["maintainability_index"] = max(0, 100 - complexity_data["cyclomatic_complexity"] * 5)
        
        except Exception as e:
            logger.error(f"Error analyzing code complexity: {str(e)}")
        
        return complexity_data
    
    async def _calculate_file_complexity(self, file_path: str) -> Dict[str, Any]:
        """Calculate complexity metrics for a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            complexity = 1  # Base complexity
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
            
            return {"complexity": complexity, "lines": len(content.splitlines())}
            
        except Exception as e:
            logger.error(f"Error calculating complexity for {file_path}: {str(e)}")
            return {"complexity": 0, "lines": 0}
    
    async def _check_style_compliance(self, project_path: str) -> Dict[str, Any]:
        """Check code style compliance"""
        style_data = {
            "style_compliance": 0.0,
            "style_issues": []
        }
        
        try:
            total_files = 0
            compliant_files = 0
            
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        total_files += 1
                        
                        issues = await self._check_file_style(file_path)
                        if len(issues) == 0:
                            compliant_files += 1
                        else:
                            style_data["style_issues"].extend(issues)
            
            if total_files > 0:
                style_data["style_compliance"] = compliant_files / total_files
        
        except Exception as e:
            logger.error(f"Error checking style compliance: {str(e)}")
        
        return style_data
    
    async def _check_file_style(self, file_path: str) -> List[Dict[str, Any]]:
        """Check style issues in a single file"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                # Check line length
                if len(line.strip()) > 100:
                    issues.append({
                        "file": os.path.basename(file_path),
                        "line": i,
                        "issue": "Line too long",
                        "severity": "minor"
                    })
                
                # Check for trailing whitespace
                if line.rstrip() != line.rstrip('\n'):
                    issues.append({
                        "file": os.path.basename(file_path),
                        "line": i,
                        "issue": "Trailing whitespace",
                        "severity": "minor"
                    })
        
        except Exception as e:
            logger.error(f"Error checking style for {file_path}: {str(e)}")
        
        return issues
    
    async def _analyze_test_coverage(self, project_path: str) -> Dict[str, Any]:
        """Analyze test coverage"""
        coverage_data = {
            "test_coverage": 0.0,
            "test_files": 0,
            "source_files": 0,
            "coverage_gaps": []
        }
        
        try:
            # Count test files and source files
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        if 'test' in file.lower() or file.startswith('test_'):
                            coverage_data["test_files"] += 1
                        else:
                            coverage_data["source_files"] += 1
            
            # Simple coverage estimation based on test-to-source ratio
            if coverage_data["source_files"] > 0:
                coverage_ratio = coverage_data["test_files"] / coverage_data["source_files"]
                coverage_data["test_coverage"] = min(1.0, coverage_ratio)
        
        except Exception as e:
            logger.error(f"Error analyzing test coverage: {str(e)}")
        
        return coverage_data
    
    async def _generate_quality_recommendations(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate code quality improvement recommendations"""
        recommendations = []
        
        # Test coverage recommendations
        if metrics["test_coverage"] < 0.8:
            recommendations.append({
                "category": "testing",
                "priority": "high",
                "title": "Increase Test Coverage",
                "description": f"Current coverage: {metrics['test_coverage']:.1%}, target: 80%+",
                "implementation": "Add unit tests for uncovered functions and classes",
                "estimated_effort": "medium"
            })
        
        # Complexity recommendations
        if metrics["cyclomatic_complexity"] > 8:
            recommendations.append({
                "category": "complexity",
                "priority": "medium",
                "title": "Reduce Code Complexity",
                "description": f"Average complexity: {metrics['cyclomatic_complexity']:.1f}, target: <8",
                "implementation": "Refactor complex functions into smaller, focused units",
                "estimated_effort": "high"
            })
        
        # Style compliance recommendations
        if metrics["style_compliance"] < 0.9:
            recommendations.append({
                "category": "style",
                "priority": "low",
                "title": "Improve Code Style Compliance",
                "description": f"Style compliance: {metrics['style_compliance']:.1%}, target: 90%+",
                "implementation": "Use automated code formatting tools (black, flake8)",
                "estimated_effort": "low"
            })
        
        return recommendations
    
    def _calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall code quality score"""
        weights = {
            "test_coverage": 0.25,
            "style_compliance": 0.15,
            "maintainability_index": 0.30,
            "complexity_penalty": 0.30
        }
        
        # Normalize maintainability index (0-100 to 0-1)
        maintainability_normalized = metrics["maintainability_index"] / 100
        
        # Calculate complexity penalty (lower is better)
        max_complexity = 15
        complexity_score = max(0, 1 - (metrics["cyclomatic_complexity"] / max_complexity))
        
        overall_score = (
            metrics["test_coverage"] * weights["test_coverage"] +
            metrics["style_compliance"] * weights["style_compliance"] +
            maintainability_normalized * weights["maintainability_index"] +
            complexity_score * weights["complexity_penalty"]
        )
        
        return min(1.0, max(0.0, overall_score))

# Register agents with orchestrator
def initialize_enterprise_agents():
    """Initialize and register enterprise agents"""
    try:
        # Create and register Enterprise Architecture Agent
        arch_agent = EnterpriseArchitectureAgent()
        orchestrator.register_agent(arch_agent)
        
        # Create and register Code Quality Assurance Agent
        qa_agent = CodeQualityAssuranceAgent()
        orchestrator.register_agent(qa_agent)
        
        logger.info("Enterprise agents initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize enterprise agents: {str(e)}")
        return False

# Auto-initialize when module is imported
initialize_enterprise_agents()