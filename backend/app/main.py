"""
Project Alfred - Backend API
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

from app.core.agent import CoreAgent
from app.core.tools import tool_registry

# Create FastAPI app
app = FastAPI(
    title="Project Alfred API",
    description="Next-generation AI agent API",
    version="0.2.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory agent storage (will be replaced with database in later sprints)
agents = {}


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    status: str
    task_id: str
    response: str
    user_id: str
    metadata: Optional[dict] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Project Alfred API is running",
        "version": "0.2.0",
        "core_engine": "operational"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    tools = tool_registry.list_tools()
    
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "pending",  # Will be implemented with Supabase
            "core_engine": "operational"
        },
        "tools_available": len(tools),
        "tools": [{"name": t.name, "category": t.category} for t in tools]
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user messages through the cognitive loop
    """
    # Generate or retrieve user_id
    user_id = request.user_id or str(uuid.uuid4())
    
    # Get or create agent for this user
    if user_id not in agents:
        agents[user_id] = CoreAgent(user_id=user_id)
    
    agent = agents[user_id]
    
    try:
        # Process the task through the cognitive loop
        result = agent.process_task(request.message)
        
        if result["status"] == "success":
            return ChatResponse(
                status="success",
                task_id=result["task_id"],
                response=result["response"],
                user_id=user_id,
                metadata=result.get("metadata")
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List all available tools"""
    tools = tool_registry.list_tools()
    return {
        "tools": [
            {
                "name": t.name,
                "description": t.description,
                "category": t.category,
                "parameters": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "description": p.description,
                        "required": p.required
                    }
                    for p in t.parameters
                ]
            }
            for t in tools
        ]
    }


@app.get("/conversation/{user_id}")
async def get_conversation(user_id: str):
    """Get conversation history for a user"""
    if user_id not in agents:
        raise HTTPException(status_code=404, detail="User not found")
    
    agent = agents[user_id]
    return {
        "user_id": user_id,
        "conversation_history": agent.world_model.conversation_history,
        "message_count": len(agent.world_model.conversation_history)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
