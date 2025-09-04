from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from app import db
from models import AIAgent, CreatorProfile, User, AgentCustomization
from enterprise_policy_enforcement import require_dlp_scan, require_permission
import json
import logging
from datetime import datetime, timedelta
import uuid

user_marketplace_bp = Blueprint('user_marketplace', __name__)

@user_marketplace_bp.route('/create-agent')
@login_required
def create_agent_form():
    """AI Agent Creation Interface - Subway-style customization"""
    
    # Get or create creator profile
    creator_profile = CreatorProfile.query.filter_by(user_id=current_user.id).first()
    if not creator_profile:
        creator_profile = CreatorProfile()
        creator_profile.user_id = current_user.id
        creator_profile.creator_name = current_user.full_name or current_user.username
        creator_profile.revenue_share_percentage = 0.70
        db.session.add(creator_profile)
        db.session.commit()
    
    # Agent categories and specializations
    categories = {
        'Business Strategy': ['C-Suite Advisory', 'Strategic Planning', 'Market Analysis', 'Competitive Intelligence'],
        'Marketing & Sales': ['Digital Marketing', 'Lead Generation', 'Sales Automation', 'Content Creation'],
        'Finance & Accounting': ['Financial Analysis', 'Tax Optimization', 'Investment Advisory', 'Risk Management'],
        'Technology & Development': ['Software Architecture', 'DevOps', 'AI/ML Engineering', 'Cybersecurity'],
        'Legal & Compliance': ['Corporate Law', 'Compliance Management', 'Contract Analysis', 'IP Protection'],
        'Operations & HR': ['Process Optimization', 'Team Management', 'Talent Acquisition', 'Performance Analytics'],
        'Creative & Design': ['Brand Strategy', 'UI/UX Design', 'Creative Direction', 'Visual Communications'],
        'Industry Specialists': ['Healthcare', 'Finance', 'E-commerce', 'Manufacturing', 'Real Estate']
    }
    
    # AI Models available
    ai_models = {
        'gpt-4o': {'name': 'GPT-4o', 'description': 'Latest OpenAI model with multimodal capabilities', 'cost_modifier': 1.0},
        'claude-sonnet-4': {'name': 'Claude 4.0 Sonnet', 'description': 'Advanced reasoning and analysis', 'cost_modifier': 1.2},
        'gemini-2.5-pro': {'name': 'Gemini 2.5 Pro', 'description': 'Google\'s most advanced model', 'cost_modifier': 1.1},
        'grok-2-1212': {'name': 'Grok 2', 'description': 'xAI\'s advanced reasoning model', 'cost_modifier': 1.3},
        'perplexity-sonar': {'name': 'Perplexity Sonar', 'description': 'Real-time web search integration', 'cost_modifier': 1.4}
    }
    
    return render_template('user_marketplace/create_agent.html', 
                         categories=categories, 
                         ai_models=ai_models,
                         creator_profile=creator_profile)

@user_marketplace_bp.route('/submit-agent', methods=['POST'])
@login_required
@require_dlp_scan('confidential')
@require_permission('submit_marketplace_agent')
def submit_agent():
    """Process agent submission with advanced validation"""
    
    try:
        # Get creator profile
        creator_profile = CreatorProfile.query.filter_by(user_id=current_user.id).first()
        if not creator_profile:
            return jsonify({'error': 'Creator profile required'}), 400
        
        # Extract form data
        agent_data = {
            'name': request.form.get('agent_name'),
            'description': request.form.get('description'),
            'category': request.form.get('category'),
            'specialization_tags': request.form.get('specialization_tags'),
            'base_prompt': request.form.get('base_prompt'),
            'pricing_tier': request.form.get('pricing_tier'),
            'base_price': float(request.form.get('base_price', 0)),
            'monthly_price': float(request.form.get('monthly_price', 0)),
            'default_model': request.form.get('ai_model'),
            'expertise_level': int(request.form.get('expertise_level', 50)),
            'practical_projects': int(request.form.get('practical_projects', 1000)),
            'industry_category': request.form.get('industry_category'),
            'success_metrics': request.form.get('success_metrics'),
            'capabilities': request.form.get('capabilities')
        }
        
        # Validate required fields
        required_fields = ['name', 'description', 'category', 'base_prompt', 'pricing_tier']
        for field in required_fields:
            if not agent_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new AI agent
        new_agent = AIAgent()
        new_agent.name = agent_data['name']
        new_agent.description = agent_data['description']
        new_agent.category = agent_data['category']
        new_agent.base_prompt = agent_data['base_prompt']
        new_agent.pricing_tier = agent_data['pricing_tier']
        new_agent.base_price = agent_data['base_price']
        new_agent.monthly_price = agent_data['monthly_price']
        new_agent.specialization_tags = agent_data['specialization_tags']
        new_agent.expertise_level = agent_data['expertise_level']
        new_agent.practical_projects = agent_data['practical_projects']
        new_agent.industry_category = agent_data['industry_category']
        new_agent.success_metrics = agent_data['success_metrics']
        new_agent.capabilities = agent_data['capabilities']
        new_agent.default_model = agent_data['default_model']
        new_agent.creator_id = creator_profile.id
        new_agent.creator_revenue_share = creator_profile.revenue_share_percentage
        new_agent.approval_status = 'pending'
        new_agent.submission_date = datetime.utcnow()
        new_agent.is_active = False  # Inactive until approved
        
        # Calculate advanced metrics
        new_agent.trust_score = calculate_trust_score(creator_profile, agent_data)
        new_agent.roi_multiplier = calculate_roi_multiplier(agent_data)
        new_agent.success_rate = 0.95  # Base success rate for new agents
        
        db.session.add(new_agent)
        
        # Update creator profile
        creator_profile.agents_created += 1
        
        db.session.commit()
        
        # Log submission
        logging.info(f"New agent submitted: {new_agent.name} by user {current_user.id}")
        
        return jsonify({
            'success': True,
            'message': 'Agent submitted successfully for review',
            'agent_id': new_agent.id,
            'estimated_review_time': '24-48 hours'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Agent submission error: {str(e)}")
        return jsonify({'error': 'Submission failed. Please try again.'}), 500

@user_marketplace_bp.route('/my-agents')
@login_required
def my_agents():
    """Dashboard for user's created agents"""
    
    creator_profile = CreatorProfile.query.filter_by(user_id=current_user.id).first()
    if not creator_profile:
        return redirect(url_for('user_marketplace.create_agent_form'))
    
    # Get user's agents
    agents = AIAgent.query.filter_by(creator_id=creator_profile.id).order_by(AIAgent.created_at.desc()).all()
    
    # Calculate earnings
    total_earnings = creator_profile.total_earnings
    pending_earnings = calculate_pending_earnings(creator_profile.id)
    
    # Get recent sales
    from models import RevenueShare
    recent_sales = RevenueShare.query.filter_by(creator_id=creator_profile.id)\
                                   .order_by(RevenueShare.created_at.desc())\
                                   .limit(10).all()
    
    return render_template('user_marketplace/my_agents.html',
                         agents=agents,
                         creator_profile=creator_profile,
                         total_earnings=total_earnings,
                         pending_earnings=pending_earnings,
                         recent_sales=recent_sales)

@user_marketplace_bp.route('/agent/<int:agent_id>/edit')
@login_required
def edit_agent(agent_id):
    """Edit existing agent (only for creator)"""
    
    agent = AIAgent.query.get_or_404(agent_id)
    creator_profile = CreatorProfile.query.filter_by(user_id=current_user.id).first()
    
    if not creator_profile or agent.creator_id != creator_profile.id:
        flash('Access denied', 'error')
        return redirect(url_for('user_marketplace.my_agents'))
    
    return render_template('user_marketplace/edit_agent.html', agent=agent)

@user_marketplace_bp.route('/agent/<int:agent_id>/update', methods=['POST'])
@login_required
def update_agent(agent_id):
    """Update agent details"""
    
    agent = AIAgent.query.get_or_404(agent_id)
    creator_profile = CreatorProfile.query.filter_by(user_id=current_user.id).first()
    
    if not creator_profile or agent.creator_id != creator_profile.id:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Update allowed fields
        updateable_fields = [
            'description', 'base_prompt', 'capabilities', 'success_metrics',
            'specialization_tags', 'pricing_tier', 'base_price', 'monthly_price'
        ]
        
        for field in updateable_fields:
            if field in request.form:
                if field in ['base_price', 'monthly_price']:
                    setattr(agent, field, float(request.form[field]))
                else:
                    setattr(agent, field, request.form[field])
        
        agent.updated_at = datetime.utcnow()
        
        # If major changes, reset to pending approval
        if any(field in request.form for field in ['base_prompt', 'capabilities', 'pricing_tier']):
            agent.approval_status = 'pending'
            agent.is_active = False
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Agent updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_marketplace_bp.route('/browse-community-agents')
def browse_community_agents():
    """Browse agents created by community"""
    
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    sort_by = request.args.get('sort', 'featured')  # featured, newest, rating, price
    
    query = AIAgent.query.filter_by(approval_status='approved', is_active=True)
    
    # Filter by category
    if category:
        query = query.filter_by(category=category)
    
    # Sort
    if sort_by == 'newest':
        query = query.order_by(AIAgent.created_at.desc())
    elif sort_by == 'rating':
        query = query.order_by(AIAgent.trust_score.desc())
    elif sort_by == 'price':
        query = query.order_by(AIAgent.monthly_price.asc())
    else:  # featured
        query = query.order_by(AIAgent.is_featured.desc(), AIAgent.trust_score.desc())
    
    agents = query.paginate(page=page, per_page=12, error_out=False)
    
    # Get categories for filter
    categories = db.session.query(AIAgent.category.distinct()).filter_by(
        approval_status='approved', is_active=True
    ).all()
    categories = [cat[0] for cat in categories]
    
    return render_template('user_marketplace/browse_agents.html',
                         agents=agents,
                         categories=categories,
                         current_category=category,
                         current_sort=sort_by)

@user_marketplace_bp.route('/agent/<int:agent_id>/preview')
def preview_agent(agent_id):
    """Preview agent details and capabilities"""
    
    agent = AIAgent.query.get_or_404(agent_id)
    
    if agent.approval_status != 'approved' or not agent.is_active:
        # Only creator and admin can view unapproved agents
        if not current_user.is_authenticated or (
            current_user.id != agent.creator.user_id and not current_user.is_admin
        ):
            flash('Agent not available', 'error')
            return redirect(url_for('user_marketplace.browse_community_agents'))
    
    # Get creator info
    creator = agent.creator
    
    # Get usage statistics if user owns this agent
    user_stats = None
    if current_user.is_authenticated:
        from models import UserAgent
        user_agent = UserAgent.query.filter_by(
            user_id=current_user.id, 
            agent_id=agent_id, 
            status='active'
        ).first()
        if user_agent:
            user_stats = {
                'usage_count': user_agent.usage_count,
                'last_used': user_agent.last_used,
                'license_type': user_agent.license_type
            }
    
    return render_template('user_marketplace/agent_preview.html',
                         agent=agent,
                         creator=creator,
                         user_stats=user_stats)

# Helper functions
def calculate_trust_score(creator_profile, agent_data):
    """Calculate initial trust score for new agent"""
    base_score = 0.75
    
    # Boost for verified creators
    if creator_profile.is_verified:
        base_score += 0.10
    
    # Boost for experience
    if creator_profile.agents_created > 5:
        base_score += 0.05
    
    # Boost for detailed description
    description = agent_data.get('description', '')
    if description and len(description) > 500:
        base_score += 0.05
    
    # Boost for high expertise level
    if agent_data.get('expertise_level', 0) > 75:
        base_score += 0.05
    
    return min(base_score, 0.95)

def calculate_roi_multiplier(agent_data):
    """Calculate expected ROI multiplier"""
    base_multiplier = 2.0
    
    # Higher multiplier for business strategy agents
    if 'strategy' in agent_data.get('category', '').lower():
        base_multiplier += 0.5
    
    # Higher multiplier for higher expertise
    expertise_bonus = agent_data.get('expertise_level', 50) / 100.0
    base_multiplier += expertise_bonus
    
    return min(base_multiplier, 5.0)

def calculate_pending_earnings(creator_id):
    """Calculate pending earnings for creator"""
    from models import RevenueShare
    
    pending = db.session.query(db.func.sum(RevenueShare.creator_amount))\
                       .filter_by(creator_id=creator_id, payout_status='pending')\
                       .scalar()
    
    return pending or 0.0

# Admin routes for agent approval
@user_marketplace_bp.route('/admin/pending-agents')
@login_required
def admin_pending_agents():
    """Admin interface for approving agents"""
    
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    pending_agents = AIAgent.query.filter_by(approval_status='pending')\
                                 .order_by(AIAgent.submission_date.desc()).all()
    
    return render_template('user_marketplace/admin_pending.html',
                         pending_agents=pending_agents)

@user_marketplace_bp.route('/admin/agent/<int:agent_id>/approve', methods=['POST'])
@login_required
def admin_approve_agent(agent_id):
    """Approve pending agent"""
    
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    agent = AIAgent.query.get_or_404(agent_id)
    
    try:
        agent.approval_status = 'approved'
        agent.is_active = True
        
        # Optional: Set as featured
        if request.form.get('featured'):
            agent.is_featured = True
        
        db.session.commit()
        
        # Notify creator (implement email notification)
        logging.info(f"Agent approved: {agent.name} (ID: {agent.id})")
        
        return jsonify({'success': True, 'message': 'Agent approved successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_marketplace_bp.route('/admin/agent/<int:agent_id>/reject', methods=['POST'])
@login_required
def admin_reject_agent(agent_id):
    """Reject pending agent"""
    
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    agent = AIAgent.query.get_or_404(agent_id)
    rejection_reason = request.form.get('reason', 'Does not meet quality standards')
    
    try:
        agent.approval_status = 'rejected'
        agent.is_active = False
        
        # Store rejection reason (you might want to add this field to the model)
        # agent.rejection_reason = rejection_reason
        
        db.session.commit()
        
        logging.info(f"Agent rejected: {agent.name} (ID: {agent.id}) - Reason: {rejection_reason}")
        
        return jsonify({'success': True, 'message': 'Agent rejected'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500