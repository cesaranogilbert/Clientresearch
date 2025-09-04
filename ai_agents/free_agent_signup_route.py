# Free Agent Signup Route with Enhanced Double Opt-in Email
from flask import request, jsonify, session
from app import app, db
from models import User
import logging
import os
import secrets
from datetime import datetime, timedelta

# Store pending signups temporarily (in production, use Redis or database)
pending_signups = {}

@app.route('/free_agent_signup', methods=['POST'])
def free_agent_signup():
    """Handle free agent signup form submission with double opt-in"""
    try:
        # Get form data
        agent_id = request.form.get('agent_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        company = request.form.get('company', '')
        
        # Basic validation
        if not all([agent_id, first_name, last_name, email]):
            return jsonify({'success': False, 'message': 'All required fields must be filled'})
        
        # Validate email format
        import re
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return jsonify({'success': False, 'message': 'Please enter a valid email address'})
        
        # Get agent details
        from agent_service import get_agent_by_id
        agent = get_agent_by_id(int(agent_id))
        if not agent:
            return jsonify({'success': False, 'message': 'Agent not found'})
        
        # Generate confirmation token
        confirmation_token = secrets.token_urlsafe(32)
        
        # Store signup data temporarily
        signup_data = {
            'agent_id': agent_id,
            'agent_name': agent['name'],
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'company': company,
            'signup_date': datetime.utcnow(),
            'status': 'pending_confirmation',
            'expires_at': datetime.utcnow() + timedelta(hours=24)
        }
        pending_signups[confirmation_token] = signup_data
        
        # Send confirmation email
        success = send_confirmation_email(email, first_name, agent['name'], confirmation_token)
        
        if success:
            logging.info(f"Free agent signup - confirmation email sent: {first_name} {last_name} ({email}) for agent {agent['name']}")
            return jsonify({
                'success': True, 
                'message': f'Thank you {first_name}! We sent a confirmation link to {email}. Please check your inbox and click the link to receive your free AI agent.'
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to send confirmation email. Please try again.'})
        
    except Exception as e:
        logging.error(f"Error processing free agent signup: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'})

@app.route('/confirm_free_agent/<token>')
def confirm_free_agent(token):
    """Handle email confirmation and deliver the free agent"""
    try:
        # Check if token exists and is valid
        if token not in pending_signups:
            return '''
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #dc3545;">❌ Invalid or Expired Link</h2>
                <p>This confirmation link is invalid or has expired.</p>
                <p><a href="/" style="color: #0d6efd;">Return to 4UAI</a></p>
            </body></html>
            '''
        
        signup_data = pending_signups[token]
        
        # Check if expired
        if datetime.utcnow() > signup_data['expires_at']:
            del pending_signups[token]
            return '''
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #dc3545;">⏰ Link Expired</h2>
                <p>This confirmation link has expired. Please sign up again.</p>
                <p><a href="/agents" style="color: #0d6efd;">Browse AI Agents</a></p>
            </body></html>
            '''
        
        # Mark as confirmed and send the agent
        signup_data['status'] = 'confirmed'
        signup_data['confirmed_at'] = datetime.utcnow()
        
        # Send the actual free agent email
        agent_delivered = send_free_agent_email(signup_data)
        
        if agent_delivered:
            # Clean up token
            del pending_signups[token]
            
            # Log successful delivery
            logging.info(f"Free agent delivered: {signup_data['agent_name']} to {signup_data['email']}")
            
            return f'''
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f8f9fa;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2 style="color: #198754;">🎉 Confirmation Successful!</h2>
                    <p style="font-size: 18px;">Thank you {signup_data['first_name']}!</p>
                    <p>Your free AI agent "<strong>{signup_data['agent_name']}</strong>" has been delivered to your email inbox.</p>
                    <p style="color: #6c757d;">Check your email for access instructions and documentation.</p>
                    <br>
                    <a href="/agents" style="background: #0d6efd; color: white; text-decoration: none; padding: 12px 24px; border-radius: 5px; display: inline-block;">Browse More AI Agents</a>
                    <br><br>
                    <p style="font-size: 14px; color: #6c757d;">- The 4UAI Team</p>
                </div>
            </body></html>
            '''
        else:
            return '''
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #ffc107;">⚠️ Delivery Issue</h2>
                <p>Email confirmed but agent delivery failed. Our team will manually send your agent within 24 hours.</p>
                <p><a href="/" style="color: #0d6efd;">Return to 4UAI</a></p>
            </body></html>
            '''
        
    except Exception as e:
        logging.error(f"Error confirming free agent: {e}")
        return '''
        <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #dc3545;">❌ Error</h2>
            <p>An error occurred during confirmation. Please contact support.</p>
            <p><a href="/" style="color: #0d6efd;">Return to 4UAI</a></p>
        </body></html>
        '''

def send_confirmation_email(email, first_name, agent_name, token):
    """Send double opt-in confirmation email"""
    try:
        # Build confirmation URL
        base_url = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
        if not base_url.startswith('http'):
            base_url = f'https://{base_url}' if 'replit' in base_url else f'http://{base_url}'
        
        confirmation_url = f'{base_url}/confirm_free_agent/{token}'
        
        email_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0;">🤖 4UAI - Confirm Your Free AI Agent</h1>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2 style="color: #333;">Hi {first_name}! 👋</h2>
                    
                    <p>Thank you for requesting the <strong>"{agent_name}"</strong> AI agent!</p>
                    
                    <p>To complete your free download and receive your AI agent, please confirm your email address by clicking the button below:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{confirmation_url}" 
                           style="background: #28a745; color: white; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-weight: bold; display: inline-block; font-size: 16px;">
                            ✅ Confirm Email & Get My Free AI Agent
                        </a>
                    </div>
                    
                    <p style="color: #666; font-size: 14px;">
                        <strong>What happens next?</strong><br>
                        1. Click the confirmation button above<br>
                        2. We'll instantly deliver your free AI agent to this email<br>
                        3. Start using your AI agent immediately!
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="color: #666; font-size: 12px;">
                        This link expires in 24 hours. If you didn't request this, you can safely ignore this email.<br><br>
                        
                        Having trouble with the button? Copy and paste this link into your browser:<br>
                        <a href="{confirmation_url}" style="color: #0066cc; word-break: break-all;">{confirmation_url}</a>
                    </p>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #999; font-size: 12px;">
                            © 2025 4UAI - Just For You AI Marketplace<br>
                            Delivering enterprise-grade AI solutions worldwide
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        
        # In production, you would use a proper email service here
        # For now, we'll log the email content and return True
        logging.info(f"CONFIRMATION EMAIL TO: {email}")
        logging.info(f"CONFIRMATION URL: {confirmation_url}")
        logging.info(f"EMAIL CONTENT: {email_content}")
        
        # TODO: Integrate with actual email service (SendGrid, etc.)
        # For demo purposes, return True
        return True
        
    except Exception as e:
        logging.error(f"Error sending confirmation email: {e}")
        return False

def send_free_agent_email(signup_data):
    """Send the actual free agent with instructions"""
    try:
        email_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0;">🎁 Your Free AI Agent Has Arrived!</h1>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2 style="color: #333;">Congratulations {signup_data['first_name']}! 🎉</h2>
                    
                    <p>Your free <strong>"{signup_data['agent_name']}"</strong> AI agent is ready to use!</p>
                    
                    <div style="background: white; padding: 20px; border-radius: 5px; border-left: 4px solid #28a745; margin: 20px 0;">
                        <h3 style="color: #28a745; margin: 0 0 10px 0;">🚀 Quick Start Guide:</h3>
                        <ol style="margin: 0; padding-left: 20px;">
                            <li>Access your agent at: <a href="/agents/{signup_data['agent_id']}" style="color: #0066cc;">4UAI Agent Portal</a></li>
                            <li>Log in with this email: {signup_data['email']}</li>
                            <li>Find your agent in "My Agents" section</li>
                            <li>Start your first conversation!</li>
                        </ol>
                    </div>
                    
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="color: #1976d2; margin: 0 0 10px 0;">💡 Pro Tips:</h4>
                        <ul style="margin: 0; padding-left: 20px; color: #666;">
                            <li>Be specific in your prompts for better results</li>
                            <li>Ask follow-up questions to dive deeper</li>
                            <li>Use the agent's specialized capabilities</li>
                            <li>Save useful conversations for future reference</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="/agents" 
                           style="background: #007bff; color: white; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-weight: bold; display: inline-block; font-size: 16px; margin-right: 10px;">
                            🤖 Start Using My Agent
                        </a>
                        <a href="/agents" 
                           style="background: #6c757d; color: white; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-weight: bold; display: inline-block; font-size: 16px;">
                            🔍 Browse More Agents
                        </a>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                    
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px;">
                        <h4 style="color: #856404; margin: 0 0 10px 0;">🔥 Want More? Upgrade to Premium!</h4>
                        <p style="margin: 0; color: #856404;">
                            Get access to 500+ professional AI agents, priority support, and exclusive features with our subscription plans.
                            <a href="/pricing" style="color: #856404; font-weight: bold;">View Pricing →</a>
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #999; font-size: 12px;">
                            Need help? Contact our support team: support@4uai.com<br><br>
                            © 2025 4UAI - Just For You AI Marketplace<br>
                            Delivering enterprise-grade AI solutions worldwide
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        
        # Log the delivery email
        logging.info(f"FREE AGENT DELIVERY EMAIL TO: {signup_data['email']}")
        logging.info(f"AGENT: {signup_data['agent_name']}")
        logging.info(f"DELIVERY EMAIL CONTENT: {email_content}")
        
        # TODO: Integrate with actual email service
        # For demo purposes, return True
        return True
        
    except Exception as e:
        logging.error(f"Error sending free agent email: {e}")
        return False