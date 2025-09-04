"""
AI Dashboard Builder Routes
Web interface and API endpoints for dashboard creation and management
"""

import json
import logging
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from ai_dashboard_models import (
    Dashboard, DashboardWidget, KPIDefinition, KPIValue,
    DashboardInsight, DashboardTemplate, ExecutiveBriefing,
    DashboardAlert, DashboardSubscription
)
from ai_dashboard_service import DashboardAIService, DashboardBuilderService
from models import AIAgent

dashboard_bp = Blueprint('ai_dashboard', __name__)

# Initialize services
ai_service = DashboardAIService()
builder_service = DashboardBuilderService()

@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Main dashboard homepage"""
    
    # Get user's dashboards
    user_dashboards = Dashboard.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(Dashboard.last_accessed.desc()).all()
    
    # Get subscription limits
    subscription_limits = builder_service.get_dashboard_subscription_limits(current_user.id)
    
    # Get recent insights
    recent_insights = DashboardInsight.query.join(Dashboard).filter(
        Dashboard.user_id == current_user.id,
        DashboardInsight.created_at >= datetime.utcnow() - timedelta(days=7),
        DashboardInsight.is_dismissed == False
    ).order_by(DashboardInsight.priority_level.desc()).limit(5).all()
    
    # Get featured templates
    featured_templates = DashboardTemplate.query.filter_by(
        is_featured=True,
        is_active=True
    ).limit(6).all()
    
    return render_template('ai_dashboard/home.html',
                         dashboards=user_dashboards,
                         subscription_limits=subscription_limits,
                         recent_insights=recent_insights,
                         featured_templates=featured_templates)

@dashboard_bp.route('/create')
@login_required
def create_dashboard():
    """Dashboard creation wizard"""
    
    # Check subscription limits
    subscription_limits = builder_service.get_dashboard_subscription_limits(current_user.id)
    current_dashboard_count = Dashboard.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).count()
    
    if current_dashboard_count >= subscription_limits['max_dashboards']:
        flash('You have reached your dashboard limit. Please upgrade your subscription.', 'warning')
        return redirect(url_for('ai_dashboard.dashboard_home'))
    
    # Get available templates
    templates = DashboardTemplate.query.filter_by(is_active=True).all()
    
    # Group templates by category
    templates_by_category = {}
    for template in templates:
        category = template.category or 'general'
        if category not in templates_by_category:
            templates_by_category[category] = []
        templates_by_category[category].append(template)
    
    # Get available AI agents for dashboard insights
    ai_agents = AIAgent.query.filter_by(is_active=True).limit(20).all()
    
    return render_template('ai_dashboard/create.html',
                         templates_by_category=templates_by_category,
                         ai_agents=ai_agents)

@dashboard_bp.route('/builder/<int:dashboard_id>')
@login_required
def dashboard_builder(dashboard_id):
    """Drag-and-drop dashboard builder interface"""
    
    dashboard = Dashboard.query.filter_by(
        id=dashboard_id,
        user_id=current_user.id
    ).first_or_404()
    
    # Update last accessed
    dashboard.last_accessed = datetime.utcnow()
    dashboard.view_count += 1
    db.session.commit()
    
    # Get dashboard widgets
    widgets = DashboardWidget.query.filter_by(
        dashboard_id=dashboard_id
    ).order_by(DashboardWidget.position_y, DashboardWidget.position_x).all()
    
    # Get available AI agents
    ai_agents = AIAgent.query.filter_by(is_active=True).all()
    
    # Get subscription limits
    subscription_limits = builder_service.get_dashboard_subscription_limits(current_user.id)
    
    return render_template('ai_dashboard/builder.html',
                         dashboard=dashboard,
                         widgets=widgets,
                         ai_agents=ai_agents,
                         subscription_limits=subscription_limits)

@dashboard_bp.route('/view/<int:dashboard_id>')
@login_required
def view_dashboard(dashboard_id):
    """View dashboard in presentation mode"""
    
    dashboard = Dashboard.query.filter_by(
        id=dashboard_id,
        user_id=current_user.id
    ).first_or_404()
    
    # Update last accessed
    dashboard.last_accessed = datetime.utcnow()
    dashboard.view_count += 1
    db.session.commit()
    
    # Get dashboard widgets
    widgets = DashboardWidget.query.filter_by(
        dashboard_id=dashboard_id,
        is_visible=True
    ).order_by(DashboardWidget.position_y, DashboardWidget.position_x).all()
    
    # Get recent insights
    recent_insights = DashboardInsight.query.filter_by(
        dashboard_id=dashboard_id,
        is_dismissed=False
    ).order_by(DashboardInsight.created_at.desc()).limit(5).all()
    
    return render_template('ai_dashboard/view.html',
                         dashboard=dashboard,
                         widgets=widgets,
                         recent_insights=recent_insights)

@dashboard_bp.route('/api/create-from-template', methods=['POST'])
@login_required
def api_create_from_template():
    """API endpoint to create dashboard from template"""
    
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        dashboard_name = data.get('name', 'New Dashboard')
        
        if not template_id:
            return jsonify({'error': 'Template ID is required'}), 400
        
        dashboard_id = builder_service.create_dashboard_from_template(
            current_user.id,
            template_id,
            dashboard_name
        )
        
        if dashboard_id:
            return jsonify({
                'success': True,
                'dashboard_id': dashboard_id,
                'redirect_url': url_for('ai_dashboard.dashboard_builder', dashboard_id=dashboard_id)
            })
        else:
            return jsonify({'error': 'Failed to create dashboard'}), 500
            
    except Exception as e:
        logging.error(f"Error creating dashboard from template: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@dashboard_bp.route('/api/generate-insights/<int:dashboard_id>', methods=['POST'])
@login_required
def api_generate_insights(dashboard_id):
    """API endpoint to generate AI insights for dashboard"""
    
    try:
        # Verify dashboard ownership
        dashboard = Dashboard.query.filter_by(
            id=dashboard_id,
            user_id=current_user.id
        ).first()
        
        if not dashboard:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        # Check subscription limits
        subscription_limits = builder_service.get_dashboard_subscription_limits(current_user.id)
        
        # Count insights generated this month
        current_month_insights = DashboardInsight.query.join(Dashboard).filter(
            Dashboard.user_id == current_user.id,
            DashboardInsight.created_at >= datetime.utcnow().replace(day=1)
        ).count()
        
        if current_month_insights >= subscription_limits['max_ai_insights_per_month']:
            return jsonify({'error': 'Monthly AI insights limit reached'}), 403
        
        # Generate insights
        insights = ai_service.generate_dashboard_insights(dashboard_id, current_user.id)
        
        return jsonify({
            'success': True,
            'insights_generated': len(insights),
            'insights': insights
        })
        
    except Exception as e:
        logging.error(f"Error generating insights: {str(e)}")
        return jsonify({'error': 'Failed to generate insights'}), 500

@dashboard_bp.route('/api/generate-briefing/<int:dashboard_id>', methods=['POST'])
@login_required
def api_generate_briefing(dashboard_id):
    """API endpoint to generate executive briefing"""
    
    try:
        data = request.get_json() or {}
        briefing_type = data.get('type', 'daily')
        
        # Verify dashboard ownership
        dashboard = Dashboard.query.filter_by(
            id=dashboard_id,
            user_id=current_user.id
        ).first()
        
        if not dashboard:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        # Check subscription limits
        subscription_limits = builder_service.get_dashboard_subscription_limits(current_user.id)
        
        # Count briefings generated this month
        current_month_briefings = ExecutiveBriefing.query.filter(
            ExecutiveBriefing.user_id == current_user.id,
            ExecutiveBriefing.created_at >= datetime.utcnow().replace(day=1)
        ).count()
        
        if current_month_briefings >= subscription_limits['max_executive_briefings_per_month']:
            return jsonify({'error': 'Monthly executive briefings limit reached'}), 403
        
        # Generate briefing
        briefing_result = ai_service.generate_executive_briefing(
            dashboard_id,
            current_user.id,
            briefing_type
        )
        
        if briefing_result:
            return jsonify({
                'success': True,
                'briefing_id': briefing_result['briefing_id'],
                'content': briefing_result['content'],
                'sections': briefing_result['sections']
            })
        else:
            return jsonify({'error': 'Failed to generate briefing'}), 500
        
    except Exception as e:
        logging.error(f"Error generating briefing: {str(e)}")
        return jsonify({'error': 'Failed to generate briefing'}), 500

@dashboard_bp.route('/api/add-widget/<int:dashboard_id>', methods=['POST'])
@login_required
def api_add_widget(dashboard_id):
    """API endpoint to add widget to dashboard"""
    
    try:
        # Verify dashboard ownership
        dashboard = Dashboard.query.filter_by(
            id=dashboard_id,
            user_id=current_user.id
        ).first()
        
        if not dashboard:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        # Check widget limits
        subscription_limits = builder_service.get_dashboard_subscription_limits(current_user.id)
        current_widget_count = DashboardWidget.query.filter_by(dashboard_id=dashboard_id).count()
        
        if current_widget_count >= subscription_limits['max_widgets_per_dashboard']:
            return jsonify({'error': 'Widget limit reached for this dashboard'}), 403
        
        data = request.get_json()
        
        # Create new widget
        widget = DashboardWidget()
        widget.dashboard_id = dashboard_id
        widget.widget_id = data.get('widget_id', f'widget_{current_widget_count + 1}')
        widget.widget_type = data.get('type', 'chart')
        widget.title = data.get('title', 'New Widget')
        widget.position_x = data.get('x', 0)
        widget.position_y = data.get('y', 0)
        widget.width = data.get('width', 4)
        widget.height = data.get('height', 3)
        widget.configuration = json.dumps(data.get('config', {}))
        
        if data.get('ai_agent_id'):
            widget.ai_agent_id = data['ai_agent_id']
            widget.ai_prompt_template = data.get('ai_prompt', '')
        
        db.session.add(widget)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'widget_id': widget.id,
            'widget': {
                'id': widget.id,
                'widget_id': widget.widget_id,
                'type': widget.widget_type,
                'title': widget.title,
                'x': widget.position_x,
                'y': widget.position_y,
                'width': widget.width,
                'height': widget.height
            }
        })
        
    except Exception as e:
        logging.error(f"Error adding widget: {str(e)}")
        return jsonify({'error': 'Failed to add widget'}), 500

@dashboard_bp.route('/api/update-widget/<int:widget_id>', methods=['PUT'])
@login_required
def api_update_widget(widget_id):
    """API endpoint to update widget configuration"""
    
    try:
        # Verify widget ownership through dashboard
        widget = db.session.query(DashboardWidget).join(Dashboard).filter(
            DashboardWidget.id == widget_id,
            Dashboard.user_id == current_user.id
        ).first()
        
        if not widget:
            return jsonify({'error': 'Widget not found'}), 404
        
        data = request.get_json()
        
        # Update widget properties
        if 'title' in data:
            widget.title = data['title']
        if 'x' in data:
            widget.position_x = data['x']
        if 'y' in data:
            widget.position_y = data['y']
        if 'width' in data:
            widget.width = data['width']
        if 'height' in data:
            widget.height = data['height']
        if 'config' in data:
            widget.configuration = json.dumps(data['config'])
        if 'is_visible' in data:
            widget.is_visible = data['is_visible']
        
        widget.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        logging.error(f"Error updating widget: {str(e)}")
        return jsonify({'error': 'Failed to update widget'}), 500

@dashboard_bp.route('/api/delete-widget/<int:widget_id>', methods=['DELETE'])
@login_required
def api_delete_widget(widget_id):
    """API endpoint to delete widget"""
    
    try:
        # Verify widget ownership through dashboard
        widget = db.session.query(DashboardWidget).join(Dashboard).filter(
            DashboardWidget.id == widget_id,
            Dashboard.user_id == current_user.id
        ).first()
        
        if not widget:
            return jsonify({'error': 'Widget not found'}), 404
        
        db.session.delete(widget)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        logging.error(f"Error deleting widget: {str(e)}")
        return jsonify({'error': 'Failed to delete widget'}), 500

@dashboard_bp.route('/templates')
@login_required
def dashboard_templates():
    """Browse available dashboard templates"""
    
    # Get templates by category
    templates = DashboardTemplate.query.filter_by(is_active=True).all()
    
    templates_by_category = {}
    for template in templates:
        category = template.category or 'general'
        if category not in templates_by_category:
            templates_by_category[category] = []
        templates_by_category[category].append(template)
    
    return render_template('ai_dashboard/templates.html',
                         templates_by_category=templates_by_category)

@dashboard_bp.route('/insights')
@login_required
def dashboard_insights():
    """View all AI insights across dashboards"""
    
    # Get all insights for user's dashboards
    insights = DashboardInsight.query.join(Dashboard).filter(
        Dashboard.user_id == current_user.id
    ).order_by(DashboardInsight.created_at.desc()).limit(50).all()
    
    # Group by priority
    insights_by_priority = {
        'high': [i for i in insights if i.priority_level == 'high'],
        'medium': [i for i in insights if i.priority_level == 'medium'],
        'low': [i for i in insights if i.priority_level == 'low']
    }
    
    return render_template('ai_dashboard/insights.html',
                         insights=insights,
                         insights_by_priority=insights_by_priority)

@dashboard_bp.route('/subscription')
@login_required
def dashboard_subscription():
    """Dashboard subscription management"""
    
    current_subscription = DashboardSubscription.query.filter_by(
        user_id=current_user.id
    ).first()
    
    # Get current usage
    current_usage = {
        'dashboards': Dashboard.query.filter_by(user_id=current_user.id, is_active=True).count(),
        'insights_this_month': DashboardInsight.query.join(Dashboard).filter(
            Dashboard.user_id == current_user.id,
            DashboardInsight.created_at >= datetime.utcnow().replace(day=1)
        ).count(),
        'briefings_this_month': ExecutiveBriefing.query.filter(
            ExecutiveBriefing.user_id == current_user.id,
            ExecutiveBriefing.created_at >= datetime.utcnow().replace(day=1)
        ).count()
    }
    
    # Available plans
    plans = [
        {
            'name': 'Starter',
            'price': 199,
            'max_dashboards': 5,
            'max_widgets_per_dashboard': 15,
            'max_ai_insights_per_month': 100,
            'max_executive_briefings_per_month': 10,
            'features': ['AI-powered insights', 'Executive briefings', 'Custom dashboards', 'Email support']
        },
        {
            'name': 'Professional',
            'price': 499,
            'max_dashboards': 20,
            'max_widgets_per_dashboard': 50,
            'max_ai_insights_per_month': 500,
            'max_executive_briefings_per_month': 50,
            'features': ['Everything in Starter', 'Advanced AI agents', 'Custom templates', 'API access', 'Priority support']
        },
        {
            'name': 'Enterprise',
            'price': 999,
            'max_dashboards': 100,
            'max_widgets_per_dashboard': 100,
            'max_ai_insights_per_month': 2000,
            'max_executive_briefings_per_month': 200,
            'features': ['Everything in Professional', 'White-label options', 'SSO integration', 'Dedicated support', 'Custom AI training']
        }
    ]
    
    return render_template('ai_dashboard/subscription.html',
                         current_subscription=current_subscription,
                         current_usage=current_usage,
                         plans=plans)