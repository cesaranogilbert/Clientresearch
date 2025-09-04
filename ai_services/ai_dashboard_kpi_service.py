"""
AI Dashboard KPI Monitoring Service
Real-time KPI monitoring, alerting, and data integration
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app import db
from ai_dashboard_models import (
    KPIDefinition, KPIValue, DashboardAlert, Dashboard, DashboardWidget
)

class KPIMonitoringService:
    """Service for real-time KPI monitoring and alerting"""
    
    def __init__(self):
        self.alert_handlers = {
            'email': self._send_email_alert,
            'webhook': self._send_webhook_alert,
            'slack': self._send_slack_alert
        }
    
    def calculate_kpi_value(self, kpi_definition_id: int, period_start: datetime, period_end: datetime) -> Optional[float]:
        """Calculate KPI value for given time period"""
        
        try:
            kpi_def = KPIDefinition.query.get(kpi_definition_id)
            if not kpi_def:
                return None
            
            calculation_method = kpi_def.calculation_method
            config = json.loads(kpi_def.calculation_config) if kpi_def.calculation_config else {}
            
            if calculation_method == 'formula':
                return self._calculate_formula_kpi(config, period_start, period_end)
            elif calculation_method == 'query':
                return self._calculate_query_kpi(config, period_start, period_end)
            elif calculation_method == 'api':
                return self._calculate_api_kpi(config, period_start, period_end)
            elif calculation_method == 'ai_generated':
                return self._calculate_ai_kpi(config, period_start, period_end)
            else:
                # Return sample data for demo
                return self._generate_sample_kpi_value(kpi_def)
                
        except Exception as e:
            logging.error(f"Error calculating KPI value: {str(e)}")
            return None
    
    def _calculate_formula_kpi(self, config: Dict, period_start: datetime, period_end: datetime) -> float:
        """Calculate KPI using formula-based method"""
        
        # Example: Revenue Growth Rate = (Current Period Revenue - Previous Period Revenue) / Previous Period Revenue
        formula = config.get('formula', 'revenue_current - revenue_previous')
        
        # This would integrate with your actual data sources
        # For demo purposes, return calculated value
        if 'revenue' in formula:
            current_revenue = 125000  # Would come from actual data source
            previous_revenue = 110000
            return ((current_revenue - previous_revenue) / previous_revenue) * 100
        
        return 15.5  # Sample value
    
    def _calculate_query_kpi(self, config: Dict, period_start: datetime, period_end: datetime) -> float:
        """Calculate KPI using database query"""
        
        query = config.get('query', '')
        
        # Example query execution (would use actual database)
        if 'revenue' in query.lower():
            # SELECT SUM(amount) FROM orders WHERE created_at BETWEEN ? AND ?
            return 125000.00
        elif 'customers' in query.lower():
            # SELECT COUNT(DISTINCT customer_id) FROM orders WHERE created_at BETWEEN ? AND ?
            return 2340
        
        return 100.0  # Sample value
    
    def _calculate_api_kpi(self, config: Dict, period_start: datetime, period_end: datetime) -> float:
        """Calculate KPI using external API"""
        
        api_endpoint = config.get('endpoint', '')
        
        # Example API integration (would make actual HTTP request)
        if 'stripe' in api_endpoint:
            # Stripe revenue data
            return 125000.00
        elif 'analytics' in api_endpoint:
            # Google Analytics data
            return 45000
        
        return 75.0  # Sample value
    
    def _calculate_ai_kpi(self, config: Dict, period_start: datetime, period_end: datetime) -> float:
        """Calculate KPI using AI prediction/analysis"""
        
        # This would use AI agents to predict or analyze KPI values
        model_type = config.get('model_type', 'prediction')
        
        if model_type == 'prediction':
            # AI-predicted revenue based on trends
            return 135000.00
        elif model_type == 'sentiment':
            # AI sentiment analysis score
            return 0.75
        
        return 85.0  # Sample value
    
    def _generate_sample_kpi_value(self, kpi_def: KPIDefinition) -> float:
        """Generate realistic sample KPI values for demo"""
        
        import random
        
        kpi_name = kpi_def.name.lower()
        
        if 'revenue' in kpi_name:
            return random.uniform(100000, 150000)
        elif 'growth' in kpi_name or 'rate' in kpi_name:
            return random.uniform(10, 25)
        elif 'customers' in kpi_name or 'users' in kpi_name:
            return random.uniform(2000, 3000)
        elif 'conversion' in kpi_name:
            return random.uniform(0.10, 0.20)
        elif 'margin' in kpi_name:
            return random.uniform(0.20, 0.35)
        elif 'cost' in kpi_name:
            return random.uniform(50, 200)
        else:
            return random.uniform(50, 100)
    
    def update_kpi_values(self, dashboard_id: int) -> Dict[str, Any]:
        """Update all KPI values for a dashboard"""
        
        try:
            # Get KPI widgets for dashboard
            kpi_widgets = DashboardWidget.query.filter_by(
                dashboard_id=dashboard_id,
                widget_type='kpi'
            ).all()
            
            results = {
                'updated_count': 0,
                'errors': [],
                'values': {}
            }
            
            for widget in kpi_widgets:
                try:
                    # For demo, create a KPI definition if it doesn't exist
                    kpi_def = self._ensure_kpi_definition(widget)
                    
                    # Calculate current value
                    period_end = datetime.utcnow()
                    period_start = period_end - timedelta(days=1)
                    
                    current_value = self.calculate_kpi_value(kpi_def.id, period_start, period_end)
                    
                    if current_value is not None:
                        # Get previous value for trend calculation
                        previous_value = self._get_previous_kpi_value(kpi_def.id)
                        
                        # Create KPI value record
                        kpi_value = KPIValue()
                        kpi_value.kpi_definition_id = kpi_def.id
                        kpi_value.value = current_value
                        kpi_value.previous_value = previous_value
                        kpi_value.period_start = period_start
                        kpi_value.period_end = period_end
                        kpi_value.period_type = 'day'
                        
                        # Calculate status and trend
                        status_info = self._calculate_kpi_status(kpi_def, current_value, previous_value)
                        kpi_value.status = status_info['status']
                        kpi_value.trend = status_info['trend']
                        kpi_value.percentage_change = status_info['percentage_change']
                        
                        kpi_value.data_source = 'ai_dashboard_service'
                        kpi_value.confidence_score = 0.85
                        kpi_value.data_quality = 'high'
                        
                        db.session.add(kpi_value)
                        
                        # Update widget cached data
                        widget.cached_data = json.dumps({
                            'value': current_value,
                            'previous_value': previous_value,
                            'trend': status_info['trend'],
                            'percentage_change': status_info['percentage_change'],
                            'status': status_info['status'],
                            'unit': kpi_def.unit_symbol or '',
                            'format': kpi_def.unit_type or 'number'
                        })
                        widget.last_data_refresh = datetime.utcnow()
                        
                        results['values'][widget.widget_id] = {
                            'value': current_value,
                            'trend': status_info['trend'],
                            'change': status_info['percentage_change']
                        }
                        results['updated_count'] += 1
                        
                        # Check for alerts
                        self._check_kpi_alerts(kpi_def, current_value)
                        
                except Exception as e:
                    results['errors'].append(f"Widget {widget.id}: {str(e)}")
                    logging.error(f"Error updating KPI widget {widget.id}: {str(e)}")
            
            db.session.commit()
            
            return results
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating KPI values: {str(e)}")
            return {'updated_count': 0, 'errors': [str(e)], 'values': {}}
    
    def _ensure_kpi_definition(self, widget: DashboardWidget) -> KPIDefinition:
        """Ensure KPI definition exists for widget"""
        
        # Try to find existing KPI definition
        config = json.loads(widget.configuration) if widget.configuration else {}
        kpi_name = config.get('kpi_name', widget.title or 'Unnamed KPI')
        
        kpi_def = KPIDefinition.query.filter_by(
            name=kpi_name,
            user_id=widget.dashboard.user_id
        ).first()
        
        if not kpi_def:
            # Create new KPI definition
            kpi_def = KPIDefinition()
            kpi_def.user_id = widget.dashboard.user_id
            kpi_def.name = kpi_name
            kpi_def.description = f"KPI for {widget.title}"
            kpi_def.category = widget.dashboard.category or 'general'
            kpi_def.calculation_method = config.get('calculation_method', 'formula')
            kpi_def.calculation_config = json.dumps(config.get('calculation_config', {}))
            kpi_def.target_value = config.get('target', 100.0)
            kpi_def.target_period = 'monthly'
            kpi_def.warning_threshold = config.get('warning_threshold', 0.8)
            kpi_def.critical_threshold = config.get('critical_threshold', 0.6)
            kpi_def.unit_type = config.get('value_format', 'number')
            kpi_def.unit_symbol = config.get('unit_symbol', '')
            kpi_def.is_active = True
            
            db.session.add(kpi_def)
            db.session.flush()  # Get ID
        
        return kpi_def
    
    def _get_previous_kpi_value(self, kpi_definition_id: int) -> Optional[float]:
        """Get the most recent previous KPI value"""
        
        previous_value = KPIValue.query.filter_by(
            kpi_definition_id=kpi_definition_id
        ).order_by(KPIValue.created_at.desc()).first()
        
        return previous_value.value if previous_value else None
    
    def _calculate_kpi_status(self, kpi_def: KPIDefinition, current_value: float, previous_value: Optional[float]) -> Dict[str, Any]:
        """Calculate KPI status, trend, and percentage change"""
        
        # Calculate percentage change
        percentage_change = 0.0
        if previous_value and previous_value != 0:
            percentage_change = ((current_value - previous_value) / previous_value) * 100
        
        # Determine trend
        if previous_value is None:
            trend = 'flat'
        elif current_value > previous_value:
            trend = 'up'
        elif current_value < previous_value:
            trend = 'down'
        else:
            trend = 'flat'
        
        # Determine status based on target and thresholds
        status = 'excellent'
        
        if kpi_def.target_value:
            target_ratio = current_value / kpi_def.target_value
            
            if target_ratio >= 1.0:
                status = 'excellent'
            elif target_ratio >= (kpi_def.warning_threshold or 0.8):
                status = 'good'
            elif target_ratio >= (kpi_def.critical_threshold or 0.6):
                status = 'warning'
            else:
                status = 'critical'
        
        return {
            'status': status,
            'trend': trend,
            'percentage_change': round(percentage_change, 2)
        }
    
    def _check_kpi_alerts(self, kpi_def: KPIDefinition, current_value: float):
        """Check if KPI value triggers any alerts"""
        
        alerts = DashboardAlert.query.filter_by(
            kpi_definition_id=kpi_def.id,
            is_active=True
        ).all()
        
        for alert in alerts:
            try:
                should_trigger = self._evaluate_alert_condition(alert, current_value)
                
                if should_trigger:
                    # Check cooldown period
                    if self._is_alert_in_cooldown(alert):
                        continue
                    
                    # Check daily limit
                    if self._has_reached_daily_limit(alert):
                        continue
                    
                    # Trigger alert
                    self._trigger_alert(alert, kpi_def, current_value)
                    
            except Exception as e:
                logging.error(f"Error checking alert {alert.id}: {str(e)}")
    
    def _evaluate_alert_condition(self, alert: DashboardAlert, current_value: float) -> bool:
        """Evaluate if alert condition is met"""
        
        if alert.alert_type == 'threshold':
            threshold = alert.threshold_value
            operator = alert.comparison_operator
            
            if operator == '>':
                return current_value > threshold
            elif operator == '<':
                return current_value < threshold
            elif operator == '>=':
                return current_value >= threshold
            elif operator == '<=':
                return current_value <= threshold
            elif operator == '==':
                return current_value == threshold
            elif operator == '!=':
                return current_value != threshold
        
        return False
    
    def _is_alert_in_cooldown(self, alert: DashboardAlert) -> bool:
        """Check if alert is in cooldown period"""
        
        if not alert.last_triggered:
            return False
        
        cooldown_period = timedelta(minutes=alert.cooldown_minutes or 60)
        return datetime.utcnow() - alert.last_triggered < cooldown_period
    
    def _has_reached_daily_limit(self, alert: DashboardAlert) -> bool:
        """Check if alert has reached daily trigger limit"""
        
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Count today's triggers (would need AlertTrigger model to track this properly)
        # For now, use simple trigger count
        
        max_daily = alert.max_alerts_per_day or 10
        return (alert.trigger_count or 0) >= max_daily
    
    def _trigger_alert(self, alert: DashboardAlert, kpi_def: KPIDefinition, current_value: float):
        """Trigger an alert notification"""
        
        try:
            # Update alert trigger info
            alert.last_triggered = datetime.utcnow()
            alert.trigger_count = (alert.trigger_count or 0) + 1
            
            # Get notification methods
            notification_methods = json.loads(alert.notification_methods) if alert.notification_methods else ['email']
            
            # Prepare alert message
            alert_message = {
                'alert_name': alert.alert_name,
                'kpi_name': kpi_def.name,
                'current_value': current_value,
                'threshold': alert.threshold_value,
                'unit': kpi_def.unit_symbol or '',
                'dashboard_id': alert.dashboard_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Send notifications
            for method in notification_methods:
                if method in self.alert_handlers:
                    try:
                        self.alert_handlers[method](alert, alert_message)
                    except Exception as e:
                        logging.error(f"Error sending {method} alert: {str(e)}")
            
            db.session.commit()
            
        except Exception as e:
            logging.error(f"Error triggering alert: {str(e)}")
    
    def _send_email_alert(self, alert: DashboardAlert, message: Dict):
        """Send email alert notification"""
        
        # This would integrate with your email service
        logging.info(f"EMAIL ALERT: {message['alert_name']} - {message['kpi_name']} = {message['current_value']}")
    
    def _send_webhook_alert(self, alert: DashboardAlert, message: Dict):
        """Send webhook alert notification"""
        
        # This would make HTTP POST to webhook URL
        logging.info(f"WEBHOOK ALERT: {message['alert_name']} - {message['kpi_name']} = {message['current_value']}")
    
    def _send_slack_alert(self, alert: DashboardAlert, message: Dict):
        """Send Slack alert notification"""
        
        # This would send message to Slack channel
        logging.info(f"SLACK ALERT: {message['alert_name']} - {message['kpi_name']} = {message['current_value']}")
    
    def get_kpi_history(self, kpi_definition_id: int, days: int = 30) -> List[Dict]:
        """Get KPI value history for charting"""
        
        since_date = datetime.utcnow() - timedelta(days=days)
        
        values = KPIValue.query.filter(
            KPIValue.kpi_definition_id == kpi_definition_id,
            KPIValue.created_at >= since_date
        ).order_by(KPIValue.created_at.asc()).all()
        
        return [
            {
                'date': value.period_end.isoformat(),
                'value': value.value,
                'trend': value.trend,
                'status': value.status
            }
            for value in values
        ]

# Global KPI monitoring service instance
kpi_monitoring_service = KPIMonitoringService()