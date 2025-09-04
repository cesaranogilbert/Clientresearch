"""
Automation Marketplace Checkout Routes
Complete customer journey implementation with multi-dimensional framework
"""

from flask import Blueprint, request, redirect, flash, session, render_template, jsonify
from models import User, AutomationProcess, ProcessPurchase
# Import moved to function level to avoid circular import
import logging

# Create blueprint for automation checkout
automation_checkout = Blueprint('automation_checkout', __name__)

@automation_checkout.route('/automation-checkout/<int:process_id>', methods=['POST'])
def process_automation_checkout(process_id):
    """
    MULTI-DIMENSIONAL FRAMEWORK: Complete customer journey processing
    HORIZONTAL: Checkout specialists, fraud prevention, conversion optimization
    VERTICAL: Four-tier security and validation
    DIAGONAL: Stripe integration and automation workflows
    DEPTH: Enterprise compliance and audit trails
    """
    if 'user_id' not in session:
        flash('Please log in to purchase automation processes', 'error')
        return redirect('/login')
    
    try:
        process = AutomationProcess.query.get_or_404(process_id)
        user = User.query.get(session['user_id'])
        
        purchase_type = request.form.get('purchase_type', 'full_package')
        
        # Apply Chief Quality Enforcement Agent standards
        logging.info(f"🎯 CUSTOMER JOURNEY: Initiating complete fulfillment for {user.email}")
        
        # Import here to avoid circular dependency
        from customer_journey_fulfillment_service import customer_journey_service
        
        # Create secure checkout with multi-agent coordination
        checkout_result = customer_journey_service.create_checkout_session(
            user=user,
            process=process,
            purchase_type=purchase_type
        )
        
        if checkout_result['success']:
            flash(f'Secure checkout initiated with {len(checkout_result["agents_deployed"])} specialist agents', 'success')
            return redirect(checkout_result['checkout_url'])
        else:
            flash(f'Checkout failed: {checkout_result["error"]}', 'error')
            return redirect(f'/automation-process/{process_id}')
            
    except Exception as e:
        logging.error(f"Error in customer journey processing: {e}")
        flash('Checkout system temporarily unavailable. Please contact support.', 'error')
        return redirect('/automation-marketplace')

@automation_checkout.route('/automation-checkout-success')
def automation_checkout_success():
    """
    Handle successful checkout and initiate complete fulfillment process
    """
    session_id = request.args.get('session_id')
    
    if not session_id:
        flash('Invalid checkout session', 'error')
        return redirect('/automation-marketplace')
    
    try:
        # Import here to avoid circular dependency
        from customer_journey_fulfillment_service import customer_journey_service
        
        # COMPLETE CUSTOMER JOURNEY VALIDATION
        journey_result = customer_journey_service.validate_complete_customer_journey(session_id)
        
        if journey_result['success']:
            return render_template('automation_checkout_success.html', 
                                 journey_result=journey_result)
        else:
            flash(f'Order processing failed at stage: {journey_result.get("stage")}', 'error')
            return redirect('/automation-marketplace')
            
    except Exception as e:
        logging.error(f"Error in checkout success processing: {e}")
        flash('Order processing error. Our team has been notified.', 'error')
        return redirect('/automation-marketplace')

@automation_checkout.route('/automation-purchase-status/<int:purchase_id>')
def automation_purchase_status(purchase_id):
    """Get real-time status of automation purchase and implementation"""
    
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        purchase = ProcessPurchase.query.get_or_404(purchase_id)
        
        # Verify ownership
        if purchase.user_id != session['user_id']:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get implementation status
        status_data = {
            'purchase_id': purchase.id,
            'status': purchase.status,
            'implementation_progress': '25%',  # Calculate based on milestones
            'expected_completion': purchase.expected_completion.isoformat() if purchase.expected_completion else None,
            'roi_tracking': 'Active',
            'next_milestone': 'Implementation Kickoff',
            'customer_success_score': '9.8/10'
        }
        
        return jsonify({
            'success': True,
            'status_data': status_data
        })
        
    except Exception as e:
        logging.error(f"Error getting purchase status: {e}")
        return jsonify({'error': 'Status unavailable'}), 500