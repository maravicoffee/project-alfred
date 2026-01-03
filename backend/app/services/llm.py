"""
Project Alfred - LLM Service
OpenAI integration for intelligent analysis and planning
"""

import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI


class LLMService:
    """Service for interacting with OpenAI's LLM"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.model = "gpt-4o"  # Using GPT-4 for best results
    
    async def analyze_intent(self, user_input: str, context: str) -> Dict[str, Any]:
        """
        Analyze user intent and extract key information
        """
        system_prompt = """You are an AI assistant that analyzes user requests.
Your job is to understand what the user wants and extract key information.

Return a JSON object with:
- intent: The primary intent (e.g., "answer_question", "perform_calculation", "create_content")
- entities: List of important entities mentioned
- requires_tools: Boolean indicating if external tools are needed
- complexity: "simple", "medium", or "complex"
- summary: Brief summary of the request"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context: {context}\n\nUser request: {user_input}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            print(f"[LLM] Error in analyze_intent: {e}")
            # Fallback to simple analysis
            return {
                "intent": "respond_to_query",
                "entities": [],
                "requires_tools": False,
                "complexity": "simple",
                "summary": user_input[:100]
            }
    
    async def create_plan(self, user_input: str, analysis: Dict[str, Any], available_tools: List[str]) -> List[Dict[str, Any]]:
        """
        Create a step-by-step execution plan
        """
        system_prompt = f"""You are an AI assistant that creates execution plans.
Given a user request and analysis, create a step-by-step plan.

Available tools: {', '.join(available_tools)}

Return a JSON array of steps, where each step has:
- step: Step number
- action: The action to perform
- tool: Tool to use (or null if no tool needed)
- description: What this step accomplishes
- parameters: Parameters for the tool (if applicable)

Keep plans concise and efficient."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User request: {user_input}\n\nAnalysis: {json.dumps(analysis)}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            plan = result.get("steps", result.get("plan", []))
            
            # Ensure plan is a list
            if not isinstance(plan, list):
                plan = [plan]
            
            return plan
            
        except Exception as e:
            print(f"[LLM] Error in create_plan: {e}")
            # Fallback to simple plan
            return [{
                "step": 1,
                "action": "generate_response",
                "tool": None,
                "description": "Generate a response to the user"
            }]
    
    async def generate_response(self, user_input: str, context: str, execution_results: Dict[str, Any]) -> str:
        """
        Generate a natural language response based on execution results
        """
        system_prompt = """You are Alfred, an intelligent AI assistant.
You help users by understanding their requests, planning actions, and providing helpful responses.

Generate a natural, conversational response based on the execution results.
Be helpful, concise, and friendly."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User request: {user_input}\n\nContext: {context}\n\nExecution results: {json.dumps(execution_results)}\n\nGenerate a helpful response:"}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[LLM] Error in generate_response: {e}")
            return f"I processed your request: '{user_input}'. I'm Alfred, and I'm here to help!"
    
    async def extract_tool_parameters(self, user_input: str, tool_name: str, tool_params: List[Dict]) -> Dict[str, Any]:
        """
        Extract parameters for a specific tool from user input
        """
        system_prompt = f"""Extract parameters for the '{tool_name}' tool from the user's request.

Tool parameters: {json.dumps(tool_params)}

Return a JSON object with the extracted parameter values."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"[LLM] Error in extract_tool_parameters: {e}")
            return {}


# Global LLM service instance
llm_service = LLMService()
