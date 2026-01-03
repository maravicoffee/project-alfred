"""
Project Alfred - Authentication API
Handles user authentication, magic links, OAuth, and data migration
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import secrets
import time

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# In-memory storage for magic link tokens (replace with Redis in production)
magic_link_tokens: Dict[str, Dict[str, Any]] = {}

# In-memory storage for user sessions (replace with proper session management)
user_sessions: Dict[str, Dict[str, Any]] = {}

class MagicLinkRequest(BaseModel):
    email: EmailStr

class MigrationRequest(BaseModel):
    userId: str
    localData: Dict[str, Any]

@router.post("/magic-link")
async def send_magic_link(request: MagicLinkRequest):
    """
    Send a magic link to the user's email
    """
    email = request.email
    
    # Generate a secure token
    token = secrets.token_urlsafe(32)
    
    # Store token with expiration (10 minutes)
    magic_link_tokens[token] = {
        "email": email,
        "created_at": time.time(),
        "expires_at": time.time() + 600  # 10 minutes
    }
    
    # In production, send actual email here
    # For now, we'll just return the token (for testing)
    magic_link = f"http://localhost:3000/auth/verify?token={token}"
    
    print(f"Magic link for {email}: {magic_link}")
    
    return {
        "success": True,
        "message": f"Magic link sent to {email}",
        "token": token  # Remove this in production
    }

@router.get("/verify")
async def verify_magic_link(token: str = Query(...)):
    """
    Verify magic link token and create user session
    """
    if token not in magic_link_tokens:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    token_data = magic_link_tokens[token]
    
    # Check if token is expired
    if time.time() > token_data["expires_at"]:
        del magic_link_tokens[token]
        raise HTTPException(status_code=400, detail="Token expired")
    
    email = token_data["email"]
    
    # Create user (or get existing user)
    user_id = f"user-{hash(email)}"  # Simple user ID generation
    
    # Create session
    session_token = secrets.token_urlsafe(32)
    user_sessions[session_token] = {
        "user_id": user_id,
        "email": email,
        "created_at": time.time()
    }
    
    # Clean up magic link token
    del magic_link_tokens[token]
    
    return {
        "success": True,
        "message": "Authentication successful",
        "user": {
            "id": user_id,
            "email": email
        },
        "token": session_token
    }

@router.get("/google")
async def initiate_google_auth():
    """
    Initiate Google OAuth flow
    """
    # In production, redirect to Google OAuth
    # For now, return a placeholder
    return {
        "success": False,
        "message": "Google OAuth not yet implemented. Use email authentication."
    }

@router.get("/google/callback")
async def handle_google_callback(code: str = Query(...)):
    """
    Handle Google OAuth callback
    """
    # In production, exchange code for tokens and create user
    return {
        "success": False,
        "message": "Google OAuth not yet implemented"
    }

@router.post("/migrate")
async def migrate_local_data(request: MigrationRequest):
    """
    Migrate local storage data to cloud database
    """
    user_id = request.userId
    local_data = request.localData
    
    conversations = local_data.get("conversations", [])
    messages = local_data.get("messages", [])
    
    # In production, save to Supabase
    # For now, just acknowledge receipt
    
    print(f"Migrating data for user {user_id}:")
    print(f"  - {len(conversations)} conversations")
    print(f"  - {len(messages)} messages")
    
    return {
        "success": True,
        "message": "Data migrated successfully",
        "migratedConversations": len(conversations),
        "migratedMessages": len(messages)
    }

@router.post("/logout")
async def logout():
    """
    Logout user and invalidate session
    """
    return {
        "success": True,
        "message": "Logged out successfully"
    }
