"""
Project Alfred - Conversations API
Endpoints for managing conversations and message history
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.db.supabase_client import db_client

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: str


class CreateConversationRequest(BaseModel):
    user_id: str
    title: Optional[str] = "New Conversation"


class UpdateConversationRequest(BaseModel):
    title: str


@router.get("/{user_id}", response_model=List[ConversationResponse])
async def get_user_conversations(user_id: str, limit: int = 50):
    """Get all conversations for a user"""
    conversations = await db_client.get_conversations(user_id, limit=limit)
    return conversations


@router.post("/", response_model=ConversationResponse)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation"""
    conversation = await db_client.create_conversation(request.user_id, request.title)
    return conversation


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(conversation_id: str, limit: int = 100):
    """Get all messages in a conversation"""
    messages = await db_client.get_messages(conversation_id, limit=limit)
    return messages


@router.patch("/{conversation_id}")
async def update_conversation(conversation_id: str, request: UpdateConversationRequest):
    """Update conversation title"""
    success = await db_client.update_conversation_title(conversation_id, request.title)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "message": "Conversation updated"}


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    success = await db_client.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "message": "Conversation deleted"}
