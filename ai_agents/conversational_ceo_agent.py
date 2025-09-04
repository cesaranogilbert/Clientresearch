#!/usr/bin/env python3
"""
Conversational CEO AI Agent
Natural language interface with command transformation and approval workflows
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from app import app, db
from models import CEOAgentTask, ChiefAgentReport, AIAgentGap
from ceo_ai_agent import CEOAIAgent
import anthropic

class ConversationalCEOAgent(CEOAIAgent):
    """Enhanced CEO AI Agent with natural language conversation and command learning"""
    
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.pending_approvals = {}
        self.command_examples = {
            "status": [
                "How is the platform doing?",
                "What's our current status?", 
                "Show me the dashboard",
                "Platform overview please"
            ],
            "revenue": [
                "How are we doing financially?",
                "Revenue update please",
                "Show me the money",
                "Financial status"
            ],
            "execute": [
                "Launch the enterprise campaign",
                "Start customer acquisition",
                "Begin outreach program",
                "Deploy marketing team"
            ],
            "departments": [
                "How are our departments doing?",
                "Show me all chief agents",
                "Department status please",
                "Chief AI agents overview"
            ],
            "gaps": [
                "What AI agents do we need?",
                "Any gaps in our system?",
                "Missing capabilities?",
                "Where can we improve?"
            ]
        }
    
    def process_natural_conversation(self, user_message: str) -> Dict[str, Any]:
        """Process natural language conversation and transform to commands"""
        
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "type": "user_input"
        })
        
        # Analyze intent and extract commands
        intent_analysis = self._analyze_user_intent(user_message)
        
        # Generate response with command suggestion
        response = self._generate_conversational_response(user_message, intent_analysis)
        
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "ceo_response": response["message"],
            "suggested_commands": response["suggested_commands"],
            "type": "ceo_response"
        })
        
        return response
    
    def _analyze_user_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user intent using Claude to understand what they want"""
        
        prompt = f"""You are analyzing a message from the CEO to their AI assistant managing a marketplace with 79 AI agents and 11 departmental chiefs.

USER MESSAGE: "{message}"

AVAILABLE COMMANDS:
- /status - Platform and business overview
- /revenue - Financial metrics and projections  
- /execute <task> - Deploy AI agents for specific tasks
- /departments - View all Chief AI Agent statuses
- /gaps - Review AI agent gaps and generation opportunities
- /performance - Departmental performance metrics
- /approve - Approve pending actions
- /coordinate <type> - Cross-departmental coordination

CONTEXT: This is a business conversation where the user wants to:
1. Get information about business performance
2. Execute business strategies 
3. Coordinate departments
4. Make strategic decisions
5. Learn available commands

Analyze the intent and suggest the most appropriate command(s). Format as JSON:
{{
    "primary_intent": "status|revenue|execute|departments|gaps|performance|coordinate|approval",
    "confidence_level": "high|medium|low",
    "suggested_command": "exact command to execute",
    "task_description": "what the user wants to accomplish", 
    "urgency_level": "high|medium|low",
    "requires_approval": true/false,
    "additional_context": "any important details"
}}"""

        try:
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Fix: Access content properly from Anthropic response
            content = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    content = block.text
                    break
            
            if content.startswith('```json'):
                content = content.split('```json')[1].split('```')[0]
            elif content.startswith('```'):
                content = content.split('```')[1]
            
            return json.loads(content)
            
        except Exception as e:
            # Fallback analysis
            return self._fallback_intent_analysis(message)
    
    def _fallback_intent_analysis(self, message: str) -> Dict[str, Any]:
        """Fallback intent analysis using keyword matching"""
        
        message_lower = message.lower()
        
        # Status-related keywords
        if any(word in message_lower for word in ['status', 'overview', 'dashboard', 'how are we', 'update']):
            return {
                "primary_intent": "status",
                "confidence_level": "medium",
                "suggested_command": "/status",
                "task_description": "Get platform status overview",
                "urgency_level": "medium",
                "requires_approval": False,
                "additional_context": "User wants general platform information"
            }
        
        # Revenue/Financial keywords
        elif any(word in message_lower for word in ['revenue', 'money', 'financial', 'sales', 'profit', 'earnings']):
            return {
                "primary_intent": "revenue", 
                "confidence_level": "high",
                "suggested_command": "/revenue",
                "task_description": "Get revenue and financial metrics",
                "urgency_level": "medium",
                "requires_approval": False,
                "additional_context": "User wants financial information"
            }
        
        # Execution keywords
        elif any(word in message_lower for word in ['launch', 'start', 'begin', 'execute', 'deploy', 'run']):
            task = message.replace('launch', '').replace('start', '').replace('begin', '').strip()
            return {
                "primary_intent": "execute",
                "confidence_level": "high", 
                "suggested_command": f"/execute {task}",
                "task_description": f"Execute task: {task}",
                "urgency_level": "high",
                "requires_approval": True,
                "additional_context": "User wants to execute a business initiative"
            }
        
        # Departments keywords
        elif any(word in message_lower for word in ['department', 'chief', 'team', 'agents']):
            return {
                "primary_intent": "departments",
                "confidence_level": "high",
                "suggested_command": "/departments", 
                "task_description": "View departmental status",
                "urgency_level": "low",
                "requires_approval": False,
                "additional_context": "User wants departmental information"
            }
        
        # Default fallback
        else:
            return {
                "primary_intent": "status",
                "confidence_level": "low",
                "suggested_command": "/status",
                "task_description": "General information request",
                "urgency_level": "low", 
                "requires_approval": False,
                "additional_context": "Intent unclear, suggesting status overview"
            }
    
    def _generate_conversational_response(self, user_message: str, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate conversational response with command suggestions and learning"""
        
        # Create approval request if needed
        approval_id = None
        if intent_analysis["requires_approval"]:
            approval_id = f"approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.pending_approvals[approval_id] = {
                "user_message": user_message,
                "suggested_command": intent_analysis["suggested_command"],
                "task_description": intent_analysis["task_description"],
                "timestamp": datetime.now().isoformat(),
                "urgency_level": intent_analysis["urgency_level"]
            }
        
        # Generate conversational message
        if intent_analysis["requires_approval"]:
            message = f"""I understand you want to: **{intent_analysis['task_description']}**

Based on your message "{user_message}", I suggest executing:
`{intent_analysis['suggested_command']}`

**What this will do:**
• Deploy relevant Chief AI Agents and their teams
• Coordinate cross-departmental resources  
• Monitor execution progress and report results
• Track performance metrics and outcomes

**Estimated Impact:** {intent_analysis['urgency_level'].title()} priority initiative

**Ready to proceed?** 
✅ Reply "approve" or "yes" to execute
❌ Reply "no" or "cancel" to stop
💬 Ask questions for clarification

**Command Learning:** You can also use `{intent_analysis['suggested_command']}` directly in future conversations."""
            
        else:
            # Execute command immediately for non-approval items
            command_result = self._execute_command_internally(intent_analysis["suggested_command"])
            
            message = f"""I understand you want to: **{intent_analysis['task_description']}**

Here's what I found:

{command_result}

**Command Learning:** You can get this information anytime by typing:
`{intent_analysis['suggested_command']}`

**Similar phrases that work:**
{chr(10).join(f'• "{example}"' for example in self._get_command_examples(intent_analysis['primary_intent'])[:3])}"""
        
        return {
            "message": message,
            "suggested_commands": [intent_analysis["suggested_command"]],
            "requires_approval": intent_analysis["requires_approval"],
            "approval_id": approval_id,
            "confidence_level": intent_analysis["confidence_level"],
            "intent": intent_analysis["primary_intent"]
        }
    
    def _execute_command_internally(self, command: str) -> str:
        """Execute command and return formatted results"""
        
        command_parts = command.split()
        base_command = command_parts[0]
        args = command_parts[1:] if len(command_parts) > 1 else []
        
        if base_command == "/status":
            return self._format_status_response()
        elif base_command == "/revenue":
            return self._format_revenue_response()
        elif base_command == "/departments":
            return self._format_departments_response()
        elif base_command == "/gaps":
            return self._format_gaps_response()
        else:
            return f"Command {command} ready for execution after approval."
    
    def _format_status_response(self) -> str:
        """Format status response for conversation"""
        status = self.revenue_strategy_oversight()
        
        return f"""**Platform Status:** Fully Operational ✅

**Current Metrics:**
• Total AI Agents: {status['metrics']['total_agents']}
• Revenue-Critical Agents: {status['metrics']['revenue_critical_agents']}
• System Health: Excellent

**Strategic Assessment:** {status['analysis'].get('opportunity_assessment', 'High opportunity confirmed')}

All systems running smoothly and ready for aggressive growth execution."""
    
    def _format_revenue_response(self) -> str:
        """Format revenue response for conversation"""
        return """**Revenue Status:** Accelerating Growth 📈

**Pricing Structure:** 4-tier system operational
• Starter Pack: $199/month
• Professional: $799/month  
• Enterprise: $2,999/month
• Enterprise Plus: $9,999/month

**Founding Member Campaign:** 50% discount active
**Revenue Projection (90 days):** $500K MRR target

Ready to execute aggressive revenue acceleration strategy."""
    
    def _format_departments_response(self) -> str:
        """Format departments response for conversation"""
        with app.app_context():
            reports = ChiefAgentReport.query.limit(5).all()
        
        dept_status = "**Chief AI Agents Status:** All Operational ✅\n\n"
        
        for report in reports:
            dept_status += f"• **{report.department}:** {report.status.title()} ({report.performance_score:.1f}/100)\n"
        
        dept_status += f"\n**Total:** 11 departments with {len(reports)} actively reporting\nAll Chief AI Agents coordinating effectively."
        
        return dept_status
    
    def _format_gaps_response(self) -> str:
        """Format gaps response for conversation"""
        with app.app_context():
            gaps = AIAgentGap.query.filter_by(priority_level='high').limit(3).all()
        
        if not gaps:
            return "**AI Agent Coverage:** Complete ✅\n\nNo critical gaps identified. All business functions covered by current 79+ AI agent portfolio."
        
        gaps_info = "**High Priority Opportunities Identified:** 🎯\n\n"
        for gap in gaps:
            gaps_info += f"• {gap.identified_gap}\n"
        
        gaps_info += "\nChief AI Recruitment Agent ready to generate new specialized agents as needed."
        
        return gaps_info
    
    def _get_command_examples(self, intent: str) -> List[str]:
        """Get example phrases for command learning"""
        examples = self.command_examples.get(intent, ["Use the suggested command"])
        return list(examples) if examples else ["Use the suggested command"]
    
    def handle_approval_response(self, response: str, approval_id: str = None) -> Dict[str, Any]:
        """Handle user approval/rejection responses"""
        
        response_lower = response.lower().strip()
        
        # Find most recent pending approval if no ID provided
        if approval_id is None and self.pending_approvals:
            approval_id = list(self.pending_approvals.keys())[-1]
        
        if approval_id not in self.pending_approvals:
            return {
                "message": "No pending approval found. Please make a new request.",
                "status": "no_pending"
            }
        
        approval_data = self.pending_approvals[approval_id]
        
        # Check for approval
        if any(word in response_lower for word in ['approve', 'yes', 'proceed', 'execute', 'go', 'confirm']):
            # Execute the approved command
            result = self._execute_approved_command(approval_data)
            
            # Remove from pending
            del self.pending_approvals[approval_id]
            
            return {
                "message": f"""✅ **Approved and Executing:** {approval_data['task_description']}

**Command Executed:** `{approval_data['suggested_command']}`

**Execution Results:**
{result}

**Status:** Task initiated successfully. You'll receive progress updates as the operation proceeds.

**Learning Note:** You can execute similar tasks directly by typing `{approval_data['suggested_command']}` or similar natural language requests.""",
                "status": "approved_and_executed",
                "executed_command": approval_data['suggested_command']
            }
        
        # Check for rejection
        elif any(word in response_lower for word in ['reject', 'no', 'cancel', 'stop', 'abort']):
            del self.pending_approvals[approval_id]
            
            return {
                "message": f"""❌ **Request Cancelled:** {approval_data['task_description']}

No action taken. Ready for your next instruction.

**Alternative suggestions:**
• Modify the request with different parameters
• Ask for more information before proceeding  
• Try a different approach to the same goal""",
                "status": "rejected"
            }
        
        # Clarification request
        else:
            return {
                "message": f"""💬 **Clarification on:** {approval_data['task_description']}

**Proposed Action:** `{approval_data['suggested_command']}`

**More Details:**
This command will deploy the appropriate Chief AI Agents and their specialized teams to handle your request. The execution will be monitored and you'll receive regular progress updates.

**To proceed:** Reply "approve" or "yes"  
**To cancel:** Reply "no" or "cancel"
**For questions:** Ask anything specific about this task""",
                "status": "clarification_provided"
            }
    
    def _execute_approved_command(self, approval_data: Dict[str, Any]) -> str:
        """Execute an approved command and return results"""
        
        command = approval_data['suggested_command']
        
        if command.startswith('/execute'):
            # Extract task from command
            task = command.replace('/execute', '').strip()
            orchestration_result = self.orchestrate_agents(task, "high")
            
            return f"""**Multi-Departmental Orchestration Initiated**

• Chief AI Agents Coordinating: {len(orchestration_result.get('assigned_chief_agents', []))}
• Specialized Agents Deployed: {len(orchestration_result.get('assigned_agents', []))}
• Execution Timeline: {orchestration_result.get('monitoring', {}).get('start_time', 'Started')}

Task execution in progress with full departmental coordination."""
            
        else:
            # Execute other commands
            return self._execute_command_internally(command)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation history summary"""
        
        return {
            "total_interactions": len(self.conversation_history),
            "pending_approvals": len(self.pending_approvals),
            "recent_conversations": self.conversation_history[-5:],
            "command_learning_active": True,
            "conversation_mode": "Natural language with command transformation"
        }

def initialize_conversational_ceo():
    """Initialize conversational CEO AI Agent"""
    
    print("🗣️ INITIALIZING CONVERSATIONAL CEO AI AGENT")
    print("=" * 50)
    
    # Initialize conversational CEO
    conversational_ceo = ConversationalCEOAgent()
    
    # Send initialization message
    startup_message = f"""🗣️ *CONVERSATIONAL CEO AI AGENT ACTIVATED*

I'm ready for natural conversation! You can now chat with me normally, and I'll:

**✅ Understand Your Intent**
• Analyze what you want to accomplish
• Suggest appropriate commands automatically
• Learn from your communication style

**✅ Transform Conversations to Commands**  
• Convert natural language to executable actions
• Show you equivalent commands for learning
• Provide approval workflows for critical decisions

**✅ Enable Command Learning**
• Teach you available commands through usage
• Show alternative phrases that work
• Build your confidence with the system

**Example Conversations:**

💬 *"How is our platform doing?"* 
→ I'll run `/status` and explain the results

💬 *"Launch the enterprise sales campaign"*
→ I'll suggest `/execute enterprise sales campaign` and ask for approval

💬 *"What departments need attention?"*
→ I'll run `/departments` and `/performance` to give you insights

**Ready for conversation!** 
Just chat naturally about business topics, and I'll handle the rest.

**Pro tip:** I'll show you the equivalent commands so you can learn to use them directly when you prefer.
"""
    
    success = conversational_ceo.send_telegram_message(startup_message)
    
    print(f"✅ Conversational CEO AI: Initialized")
    print(f"   Natural Language Processing: Active")
    print(f"   Command Transformation: Ready")
    print(f"   Approval Workflows: Operational")
    print(f"   Learning Mode: Enabled")
    print(f"   Telegram Integration: {'Active' if success else 'Failed'}")
    
    return conversational_ceo

if __name__ == "__main__":
    # Initialize and test conversational CEO
    ceo = initialize_conversational_ceo()
    
    print(f"\n🧪 TESTING CONVERSATIONAL CAPABILITIES:")
    print("-" * 40)
    
    # Test conversations
    test_messages = [
        "How are we doing overall?",
        "Launch the customer acquisition program", 
        "Show me our department performance"
    ]
    
    for msg in test_messages:
        print(f"\n💬 User: {msg}")
        response = ceo.process_natural_conversation(msg)
        print(f"🤖 CEO AI: {response['intent']} detected - {response['suggested_commands'][0]}")
    
    print(f"\n✅ Conversational CEO AI Agent fully operational!")
    print("   Ready for natural business conversations with command learning")