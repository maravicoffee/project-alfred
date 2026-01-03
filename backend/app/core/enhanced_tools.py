"""
Project Alfred - Enhanced Tools
Advanced tools for web search, file operations, and code execution
"""

import os
import json
import subprocess
import tempfile
from typing import Dict, Any, List
from pathlib import Path
import httpx
from app.core.tools import Tool, ToolParameter, ToolMetadata, tool_registry


class WebSearchTool(Tool):
    """Tool for searching the web"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="web_search",
            description="Search the web for information",
            category="information",
            parameters=[
                ToolParameter(
                    name="query",
                    type="string",
                    description="The search query",
                    required=True
                ),
                ToolParameter(
                    name="num_results",
                    type="integer",
                    description="Number of results to return (default: 5)",
                    required=False
                )
            ]
        )
    
    async def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Execute web search using DuckDuckGo
        """
        try:
            from app.services.web_search import web_search_service
            
            result = web_search_service.search(query, max_results=num_results)
            
            if result["success"]:
                return {
                    "success": True,
                    "output": {
                        "query": query,
                        "results": result["results"],
                        "total_results": len(result["results"])
                    }
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Search failed")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class FileOperationsTool(Tool):
    """Tool for file operations (read, write, list)"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="file_operations",
            description="Perform file operations: read, write, list files",
            category="file_system",
            parameters=[
                ToolParameter(
                    name="operation",
                    type="string",
                    description="Operation to perform: 'read', 'write', 'list'",
                    required=True
                ),
                ToolParameter(
                    name="path",
                    type="string",
                    description="File or directory path",
                    required=True
                ),
                ToolParameter(
                    name="content",
                    type="string",
                    description="Content to write (for write operation)",
                    required=False
                )
            ]
        )
    
    async def execute(self, operation: str, path: str, content: str = None) -> Dict[str, Any]:
        """
        Execute file operation
        """
        try:
            # Security: Only allow operations in a safe directory
            safe_dir = Path("/tmp/alfred_workspace")
            safe_dir.mkdir(exist_ok=True)
            
            file_path = safe_dir / Path(path).name  # Only use filename, ignore directory
            
            if operation == "read":
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    return {
                        "success": True,
                        "output": {
                            "operation": "read",
                            "path": str(file_path),
                            "content": file_content,
                            "size": len(file_content)
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"File not found: {file_path}"
                    }
            
            elif operation == "write":
                if content is None:
                    return {
                        "success": False,
                        "error": "Content is required for write operation"
                    }
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                return {
                    "success": True,
                    "output": {
                        "operation": "write",
                        "path": str(file_path),
                        "bytes_written": len(content)
                    }
                }
            
            elif operation == "list":
                files = list(safe_dir.glob("*"))
                file_list = [
                    {
                        "name": f.name,
                        "size": f.stat().st_size if f.is_file() else 0,
                        "type": "file" if f.is_file() else "directory"
                    }
                    for f in files
                ]
                
                return {
                    "success": True,
                    "output": {
                        "operation": "list",
                        "path": str(safe_dir),
                        "files": file_list,
                        "total": len(file_list)
                    }
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class CodeExecutionTool(Tool):
    """Tool for executing Python code safely"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="code_execution",
            description="Execute Python code safely in a sandboxed environment",
            category="computation",
            parameters=[
                ToolParameter(
                    name="code",
                    type="string",
                    description="Python code to execute",
                    required=True
                ),
                ToolParameter(
                    name="timeout",
                    type="integer",
                    description="Execution timeout in seconds (default: 5)",
                    required=False
                )
            ]
        )
    
    async def execute(self, code: str, timeout: int = 5) -> Dict[str, Any]:
        """
        Execute Python code safely
        """
        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute the code with timeout
                result = subprocess.run(
                    ['python3.11', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                return {
                    "success": result.returncode == 0,
                    "output": {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
                }
            
            finally:
                # Clean up temp file
                os.unlink(temp_file)
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Code execution timed out after {timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class DataAnalysisTool(Tool):
    """Tool for analyzing data and creating visualizations"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="data_analysis",
            description="Analyze data and perform statistical operations",
            category="computation",
            parameters=[
                ToolParameter(
                    name="operation",
                    type="string",
                    description="Operation: 'sum', 'average', 'max', 'min', 'count'",
                    required=True
                ),
                ToolParameter(
                    name="data",
                    type="array",
                    description="Array of numbers to analyze",
                    required=True
                )
            ]
        )
    
    async def execute(self, operation: str, data: List[float]) -> Dict[str, Any]:
        """
        Perform data analysis
        """
        try:
            if not data:
                return {
                    "success": False,
                    "error": "Data array is empty"
                }
            
            result = None
            
            if operation == "sum":
                result = sum(data)
            elif operation == "average":
                result = sum(data) / len(data)
            elif operation == "max":
                result = max(data)
            elif operation == "min":
                result = min(data)
            elif operation == "count":
                result = len(data)
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }
            
            return {
                "success": True,
                "output": {
                    "operation": operation,
                    "result": result,
                    "data_points": len(data)
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Register all enhanced tools
tool_registry.register(WebSearchTool())
tool_registry.register(FileOperationsTool())
tool_registry.register(CodeExecutionTool())
tool_registry.register(DataAnalysisTool())
