"""
Project Alfred - Core Agent
State machine and lifecycle management for the cognitive loop
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid


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
        
    def process_task(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point: Process a user task through the cognitive loop
        """
        # Create new task
        self.current_task = Task(user_input=user_input)
        self.world_model.add_message("user", user_input)
        
        try:
            # ANALYZE: Understand the task
            self._transition_to(AgentState.ANALYZING)
            analysis = self._analyze()
            
            # PLAN: Create execution plan
            self._transition_to(AgentState.PLANNING)
            self.plan = self._plan(analysis)
            
            # EXECUTE: Carry out the plan
            self._transition_to(AgentState.EXECUTING)
            execution_result = self._execute(self.plan)
            
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
    
    def _analyze(self) -> Dict[str, Any]:
        """
        ANALYZE phase: Understand the user's intent and context
        """
        user_input = self.current_task.user_input
        context = self.world_model.get_context_summary()
        
        # Simple analysis for now (will be enhanced with LLM in later sprints)
        analysis = {
            "intent": "respond_to_query",  # Placeholder
            "entities": [],
            "context_relevant": True,
            "requires_tools": False,
            "complexity": "simple"
        }
        
        return analysis
    
    def _plan(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        PLAN phase: Create a step-by-step execution plan
        """
        # Simple planning for now (will be enhanced with LLM in later sprints)
        plan = [
            {
                "step": 1,
                "action": "generate_response",
                "tool": None,
                "description": "Generate a response to the user"
            }
        ]
        
        return plan
    
    def _execute(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        EXECUTE phase: Carry out the plan step by step
        """
        results = []
        
        for step in plan:
            action = step.get("action")
            
            if action == "generate_response":
                # Simple response generation (will be enhanced with LLM)
                result = {
                    "step": step["step"],
                    "success": True,
                    "output": f"I received your message: '{self.current_task.user_input}'. I'm Alfred, and I'm here to help!"
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
        if execution_result.get("overall_success"):
            # Extract the response from execution results
            response = execution_result["results"][0].get("output", "Task completed successfully.")
            
            return {
                "task_complete": True,
                "response": response,
                "confidence": 1.0,
                "follow_up_needed": False
            }
        else:
            return {
                "task_complete": False,
                "response": "I encountered an issue while processing your request.",
                "confidence": 0.0,
                "follow_up_needed": True,
                "error": "Execution failed"
            }
