"""
AI Agent Quality Management Routes
Admin routes for managing agent quality standards and performing quality audits
"""

from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import AIAgent
from agent_quality_service import quality_service
import logging

logger = logging.getLogger(__name__)

@app.route('/admin/agent-quality')
def agent_quality_dashboard():
    """Agent quality management dashboard"""
    try:
        # Get quality metrics report
        quality_report = quality_service.get_quality_metrics_report()
        
        # Get recent non-compliant agents for quick view
        audit_results = quality_service.audit_all_agents()
        recent_issues = audit_results.get('upgrade_candidates', [])[:10]  # Show top 10 issues
        
        return render_template('admin/agent_quality.html', 
                             quality_report=quality_report,
                             recent_issues=recent_issues)
    except Exception as e:
        logger.error(f"Error loading agent quality dashboard: {e}")
        flash('Error loading quality dashboard', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/api/admin/agent-quality/audit')
def api_agent_quality_audit():
    """API endpoint for complete agent quality audit"""
    try:
        audit_results = quality_service.audit_all_agents()
        return jsonify({
            'success': True,
            'audit_results': audit_results
        })
    except Exception as e:
        logger.error(f"Error during agent quality audit: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/agent-quality/upgrade', methods=['POST'])
def api_upgrade_agents():
    """API endpoint to upgrade non-compliant agents"""
    try:
        # First, get audit results
        audit_results = quality_service.audit_all_agents()
        upgrade_candidates = audit_results.get('upgrade_candidates', [])
        
        if not upgrade_candidates:
            return jsonify({
                'success': True,
                'message': 'All agents already meet quality standards',
                'upgrade_results': {'total_upgrades': 0, 'successful_upgrades': 0}
            })
        
        # Perform upgrades
        upgrade_results = quality_service.upgrade_non_compliant_agents(upgrade_candidates)
        
        return jsonify({
            'success': True,
            'message': f"Successfully upgraded {upgrade_results['successful_upgrades']} agents",
            'upgrade_results': upgrade_results
        })
        
    except Exception as e:
        logger.error(f"Error upgrading agents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/agent-quality/metrics')
def api_quality_metrics():
    """API endpoint for quality metrics report"""
    try:
        quality_report = quality_service.get_quality_metrics_report()
        return jsonify({
            'success': True,
            'quality_report': quality_report
        })
    except Exception as e:
        logger.error(f"Error generating quality metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/agent-quality/agent/<int:agent_id>')
def api_agent_quality_details(agent_id):
    """Get quality details for a specific agent"""
    try:
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404
        
        # Check compliance for this specific agent
        compliance_result = quality_service._check_agent_compliance(agent)
        quality_tier = quality_service._determine_quality_tier(agent.expertise_level)
        
        return jsonify({
            'success': True,
            'agent_quality': {
                'agent_id': agent.id,
                'name': agent.name,
                'category': agent.category,
                'expertise_level': agent.expertise_level,
                'practical_projects': agent.practical_projects,
                'collaboration_rate': agent.collaboration_rate,
                'quality_tier': quality_tier,
                'is_compliant': compliance_result['is_compliant'],
                'issues': compliance_result['issues'],
                'recommended_upgrades': compliance_result.get('recommended_upgrades', {}),
                'created_at': agent.created_at.isoformat() if agent.created_at else None,
                'updated_at': agent.updated_at.isoformat() if agent.updated_at else None
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting agent quality details: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/agent-quality/upgrade-single/<int:agent_id>', methods=['POST'])
def api_upgrade_single_agent(agent_id):
    """Upgrade a single agent to meet quality standards"""
    try:
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404
        
        # Check if upgrade is needed
        compliance_result = quality_service._check_agent_compliance(agent)
        if compliance_result['is_compliant']:
            return jsonify({
                'success': True,
                'message': 'Agent already meets quality standards',
                'no_upgrade_needed': True
            })
        
        # Prepare upgrade candidate
        upgrade_candidate = {
            'agent_id': agent.id,
            'name': agent.name,
            'category': agent.category,
            'current_experience': agent.expertise_level,
            'current_projects': agent.practical_projects,
            'current_collaboration': agent.collaboration_rate,
            'issues': compliance_result['issues'],
            'recommended_upgrades': compliance_result['recommended_upgrades']
        }
        
        # Perform upgrade
        upgrade_results = quality_service.upgrade_non_compliant_agents([upgrade_candidate])
        
        if upgrade_results['successful_upgrades'] > 0:
            return jsonify({
                'success': True,
                'message': f"Successfully upgraded agent: {agent.name}",
                'upgrade_details': upgrade_results['upgrade_details'][0] if upgrade_results['upgrade_details'] else {}
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to upgrade agent'
            }), 500
            
    except Exception as e:
        logger.error(f"Error upgrading single agent: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500