"""
Automation Marketplace Service
Manages high-ROI automation processes with AI agent integration and pricing
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from app import db
from models import AutomationProcess, ProcessAgent, ProcessPurchase, AIAgent, User, ROITracking
from top_100_ai_automation_processes import analyze_top_100_automation_processes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomationMarketplaceService:
    """Service for managing automation process marketplace"""
    
    def __init__(self):
        self.pricing_strategy = {
            'revenue_generation': {'base_multiplier': 1.5, 'setup_multiplier': 2.0},
            'cost_reduction': {'base_multiplier': 1.2, 'setup_multiplier': 1.5},
            'customer_experience': {'base_multiplier': 1.3, 'setup_multiplier': 1.8},
            'operational_efficiency': {'base_multiplier': 1.1, 'setup_multiplier': 1.3},
            'compliance_risk': {'base_multiplier': 1.4, 'setup_multiplier': 2.2},
            'innovation_growth': {'base_multiplier': 1.6, 'setup_multiplier': 2.5},
            'financial_optimization': {'base_multiplier': 1.4, 'setup_multiplier': 2.0},
            'marketing_sales': {'base_multiplier': 1.3, 'setup_multiplier': 1.8},
            'hr_talent': {'base_multiplier': 1.2, 'setup_multiplier': 1.6},
            'data_analytics': {'base_multiplier': 1.4, 'setup_multiplier': 1.9}
        }
    
    def populate_automation_processes(self) -> Dict[str, Any]:
        """Populate database with top automation processes"""
        try:
            # Get top 100 automation processes
            from top_100_ai_automation_processes_complete import analyze_top_100_automation_processes
            analysis_result = analyze_top_100_automation_processes()
            
            if not analysis_result or 'top_100_processes' not in analysis_result:
                return {'success': False, 'error': 'Failed to get automation processes'}
            
            processes_created = 0
            processes_skipped = 0
            
            for process_data in analysis_result['top_100_processes']:  # All 100 processes for complete marketplace
                # Check if process already exists
                existing = AutomationProcess.query.filter_by(name=process_data['name']).first()
                if existing:
                    processes_skipped += 1
                    continue
                
                # Calculate pricing based on category and ROI
                pricing = self._calculate_process_pricing(process_data)
                
                # Create automation process
                process = AutomationProcess()
                process.name = process_data['name']
                process.description = process_data['description']
                process.category = process_data['category']
                process.roi_potential = process_data['roi_potential']
                process.roi_score = process_data['roi_score']
                process.implementation_ease = process_data['implementation_ease']
                process.time_to_value = process_data['time_to_value']
                process.base_price = pricing['base_price']
                process.monthly_price = pricing['monthly_price']
                process.setup_fee = pricing['setup_fee']
                
                if 'automation_components' in process_data:
                    process.automation_components = json.dumps(process_data['automation_components'])
                
                if 'win_win_win' in process_data:
                    process.win_win_benefits = process_data['win_win_win']
                
                db.session.add(process)
                db.session.flush()  # Get the ID
                
                # Assign AI agents to the process
                if 'relevant_agents' in process_data:
                    self._assign_agents_to_process(process.id, process_data['relevant_agents'])
                
                processes_created += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'processes_created': processes_created,
                'processes_skipped': processes_skipped,
                'total_processes': AutomationProcess.query.count()
            }
            
        except Exception as e:
            logger.error(f"Error populating automation processes: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _calculate_process_pricing(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate pricing for automation process based on ROI and category"""
        category = process_data.get('category', 'operational_efficiency')
        roi_score = process_data.get('roi_score', 50)
        implementation_ease = process_data.get('implementation_ease', 50)
        
        # Base pricing tiers
        base_price_ranges = {
            'high_roi': {'min': 2500, 'max': 8000},    # 80+ ROI score
            'medium_roi': {'min': 1500, 'max': 4000},  # 60-79 ROI score
            'standard_roi': {'min': 800, 'max': 2500}  # <60 ROI score
        }
        
        # Determine pricing tier
        if roi_score >= 80:
            tier = 'high_roi'
        elif roi_score >= 60:
            tier = 'medium_roi'
        else:
            tier = 'standard_roi'
        
        # Calculate base price
        price_range = base_price_ranges[tier]
        base_price = price_range['min'] + (price_range['max'] - price_range['min']) * (roi_score / 100)
        
        # Apply category multipliers
        category_config = self.pricing_strategy.get(category, {'base_multiplier': 1.0, 'setup_multiplier': 1.0})
        
        # Calculate final pricing
        final_base_price = base_price * category_config['base_multiplier']
        monthly_price = final_base_price * 0.15  # 15% monthly rate
        setup_fee = final_base_price * 0.3 * category_config['setup_multiplier']  # Setup fee
        
        # Difficulty adjustment (easier = lower price)
        ease_factor = 1.0 - (implementation_ease - 50) / 200  # Adjust by up to ±25%
        
        return {
            'base_price': round(final_base_price * ease_factor, 2),
            'monthly_price': round(monthly_price * ease_factor, 2),
            'setup_fee': round(setup_fee, 2)
        }
    
    def _assign_agents_to_process(self, process_id: int, agent_names: List[str]):
        """Assign AI agents to automation process"""
        try:
            for i, agent_name in enumerate(agent_names):
                # Find agent by name (flexible matching)
                agent = AIAgent.query.filter(AIAgent.name.contains(agent_name.split()[0])).first()
                if not agent:
                    # Try finding by category or specialization
                    search_terms = agent_name.lower().split()
                    for term in search_terms:
                        agent = AIAgent.query.filter(
                            db.or_(
                                AIAgent.category.contains(term),
                                AIAgent.specialization_tags.contains(term)
                            )
                        ).first()
                        if agent:
                            break
                
                if agent:
                    # Create process-agent assignment
                    assignment = ProcessAgent()
                    assignment.process_id = process_id
                    assignment.agent_id = agent.id
                    assignment.is_primary = (i == 0)  # First agent is primary
                    assignment.role_description = f"Primary specialist for {agent_name}" if i == 0 else f"Supporting expertise in {agent.category}"
                    
                    db.session.add(assignment)
        
        except Exception as e:
            logger.error(f"Error assigning agents to process {process_id}: {e}")
    
    def get_marketplace_data(self, category: str = 'all', sort_by: str = 'roi_score') -> Dict[str, Any]:
        """Get automation processes for marketplace display"""
        try:
            query = AutomationProcess.query.filter_by(is_active=True)
            
            if category != 'all':
                query = query.filter_by(category=category)
            
            # Sort options
            if sort_by == 'roi_score':
                query = query.order_by(AutomationProcess.roi_score.desc())
            elif sort_by == 'price_low':
                query = query.order_by(AutomationProcess.base_price.asc())
            elif sort_by == 'price_high':
                query = query.order_by(AutomationProcess.base_price.desc())
            elif sort_by == 'time_to_value':
                query = query.order_by(AutomationProcess.time_to_value.asc())
            else:
                query = query.order_by(AutomationProcess.roi_score.desc())
            
            processes = query.all()
            
            # Enrich with agent data
            enriched_processes = []
            for process in processes:
                process_data = {
                    'id': process.id,
                    'name': process.name,
                    'description': process.description,
                    'category': process.category,
                    'roi_potential': process.roi_potential,
                    'roi_score': process.roi_score,
                    'implementation_ease': process.implementation_ease,
                    'time_to_value': process.time_to_value,
                    'base_price': process.base_price,
                    'monthly_price': process.monthly_price,
                    'setup_fee': process.setup_fee,
                    'win_win_benefits': process.win_win_benefits,
                    'agents': []
                }
                
                # Get assigned agents
                for assignment in process.process_agents:
                    agent_data = {
                        'name': assignment.agent.name,
                        'category': assignment.agent.category,
                        'expertise_level': assignment.agent.expertise_level,
                        'is_primary': assignment.is_primary,
                        'role': assignment.role_description
                    }
                    process_data['agents'].append(agent_data)
                
                # Calculate revenue projections
                process_data['revenue_projections'] = self._calculate_revenue_projections(process)
                
                enriched_processes.append(process_data)
            
            # Get categories for filtering
            categories = db.session.query(AutomationProcess.category.distinct()).all()
            category_list = [cat[0] for cat in categories if cat[0]]
            
            return {
                'processes': enriched_processes,
                'categories': category_list,
                'total_processes': len(enriched_processes),
                'stats': self._get_marketplace_stats()
            }
            
        except Exception as e:
            logger.error(f"Error getting marketplace data: {e}")
            return {'processes': [], 'categories': [], 'total_processes': 0, 'stats': {}}
    
    def _calculate_revenue_projections(self, process: AutomationProcess) -> Dict[str, str]:
        """Calculate revenue projections for 30 and 90 days"""
        try:
            # Parse ROI potential (e.g., "300-500%" -> average 400%)
            roi_str = process.roi_potential.replace('%', '')
            if '-' in roi_str:
                roi_parts = roi_str.split('-')
                avg_roi = (float(roi_parts[0]) + float(roi_parts[1])) / 2
            else:
                avg_roi = float(roi_str)
            
            # Assume customer invests the process cost as baseline
            investment_baseline = process.base_price + process.setup_fee
            
            # Calculate projected returns
            annual_return = investment_baseline * (avg_roi / 100)
            monthly_return = annual_return / 12
            
            return {
                '30_day_projection': f"${monthly_return:,.0f} additional revenue",
                '90_day_projection': f"${monthly_return * 3:,.0f} cumulative return",
                'annual_projection': f"${annual_return:,.0f} annual ROI potential",
                'payback_period': f"{(investment_baseline / monthly_return):.1f} months"
            }
            
        except Exception as e:
            logger.error(f"Error calculating revenue projections: {e}")
            return {
                '30_day_projection': "Contact for projection",
                '90_day_projection': "Contact for projection", 
                'annual_projection': "Contact for projection",
                'payback_period': "Contact for analysis"
            }
    
    def _get_marketplace_stats(self) -> Dict[str, Any]:
        """Get marketplace statistics"""
        try:
            total_processes = AutomationProcess.query.filter_by(is_active=True).count()
            avg_roi = db.session.query(db.func.avg(AutomationProcess.roi_score)).scalar() or 0
            total_agents_involved = db.session.query(ProcessAgent.agent_id.distinct()).count()
            
            # Get price ranges
            min_price = db.session.query(db.func.min(AutomationProcess.base_price)).scalar() or 0
            max_price = db.session.query(db.func.max(AutomationProcess.base_price)).scalar() or 0
            
            return {
                'total_processes': total_processes,
                'average_roi_score': round(avg_roi, 1),
                'total_agents_involved': total_agents_involved,
                'price_range': f"${min_price:,.0f} - ${max_price:,.0f}",
                'categories_available': AutomationProcess.query.with_entities(AutomationProcess.category.distinct()).count()
            }
            
        except Exception as e:
            logger.error(f"Error getting marketplace stats: {e}")
            return {}
    
    def create_process_purchase(self, user_id: int, process_id: int, purchase_type: str = 'full_package') -> Dict[str, Any]:
        """Create a process purchase record"""
        try:
            process = AutomationProcess.query.get_or_404(process_id)
            user = User.query.get_or_404(user_id)
            
            # Calculate total amount based on purchase type
            if purchase_type == 'full_package':
                total_amount = process.base_price + process.setup_fee
            elif purchase_type == 'consultation':
                total_amount = process.base_price * 0.2  # 20% for consultation
            elif purchase_type == 'setup_only':
                total_amount = process.setup_fee
            else:
                total_amount = process.base_price + process.setup_fee
            
            # Create purchase record
            purchase = ProcessPurchase()
            purchase.user_id = user_id
            purchase.process_id = process_id
            purchase.purchase_type = purchase_type
            purchase.total_amount = total_amount
            purchase.status = 'pending'
            
            # Set expected completion based on time_to_value
            if process.time_to_value:
                # Parse time to value (e.g., "2-4 weeks" -> 4 weeks)
                time_str = process.time_to_value.lower()
                if 'week' in time_str:
                    weeks = 4  # Default to 4 weeks
                    if '-' in time_str:
                        weeks = int(time_str.split('-')[-1].split()[0])
                    elif time_str[0].isdigit():
                        weeks = int(time_str[0])
                    
                    purchase.expected_completion = datetime.utcnow() + timedelta(weeks=weeks)
            
            db.session.add(purchase)
            db.session.commit()
            
            return {
                'success': True,
                'purchase_id': purchase.id,
                'total_amount': total_amount,
                'process_name': process.name
            }
            
        except Exception as e:
            logger.error(f"Error creating process purchase: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}

# Export service instance
automation_service = AutomationMarketplaceService()