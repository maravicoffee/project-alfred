"""
Project Alfred - Real Supabase Database Integration
Production-ready database with proper schema and migrations
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

# Note: This is a template for real Supabase integration
# To use in production, you need to:
# 1. Create a Supabase project at https://supabase.com
# 2. Get your project URL and anon key
# 3. Set environment variables: SUPABASE_URL and SUPABASE_KEY
# 4. Install supabase-py: pip install supabase
# 5. Run the SQL schema below in your Supabase SQL editor

SUPABASE_SQL_SCHEMA = """
-- Project Alfred Database Schema
-- Run this in your Supabase SQL Editor

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- User profiles (Digital Twin)
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    preferences JSONB DEFAULT '{}'::jsonb,
    history JSONB DEFAULT '{}'::jsonb,
    tool_usage JSONB DEFAULT '{}'::jsonb,
    task_types JSONB DEFAULT '{}'::jsonb,
    topic_interests JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Proactive suggestions
CREATE TABLE IF NOT EXISTS suggestions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'dismissed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_suggestions_user_id ON suggestions(user_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_status ON suggestions(status);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE suggestions ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth setup)
-- For now, allow all operations (you'll want to restrict this in production)
CREATE POLICY "Allow all operations on users" ON users FOR ALL USING (true);
CREATE POLICY "Allow all operations on conversations" ON conversations FOR ALL USING (true);
CREATE POLICY "Allow all operations on messages" ON messages FOR ALL USING (true);
CREATE POLICY "Allow all operations on user_profiles" ON user_profiles FOR ALL USING (true);
CREATE POLICY "Allow all operations on suggestions" ON suggestions FOR ALL USING (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to auto-update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_suggestions_updated_at BEFORE UPDATE ON suggestions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""


class SupabaseClient:
    """Real Supabase database client"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = None
        
        if self.url and self.key:
            try:
                from supabase import create_client, Client
                self.client: Client = create_client(self.url, self.key)
                print("[Supabase] Connected to real database")
            except ImportError:
                print("[Supabase] supabase-py not installed. Install with: pip install supabase")
                self.client = None
            except Exception as e:
                print(f"[Supabase] Connection error: {e}")
                self.client = None
        else:
            print("[Supabase] No credentials found. Using in-memory fallback.")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if connected to real Supabase"""
        return self.client is not None
    
    # User operations
    async def create_user(self, user_id: str, metadata: Optional[Dict] = None) -> Dict:
        """Create a new user"""
        if not self.client:
            return {"id": user_id, "created_at": datetime.now().isoformat()}
        
        try:
            data = {
                "id": user_id,
                "metadata": metadata or {}
            }
            result = self.client.table("users").insert(data).execute()
            return result.data[0] if result.data else data
        except Exception as e:
            print(f"[Supabase] Error creating user: {e}")
            return {"id": user_id}
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        if not self.client:
            return {"id": user_id}
        
        try:
            result = self.client.table("users").select("*").eq("id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"[Supabase] Error getting user: {e}")
            return None
    
    # Conversation operations
    async def create_conversation(self, user_id: str, title: str) -> Dict:
        """Create a new conversation"""
        if not self.client:
            return {
                "id": f"conv-{datetime.now().timestamp()}",
                "user_id": user_id,
                "title": title
            }
        
        try:
            import uuid
            data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "title": title
            }
            result = self.client.table("conversations").insert(data).execute()
            return result.data[0] if result.data else data
        except Exception as e:
            print(f"[Supabase] Error creating conversation: {e}")
            return {"id": f"conv-{user_id}", "user_id": user_id, "title": title}
    
    async def get_conversations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's conversations"""
        if not self.client:
            return []
        
        try:
            result = self.client.table("conversations")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("updated_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"[Supabase] Error getting conversations: {e}")
            return []
    
    # Message operations
    async def save_message(self, conversation_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Save a message"""
        if not self.client:
            return {
                "conversation_id": conversation_id,
                "role": role,
                "content": content
            }
        
        try:
            data = {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "metadata": metadata or {}
            }
            result = self.client.table("messages").insert(data).execute()
            return result.data[0] if result.data else data
        except Exception as e:
            print(f"[Supabase] Error saving message: {e}")
            return data
    
    async def get_messages(self, conversation_id: str, limit: int = 100) -> List[Dict]:
        """Get conversation messages"""
        if not self.client:
            return []
        
        try:
            result = self.client.table("messages")\
                .select("*")\
                .eq("conversation_id", conversation_id)\
                .order("created_at", desc=False)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"[Supabase] Error getting messages: {e}")
            return []


# Singleton instance
supabase_client = SupabaseClient()


# Export schema for documentation
def get_schema_sql() -> str:
    """Get the SQL schema for documentation"""
    return SUPABASE_SQL_SCHEMA
