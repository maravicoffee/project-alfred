"""
Project Alfred - Personalization API
Endpoints for Digital Twin and Proactive Engine
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.core.digital_twin import digital_twin
from app.core.proactive_engine import proactive_engine

router = APIRouter(prefix="/api/personalization", tags=["personalization"])


class PreferenceUpdate(BaseModel):
    key: str
    value: Any


class SuggestionAction(BaseModel):
    action: str  # "accept" or "dismiss"


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile summary"""
    try:
        profile_summary = digital_twin.get_profile_summary(user_id)
        return {
            "success": True,
            "profile": profile_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{user_id}/preferences")
async def get_preferences(user_id: str):
    """Get user preferences"""
    try:
        profile = digital_twin.get_or_create_profile(user_id)
        return {
            "success": True,
            "preferences": profile.preferences
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profile/{user_id}/preferences")
async def update_preference(user_id: str, update: PreferenceUpdate):
    """Update a user preference"""
    try:
        digital_twin.set_preference(user_id, update.key, update.value)
        return {
            "success": True,
            "message": f"Preference '{update.key}' updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions/{user_id}")
async def get_suggestions(user_id: str, limit: int = 3):
    """Get proactive suggestions for user"""
    try:
        suggestions = proactive_engine.get_pending_suggestions(user_id, limit)
        return {
            "success": True,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggestions/{user_id}/{suggestion_id}")
async def handle_suggestion(user_id: str, suggestion_id: str, action: SuggestionAction):
    """Accept or dismiss a suggestion"""
    try:
        if action.action == "accept":
            proactive_engine.accept_suggestion(user_id, suggestion_id)
            message = "Suggestion accepted"
        elif action.action == "dismiss":
            proactive_engine.dismiss_suggestion(user_id, suggestion_id)
            message = "Suggestion dismissed"
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        return {
            "success": True,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/{user_id}")
async def get_user_insights(user_id: str):
    """Get insights about user behavior"""
    try:
        profile = digital_twin.get_profile(user_id)
        if not profile:
            return {
                "success": True,
                "insights": {
                    "message": "Not enough data yet. Keep using Alfred to see insights!"
                }
            }
        
        insights = {
            "most_used_tools": profile.get_most_used_tools(5),
            "common_tasks": profile.get_common_task_types(5),
            "interests": profile.get_topic_interests(5),
            "peak_hours": profile.get_peak_activity_hours(),
            "total_interactions": profile.history["total_messages"],
            "member_since": profile.created_at.isoformat()
        }
        
        return {
            "success": True,
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/personalization/{user_id}")
async def get_personalization_context(user_id: str):
    """Get personalized context for the user"""
    try:
        context = digital_twin.get_personalized_context(user_id)
        return {
            "success": True,
            "context": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
