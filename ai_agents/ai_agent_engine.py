"""
4UAI AI Agent Engine - Core Implementation
Production-ready AI agent system with multi-model support
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import openai
import anthropic
from flask import current_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Structured response from AI agent"""
    content: str
    agent_name: str
    model_used: str
    processing_time: float
    confidence_score: float
    usage_tokens: int

@dataclass
class AgentConfig:
    """AI Agent Configuration"""
    name: str
    specialization: str
    base_prompt: str
    capabilities: List[str]
    pricing_tier: str
    monthly_limit: int
    model_preference: str = "openai"

class AIAgentEngine:
    """Core AI Agent Engine with multi-model support"""
    
    def __init__(self):
        """Initialize the AI Agent Engine"""
        self.openai_client = None
        self.anthropic_client = None
        self.agents_registry = {}
        self.usage_tracker = {}
        self._initialize_clients()
        self._load_agent_configurations()
        logger.info("🤖 AI Agent Engine initialized successfully")
    
    def _initialize_clients(self):
        """Initialize AI model clients"""
        try:
            # Initialize OpenAI
            if os.getenv('OPENAI_API_KEY'):
                self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                logger.info("✅ OpenAI GPT-4o client initialized")
            
            # Initialize Anthropic
            if os.getenv('ANTHROPIC_API_KEY'):
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                logger.info("✅ Anthropic Claude client initialized")
                
        except Exception as e:
            logger.error(f"❌ Error initializing AI clients: {e}")
    
    def _load_agent_configurations(self):
        """Load AI agent configurations"""
        # Customer Service Agent (FREE)
        self.agents_registry['customer_service'] = AgentConfig(
            name="Customer Service Master",
            specialization="customer_support",
            base_prompt="""You are an expert Customer Service Master with 15+ years of experience in customer support, complaint resolution, and customer satisfaction. You excel at:

CORE EXPERTISE:
- De-escalating difficult situations with empathy and professionalism
- Providing clear, actionable solutions to customer problems
- Understanding customer needs and emotions behind complaints
- Turning negative experiences into positive outcomes
- Managing multiple communication channels (email, chat, phone)

RESPONSE APPROACH:
1. ACKNOWLEDGE the customer's concern with genuine empathy
2. CLARIFY the situation by asking relevant questions if needed
3. PROVIDE specific solutions or next steps
4. FOLLOW UP with timeline and expectations
5. ENSURE customer satisfaction before closing

COMMUNICATION STYLE:
- Professional yet warm and approachable
- Clear and jargon-free language
- Solution-focused mindset
- Proactive in offering alternatives
- Always end with a positive note

Handle all customer service scenarios including complaints, product issues, billing questions, refund requests, and general inquiries with the highest level of professionalism.""",
            capabilities=["complaint_handling", "product_support", "billing_assistance", "refund_processing"],
            pricing_tier="free",
            monthly_limit=50,
            model_preference="openai"
        )
        
        # Marketing Content Helper (FREE)
        self.agents_registry['marketing_content'] = AgentConfig(
            name="Marketing Content Helper",
            specialization="content_marketing",
            base_prompt="""You are a Marketing Content Expert with 12+ years in content strategy, copywriting, and digital marketing. You specialize in:

CONTENT CREATION:
- Engaging social media posts that drive interaction
- Conversion-focused email marketing campaigns
- SEO-optimized blog content that provides real value
- Compelling ad copy that converts prospects to customers
- Brand storytelling that builds emotional connections

MARKETING PSYCHOLOGY:
- Understanding target audience pain points and desires
- Using proven copywriting formulas (AIDA, PAS, etc.)
- Creating urgency and scarcity without being pushy
- Building trust through valuable content
- Optimizing for different stages of the customer journey

CONTENT STRATEGY:
- Platform-specific content optimization
- Consistent brand voice and messaging
- Content that educates, entertains, and converts
- Call-to-action optimization
- Performance-driven content creation

Provide practical, ready-to-use marketing content that businesses can implement immediately to grow their audience and increase sales.""",
            capabilities=["social_media", "email_campaigns", "blog_content", "ad_copy"],
            pricing_tier="free",
            monthly_limit=50,
            model_preference="openai"
        )
        
        logger.info(f"📋 Loaded {len(self.agents_registry)} AI agents")
    
    def get_available_agents(self, user_tier: str = "free") -> List[Dict]:
        """Get list of available agents for user tier"""
        available = []
        for agent_id, config in self.agents_registry.items():
            if user_tier == "free" and config.pricing_tier != "free":
                continue
            available.append({
                'id': agent_id,
                'name': config.name,
                'specialization': config.specialization,
                'capabilities': config.capabilities,
                'pricing_tier': config.pricing_tier,
                'monthly_limit': config.monthly_limit
            })
        return available
    
    def check_usage_limit(self, user_id: int, agent_id: str) -> tuple[bool, int]:
        """Check if user has exceeded usage limit for agent"""
        key = f"{user_id}_{agent_id}"
        current_month = datetime.now().strftime("%Y-%m")
        
        if key not in self.usage_tracker:
            self.usage_tracker[key] = {"month": current_month, "count": 0}
        
        usage = self.usage_tracker[key]
        if usage["month"] != current_month:
            # Reset for new month
            usage["month"] = current_month
            usage["count"] = 0
        
        agent_config = self.agents_registry.get(agent_id)
        if not agent_config:
            return False, 0
            
        limit = agent_config.monthly_limit
        remaining = max(0, limit - usage["count"])
        
        return usage["count"] < limit, remaining
    
    def process_request(self, agent_id: str, user_input: str, user_id: int, 
                       context: Optional[Dict] = None) -> AgentResponse:
        """Process user request through specified AI agent"""
        start_time = datetime.now()
        
        # Validate agent exists
        if agent_id not in self.agents_registry:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent_config = self.agents_registry[agent_id]
        
        # Check usage limits for free agents
        if agent_config.pricing_tier == "free":
            can_use, remaining = self.check_usage_limit(user_id, agent_id)
            if not can_use:
                raise ValueError(f"Monthly usage limit exceeded for {agent_config.name}")
        
        # Build enhanced prompt
        enhanced_prompt = self._build_enhanced_prompt(agent_config, user_input, context)
        
        # Route to appropriate model
        response_content, model_used, tokens_used = self._call_ai_model(
            agent_config.model_preference, enhanced_prompt
        )
        
        # Update usage tracking
        self._update_usage(user_id, agent_id)
        
        # Calculate metrics
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return AgentResponse(
            content=response_content,
            agent_name=agent_config.name,
            model_used=model_used,
            processing_time=processing_time,
            confidence_score=0.85,  # Default confidence
            usage_tokens=tokens_used
        )
    
    def _build_enhanced_prompt(self, agent_config: AgentConfig, user_input: str, 
                              context: Optional[Dict] = None) -> str:
        """Build enhanced prompt for AI model"""
        prompt = f"{agent_config.base_prompt}\n\n"
        
        if context:
            prompt += f"CONTEXT:\n{json.dumps(context, indent=2)}\n\n"
        
        prompt += f"USER REQUEST:\n{user_input}\n\n"
        prompt += "RESPONSE:"
        
        return prompt
    
    def _call_ai_model(self, model_preference: str, prompt: str) -> tuple[str, str, int]:
        """Call appropriate AI model"""
        try:
            if model_preference == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )
                
                # Safely extract content
                content = ""
                if response.choices and len(response.choices) > 0:
                    message = response.choices[0].message
                    if message and message.content:
                        content = message.content
                
                # Safely extract token usage
                tokens = 0
                if response.usage and hasattr(response.usage, 'total_tokens'):
                    tokens = response.usage.total_tokens
                
                if not content:
                    content = "I apologize, but I couldn't generate a response at the moment."
                
                return content, "gpt-4o", tokens
            
            elif model_preference == "anthropic" and self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022", 
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                
                # Safely extract content
                content = ""
                if response.content and len(response.content) > 0:
                    # Handle different content block types
                    for block in response.content:
                        if hasattr(block, 'text') and block.text:
                            content += block.text
                        elif hasattr(block, 'type') and block.type == 'text':
                            content += getattr(block, 'text', '')
                
                # Safely extract token usage
                tokens = 0
                if response.usage:
                    input_tokens = getattr(response.usage, 'input_tokens', 0)
                    output_tokens = getattr(response.usage, 'output_tokens', 0)
                    tokens = input_tokens + output_tokens
                
                if not content:
                    content = "I apologize, but I couldn't generate a response at the moment."
                
                return content, "claude-3-5-sonnet", tokens
            
            else:
                raise ValueError("No available AI model client")
                
        except Exception as e:
            logger.error(f"AI model call failed: {e}")
            # Return fallback response instead of raising
            return "I apologize, but I encountered an error while processing your request. Please try again.", "fallback", 0
    
    def _update_usage(self, user_id: int, agent_id: str):
        """Update usage tracking"""
        key = f"{user_id}_{agent_id}"
        current_month = datetime.now().strftime("%Y-%m")
        
        if key not in self.usage_tracker:
            self.usage_tracker[key] = {"month": current_month, "count": 0}
        
        self.usage_tracker[key]["count"] += 1
        logger.info(f"📊 Usage updated for user {user_id}, agent {agent_id}: {self.usage_tracker[key]['count']}")

# Global agent engine instance
agent_engine = None

def get_agent_engine():
    """Get or create agent engine instance"""
    global agent_engine
    if agent_engine is None:
        agent_engine = AIAgentEngine()
    return agent_engine

def initialize_agent_engine():
    """Initialize agent engine for Flask app"""
    global agent_engine
    agent_engine = AIAgentEngine()
    logger.info("🚀 AI Agent Engine ready for production")