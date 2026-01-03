"""
Project Alfred - Supabase Database Client
Handles all database operations using Supabase
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class SupabaseClient:
    """
    Supabase client for database operations
    Using a simple in-memory store for now (free tier simulation)
    Will be replaced with actual Supabase when credentials are provided
    """
    
    def __init__(self):
        # In-memory storage (simulating database)
        self.users = {}
        self.conversations = {}
        self.messages = {}
        self.user_preferences = {}
        
    async def create_user(self, user_id: str, email: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new user"""
        user = {
            "id": user_id,
            "email": email,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        self.users[user_id] = user
        return user
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Create a new conversation"""
        import uuid
        conversation_id = str(uuid.uuid4())
        
        conversation = {
            "id": conversation_id,
            "user_id": user_id,
            "title": title or "New Conversation",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append(conversation)
        
        return conversation
    
    async def get_conversations(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all conversations for a user"""
        user_convos = self.conversations.get(user_id, [])
        return sorted(user_convos, key=lambda x: x["updated_at"], reverse=True)[:limit]
    
    async def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific conversation"""
        for user_convos in self.conversations.values():
            for convo in user_convos:
                if convo["id"] == conversation_id:
                    return convo
        return None
    
    async def save_message(self, conversation_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Save a message to a conversation"""
        import uuid
        message_id = str(uuid.uuid4())
        
        message = {
            "id": message_id,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        if conversation_id not in self.messages:
            self.messages[conversation_id] = []
        self.messages[conversation_id].append(message)
        
        return message
    
    async def get_messages(self, conversation_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all messages in a conversation"""
        convo_messages = self.messages.get(conversation_id, [])
        return sorted(convo_messages, key=lambda x: x["created_at"])[:limit]
    
    async def save_user_preference(self, user_id: str, key: str, value: Any) -> Dict[str, Any]:
        """Save a user preference"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        self.user_preferences[user_id][key] = {
            "value": value,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        return self.user_preferences[user_id][key]
    
    async def get_user_preference(self, user_id: str, key: str) -> Optional[Any]:
        """Get a user preference"""
        user_prefs = self.user_preferences.get(user_id, {})
        pref = user_prefs.get(key)
        return pref["value"] if pref else None
    
    async def get_all_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get all preferences for a user"""
        user_prefs = self.user_preferences.get(user_id, {})
        return {k: v["value"] for k, v in user_prefs.items()}
    
    async def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """Update conversation title"""
        for user_convos in self.conversations.values():
            for convo in user_convos:
                if convo["id"] == conversation_id:
                    convo["title"] = title
                    convo["updated_at"] = datetime.utcnow().isoformat()
                    return True
        return False
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and all its messages"""
        # Delete messages
        if conversation_id in self.messages:
            del self.messages[conversation_id]
        
        # Delete conversation
        for user_id, user_convos in self.conversations.items():
            for i, convo in enumerate(user_convos):
                if convo["id"] == conversation_id:
                    del self.conversations[user_id][i]
                    return True
        return False


# Global database client instance
db_client = SupabaseClient()
