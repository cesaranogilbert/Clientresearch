"""
AI Dashboard Service
Core business logic for AI-powered dashboard creation and management
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from openai import OpenAI
import os

from app import db
from ai_dashboard_models import (
    Dashboard, DashboardWidget, KPIDefinition, KPIValue,
    DashboardInsight, DashboardTemplate, ExecutiveBriefing,
    DashboardAlert, DashboardSubscription
)
from models import AIAgent, User

class DashboardAIService:
    """Service for AI-powered dashboard insights and automation"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.default_model = "gpt-4o"  # Latest OpenAI model
    
    def generate_dashboard_insights(self, dashboard_id: int, user_id: int) -> List[Dict]:
        """Generate AI insights for a dashboard using multiple specialized agents"""
        
        try:
            dashboard = Dashboard.query.filter_by(id=dashboard_id, user_id=user_id).first()
            if not dashboard:
                raise ValueError("Dashboard not found")
            
            insights = []
            
            # Get KPI data for the dashboard
            kpi_data = self._get_dashboard_kpi_data(dashboard_id)
            
            # Generate different types of insights using specialized agents
            insights.extend(self._generate_trend_analysis(dashboard, kpi_data))
            insights.extend(self._generate_anomaly_detection(dashboard, kpi_data))
            insights.extend(self._generate_performance_predictions(dashboard, kpi_data))
            insights.extend(self._generate_strategic_recommendations(dashboard, kpi_data))
            
            # Store insights in database
            for insight_data in insights:
                insight = DashboardInsight()
                insight.dashboard_id = dashboard_id
                insight.ai_agent_id = insight_data.get('ai_agent_id', 1)  # Default agent
                insight.insight_type = insight_data.get('type', 'general')
                insight.title = insight_data.get('title', '')
                insight.summary = insight_data.get('summary', '')
                insight.detailed_analysis = insight_data.get('detailed_analysis', '')
                insight.priority_level = insight_data.get('priority', 'medium')
                insight.confidence_score = insight_data.get('confidence', 0.8)
                insight.business_impact = insight_data.get('impact', 'medium')
                insight.recommended_actions = json.dumps(insight_data.get('actions', []))
                insight.ai_model_used = self.default_model
                
                db.session.add(insight)
            
            db.session.commit()
            
            return insights
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error generating dashboard insights: {str(e)}")
            return []
    
    def _generate_trend_analysis(self, dashboard: Dashboard, kpi_data: List[Dict]) -> List[Dict]:
        """Generate trend analysis insights"""
        
        if not kpi_data:
            return []
        
        # Create context for AI analysis
        context = self._create_kpi_context(kpi_data)
        
        prompt = f"""
        As a senior business analyst AI agent with 25+ years of experience, analyze the following KPI trends for {dashboard.name}:
        
        KPI Data:
        {context}
        
        Provide trend analysis insights in the following format:
        1. Key trends identified (positive and negative)
        2. Business implications of these trends
        3. Specific metrics showing concerning patterns
        4. Recommended immediate actions
        
        Focus on actionable insights that executives can act upon immediately.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a senior business intelligence AI agent with expertise in trend analysis and executive reporting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            
            return [{
                'type': 'trend_analysis',
                'title': 'Business Trend Analysis',
                'summary': self._extract_summary(analysis),
                'detailed_analysis': analysis,
                'priority': 'high',
                'confidence': 0.85,
                'impact': 'high',
                'actions': self._extract_actions(analysis),
                'ai_agent_id': 1  # Business Intelligence Agent
            }]
            
        except Exception as e:
            logging.error(f"Error in trend analysis: {str(e)}")
            return []
    
    def _generate_anomaly_detection(self, dashboard: Dashboard, kpi_data: List[Dict]) -> List[Dict]:
        """Generate anomaly detection insights"""
        
        if not kpi_data:
            return []
        
        context = self._create_kpi_context(kpi_data)
        
        prompt = f"""
        As an AI anomaly detection specialist with advanced pattern recognition capabilities, analyze this KPI data for unusual patterns:
        
        KPI Data:
        {context}
        
        Identify:
        1. Statistical anomalies or unusual patterns
        2. Sudden changes or unexpected spikes/drops
        3. Potential root causes for these anomalies
        4. Risk assessment for business impact
        5. Immediate investigation steps needed
        
        Flag only significant anomalies that require attention.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are an AI anomaly detection specialist with expertise in statistical analysis and business intelligence."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=600
            )
            
            analysis = response.choices[0].message.content
            
            # Only create insight if significant anomalies are detected
            if "no significant anomalies" not in analysis.lower():
                return [{
                    'type': 'anomaly_detection',
                    'title': 'Anomaly Alert: Unusual Patterns Detected',
                    'summary': self._extract_summary(analysis),
                    'detailed_analysis': analysis,
                    'priority': 'high',
                    'confidence': 0.9,
                    'impact': 'high',
                    'actions': self._extract_actions(analysis),
                    'ai_agent_id': 2  # Anomaly Detection Agent
                }]
            
            return []
            
        except Exception as e:
            logging.error(f"Error in anomaly detection: {str(e)}")
            return []
    
    def _generate_performance_predictions(self, dashboard: Dashboard, kpi_data: List[Dict]) -> List[Dict]:
        """Generate performance predictions"""
        
        if not kpi_data:
            return []
        
        context = self._create_kpi_context(kpi_data)
        
        prompt = f"""
        As a senior financial forecasting AI agent with predictive analytics expertise, analyze current performance trends and predict future outcomes:
        
        Current KPI Data:
        {context}
        
        Provide:
        1. 30-day performance predictions based on current trends
        2. 90-day outlook with confidence intervals
        3. Key factors that could impact these predictions
        4. Recommended actions to improve predicted outcomes
        5. Risk factors that could negatively impact projections
        
        Focus on actionable predictions that help with strategic planning.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a senior financial forecasting AI agent with expertise in predictive analytics and business planning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=700
            )
            
            analysis = response.choices[0].message.content
            
            return [{
                'type': 'prediction',
                'title': 'Performance Forecast & Predictions',
                'summary': self._extract_summary(analysis),
                'detailed_analysis': analysis,
                'priority': 'medium',
                'confidence': 0.75,
                'impact': 'high',
                'actions': self._extract_actions(analysis),
                'ai_agent_id': 3  # Predictive Analytics Agent
            }]
            
        except Exception as e:
            logging.error(f"Error in performance predictions: {str(e)}")
            return []
    
    def _generate_strategic_recommendations(self, dashboard: Dashboard, kpi_data: List[Dict]) -> List[Dict]:
        """Generate strategic business recommendations"""
        
        if not kpi_data:
            return []
        
        context = self._create_kpi_context(kpi_data)
        
        prompt = f"""
        As a C-suite strategic advisor AI agent with 30+ years of executive experience, analyze this business performance data and provide strategic recommendations:
        
        Performance Data:
        {context}
        
        Dashboard Category: {dashboard.category}
        
        Provide:
        1. Strategic insights based on current performance
        2. High-impact improvement opportunities
        3. Resource allocation recommendations
        4. Competitive positioning analysis
        5. Long-term strategic actions for sustainable growth
        
        Focus on C-level strategic decisions that drive significant business impact.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a C-suite strategic advisor AI agent with expertise in business strategy and executive decision making."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            
            return [{
                'type': 'recommendation',
                'title': 'Strategic Business Recommendations',
                'summary': self._extract_summary(analysis),
                'detailed_analysis': analysis,
                'priority': 'high',
                'confidence': 0.8,
                'impact': 'high',
                'actions': self._extract_actions(analysis),
                'ai_agent_id': 4  # Strategic Advisory Agent
            }]
            
        except Exception as e:
            logging.error(f"Error in strategic recommendations: {str(e)}")
            return []
    
    def generate_executive_briefing(self, dashboard_id: int, user_id: int, briefing_type: str = 'daily') -> Optional[Dict]:
        """Generate executive briefing for a dashboard"""
        
        try:
            dashboard = Dashboard.query.filter_by(id=dashboard_id, user_id=user_id).first()
            if not dashboard:
                return None
            
            # Get recent insights and KPI data
            recent_insights = DashboardInsight.query.filter_by(
                dashboard_id=dashboard_id
            ).filter(
                DashboardInsight.created_at >= datetime.utcnow() - timedelta(days=7)
            ).order_by(DashboardInsight.priority_level.desc()).limit(10).all()
            
            kpi_data = self._get_dashboard_kpi_data(dashboard_id)
            
            # Create briefing context
            insights_summary = "\n".join([
                f"- {insight.title}: {insight.summary}" 
                for insight in recent_insights
            ])
            
            kpi_context = self._create_kpi_context(kpi_data)
            
            prompt = f"""
            As a senior executive assistant AI agent, create a comprehensive {briefing_type} executive briefing for {dashboard.name}:
            
            Current KPI Performance:
            {kpi_context}
            
            Recent AI Insights:
            {insights_summary}
            
            Create a structured executive briefing with:
            
            1. EXECUTIVE SUMMARY (2-3 sentences)
            2. KEY METRICS PERFORMANCE
            3. CRITICAL INSIGHTS & TRENDS
            4. RECOMMENDED ACTIONS
            5. UPCOMING PRIORITIES
            
            Keep it concise, executive-focused, and actionable. Highlight only the most important items that require executive attention.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a senior executive assistant AI agent with expertise in executive communication and business reporting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            briefing_content = response.choices[0].message.content
            
            # Parse briefing into sections
            sections = self._parse_briefing_sections(briefing_content)
            
            # Create briefing record
            briefing = ExecutiveBriefing()
            briefing.user_id = user_id
            briefing.dashboard_id = dashboard_id
            briefing.briefing_type = briefing_type
            briefing.executive_summary = sections.get('executive_summary', '')
            briefing.key_metrics_summary = sections.get('key_metrics', '')
            briefing.trends_analysis = sections.get('insights_trends', '')
            briefing.recommendations = sections.get('recommended_actions', '')
            briefing.ai_agent_id = 5  # Executive Assistant Agent
            briefing.period_start = datetime.utcnow() - timedelta(days=1)
            briefing.period_end = datetime.utcnow()
            
            db.session.add(briefing)
            db.session.commit()
            
            return {
                'briefing_id': briefing.id,
                'content': briefing_content,
                'sections': sections
            }
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error generating executive briefing: {str(e)}")
            return None
    
    def _get_dashboard_kpi_data(self, dashboard_id: int) -> List[Dict]:
        """Get KPI data for dashboard analysis"""
        
        try:
            # Get widgets that display KPIs
            kpi_widgets = DashboardWidget.query.filter_by(
                dashboard_id=dashboard_id,
                widget_type='kpi'
            ).all()
            
            kpi_data = []
            
            for widget in kpi_widgets:
                if widget.cached_data:
                    try:
                        data = json.loads(widget.cached_data)
                        kpi_data.append({
                            'widget_title': widget.title,
                            'data': data,
                            'last_updated': widget.last_data_refresh.isoformat() if widget.last_data_refresh else None
                        })
                    except json.JSONDecodeError:
                        continue
            
            return kpi_data
            
        except Exception as e:
            logging.error(f"Error getting KPI data: {str(e)}")
            return []
    
    def _create_kpi_context(self, kpi_data: List[Dict]) -> str:
        """Create formatted context string from KPI data"""
        
        if not kpi_data:
            return "No KPI data available"
        
        context_lines = []
        for kpi in kpi_data:
            context_lines.append(f"KPI: {kpi.get('widget_title', 'Unknown')}")
            if isinstance(kpi.get('data'), dict):
                for key, value in kpi['data'].items():
                    context_lines.append(f"  {key}: {value}")
            context_lines.append("")
        
        return "\n".join(context_lines)
    
    def _extract_summary(self, analysis: str) -> str:
        """Extract summary from AI analysis"""
        lines = analysis.split('\n')
        summary_lines = []
        
        for line in lines[:3]:  # Take first 3 lines as summary
            if line.strip():
                summary_lines.append(line.strip())
        
        return " ".join(summary_lines)[:300]  # Limit to 300 characters
    
    def _extract_actions(self, analysis: str) -> List[str]:
        """Extract action items from AI analysis"""
        actions = []
        lines = analysis.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['recommend', 'should', 'action', 'next step']):
                if len(line) > 10:  # Avoid short/empty lines
                    actions.append(line)
        
        return actions[:5]  # Limit to 5 actions
    
    def _parse_briefing_sections(self, content: str) -> Dict[str, str]:
        """Parse briefing content into structured sections"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            if any(header in line.upper() for header in ['EXECUTIVE SUMMARY', 'KEY METRICS', 'CRITICAL INSIGHTS', 'RECOMMENDED ACTIONS', 'UPCOMING PRIORITIES']):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                if 'EXECUTIVE SUMMARY' in line.upper():
                    current_section = 'executive_summary'
                elif 'KEY METRICS' in line.upper():
                    current_section = 'key_metrics'
                elif 'CRITICAL INSIGHTS' in line.upper() or 'TRENDS' in line.upper():
                    current_section = 'insights_trends'
                elif 'RECOMMENDED ACTIONS' in line.upper():
                    current_section = 'recommended_actions'
                elif 'UPCOMING PRIORITIES' in line.upper():
                    current_section = 'upcoming_priorities'
                
                current_content = []
            else:
                if current_section and line:
                    current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections

class DashboardBuilderService:
    """Service for dashboard creation and management"""
    
    def create_dashboard_from_template(self, user_id: int, template_id: int, dashboard_name: str) -> Optional[int]:
        """Create a new dashboard from a template"""
        
        try:
            template = DashboardTemplate.query.get(template_id)
            if not template:
                return None
            
            # Create new dashboard
            dashboard = Dashboard()
            dashboard.user_id = user_id
            dashboard.name = dashboard_name
            dashboard.description = f"Dashboard created from {template.name} template"
            dashboard.category = template.category
            
            if template.template_config:
                config = json.loads(template.template_config)
                dashboard.layout_config = json.dumps(config.get('layout', {}))
                dashboard.theme_config = json.dumps(config.get('theme', {}))
                
                # Set AI agent preferences from template
                if template.default_ai_agents:
                    dashboard.ai_agent_preferences = template.default_ai_agents
            
            db.session.add(dashboard)
            db.session.flush()  # Get dashboard ID
            
            # Create widgets from template
            if template.template_config:
                config = json.loads(template.template_config)
                widgets = config.get('widgets', [])
                
                for widget_config in widgets:
                    widget = DashboardWidget()
                    widget.dashboard_id = dashboard.id
                    widget.widget_id = widget_config.get('widget_id', f'widget_{len(widgets)}')
                    widget.widget_type = widget_config.get('type', 'chart')
                    widget.title = widget_config.get('title', 'Widget')
                    widget.position_x = widget_config.get('x', 0)
                    widget.position_y = widget_config.get('y', 0)
                    widget.width = widget_config.get('width', 4)
                    widget.height = widget_config.get('height', 3)
                    widget.configuration = json.dumps(widget_config.get('config', {}))
                    
                    if widget_config.get('ai_agent_id'):
                        widget.ai_agent_id = widget_config['ai_agent_id']
                    
                    db.session.add(widget)
            
            db.session.commit()
            
            return dashboard.id
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating dashboard from template: {str(e)}")
            return None
    
    def get_dashboard_subscription_limits(self, user_id: int) -> Dict[str, int]:
        """Get subscription limits for a user"""
        
        subscription = DashboardSubscription.query.filter_by(user_id=user_id).first()
        
        if not subscription:
            # Return free tier limits
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