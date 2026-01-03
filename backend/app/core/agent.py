"""
Project Alfred - Core Agent
State machine and lifecycle management for the cognitive loop
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from app.services.llm import llm_service
from app.core.tools import tool_registry
from app.core.digital_twin import digital_twin
from app.core.proactive_engine import proactive_engine


class AgentState(Enum):
    """Agent lifecycle states"""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    OBSERVING = "observing"
    ERROR = "error"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a user task"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_input: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class WorldModel:
    """Stateful context and knowledge about the user and environment"""
    user_id: str
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    tools_available: List[str] = field(default_factory=list)
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_context_summary(self) -> str:
        """Generate a summary of current context"""
        recent_messages = self.conversation_history[-5:] if len(self.conversation_history) > 5 else self.conversation_history
        return f"Recent conversation: {len(recent_messages)} messages. Available tools: {', '.join(self.tools_available)}"


class CoreAgent:
    """
    The core cognitive agent implementing the Analyze -> Plan -> Execute -> Observe loop
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.state = AgentState.IDLE
        self.world_model = WorldModel(user_id=user_id)
        self.current_task: Optional[Task] = None
        self.plan: Optional[List[Dict[str, Any]]] = None
        
    async def process_task(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point: Process a user task through the cognitive loop
        """
        # Create new task
        self.current_task = Task(user_input=user_input)
        self.world_model.add_message("user", user_input)
        
        try:
            # ANALYZE: Understand the task
            self._transition_to(AgentState.ANALYZING)
            analysis = await self._analyze()
            
            # PLAN: Create execution plan
            self._transition_to(AgentState.PLANNING)
            self.plan = await self._plan(analysis)
            
            # EXECUTE: Carry out the plan
            self._transition_to(AgentState.EXECUTING)
            execution_result = await self._execute(self.plan)
            
            # OBSERVE: Evaluate the result
            self._transition_to(AgentState.OBSERVING)
            observation = self._observe(execution_result)
            
            # Mark as complete
            self._transition_to(AgentState.COMPLETE)
            self.current_task.status = "complete"
            self.current_task.completed_at = datetime.now()
            self.current_task.result = observation
            
            # Add assistant response to world model
            self.world_model.add_message("assistant", observation.get("response", ""))
            
            return {
                "status": "success",
                "task_id": self.current_task.id,
                "response": observation.get("response"),
                "metadata": {
                    "analysis": analysis,
                    "plan": self.plan,
                    "execution": execution_result
                }
            }
            
        except Exception as e:
            self._transition_to(AgentState.ERROR)
            self.current_task.status = "error"
            self.current_task.error = str(e)
            
            return {
                "status": "error",
                "task_id": self.current_task.id,
                "error": str(e)
            }
    
    def _transition_to(self, new_state: AgentState):
        """Transition to a new state"""
        print(f"[Agent] {self.state.value} -> {new_state.value}")
        self.state = new_state
    
    async def _analyze(self) -> Dict[str, Any]:
        """
        ANALYZE phase: Understand the user's intent and context using LLM
        """
        user_input = self.current_task.user_input
        context = self.world_model.get_context_summary()
        
        # Get personalized context from Digital Twin
        personalization = proactive_engine.get_contextual_prompt_enhancement(self.user_id, user_input)
        enhanced_context = f"{context}\n\n{personalization}" if personalization else context
        
        # Use LLM to analyze intent
        analysis = await llm_service.analyze_intent(user_input, enhanced_context)
        
        return analysis
    
    async def _plan(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        PLAN phase: Create a step-by-step execution plan using LLM
        """
        user_input = self.current_task.user_input
        
        # Get available tools
        tools = tool_registry.list_tools()
        available_tools = [t.name for t in tools]
        
        # Use LLM to create plan
        plan = await llm_service.create_plan(user_input, analysis, available_tools)
        
        return plan
    
    async def _execute(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        EXECUTE phase: Carry out the plan step by step
        """
        results = []
        
        for step in plan:
            action = step.get("action")
            
            if action == "generate_response":
                # Generate response using LLM
                context = self.world_model.get_context_summary()
                response_text = await llm_service.generate_response(
                    self.current_task.user_input,
                    context,
                    {"previous_results": results}
                )
                result = {
                    "step": step["step"],
                    "success": True,
                    "output": response_text
                }
            elif action == "use_tool":
                # Execute a tool
                tool_name = step.get("tool")
                tool = tool_registry.get_tool(tool_name)
                
                if tool:
                    # Extract parameters
                    params = step.get("parameters", {})
                    if not params:
                        # Try to extract from user input
                        tool_metadata = tool.get_metadata()
                        params = await llm_service.extract_tool_parameters(
                            self.current_task.user_input,
                            tool_name,
                            [{
                                "name": p.name,
                                "type": p.type,
                                "description": p.description
                            } for p in tool_metadata.parameters]
                        )
                    
                    # Execute tool
                    tool_result = await tool.execute(**params)
                    result = {
                        "step": step["step"],
                        "success": tool_result.get("success", False),
                        "output": tool_result.get("output"),
                        "tool": tool_name
                    }
                else:
                    result = {
                        "step": step["step"],
                        "success": False,
                        "error": f"Tool not found: {tool_name}"
                    }
            else:
                result = {
                    "step": step["step"],
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
            
            results.append(result)
        
        return {
            "steps_completed": len(results),
            "results": results,
            "overall_success": all(r.get("success", False) for r in results)
        }
    
    def _observe(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        OBSERVE phase: Evaluate the execution and determine if task is complete
        """
        # Update Digital Twin with interaction data
        tools_used = [r.get("tool") for r in execution_result.get("results", []) if r.get("tool")]
        interaction_data = {
            "task_type": "general",
            "tools_used": tools_used,
            "topics": [],
            "intent": "task_completion"
        }
        digital_twin.update_profile(self.user_id, interaction_data)
        
        # Generate proactive suggestions
        suggestions = proactive_engine.generate_suggestions(self.user_id, {"current_task": self.current_task.user_input})
        
        if execution_result.get("overall_success"):
            # Extract the response from execution results
            response = execution_result["results"][0].get("output", "Task completed successfully.")
            
            return {
                "task_complete": True,
                "response": response,
                "confidence": 1.0,
                "follow_up_needed": False,
                "suggestions": [s.to_dict() for s in suggestions[:2]]  # Include top 2 suggestions
            }
        else:
            return {
                "task_complete": False,
                "response": "I encountered an issue while processing your request.",
                "confidence": 0.0,
                "follow_up_needed": True,
                "error": "Execution failed",
                "suggestions": []
            }
