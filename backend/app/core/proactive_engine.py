"""
Project Alfred - Proactive Engine
Intelligent suggestion and anticipation system
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.core.digital_twin import digital_twin, UserProfile


class Suggestion:
    """Represents a proactive suggestion"""
    
    def __init__(
        self,
        suggestion_type: str,
        title: str,
        description: str,
        action: Optional[str] = None,
        priority: str = "medium",
        context: Optional[Dict[str, Any]] = None
    ):
        self.id = f"sug_{datetime.utcnow().timestamp()}"
        self.type = suggestion_type  # task, tool, reminder, insight, tip
        self.title = title
        self.description = description
        self.action = action  # Suggested action/command
        self.priority = priority  # low, medium, high
        self.context = context or {}
        self.created_at = datetime.utcnow()
        self.shown = False
        self.accepted = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "action": self.action,
            "priority": self.priority,
            "context": self.context,
            "created_at": self.created_at.isoformat()
        }


class ProactiveEngine:
    """
    Proactive Engine - Generates intelligent suggestions and anticipates user needs
    """
    
    def __init__(self):
        self.pending_suggestions: Dict[str, List[Suggestion]] = {}
        self.suggestion_history: Dict[str, List[Suggestion]] = {}
    
    def generate_suggestions(self, user_id: str, current_context: Optional[Dict[str, Any]] = None) -> List[Suggestion]:
        """Generate proactive suggestions for a user"""
        profile = digital_twin.get_profile(user_id)
        if not profile or not profile.should_be_proactive():
            return []
        
        suggestions = []
        current_context = current_context or {}
        
        # Tool suggestions based on usage patterns
        tool_suggestions = self._suggest_tools(profile, current_context)
        suggestions.extend(tool_suggestions)
        
        # Task suggestions based on patterns
        task_suggestions = self._suggest_tasks(profile, current_context)
        suggestions.extend(task_suggestions)
        
        # Contextual insights
        insights = self._generate_insights(profile, current_context)
        suggestions.extend(insights)
        
        # Tips and best practices
        tips = self._generate_tips(profile)
        suggestions.extend(tips)
        
        # Filter by frequency preference
        suggestions = self._filter_by_frequency(profile, suggestions)
        
        # Store pending suggestions
        if user_id not in self.pending_suggestions:
            self.pending_suggestions[user_id] = []
        self.pending_suggestions[user_id].extend(suggestions)
        
        return suggestions
    
    def _suggest_tools(self, profile: UserProfile, context: Dict[str, Any]) -> List[Suggestion]:
        """Suggest tools based on user patterns and context"""
        suggestions = []
        
        # If user frequently uses certain tools, suggest related ones
        common_tools = profile.get_most_used_tools(3)
        
        if "calculator" in common_tools and "data_analysis" not in common_tools:
            suggestions.append(Suggestion(
                suggestion_type="tool",
                title="Try Data Analysis",
                description="Since you use the calculator often, you might find the data analysis tool helpful for working with datasets.",
                action="Use data_analysis tool",
                priority="low",
                context={"related_tool": "calculator"}
            ))
        
        if "file_operations" in common_tools and "code_execution" not in common_tools:
            suggestions.append(Suggestion(
                suggestion_type="tool",
                title="Execute Code Directly",
                description="You can run Python code directly instead of saving to files first. Try the code execution tool.",
                action="Use code_execution tool",
                priority="low",
                context={"related_tool": "file_operations"}
            ))
        
        # Context-based tool suggestions
        recent_topics = profile.current_context.get("recent_topics", [])
        
        if any("search" in topic.lower() or "find" in topic.lower() for topic in recent_topics):
            if "web_search" not in common_tools:
                suggestions.append(Suggestion(
                    suggestion_type="tool",
                    title="Search the Web",
                    description="Looking for information? I can search the web for you using the web_search tool.",
                    action="Search for: [your query]",
                    priority="medium",
                    context={"trigger": "search_intent"}
                ))
        
        return suggestions
    
    def _suggest_tasks(self, profile: UserProfile, context: Dict[str, Any]) -> List[Suggestion]:
        """Suggest tasks based on patterns"""
        suggestions = []
        
        common_tasks = profile.get_common_task_types(3)
        
        # Suggest related tasks
        if "calculation" in common_tasks:
            suggestions.append(Suggestion(
                suggestion_type="task",
                title="Analyze Your Data",
                description="I notice you do calculations often. Would you like me to analyze a dataset for you?",
                action="Analyze data: [provide numbers]",
                priority="low",
                context={"pattern": "calculation"}
            ))
        
        if "file_management" in common_tasks:
            suggestions.append(Suggestion(
                suggestion_type="task",
                title="Organize Your Workspace",
                description="Want me to help organize your files? I can list, rename, or categorize them.",
                action="List all files",
                priority="low",
                context={"pattern": "file_management"}
            ))
        
        return suggestions
    
    def _generate_insights(self, profile: UserProfile, context: Dict[str, Any]) -> List[Suggestion]:
        """Generate insights about user behavior"""
        suggestions = []
        
        # Activity pattern insights
        peak_hours = profile.get_peak_activity_hours()
        if peak_hours:
            suggestions.append(Suggestion(
                suggestion_type="insight",
                title="Your Peak Hours",
                description=f"You're most active around {', '.join(map(str, peak_hours))}:00. I'm here whenever you need me!",
                priority="low",
                context={"peak_hours": peak_hours}
            ))
        
        # Tool usage insights
        total_tools = len(profile.history["tools_used"])
        if total_tools >= 3:
            suggestions.append(Suggestion(
                suggestion_type="insight",
                title="Tool Explorer",
                description=f"You've used {total_tools} different tools! You're making great use of my capabilities.",
                priority="low",
                context={"tools_count": total_tools}
            ))
        
        # Conversation insights
        if profile.history["total_messages"] >= 50:
            suggestions.append(Suggestion(
                suggestion_type="insight",
                title="Milestone Reached",
                description=f"We've exchanged {profile.history['total_messages']} messages! Our collaboration is growing.",
                priority="low",
                context={"messages": profile.history["total_messages"]}
            ))
        
        return suggestions
    
    def _generate_tips(self, profile: UserProfile) -> List[Suggestion]:
        """Generate helpful tips"""
        suggestions = []
        
        # Beginner tips
        if profile.history["total_messages"] < 20:
            suggestions.append(Suggestion(
                suggestion_type="tip",
                title="Pro Tip: Natural Language",
                description="You can ask me anything in natural language. No need for specific commands!",
                priority="low",
                context={"tip_type": "beginner"}
            ))
        
        # Feature discovery
        if "web_search" not in profile.history["tools_used"]:
            suggestions.append(Suggestion(
                suggestion_type="tip",
                title="Did You Know?",
                description="I can search the web for you. Just ask me to find information on any topic!",
                priority="low",
                context={"feature": "web_search"}
            ))
        
        if "code_execution" not in profile.history["tools_used"]:
            suggestions.append(Suggestion(
                suggestion_type="tip",
                title="Code Execution",
                description="I can run Python code for you. Try asking me to execute a script!",
                priority="low",
                context={"feature": "code_execution"}
            ))
        
        return suggestions
    
    def _filter_by_frequency(self, profile: UserProfile, suggestions: List[Suggestion]) -> List[Suggestion]:
        """Filter suggestions based on user's frequency preference"""
        frequency = profile.get_suggestion_frequency()
        
        if frequency == "rare":
            # Only high priority suggestions
            return [s for s in suggestions if s.priority == "high"]
        elif frequency == "moderate":
            # High and medium priority
            return [s for s in suggestions if s.priority in ["high", "medium"]]
        else:  # frequent
            # All suggestions
            return suggestions
    
    def get_pending_suggestions(self, user_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get pending suggestions for a user"""
        if user_id not in self.pending_suggestions:
            return []
        
        # Get unshown suggestions
        unshown = [s for s in self.pending_suggestions[user_id] if not s.shown]
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        unshown.sort(key=lambda s: priority_order.get(s.priority, 3))
        
        # Mark as shown
        for suggestion in unshown[:limit]:
            suggestion.shown = True
        
        return [s.to_dict() for s in unshown[:limit]]
    
    def accept_suggestion(self, user_id: str, suggestion_id: str):
        """Mark a suggestion as accepted"""
        if user_id in self.pending_suggestions:
            for suggestion in self.pending_suggestions[user_id]:
                if suggestion.id == suggestion_id:
                    suggestion.accepted = True
                    
                    # Move to history
                    if user_id not in self.suggestion_history:
                        self.suggestion_history[user_id] = []
                    self.suggestion_history[user_id].append(suggestion)
                    break
    
    def dismiss_suggestion(self, user_id: str, suggestion_id: str):
        """Dismiss a suggestion"""
        if user_id in self.pending_suggestions:
            self.pending_suggestions[user_id] = [
                s for s in self.pending_suggestions[user_id]
                if s.id != suggestion_id
            ]
    
    def get_contextual_prompt_enhancement(self, user_id: str, user_message: str) -> Optional[str]:
        """Generate contextual enhancement for LLM prompts based on user patterns"""
        profile = digital_twin.get_profile(user_id)
        if not profile:
            return None
        
        personalization = digital_twin.get_personalized_context(user_id)
        
        enhancement = f"""
User Context:
- Communication style: {personalization['communication_style']}
- Preferred response length: {personalization['response_length']}
- Common tools: {', '.join(personalization['common_tools']) if personalization['common_tools'] else 'None yet'}
- Interests: {', '.join(personalization['interests']) if personalization['interests'] else 'Learning'}
- Recent topics: {', '.join(personalization['recent_topics'][:3]) if personalization['recent_topics'] else 'New conversation'}
"""
        
        return enhancement.strip()


# Global proactive engine instance
proactive_engine = ProactiveEngine()
