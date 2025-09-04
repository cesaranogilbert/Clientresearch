"""
AI Dashboard Builder Default Templates
Pre-configured dashboard templates for various business needs
"""

import json
from ai_dashboard_models import DashboardTemplate
from app import db

def create_default_templates():
    """Create default dashboard templates for various business needs"""
    
    templates = [
        {
            'name': 'Executive Overview Dashboard',
            'description': 'High-level KPIs and insights for C-suite executives',
            'category': 'executive',
            'industry': 'general',
            'is_featured': True,
            'template_config': {
                'layout': {
                    'grid_columns': 12,
                    'grid_rows': 8,
                    'theme': 'professional'
                },
                'theme': {
                    'primary_color': '#0d6efd',
                    'secondary_color': '#6c757d',
                    'background': '#f8f9fa'
                },
                'widgets': [
                    {
                        'widget_id': 'revenue_kpi',
                        'type': 'kpi',
                        'title': 'Total Revenue',
                        'x': 0, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 1000000,
                            'comparison_period': 'previous_month'
                        },
                        'ai_agent_id': 1
                    },
                    {
                        'widget_id': 'growth_kpi',
                        'type': 'kpi',
                        'title': 'Revenue Growth',
                        'x': 3, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.15,
                            'comparison_period': 'year_over_year'
                        },
                        'ai_agent_id': 2
                    },
                    {
                        'widget_id': 'customers_kpi',
                        'type': 'kpi',
                        'title': 'Active Customers',
                        'x': 6, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'number',
                            'target': 5000
                        },
                        'ai_agent_id': 3
                    },
                    {
                        'widget_id': 'profit_margin_kpi',
                        'type': 'kpi',
                        'title': 'Profit Margin',
                        'x': 9, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.25
                        },
                        'ai_agent_id': 4
                    },
                    {
                        'widget_id': 'revenue_trend',
                        'type': 'chart',
                        'title': 'Revenue Trend (12 Months)',
                        'x': 0, 'y': 2, 'width': 6, 'height': 3,
                        'config': {
                            'chart_type': 'line',
                            'time_period': '12_months',
                            'y_axis_format': 'currency'
                        },
                        'ai_agent_id': 5
                    },
                    {
                        'widget_id': 'key_metrics_table',
                        'type': 'table',
                        'title': 'Key Performance Metrics',
                        'x': 6, 'y': 2, 'width': 6, 'height': 3,
                        'config': {
                            'metrics': ['CAC', 'LTV', 'Churn Rate', 'ARPU'],
                            'comparison_period': 'previous_month'
                        },
                        'ai_agent_id': 6
                    },
                    {
                        'widget_id': 'strategic_insights',
                        'type': 'ai_insight',
                        'title': 'Strategic AI Insights',
                        'x': 0, 'y': 5, 'width': 12, 'height': 3,
                        'config': {
                            'insight_types': ['trend_analysis', 'recommendations'],
                            'refresh_frequency': 'daily'
                        },
                        'ai_agent_id': 7
                    }
                ]
            },
            'default_ai_agents': [1, 2, 3, 4, 5, 6, 7],
            'required_data_sources': ['revenue', 'customers', 'financial_metrics']
        },
        
        {
            'name': 'Sales Performance Dashboard',
            'description': 'Comprehensive sales metrics and pipeline analysis',
            'category': 'sales',
            'industry': 'general',
            'is_featured': True,
            'template_config': {
                'layout': {
                    'grid_columns': 12,
                    'grid_rows': 8,
                    'theme': 'sales'
                },
                'theme': {
                    'primary_color': '#198754',
                    'secondary_color': '#20c997',
                    'background': '#f8f9fa'
                },
                'widgets': [
                    {
                        'widget_id': 'monthly_sales',
                        'type': 'kpi',
                        'title': 'Monthly Sales',
                        'x': 0, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 500000
                        }
                    },
                    {
                        'widget_id': 'pipeline_value',
                        'type': 'kpi',
                        'title': 'Pipeline Value',
                        'x': 3, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 2000000
                        }
                    },
                    {
                        'widget_id': 'conversion_rate',
                        'type': 'kpi',
                        'title': 'Lead Conversion Rate',
                        'x': 6, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.15
                        }
                    },
                    {
                        'widget_id': 'sales_cycle',
                        'type': 'kpi',
                        'title': 'Avg Sales Cycle',
                        'x': 9, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'days',
                            'target': 45
                        }
                    },
                    {
                        'widget_id': 'sales_funnel',
                        'type': 'chart',
                        'title': 'Sales Funnel Analysis',
                        'x': 0, 'y': 2, 'width': 6, 'height': 3,
                        'config': {
                            'chart_type': 'funnel',
                            'stages': ['Leads', 'Qualified', 'Proposal', 'Closed Won']
                        }
                    },
                    {
                        'widget_id': 'top_performers',
                        'type': 'table',
                        'title': 'Top Sales Performers',
                        'x': 6, 'y': 2, 'width': 6, 'height': 3,
                        'config': {
                            'sort_by': 'monthly_sales',
                            'limit': 10
                        }
                    },
                    {
                        'widget_id': 'sales_insights',
                        'type': 'ai_insight',
                        'title': 'Sales Performance Insights',
                        'x': 0, 'y': 5, 'width': 12, 'height': 3,
                        'config': {
                            'insight_types': ['pipeline_analysis', 'forecast'],
                            'refresh_frequency': 'daily'
                        }
                    }
                ]
            },
            'default_ai_agents': [8, 9, 10, 11],
            'required_data_sources': ['crm', 'sales_pipeline', 'sales_performance']
        },
        
        {
            'name': 'Marketing ROI Dashboard',
            'description': 'Marketing campaign performance and ROI analysis',
            'category': 'marketing',
            'industry': 'general',
            'is_featured': True,
            'template_config': {
                'layout': {
                    'grid_columns': 12,
                    'grid_rows': 8,
                    'theme': 'marketing'
                },
                'theme': {
                    'primary_color': '#dc3545',
                    'secondary_color': '#fd7e14',
                    'background': '#f8f9fa'
                },
                'widgets': [
                    {
                        'widget_id': 'marketing_roi',
                        'type': 'kpi',
                        'title': 'Marketing ROI',
                        'x': 0, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 3.0
                        }
                    },
                    {
                        'widget_id': 'cac',
                        'type': 'kpi',
                        'title': 'Customer Acquisition Cost',
                        'x': 3, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 150
                        }
                    },
                    {
                        'widget_id': 'lead_volume',
                        'type': 'kpi',
                        'title': 'Monthly Leads',
                        'x': 6, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'number',
                            'target': 1000
                        }
                    },
                    {
                        'widget_id': 'website_traffic',
                        'type': 'kpi',
                        'title': 'Website Traffic',
                        'x': 9, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'number',
                            'target': 50000
                        }
                    },
                    {
                        'widget_id': 'campaign_performance',
                        'type': 'chart',
                        'title': 'Campaign Performance',
                        'x': 0, 'y': 2, 'width': 8, 'height': 3,
                        'config': {
                            'chart_type': 'bar',
                            'metrics': ['impressions', 'clicks', 'conversions'],
                            'group_by': 'campaign'
                        }
                    },
                    {
                        'widget_id': 'channel_attribution',
                        'type': 'chart',
                        'title': 'Channel Attribution',
                        'x': 8, 'y': 2, 'width': 4, 'height': 3,
                        'config': {
                            'chart_type': 'pie',
                            'metric': 'conversions',
                            'group_by': 'channel'
                        }
                    },
                    {
                        'widget_id': 'marketing_insights',
                        'type': 'ai_insight',
                        'title': 'Marketing Optimization Insights',
                        'x': 0, 'y': 5, 'width': 12, 'height': 3,
                        'config': {
                            'insight_types': ['campaign_optimization', 'channel_performance'],
                            'refresh_frequency': 'daily'
                        }
                    }
                ]
            },
            'default_ai_agents': [12, 13, 14, 15],
            'required_data_sources': ['marketing_campaigns', 'web_analytics', 'ad_platforms']
        },
        
        {
            'name': 'Financial Performance Dashboard',
            'description': 'Financial metrics and cash flow analysis',
            'category': 'finance',
            'industry': 'general',
            'is_featured': True,
            'template_config': {
                'layout': {
                    'grid_columns': 12,
                    'grid_rows': 8,
                    'theme': 'financial'
                },
                'theme': {
                    'primary_color': '#6f42c1',
                    'secondary_color': '#6610f2',
                    'background': '#f8f9fa'
                },
                'widgets': [
                    {
                        'widget_id': 'net_profit',
                        'type': 'kpi',
                        'title': 'Net Profit',
                        'x': 0, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 250000
                        }
                    },
                    {
                        'widget_id': 'cash_flow',
                        'type': 'kpi',
                        'title': 'Operating Cash Flow',
                        'x': 3, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 300000
                        }
                    },
                    {
                        'widget_id': 'gross_margin',
                        'type': 'kpi',
                        'title': 'Gross Margin',
                        'x': 6, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.65
                        }
                    },
                    {
                        'widget_id': 'burn_rate',
                        'type': 'kpi',
                        'title': 'Monthly Burn Rate',
                        'x': 9, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'currency',
                            'target': 100000
                        }
                    },
                    {
                        'widget_id': 'pnl_chart',
                        'type': 'chart',
                        'title': 'P&L Trend (12 Months)',
                        'x': 0, 'y': 2, 'width': 8, 'height': 3,
                        'config': {
                            'chart_type': 'line',
                            'metrics': ['revenue', 'expenses', 'profit'],
                            'time_period': '12_months'
                        }
                    },
                    {
                        'widget_id': 'expense_breakdown',
                        'type': 'chart',
                        'title': 'Expense Breakdown',
                        'x': 8, 'y': 2, 'width': 4, 'height': 3,
                        'config': {
                            'chart_type': 'pie',
                            'metric': 'expenses',
                            'group_by': 'category'
                        }
                    },
                    {
                        'widget_id': 'financial_insights',
                        'type': 'ai_insight',
                        'title': 'Financial Health Insights',
                        'x': 0, 'y': 5, 'width': 12, 'height': 3,
                        'config': {
                            'insight_types': ['cash_flow_analysis', 'cost_optimization'],
                            'refresh_frequency': 'weekly'
                        }
                    }
                ]
            },
            'default_ai_agents': [16, 17, 18, 19],
            'required_data_sources': ['accounting', 'financial_statements', 'cash_flow']
        },
        
        {
            'name': 'Operations Efficiency Dashboard',
            'description': 'Operational metrics and process optimization',
            'category': 'operations',
            'industry': 'general',
            'is_featured': True,
            'template_config': {
                'layout': {
                    'grid_columns': 12,
                    'grid_rows': 8,
                    'theme': 'operations'
                },
                'theme': {
                    'primary_color': '#20c997',
                    'secondary_color': '#0dcaf0',
                    'background': '#f8f9fa'
                },
                'widgets': [
                    {
                        'widget_id': 'productivity',
                        'type': 'kpi',
                        'title': 'Team Productivity',
                        'x': 0, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.85
                        }
                    },
                    {
                        'widget_id': 'cycle_time',
                        'type': 'kpi',
                        'title': 'Avg Cycle Time',
                        'x': 3, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'hours',
                            'target': 24
                        }
                    },
                    {
                        'widget_id': 'quality_score',
                        'type': 'kpi',
                        'title': 'Quality Score',
                        'x': 6, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.95
                        }
                    },
                    {
                        'widget_id': 'uptime',
                        'type': 'kpi',
                        'title': 'System Uptime',
                        'x': 9, 'y': 0, 'width': 3, 'height': 2,
                        'config': {
                            'value_format': 'percentage',
                            'target': 0.999
                        }
                    },
                    {
                        'widget_id': 'process_efficiency',
                        'type': 'chart',
                        'title': 'Process Efficiency Trends',
                        'x': 0, 'y': 2, 'width': 8, 'height': 3,
                        'config': {
                            'chart_type': 'line',
                            'metrics': ['throughput', 'efficiency', 'quality'],
                            'time_period': '30_days'
                        }
                    },
                    {
                        'widget_id': 'bottlenecks',
                        'type': 'table',
                        'title': 'Process Bottlenecks',
                        'x': 8, 'y': 2, 'width': 4, 'height': 3,
                        'config': {
                            'sort_by': 'impact_score',
                            'limit': 5
                        }
                    },
                    {
                        'widget_id': 'operations_insights',
                        'type': 'ai_insight',
                        'title': 'Operations Optimization Insights',
                        'x': 0, 'y': 5, 'width': 12, 'height': 3,
                        'config': {
                            'insight_types': ['process_optimization', 'bottleneck_analysis'],
                            'refresh_frequency': 'daily'
                        }
                    }
                ]
            },
            'default_ai_agents': [20, 21, 22, 23],
            'required_data_sources': ['operations', 'process_metrics', 'quality_data']
        }
    ]
    
    # Create templates in database
    created_templates = []
    for template_data in templates:
        # Check if template already exists
        existing = DashboardTemplate.query.filter_by(name=template_data['name']).first()
        if existing:
            continue
            
        template = DashboardTemplate()
        template.creator_id = 1  # System user
        template.name = template_data['name']
        template.description = template_data['description']
        template.category = template_data['category']
        template.industry = template_data['industry']
        template.template_config = json.dumps(template_data['template_config'])
        template.default_ai_agents = json.dumps(template_data['default_ai_agents'])
        template.required_data_sources = json.dumps(template_data['required_data_sources'])
        template.is_public = True
        template.is_featured = template_data.get('is_featured', False)
        template.price = 0.0  # Free templates
        template.is_active = True
        
        db.session.add(template)
        created_templates.append(template)
    
    try:
        db.session.commit()
        print(f"Created {len(created_templates)} dashboard templates")
        return created_templates
    except Exception as e:
        db.session.rollback()
        print(f"Error creating templates: {str(e)}")
        return []

def get_template_preview_data(template_id):
    """Get preview data for a template"""
    template = DashboardTemplate.query.get(template_id)
    if not template:
        return None
    
    config = json.loads(template.template_config)
    
    # Generate sample data for widgets
    preview_data = {
        'template': template,
        'widgets': [],
        'sample_insights': []
    }
    
    for widget in config.get('widgets', []):
        widget_data = {
            'id': widget['widget_id'],
            'type': widget['type'],
            'title': widget['title'],
            'sample_value': generate_sample_data(widget)
        }
        preview_data['widgets'].append(widget_data)
    
    return preview_data

def generate_sample_data(widget_config):
    """Generate sample data for widget previews"""
    widget_type = widget_config['type']
    
    if widget_type == 'kpi':
        config = widget_config.get('config', {})
        if 'currency' in config.get('value_format', ''):
            return {'value': 125000, 'trend': '+12.5%', 'status': 'good'}
        elif 'percentage' in config.get('value_format', ''):
            return {'value': 0.235, 'trend': '+2.1%', 'status': 'good'}
        else:
            return {'value': 2340, 'trend': '+156', 'status': 'good'}
    
    elif widget_type == 'chart':
        return {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'data': [65, 59, 80, 81, 56, 55],
            'trend': 'increasing'
        }
    
    elif widget_type == 'table':
        return {
            'headers': ['Metric', 'Current', 'Target', 'Status'],
            'rows': [
                ['Revenue', '$125K', '$150K', 'Good'],
                ['Customers', '2,340', '2,500', 'Good'],
                ['Conversion', '12.5%', '15%', 'Warning']
            ]
        }
    
    elif widget_type == 'ai_insight':
        return {
            'title': 'Revenue Growth Opportunity',
            'summary': 'Customer acquisition has increased 15% this quarter, suggesting strong market demand...',
            'priority': 'high',
            'confidence': 0.85
        }
    
    return {'placeholder': True}