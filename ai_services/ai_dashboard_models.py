"""
AI Dashboard Builder Models
Comprehensive data models for enterprise dashboard creation and management
"""

from datetime import datetime
from sqlalchemy import JSON
from app import db

class Dashboard(db.Model):
    __tablename__ = 'dashboards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Dashboard Metadata
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # executive, sales, marketing, finance, operations
    
    # Configuration
    layout_config = db.Column(db.Text)  # JSON configuration for dashboard layout
    theme_config = db.Column(db.Text)   # JSON for colors, fonts, styling
    
    # Access Control
    visibility = db.Column(db.String(20), default='private')  # private, team, company, public
    shared_with_users = db.Column(db.Text)  # JSON array of user IDs with access
    
    # AI Configuration
    auto_insights_enabled = db.Column(db.Boolean, default=True)
    insights_frequency = db.Column(db.String(20), default='daily')  # hourly, daily, weekly
    ai_agent_preferences = db.Column(db.Text)  # JSON config for which agents to use
    
    # Status and Metrics
    is_active = db.Column(db.Boolean, default=True)
    last_accessed = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    
    # Performance
    refresh_interval_minutes = db.Column(db.Integer, default=15)
    auto_refresh_enabled = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    widgets = db.relationship('DashboardWidget', backref='dashboard', lazy=True, cascade='all, delete-orphan')
    insights = db.relationship('DashboardInsight', backref='dashboard', lazy=True)
    user = db.relationship('User', backref='dashboards')

class DashboardWidget(db.Model):
    __tablename__ = 'dashboard_widgets'
    
    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    
    # Widget Identity
    widget_id = db.Column(db.String(50), nullable=False)  # Unique within dashboard
    widget_type = db.Column(db.String(50), nullable=False)  # chart, kpi, table, text, ai_insight
    
    # Layout and Position
    position_x = db.Column(db.Integer, default=0)
    position_y = db.Column(db.Integer, default=0)
    width = db.Column(db.Integer, default=4)  # Grid units
    height = db.Column(db.Integer, default=3)  # Grid units
    z_index = db.Column(db.Integer, default=1)
    
    # Widget Configuration
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(300))
    configuration = db.Column(db.Text)  # JSON configuration specific to widget type
    
    # Data Source
    data_source_type = db.Column(db.String(50))  # api, database, static, ai_generated
    data_source_config = db.Column(db.Text)  # JSON configuration for data source
    
    # AI Integration
    ai_agent_id = db.Column(db.Integer, db.ForeignKey('ai_agent.id'))  # AI agent for generating content
    ai_prompt_template = db.Column(db.Text)  # Template for AI agent prompts
    ai_refresh_frequency = db.Column(db.String(20), default='hourly')
    
    # Visual Configuration
    style_config = db.Column(db.Text)  # JSON for colors, fonts, etc.
    chart_config = db.Column(db.Text)   # JSON for chart-specific settings
    
    # Cache and Performance
    cached_data = db.Column(db.Text)    # JSON cached data
    last_data_refresh = db.Column(db.DateTime)
    refresh_error = db.Column(db.Text)
    
    # Status
    is_visible = db.Column(db.Boolean, default=True)
    is_loading = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ai_agent = db.relationship('AIAgent', backref='dashboard_widgets')

class KPIDefinition(db.Model):
    __tablename__ = 'kpi_definitions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # KPI Identity
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # revenue, growth, efficiency, customer, etc.
    
    # Calculation Configuration
    calculation_method = db.Column(db.String(50))  # formula, query, api, ai_generated
    calculation_config = db.Column(db.Text)  # JSON configuration for calculation
    
    # Target and Thresholds
    target_value = db.Column(db.Float)
    target_period = db.Column(db.String(20))  # daily, weekly, monthly, quarterly, yearly
    
    warning_threshold = db.Column(db.Float)  # Yellow alert threshold
    critical_threshold = db.Column(db.Float)  # Red alert threshold
    
    # Units and Formatting
    unit_type = db.Column(db.String(20))  # currency, percentage, count, ratio
    unit_symbol = db.Column(db.String(10))  # $, %, #, etc.
    decimal_places = db.Column(db.Integer, default=2)
    
    # AI Enhancement
    ai_analysis_enabled = db.Column(db.Boolean, default=True)
    ai_agent_id = db.Column(db.Integer, db.ForeignKey('ai_agent.id'))
    insights_prompt_template = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    values = db.relationship('KPIValue', backref='kpi_definition', lazy=True)
    ai_agent = db.relationship('AIAgent', backref='kpi_definitions')
    user = db.relationship('User', backref='kpi_definitions')

class KPIValue(db.Model):
    __tablename__ = 'kpi_values'
    
    id = db.Column(db.Integer, primary_key=True)
    kpi_definition_id = db.Column(db.Integer, db.ForeignKey('kpi_definitions.id'), nullable=False)
    
    # Value Data
    value = db.Column(db.Float, nullable=False)
    previous_value = db.Column(db.Float)  # For trend calculation
    
    # Time Period
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    period_type = db.Column(db.String(20))  # hour, day, week, month, quarter, year
    
    # Status Indicators
    status = db.Column(db.String(20))  # excellent, good, warning, critical
    trend = db.Column(db.String(20))   # up, down, flat
    percentage_change = db.Column(db.Float)
    
    # Data Source
    data_source = db.Column(db.String(100))  # Where this value came from
    calculation_details = db.Column(db.Text)  # JSON with calculation breakdown
    
    # Quality Indicators
    confidence_score = db.Column(db.Float)  # 0.0 to 1.0
    data_quality = db.Column(db.String(20))  # high, medium, low
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DashboardInsight(db.Model):
    __tablename__ = 'dashboard_insights'
    
    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    ai_agent_id = db.Column(db.Integer, db.ForeignKey('ai_agent.id'), nullable=False)
    
    # Insight Content
    insight_type = db.Column(db.String(50))  # trend_analysis, anomaly_detection, prediction, recommendation
    title = db.Column(db.String(300), nullable=False)
    summary = db.Column(db.Text)
    detailed_analysis = db.Column(db.Text)
    
    # Relevance and Priority
    priority_level = db.Column(db.String(20))  # high, medium, low
    confidence_score = db.Column(db.Float)  # 0.0 to 1.0
    business_impact = db.Column(db.String(20))  # high, medium, low
    
    # Action Items
    recommended_actions = db.Column(db.Text)  # JSON array of recommended actions
    affected_kpis = db.Column(db.Text)  # JSON array of KPI IDs that are affected
    
    # Time Context
    insight_period_start = db.Column(db.DateTime)
    insight_period_end = db.Column(db.DateTime)
    relevant_until = db.Column(db.DateTime)
    
    # User Interaction
    is_read = db.Column(db.Boolean, default=False)
    is_dismissed = db.Column(db.Boolean, default=False)
    user_rating = db.Column(db.Integer)  # 1-5 stars
    user_feedback = db.Column(db.Text)
    
    # AI Generation Details
    ai_model_used = db.Column(db.String(50))
    generation_prompt = db.Column(db.Text)
    processing_time_ms = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ai_agent = db.relationship('AIAgent', backref='dashboard_insights')

class DashboardTemplate(db.Model):
    __tablename__ = 'dashboard_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Template Metadata
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # executive, sales, marketing, finance, operations
    industry = db.Column(db.String(50))  # saas, ecommerce, manufacturing, etc.
    
    # Template Configuration
    template_config = db.Column(db.Text)  # JSON configuration for widgets and layout
    default_ai_agents = db.Column(db.Text)  # JSON array of recommended AI agent IDs
    required_data_sources = db.Column(db.Text)  # JSON array of required data sources
    
    # Marketplace
    is_public = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, default=0.0)  # 0.0 for free templates
    
    # Usage Statistics
    usage_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='dashboard_templates')

class ExecutiveBriefing(db.Model):
    __tablename__ = 'executive_briefings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    
    # Briefing Content
    briefing_type = db.Column(db.String(20))  # daily, weekly, monthly, ad_hoc
    executive_summary = db.Column(db.Text)
    key_metrics_summary = db.Column(db.Text)
    trends_analysis = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    
    # AI Generation
    ai_agent_id = db.Column(db.Integer, db.ForeignKey('ai_agent.id'), nullable=False)
    generation_prompt = db.Column(db.Text)
    
    # Time Period
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    
    # Distribution
    recipients = db.Column(db.Text)  # JSON array of user IDs or email addresses
    delivery_method = db.Column(db.String(20))  # email, dashboard, both
    
    # Status
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='executive_briefings')
    ai_agent = db.relationship('AIAgent', backref='executive_briefings')

class DashboardAlert(db.Model):
    __tablename__ = 'dashboard_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    kpi_definition_id = db.Column(db.Integer, db.ForeignKey('kpi_definitions.id'))
    
    # Alert Configuration
    alert_name = db.Column(db.String(200), nullable=False)
    alert_type = db.Column(db.String(50))  # threshold, anomaly, trend, ai_detected
    
    # Conditions
    condition_config = db.Column(db.Text)  # JSON configuration for alert conditions
    threshold_value = db.Column(db.Float)
    comparison_operator = db.Column(db.String(10))  # >, <, >=, <=, ==, !=
    
    # Notification Settings
    notification_methods = db.Column(db.Text)  # JSON array: email, sms, slack, webhook
    recipients = db.Column(db.Text)  # JSON array of recipient configurations
    
    # Frequency Control
    cooldown_minutes = db.Column(db.Integer, default=60)  # Minimum time between alerts
    max_alerts_per_day = db.Column(db.Integer, default=10)
    
    # AI Enhancement
    ai_context_analysis = db.Column(db.Boolean, default=True)
    ai_agent_id = db.Column(db.Integer, db.ForeignKey('ai_agent.id'))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_triggered = db.Column(db.DateTime)
    trigger_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    kpi_definition = db.relationship('KPIDefinition', backref='alerts')
    ai_agent = db.relationship('AIAgent', backref='dashboard_alerts')

class DashboardSubscription(db.Model):
    __tablename__ = 'dashboard_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Subscription Details
    plan_name = db.Column(db.String(50), nullable=False)  # starter, professional, enterprise
    billing_cycle = db.Column(db.String(20), default='monthly')  # monthly, yearly
    
    # Limits and Features
    max_dashboards = db.Column(db.Integer, default=5)
    max_widgets_per_dashboard = db.Column(db.Integer, default=20)
    max_ai_insights_per_month = db.Column(db.Integer, default=100)
    max_executive_briefings_per_month = db.Column(db.Integer, default=10)
    
    # Usage Tracking
    current_dashboards = db.Column(db.Integer, default=0)
    current_month_ai_insights = db.Column(db.Integer, default=0)
    current_month_briefings = db.Column(db.Integer, default=0)
    
    # Billing
    monthly_price = db.Column(db.Float, nullable=False)
    stripe_subscription_id = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, cancelled, suspended
    trial_ends_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='dashboard_subscription')

# Add the models to the main models file's imports
def register_dashboard_models():
    """Register dashboard models with the main application"""
    return [
        Dashboard, DashboardWidget, KPIDefinition, KPIValue,
        DashboardInsight, DashboardTemplate, ExecutiveBriefing,
        DashboardAlert, DashboardSubscription
    ]