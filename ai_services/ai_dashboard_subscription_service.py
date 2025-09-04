"""
AI Dashboard Subscription Service
Subscription management and billing integration for dashboard enterprise plans
"""

import json
import logging
import stripe
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app import db
from ai_dashboard_models import DashboardSubscription, Dashboard, DashboardInsight, ExecutiveBriefing
from models import User

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class DashboardSubscriptionService:
    """Service for managing dashboard subscriptions and billing"""
    
    def __init__(self):
        self.plans = {
            'starter': {
                'name': 'Starter',
                'monthly_price': 199,
                'yearly_price': 1990,  # 2 months free
                'max_dashboards': 5,
                'max_widgets_per_dashboard': 15,
                'max_ai_insights_per_month': 100,
                'max_executive_briefings_per_month': 10,
                'features': [
                    'AI-powered insights',
                    'Executive briefings',
                    'Custom dashboards',
                    'Email support',
                    'Real-time KPI monitoring'
                ]
            },
            'professional': {
                'name': 'Professional',
                'monthly_price': 499,
                'yearly_price': 4990,  # 2 months free
                'max_dashboards': 20,
                'max_widgets_per_dashboard': 50,
                'max_ai_insights_per_month': 500,
                'max_executive_briefings_per_month': 50,
                'features': [
                    'Everything in Starter',
                    'Advanced AI agents',
                    'Custom templates',
                    'API access',
                    'Priority support',
                    'White-label options'
                ]
            },
            'enterprise': {
                'name': 'Enterprise',
                'monthly_price': 999,
                'yearly_price': 9990,  # 2 months free
                'max_dashboards': 100,
                'max_widgets_per_dashboard': 100,
                'max_ai_insights_per_month': 2000,
                'max_executive_briefings_per_month': 200,
                'features': [
                    'Everything in Professional',
                    'Unlimited AI insights',
                    'SSO integration',
                    'Dedicated support',
                    'Custom AI training',
                    'Advanced analytics',
                    'Multi-tenant support'
                ]
            }
        }
    
    def get_user_subscription(self, user_id: int) -> Optional[DashboardSubscription]:
        """Get current subscription for user"""
        
        return DashboardSubscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
    
    def get_subscription_limits(self, user_id: int) -> Dict[str, int]:
        """Get subscription limits for a user"""
        
        subscription = self.get_user_subscription(user_id)
        
        if not subscription:
            # Free tier limits
            return {
                'max_dashboards': 2,
                'max_widgets_per_dashboard': 10,
                'max_ai_insights_per_month': 20,
                'max_executive_briefings_per_month': 2
            }
        
        return {
            'max_dashboards': subscription.max_dashboards,
            'max_widgets_per_dashboard': subscription.max_widgets_per_dashboard,
            'max_ai_insights_per_month': subscription.max_ai_insights_per_month,
            'max_executive_briefings_per_month': subscription.max_executive_briefings_per_month
        }
    
    def get_current_usage(self, user_id: int) -> Dict[str, int]:
        """Get current usage statistics for user"""
        
        # Current month start
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        return {
            'dashboards': Dashboard.query.filter_by(user_id=user_id, is_active=True).count(),
            'insights_this_month': DashboardInsight.query.join(Dashboard).filter(
                Dashboard.user_id == user_id,
                DashboardInsight.created_at >= current_month_start
            ).count(),
            'briefings_this_month': ExecutiveBriefing.query.filter(
                ExecutiveBriefing.user_id == user_id,
                ExecutiveBriefing.created_at >= current_month_start
            ).count()
        }
    
    def check_usage_limits(self, user_id: int, action: str) -> Dict[str, Any]:
        """Check if user can perform action based on subscription limits"""
        
        limits = self.get_subscription_limits(user_id)
        usage = self.get_current_usage(user_id)
        
        if action == 'create_dashboard':
            if usage['dashboards'] >= limits['max_dashboards']:
                return {
                    'allowed': False,
                    'reason': f"Dashboard limit reached ({limits['max_dashboards']})",
                    'upgrade_required': True
                }
        
        elif action == 'generate_insights':
            if usage['insights_this_month'] >= limits['max_ai_insights_per_month']:
                return {
                    'allowed': False,
                    'reason': f"Monthly AI insights limit reached ({limits['max_ai_insights_per_month']})",
                    'upgrade_required': True
                }
        
        elif action == 'generate_briefing':
            if usage['briefings_this_month'] >= limits['max_executive_briefings_per_month']:
                return {
                    'allowed': False,
                    'reason': f"Monthly executive briefings limit reached ({limits['max_executive_briefings_per_month']})",
                    'upgrade_required': True
                }
        
        return {'allowed': True}
    
    def create_stripe_checkout_session(self, user_id: int, plan: str, billing_cycle: str = 'monthly') -> Dict[str, Any]:
        """Create Stripe checkout session for subscription"""
        
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            if plan not in self.plans:
                raise ValueError("Invalid plan")
            
            plan_config = self.plans[plan]
            
            # Determine price based on billing cycle
            if billing_cycle == 'yearly':
                price = plan_config['yearly_price']
                interval = 'year'
            else:
                price = plan_config['monthly_price']
                interval = 'month'
            
            # Create or get Stripe customer
            stripe_customer = self._get_or_create_stripe_customer(user)
            
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer=stripe_customer.id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'4UAI Dashboard {plan_config["name"]} Plan',
                            'description': f'AI-powered business dashboard with {plan_config["max_dashboards"]} dashboards',
                        },
                        'unit_amount': price * 100,  # Convert to cents
                        'recurring': {
                            'interval': interval,
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f'{os.getenv("REPLIT_DEV_DOMAIN", "")}/ai-dashboard/subscription?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{os.getenv("REPLIT_DEV_DOMAIN", "")}/ai-dashboard/subscription',
                metadata={
                    'user_id': str(user_id),
                    'plan': plan,
                    'billing_cycle': billing_cycle
                }
            )
            
            return {
                'success': True,
                'checkout_url': session.url,
                'session_id': session.id
            }
            
        except Exception as e:
            logging.error(f"Error creating checkout session: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_or_create_stripe_customer(self, user: User) -> Any:
        """Get existing Stripe customer or create new one"""
        
        # Check if user already has Stripe customer ID
        if hasattr(user, 'stripe_customer_id') and user.stripe_customer_id:
            try:
                return stripe.Customer.retrieve(user.stripe_customer_id)
            except stripe.error.InvalidRequestError:
                # Customer doesn't exist, create new one
                pass
        
        # Create new Stripe customer
        customer = stripe.Customer.create(
            email=user.email,
            name=user.username,
            metadata={
                'user_id': str(user.id),
                'platform': '4uai_dashboards'
            }
        )
        
        # Save customer ID to user (would need to add field to User model)
        # user.stripe_customer_id = customer.id
        # db.session.commit()
        
        return customer
    
    def handle_stripe_webhook(self, event: Dict) -> Dict[str, Any]:
        """Handle Stripe webhook events"""
        
        try:
            event_type = event['type']
            
            if event_type == 'checkout.session.completed':
                return self._handle_checkout_completed(event['data']['object'])
            
            elif event_type == 'invoice.payment_succeeded':
                return self._handle_payment_succeeded(event['data']['object'])
            
            elif event_type == 'invoice.payment_failed':
                return self._handle_payment_failed(event['data']['object'])
            
            elif event_type == 'customer.subscription.deleted':
                return self._handle_subscription_cancelled(event['data']['object'])
            
            return {'success': True, 'message': 'Event processed'}
            
        except Exception as e:
            logging.error(f"Error handling Stripe webhook: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_checkout_completed(self, session: Dict) -> Dict[str, Any]:
        """Handle successful checkout completion"""
        
        try:
            user_id = int(session['metadata']['user_id'])
            plan = session['metadata']['plan']
            billing_cycle = session['metadata']['billing_cycle']
            
            # Get subscription from Stripe
            subscription = stripe.Subscription.retrieve(session['subscription'])
            
            # Create or update subscription record
            self._create_subscription_record(user_id, plan, billing_cycle, subscription)
            
            return {'success': True, 'message': 'Subscription created'}
            
        except Exception as e:
            logging.error(f"Error handling checkout completion: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _create_subscription_record(self, user_id: int, plan: str, billing_cycle: str, stripe_subscription: Any):
        """Create subscription record in database"""
        
        try:
            plan_config = self.plans[plan]
            
            # Cancel existing subscription if any
            existing = DashboardSubscription.query.filter_by(
                user_id=user_id,
                status='active'
            ).first()
            
            if existing:
                existing.status = 'cancelled'
            
            # Create new subscription
            subscription = DashboardSubscription()
            subscription.user_id = user_id
            subscription.plan_name = plan
            subscription.billing_cycle = billing_cycle
            subscription.max_dashboards = plan_config['max_dashboards']
            subscription.max_widgets_per_dashboard = plan_config['max_widgets_per_dashboard']
            subscription.max_ai_insights_per_month = plan_config['max_ai_insights_per_month']
            subscription.max_executive_briefings_per_month = plan_config['max_executive_briefings_per_month']
            subscription.monthly_price = plan_config['yearly_price'] / 12 if billing_cycle == 'yearly' else plan_config['monthly_price']
            subscription.stripe_subscription_id = stripe_subscription.id
            subscription.status = 'active'
            
            db.session.add(subscription)
            db.session.commit()
            
            logging.info(f"Created subscription for user {user_id}: {plan} ({billing_cycle})")
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating subscription record: {str(e)}")
            raise
    
    def _handle_payment_succeeded(self, invoice: Dict) -> Dict[str, Any]:
        """Handle successful payment"""
        
        try:
            subscription_id = invoice['subscription']
            
            # Find subscription by Stripe ID
            subscription = DashboardSubscription.query.filter_by(
                stripe_subscription_id=subscription_id
            ).first()
            
            if subscription:
                # Reset monthly usage counters
                subscription.current_month_ai_insights = 0
                subscription.current_month_briefings = 0
                db.session.commit()
                
                logging.info(f"Payment succeeded for subscription {subscription.id}")
            
            return {'success': True, 'message': 'Payment processed'}
            
        except Exception as e:
            logging.error(f"Error handling payment success: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_payment_failed(self, invoice: Dict) -> Dict[str, Any]:
        """Handle failed payment"""
        
        try:
            subscription_id = invoice['subscription']
            
            # Find subscription by Stripe ID
            subscription = DashboardSubscription.query.filter_by(
                stripe_subscription_id=subscription_id
            ).first()
            
            if subscription:
                # Mark subscription as suspended
                subscription.status = 'suspended'
                db.session.commit()
                
                logging.warning(f"Payment failed for subscription {subscription.id}")
            
            return {'success': True, 'message': 'Payment failure processed'}
            
        except Exception as e:
            logging.error(f"Error handling payment failure: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_subscription_cancelled(self, stripe_subscription: Dict) -> Dict[str, Any]:
        """Handle subscription cancellation"""
        
        try:
            subscription_id = stripe_subscription['id']
            
            # Find subscription by Stripe ID
            subscription = DashboardSubscription.query.filter_by(
                stripe_subscription_id=subscription_id
            ).first()
            
            if subscription:
                subscription.status = 'cancelled'
                db.session.commit()
                
                logging.info(f"Subscription cancelled: {subscription.id}")
            
            return {'success': True, 'message': 'Subscription cancellation processed'}
            
        except Exception as e:
            logging.error(f"Error handling subscription cancellation: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def cancel_subscription(self, user_id: int) -> Dict[str, Any]:
        """Cancel user's subscription"""
        
        try:
            subscription = self.get_user_subscription(user_id)
            
            if not subscription:
                return {'success': False, 'error': 'No active subscription found'}
            
            # Cancel in Stripe
            stripe.Subscription.delete(subscription.stripe_subscription_id)
            
            # Update local record
            subscription.status = 'cancelled'
            db.session.commit()
            
            return {'success': True, 'message': 'Subscription cancelled successfully'}
            
        except Exception as e:
            logging.error(f"Error cancelling subscription: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_available_plans(self) -> List[Dict]:
        """Get list of available subscription plans"""
        
        return [
            {
                'id': plan_id,
                'name': plan_config['name'],
                'monthly_price': plan_config['monthly_price'],
                'yearly_price': plan_config['yearly_price'],
                'features': plan_config['features'],
                'limits': {
                    'dashboards': plan_config['max_dashboards'],
                    'widgets': plan_config['max_widgets_per_dashboard'],
                    'insights': plan_config['max_ai_insights_per_month'],
                    'briefings': plan_config['max_executive_briefings_per_month']
                }
            }
            for plan_id, plan_config in self.plans.items()
        ]

# Global subscription service instance
subscription_service = DashboardSubscriptionService()