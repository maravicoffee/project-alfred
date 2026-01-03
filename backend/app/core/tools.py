"""
Project Alfred - Tool System
Dynamic tool binding and execution
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ToolParameter:
    """Represents a tool parameter"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None


@dataclass
class ToolMetadata:
    """Metadata about a tool"""
    name: str
    description: str
    parameters: List[ToolParameter]
    category: str = "general"


class Tool(ABC):
    """Base class for all tools"""
    
    @abstractmethod
    def get_metadata(self) -> ToolMetadata:
        """Return tool metadata"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        pass


class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """Register a new tool"""
        metadata = tool.get_metadata()
        self.tools[metadata.name] = tool
        print(f"[ToolRegistry] Registered tool: {metadata.name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[ToolMetadata]:
        """List all available tools"""
        return [tool.get_metadata() for tool in self.tools.values()]
    
    def get_tools_by_category(self, category: str) -> List[Tool]:
        """Get all tools in a category"""
        return [
            tool for tool in self.tools.values()
            if tool.get_metadata().category == category
        ]


# Example tool implementations

class EchoTool(Tool):
    """Simple echo tool for testing"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="echo",
            description="Echoes back the input message",
            parameters=[
                ToolParameter(
                    name="message",
                    type="string",
                    description="The message to echo back"
                )
            ],
            category="utility"
        )
    
    async def execute(self, message: str, **kwargs) -> Dict[str, Any]:
        return {
            "success": True,
            "output": f"Echo: {message}"
        }


class CalculatorTool(Tool):
    """Simple calculator tool"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="calculator",
            description="Performs basic arithmetic operations",
            parameters=[
                ToolParameter(
                    name="operation",
                    type="string",
                    description="The operation to perform: add, subtract, multiply, divide"
                ),
                ToolParameter(
                    name="a",
                    type="number",
                    description="First number"
                ),
                ToolParameter(
                    name="b",
                    type="number",
                    description="Second number"
                )
            ],
            category="computation"
        )
    
    async def execute(self, operation: str, a: float, b: float, **kwargs) -> Dict[str, Any]:
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    return {"success": False, "error": "Division by zero"}
                result = a / b
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
            
            return {
                "success": True,
                "output": result,
                "operation": operation,
                "operands": [a, b]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global tool registry instance
tool_registry = ToolRegistry()

# Register default tools
tool_registry.register(EchoTool())
tool_registry.register(CalculatorTool())
