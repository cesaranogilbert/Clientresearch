from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from app import db
from models import AIAgent, AgentCustomization, User
from enterprise_policy_enforcement import require_dlp_scan, require_permission
import json
import uuid
import logging
from datetime import datetime, timedelta

workflow_bp = Blueprint('workflow_automation', __name__)

# Workflow Models - Add these to models.py
class WorkflowTemplate(db.Model):
    __tablename__ = 'workflow_template'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    workflow_data = db.Column(db.Text)  # JSON workflow configuration
    trigger_type = db.Column(db.String(50))  # schedule, webhook, manual, email
    trigger_config = db.Column(db.Text)  # JSON trigger configuration
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)
    execution_count = db.Column(db.Integer, default=0)
    last_executed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WorkflowExecution(db.Model):
    __tablename__ = 'workflow_execution'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow_template.id'), nullable=False)
    execution_id = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), default='running')  # running, completed, failed, paused
    trigger_data = db.Column(db.Text)  # JSON data that triggered this execution
    execution_log = db.Column(db.Text)  # JSON execution steps and results
    total_cost = db.Column(db.Float, default=0.0)
    execution_time_seconds = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class WorkflowStep(db.Model):
    __tablename__ = 'workflow_step'
    
    id = db.Column(db.Integer, primary_key=True)
    execution_id = db.Column(db.String(100), db.ForeignKey('workflow_execution.execution_id'), nullable=False)
    step_id = db.Column(db.String(100), nullable=False)  # Unique within workflow
    agent_id = db.Column(db.Integer, db.ForeignKey('ai_agent.id'))
    step_type = db.Column(db.String(50))  # agent, condition, delay, webhook, email
    input_data = db.Column(db.Text)  # JSON input
    output_data = db.Column(db.Text)  # JSON output
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed, skipped
    cost = db.Column(db.Float, default=0.0)
    execution_time_ms = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

@workflow_bp.route('/builder')
@login_required
def workflow_builder():
    """Visual workflow builder interface"""
    
    # Get user's available AI agents
    user_agents = AgentCustomization.query.filter_by(user_id=current_user.id).all()
    
    # Get available workflow templates
    public_templates = WorkflowTemplate.query.filter_by(is_public=True, is_active=True).limit(10).all()
    
    # Get pre-built node types
    node_types = get_workflow_node_types()
    
    return render_template('workflow/builder.html',
                         user_agents=user_agents,
                         public_templates=public_templates,
                         node_types=node_types)

@workflow_bp.route('/templates')
@login_required
def workflow_templates():
    """Browse workflow templates marketplace"""
    
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = WorkflowTemplate.query.filter_by(is_public=True, is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(WorkflowTemplate.name.contains(search) | 
                           WorkflowTemplate.description.contains(search))
    
    templates = query.order_by(WorkflowTemplate.execution_count.desc()).all()
    
    # Get categories for filtering
    categories = db.session.query(WorkflowTemplate.category.distinct())\
                          .filter_by(is_public=True, is_active=True)\
                          .all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('workflow/templates.html',
                         templates=templates,
                         categories=categories,
                         current_category=category,
                         current_search=search)

@workflow_bp.route('/save-workflow', methods=['POST'])
@login_required
@require_dlp_scan('internal')
@require_permission('create_workflow')
def save_workflow():
    """Save workflow configuration"""
    
    try:
        data = request.get_json()
        
        workflow_data = {
            'nodes': data.get('nodes', []),
            'connections': data.get('connections', []),
            'settings': data.get('settings', {})
        }
        
        # Validate workflow
        validation_result = validate_workflow(workflow_data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        # Create or update workflow
        workflow_id = data.get('workflow_id')
        if workflow_id:
            workflow = WorkflowTemplate.query.get(workflow_id)
            if not workflow or workflow.user_id != current_user.id:
                return jsonify({'error': 'Workflow not found'}), 404
        else:
            workflow = WorkflowTemplate()
            workflow.user_id = current_user.id
        
        workflow.name = data.get('name', 'Untitled Workflow')
        workflow.description = data.get('description', '')
        workflow.category = data.get('category', 'Custom')
        workflow.workflow_data = json.dumps(workflow_data)
        workflow.trigger_type = data.get('trigger_type', 'manual')
        workflow.trigger_config = json.dumps(data.get('trigger_config', {}))
        workflow.is_public = data.get('is_public', False)
        
        if not workflow_id:
            db.session.add(workflow)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'workflow_id': workflow.id,
            'message': 'Workflow saved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Workflow save error: {str(e)}")
        return jsonify({'error': 'Failed to save workflow'}), 500

@workflow_bp.route('/execute-workflow', methods=['POST'])
@login_required
def execute_workflow():
    """Execute a workflow"""
    
    try:
        data = request.get_json()
        workflow_id = data.get('workflow_id')
        input_data = data.get('input_data', {})
        
        workflow = WorkflowTemplate.query.get(workflow_id)
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        # Check permissions
        if workflow and workflow.user_id != current_user.id and not workflow.is_public:
            return jsonify({'error': 'Access denied'}), 403
        
        # Create execution record
        execution_id = str(uuid.uuid4())
        execution = WorkflowExecution()
        execution.workflow_id = workflow.id
        execution.execution_id = execution_id
        execution.trigger_data = json.dumps(input_data)
        execution.status = 'running'
        
        db.session.add(execution)
        db.session.commit()
        
        # Start workflow execution asynchronously
        from threading import Thread
        execution_thread = Thread(target=execute_workflow_async, 
                                args=(execution_id, workflow, input_data))
        execution_thread.start()
        
        return jsonify({
            'success': True,
            'execution_id': execution_id,
            'message': 'Workflow execution started'
        })
        
    except Exception as e:
        logging.error(f"Workflow execution error: {str(e)}")
        return jsonify({'error': 'Failed to start workflow execution'}), 500

@workflow_bp.route('/execution/<execution_id>/status')
@login_required
def get_execution_status(execution_id):
    """Get workflow execution status"""
    
    execution = WorkflowExecution.query.filter_by(execution_id=execution_id).first()
    if not execution:
        return jsonify({'error': 'Execution not found'}), 404
    
    # Check permissions
    workflow = WorkflowTemplate.query.get(execution.workflow_id)
    if workflow.user_id != current_user.id and not workflow.is_public:
        return jsonify({'error': 'Access denied'}), 403
    
    # Get execution steps
    steps = WorkflowStep.query.filter_by(execution_id=execution_id)\
                             .order_by(WorkflowStep.started_at).all()
    
    return jsonify({
        'execution_id': execution.execution_id,
        'status': execution.status,
        'total_cost': execution.total_cost,
        'execution_time': execution.execution_time_seconds,
        'error_message': execution.error_message,
        'started_at': execution.started_at.isoformat() if execution.started_at else None,
        'completed_at': execution.completed_at.isoformat() if execution.completed_at else None,
        'steps': [{
            'step_id': step.step_id,
            'step_type': step.step_type,
            'status': step.status,
            'cost': step.cost,
            'execution_time_ms': step.execution_time_ms,
            'error_message': step.error_message,
            'output_preview': json.loads(step.output_data or '{}').get('preview', '') if step.output_data else ''
        } for step in steps]
    })

@workflow_bp.route('/my-workflows')
@login_required
def my_workflows():
    """User's workflow dashboard"""
    
    workflows = WorkflowTemplate.query.filter_by(user_id=current_user.id)\
                                     .order_by(WorkflowTemplate.updated_at.desc()).all()
    
    # Get recent executions
    recent_executions = db.session.query(WorkflowExecution)\
                                 .join(WorkflowTemplate)\
                                 .filter(WorkflowTemplate.user_id == current_user.id)\
                                 .order_by(WorkflowExecution.started_at.desc())\
                                 .limit(10).all()
    
    # Calculate usage statistics
    total_executions = db.session.query(WorkflowExecution)\
                                .join(WorkflowTemplate)\
                                .filter(WorkflowTemplate.user_id == current_user.id)\
                                .count()
    
    total_cost = db.session.query(db.func.sum(WorkflowExecution.total_cost))\
                          .join(WorkflowTemplate)\
                          .filter(WorkflowTemplate.user_id == current_user.id)\
                          .scalar() or 0.0
    
    return render_template('workflow/dashboard.html',
                         workflows=workflows,
                         recent_executions=recent_executions,
                         total_executions=total_executions,
                         total_cost=total_cost)

# Helper functions
def get_workflow_node_types():
    """Get available workflow node types"""
    return {
        'ai_agent': {
            'name': 'AI Agent',
            'description': 'Execute an AI agent with specific input',
            'icon': 'bi-robot',
            'color': '#007bff',
            'inputs': ['text', 'json', 'file'],
            'outputs': ['text', 'json', 'analysis']
        },
        'condition': {
            'name': 'Condition',
            'description': 'Branch workflow based on conditions',
            'icon': 'bi-diagram-3',
            'color': '#28a745',
            'inputs': ['any'],
            'outputs': ['true', 'false']
        },
        'delay': {
            'name': 'Delay',
            'description': 'Wait for specified time',
            'icon': 'bi-clock',
            'color': '#ffc107',
            'inputs': ['trigger'],
            'outputs': ['trigger']
        },
        'webhook': {
            'name': 'Webhook',
            'description': 'Send HTTP request to external service',
            'icon': 'bi-link-45deg',
            'color': '#6f42c1',
            'inputs': ['json', 'text'],
            'outputs': ['json', 'text']
        },
        'email': {
            'name': 'Email',
            'description': 'Send email notification',
            'icon': 'bi-envelope',
            'color': '#dc3545',
            'inputs': ['text', 'html'],
            'outputs': ['status']
        },
        'data_transform': {
            'name': 'Transform Data',
            'description': 'Transform and format data',
            'icon': 'bi-arrow-left-right',
            'color': '#20c997',
            'inputs': ['json', 'text'],
            'outputs': ['json', 'text']
        },
        'file_operation': {
            'name': 'File Operation',
            'description': 'Read, write, or process files',
            'icon': 'bi-file-earmark',
            'color': '#fd7e14',
            'inputs': ['file', 'text'],
            'outputs': ['file', 'text']
        }
    }

def validate_workflow(workflow_data):
    """Validate workflow configuration"""
    nodes = workflow_data.get('nodes', [])
    connections = workflow_data.get('connections', [])
    
    if not nodes:
        return {'valid': False, 'message': 'Workflow must have at least one node'}
    
    # Check for start node
    has_start = any(node.get('type') == 'start' for node in nodes)
    if not has_start:
        return {'valid': False, 'message': 'Workflow must have a start node'}
    
    # Validate connections
    node_ids = {node['id'] for node in nodes}
    for connection in connections:
        if connection['source'] not in node_ids or connection['target'] not in node_ids:
            return {'valid': False, 'message': 'Invalid connection detected'}
    
    # Check for circular dependencies (simplified)
    # In a production system, you'd want more sophisticated cycle detection
    
    return {'valid': True, 'message': 'Workflow is valid'}

def execute_workflow_async(execution_id, workflow, input_data):
    """Execute workflow asynchronously"""
    try:
        with db.app.app_context():
            execution = WorkflowExecution.query.filter_by(execution_id=execution_id).first()
            if not execution:
                return
            
            workflow_data = json.loads(workflow.workflow_data)
            nodes = workflow_data.get('nodes', [])
            connections = workflow_data.get('connections', [])
            
            # Build execution graph
            execution_graph = build_execution_graph(nodes, connections)
            
            # Execute workflow
            total_cost = 0.0
            execution_log = []
            
            start_time = datetime.utcnow()
            
            try:
                for step_config in execution_graph:
                    step_result = execute_workflow_step(execution_id, step_config, input_data)
                    total_cost += step_result.get('cost', 0.0)
                    execution_log.append(step_result)
                    
                    # Update input_data for next step
                    input_data.update(step_result.get('output', {}))
                
                # Mark as completed
                execution.status = 'completed'
                execution.total_cost = total_cost
                execution.execution_time_seconds = (datetime.utcnow() - start_time).total_seconds()
                execution.completed_at = datetime.utcnow()
                execution.execution_log = json.dumps(execution_log)
                
            except Exception as step_error:
                execution.status = 'failed'
                execution.error_message = str(step_error)
                execution.completed_at = datetime.utcnow()
                logging.error(f"Workflow step failed: {str(step_error)}")
            
            # Update workflow execution count
            workflow.execution_count += 1
            workflow.last_executed = datetime.utcnow()
            
            db.session.commit()
            
    except Exception as e:
        logging.error(f"Workflow execution error: {str(e)}")
        with db.app.app_context():
            execution = WorkflowExecution.query.filter_by(execution_id=execution_id).first()
            if execution:
                execution.status = 'failed'
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                db.session.commit()

def build_execution_graph(nodes, connections):
    """Build ordered execution graph from workflow nodes and connections"""
    # Simplified topological sort for workflow execution
    # In production, you'd want a more sophisticated graph algorithm
    
    # Find start node
    start_node = next((node for node in nodes if node.get('type') == 'start'), None)
    if not start_node:
        raise ValueError("No start node found")
    
    # Build adjacency list
    graph = {node['id']: [] for node in nodes}
    for connection in connections:
        graph[connection['source']].append(connection['target'])
    
    # Simple DFS-based execution order
    visited = set()
    execution_order = []
    
    def dfs(node_id):
        if node_id in visited:
            return
        visited.add(node_id)
        
        # Find node config
        node_config = next((node for node in nodes if node['id'] == node_id), None)
        if node_config and node_config.get('type') != 'start':
            execution_order.append(node_config)
        
        # Visit connected nodes
        for next_node_id in graph[node_id]:
            dfs(next_node_id)
    
    dfs(start_node['id'])
    return execution_order

def execute_workflow_step(execution_id, step_config, input_data):
    """Execute a single workflow step"""
    step_id = step_config['id']
    step_type = step_config['type']
    
    # Create workflow step record
    step = WorkflowStep()
    step.execution_id = execution_id
    step.step_id = step_id
    step.step_type = step_type
    step.input_data = json.dumps(input_data)
    step.status = 'running'
    step.started_at = datetime.utcnow()
    
    db.session.add(step)
    db.session.commit()
    
    start_time = datetime.utcnow()
    
    try:
        if step_type == 'ai_agent':
            result = execute_ai_agent_step(step_config, input_data)
        elif step_type == 'condition':
            result = execute_condition_step(step_config, input_data)
        elif step_type == 'delay':
            result = execute_delay_step(step_config, input_data)
        elif step_type == 'webhook':
            result = execute_webhook_step(step_config, input_data)
        elif step_type == 'email':
            result = execute_email_step(step_config, input_data)
        else:
            result = {'output': input_data, 'cost': 0.0}
        
        step.status = 'completed'
        step.output_data = json.dumps(result)
        step.cost = result.get('cost', 0.0)
        
    except Exception as e:
        step.status = 'failed'
        step.error_message = str(e)
        result = {'output': {}, 'cost': 0.0, 'error': str(e)}
    
    step.execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    step.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    return result

def execute_ai_agent_step(step_config, input_data):
    """Execute AI agent workflow step"""
    from openai import OpenAI
    import os
    
    agent_id = step_config.get('agent_id')
    prompt_template = step_config.get('prompt', '{input}')
    
    # Get agent
    agent = AIAgent.query.get(agent_id)
    if not agent:
        raise ValueError(f"Agent {agent_id} not found")
    
    # Format prompt
    formatted_prompt = prompt_template.format(**input_data)
    
    # Execute with OpenAI
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    response = client.chat.completions.create(
        model=agent.default_model or 'gpt-4o',
        messages=[
            {"role": "system", "content": agent.base_prompt},
            {"role": "user", "content": formatted_prompt}
        ],
        max_tokens=1000
    )
    
    result_text = response.choices[0].message.content
    cost = calculate_api_cost(response.usage)
    
    return {
        'output': {
            'agent_response': result_text,
            'agent_name': agent.name,
            'preview': result_text[:200] + ('...' if len(result_text) > 200 else '')
        },
        'cost': cost
    }

def execute_condition_step(step_config, input_data):
    """Execute condition workflow step"""
    condition = step_config.get('condition', 'true')
    
    # Simple condition evaluation
    # In production, you'd want a safer evaluation system
    try:
        # Replace input references with actual values
        for key, value in input_data.items():
            condition = condition.replace(f'{{{key}}}', str(value))
        
        result = eval(condition)  # WARNING: Unsafe in production!
        
        return {
            'output': {'condition_result': result, 'branch': 'true' if result else 'false'},
            'cost': 0.0
        }
    except Exception as e:
        return {
            'output': {'condition_result': False, 'branch': 'false', 'error': str(e)},
            'cost': 0.0
        }

def execute_delay_step(step_config, input_data):
    """Execute delay workflow step"""
    import time
    
    delay_seconds = step_config.get('delay_seconds', 1)
    time.sleep(delay_seconds)
    
    return {
        'output': {'delayed_seconds': delay_seconds},
        'cost': 0.0
    }

def execute_webhook_step(step_config, input_data):
    """Execute webhook workflow step"""
    import requests
    
    url = step_config.get('url')
    method = step_config.get('method', 'POST')
    headers = step_config.get('headers', {})
    
    if method.upper() == 'POST':
        response = requests.post(url, json=input_data, headers=headers, timeout=30)
    else:
        response = requests.get(url, headers=headers, timeout=30)
    
    return {
        'output': {
            'status_code': response.status_code,
            'response_data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        },
        'cost': 0.01  # Small cost for webhook calls
    }

def execute_email_step(step_config, input_data):
    """Execute email workflow step"""
    # Placeholder for email functionality
    # In production, integrate with SendGrid or similar service
    
    recipient = step_config.get('recipient')
    subject = step_config.get('subject', 'Workflow Notification')
    body = step_config.get('body', 'Workflow completed successfully')
    
    # Format email content
    subject = subject.format(**input_data)
    body = body.format(**input_data)
    
    # Log email (replace with actual sending)
    logging.info(f"Email sent to {recipient}: {subject}")
    
    return {
        'output': {
            'email_sent': True,
            'recipient': recipient,
            'subject': subject
        },
        'cost': 0.005  # Small cost for email
    }

def calculate_api_cost(usage):
    """Calculate API cost based on usage"""
    # Simplified cost calculation for GPT-4o
    input_cost_per_1k = 0.005
    output_cost_per_1k = 0.015
    
    input_cost = (usage.prompt_tokens / 1000) * input_cost_per_1k
    output_cost = (usage.completion_tokens / 1000) * output_cost_per_1k
    
    return input_cost + output_cost