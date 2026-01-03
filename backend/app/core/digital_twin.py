"""
Project Alfred - Digital Twin System
User modeling and personalization engine
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import json


class UserProfile:
    """Represents a user's digital twin - their preferences, patterns, and behaviors"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()
        
        # Explicit preferences set by user
        self.preferences = {
            "communication_style": "balanced",  # casual, professional, balanced
            "response_length": "medium",  # brief, medium, detailed
            "proactivity_level": "medium",  # low, medium, high
            "learning_enabled": True,
            "suggestion_frequency": "moderate"  # rare, moderate, frequent
        }
        
        # Learned patterns from behavior
        self.patterns = {
            "active_hours": [],  # Hours of day when user is most active
            "common_tasks": defaultdict(int),  # Task types and frequency
            "tool_usage": defaultdict(int),  # Tools used and frequency
            "topic_interests": defaultdict(int),  # Topics discussed
            "session_duration": [],  # Typical session lengths
            "response_time_preference": None  # Preferred response speed
        }
        
        # Interaction history summary
        self.history = {
            "total_conversations": 0,
            "total_messages": 0,
            "total_tasks_completed": 0,
            "tools_used": set(),
            "first_interaction": None,
            "last_interaction": None,
            "favorite_features": []
        }
        
        # Context and state
        self.current_context = {
            "active_project": None,
            "recent_topics": [],
            "pending_tasks": [],
            "last_query_intent": None
        }
    
    def update_from_interaction(self, interaction_data: Dict[str, Any]):
        """Learn from a user interaction"""
        self.last_updated = datetime.utcnow()
        
        # Update history
        if self.history["first_interaction"] is None:
            self.history["first_interaction"] = datetime.utcnow().isoformat()
        self.history["last_interaction"] = datetime.utcnow().isoformat()
        self.history["total_messages"] += 1
        
        # Learn from task type
        if "task_type" in interaction_data:
            self.patterns["common_tasks"][interaction_data["task_type"]] += 1
        
        # Learn from tool usage
        if "tools_used" in interaction_data:
            for tool in interaction_data["tools_used"]:
                self.patterns["tool_usage"][tool] += 1
                self.history["tools_used"].add(tool)
        
        # Learn from topics
        if "topics" in interaction_data:
            for topic in interaction_data["topics"]:
                self.patterns["topic_interests"][topic] += 1
        
        # Learn active hours
        current_hour = datetime.utcnow().hour
        self.patterns["active_hours"].append(current_hour)
        
        # Update context
        if "intent" in interaction_data:
            self.current_context["last_query_intent"] = interaction_data["intent"]
        
        if "topics" in interaction_data and interaction_data["topics"]:
            self.current_context["recent_topics"] = (
                interaction_data["topics"] + self.current_context["recent_topics"]
            )[:10]  # Keep last 10 topics
    
    def get_preferred_communication_style(self) -> str:
        """Get user's preferred communication style"""
        return self.preferences.get("communication_style", "balanced")
    
    def get_preferred_response_length(self) -> str:
        """Get user's preferred response length"""
        return self.preferences.get("response_length", "medium")
    
    def should_be_proactive(self) -> bool:
        """Determine if Alfred should be proactive with this user"""
        level = self.preferences.get("proactivity_level", "medium")
        return level in ["medium", "high"]
    
    def get_suggestion_frequency(self) -> str:
        """Get how often to show suggestions"""
        return self.preferences.get("suggestion_frequency", "moderate")
    
    def get_most_used_tools(self, limit: int = 5) -> List[str]:
        """Get user's most frequently used tools"""
        sorted_tools = sorted(
            self.patterns["tool_usage"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [tool for tool, _ in sorted_tools[:limit]]
    
    def get_common_task_types(self, limit: int = 5) -> List[str]:
        """Get user's most common task types"""
        sorted_tasks = sorted(
            self.patterns["common_tasks"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [task for task, _ in sorted_tasks[:limit]]
    
    def get_topic_interests(self, limit: int = 5) -> List[str]:
        """Get user's topic interests"""
        sorted_topics = sorted(
            self.patterns["topic_interests"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [topic for topic, _ in sorted_topics[:limit]]
    
    def get_peak_activity_hours(self) -> List[int]:
        """Get hours when user is most active"""
        if not self.patterns["active_hours"]:
            return []
        
        # Count frequency of each hour
        hour_counts = defaultdict(int)
        for hour in self.patterns["active_hours"]:
            hour_counts[hour] += 1
        
        # Get top 3 hours
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        return [hour for hour, _ in sorted_hours[:3]]
    
    def is_learning_enabled(self) -> bool:
        """Check if user has enabled learning"""
        return self.preferences.get("learning_enabled", True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary"""
        return {
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "preferences": self.preferences,
            "patterns": {
                "active_hours": self.patterns["active_hours"],
                "common_tasks": dict(self.patterns["common_tasks"]),
                "tool_usage": dict(self.patterns["tool_usage"]),
                "topic_interests": dict(self.patterns["topic_interests"]),
                "session_duration": self.patterns["session_duration"]
            },
            "history": {
                **self.history,
                "tools_used": list(self.history["tools_used"])
            },
            "current_context": self.current_context
        }


class DigitalTwin:
    """
    Digital Twin System - Manages user profiles and personalization
    """
    
    def __init__(self):
        self.profiles: Dict[str, UserProfile] = {}
    
    def get_or_create_profile(self, user_id: str) -> UserProfile:
        """Get existing profile or create new one"""
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(user_id)
        return self.profiles[user_id]
    
    def update_profile(self, user_id: str, interaction_data: Dict[str, Any]):
        """Update user profile based on interaction"""
        profile = self.get_or_create_profile(user_id)
        if profile.is_learning_enabled():
            profile.update_from_interaction(interaction_data)
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile"""
        return self.profiles.get(user_id)
    
    def set_preference(self, user_id: str, key: str, value: Any):
        """Set a user preference"""
        profile = self.get_or_create_profile(user_id)
        profile.preferences[key] = value
        profile.last_updated = datetime.utcnow()
    
    def get_personalized_context(self, user_id: str) -> Dict[str, Any]:
        """Get personalized context for LLM prompts"""
        profile = self.get_or_create_profile(user_id)
        
        return {
            "communication_style": profile.get_preferred_communication_style(),
            "response_length": profile.get_preferred_response_length(),
            "common_tools": profile.get_most_used_tools(3),
            "common_tasks": profile.get_common_task_types(3),
            "interests": profile.get_topic_interests(3),
            "recent_topics": profile.current_context["recent_topics"][:5],
            "proactivity_enabled": profile.should_be_proactive()
        }
    
    def get_profile_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user profile for display"""
        profile = self.get_or_create_profile(user_id)
        
        return {
            "user_id": user_id,
            "member_since": profile.created_at.isoformat(),
            "total_conversations": profile.history["total_conversations"],
            "total_messages": profile.history["total_messages"],
            "favorite_tools": profile.get_most_used_tools(5),
            "interests": profile.get_topic_interests(5),
            "preferences": profile.preferences,
            "peak_hours": profile.get_peak_activity_hours()
        }


# Global digital twin instance
digital_twin = DigitalTwin()
