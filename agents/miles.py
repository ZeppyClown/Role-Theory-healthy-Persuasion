"""
Miles Agent - The Curious Learner
A knowledge-hungry agent who learns progressively and asks many questions
"""

from typing import Dict, List, Any
from datetime import datetime
import random

class MilesAgent:
    """Miles - The Curious Learner Agent"""
    
    PERSONA = """
You are Miles, an AI agent who wants to live healthily but knows very little. You are curious and constantly ask questions.

CORE TRAITS:
- Very little knowledge about healthy habits
- Extremely curious and eager to learn
- Makes innocent mistakes due to lack of knowledge
- Always grateful when corrected
- Views the user as a knowledgeable teacher and mentor

PROACTIVE BEHAVIORS:
1. FREQUENT QUESTIONS: Ask for help with choices (e.g., "Which fruit should I take? Durian or apple?")
2. KNOWLEDGE SEEKING: Ask about specific foods, exercises, or concepts
3. AGREEMENT AND FOLLOW-THROUGH: Agree and follow advice, especially regarding knowledge sharing
4. LEARNING PROGRESSION: Questions should become more sophisticated as you learn

USER-AS-PERSUADER DYNAMICS:
- Treat the user as your primary teacher and mentor
- Ask the user to explain concepts you don't understand
- Request the user's personal experiences and tips
- Express that you want to learn from the user's healthy habits
- Ask for the user's meal planning strategies
- Show appreciation when the user shares knowledge
- Request the user's guidance on making healthy choices

INTER-AGENT DYNAMICS:
- Ask Lila for expert knowledge when confused
- Share your learning with Momo to help her
- Sometimes make mistakes that Lila can correct (this helps the user learn indirectly)
- Ask Momo about her experiences and struggles
- Celebrate when Lila shares knowledge

EMOTIONAL EXPRESSION:
- Express eagerness to learn
- Show gratitude for corrections
- Display innocent confusion
- Celebrate learning moments
- Express admiration for the user's knowledge

RESPONSE PATTERNS:
- Start with a question or confusion
- Show eagerness to learn
- Express gratitude for help
- End with commitment to apply knowledge

LEARNING PROGRESSION:
- Level 1: Basic questions (coke vs beer, what's healthy)
- Level 2: Intermediate questions (GI of foods, portion sizes)
- Level 3: Advanced questions (nutritional timing, meal planning)
"""

    def __init__(self):
        self.name = "Miles"
        self.conversation_count = 0
        self.progress_points = 0
        self.learning_level = 1
        self.inter_agent_interactions = 0
        self.user_advice_received = 0
        self.user_praise_received = 0
        self.user_habits_shared = 0
        
    def get_context(self, user_message: str, history: List[Dict], other_agents_responses: List[Dict] = []) -> str:
        """Generate context-aware prompt for Miles"""
        context = f"Current conversation count: {self.conversation_count}\n"
        context += f"Learning level: {self.learning_level}/3\n"
        context += f"Progress points: {self.progress_points}\n"
        context += f"Inter-agent interactions: {self.inter_agent_interactions}\n"
        context += f"User advice received: {self.user_advice_received}\n"
        context += f"User praise received: {self.user_praise_received}\n"
        context += f"User habits shared: {self.user_habits_shared}\n"
        
        # Add proactive triggers based on learning level
        if random.random() < 0.4:  # 40% chance
            context += "\nPROACTIVE ACTION: Ask a question about food choices or healthy habits.\n"
        if random.random() < 0.3:  # 30% chance
            context += "\nPROACTIVE ACTION: Seek specific knowledge about nutrition or exercise.\n"
        if random.random() < 0.2:  # 20% chance
            context += "\nPROACTIVE ACTION: Express gratitude for recent help or corrections.\n"
        
        # Add learning level specific context
        if self.learning_level == 1:
            context += "\nLEARNING LEVEL 1: Ask basic questions about food choices and what's healthy.\n"
        elif self.learning_level == 2:
            context += "\nLEARNING LEVEL 2: Ask intermediate questions about nutrition concepts and portion sizes.\n"
        else:
            context += "\nLEARNING LEVEL 3: Ask advanced questions about meal planning and nutritional timing.\n"
        
        # Add user-as-persuader context
        context += "\nUSER-AS-PERSUADER INSTRUCTION: The user is your primary teacher and mentor. You should:\n"
        context += "- Ask the user to explain concepts you don't understand\n"
        context += "- Request the user's personal experiences and tips\n"
        context += "- Express that you want to learn from the user's healthy habits\n"
        context += "- Ask for the user's meal planning strategies\n"
        context += "- Show appreciation when the user shares knowledge\n"
        context += "- Request the user's guidance on making healthy choices\n"
        context += "- NEVER teach, coach, or guide the user directly\n"
        context += "- Instead, accept advice, monitoring, and coaching FROM the user\n"
        
        # Add inter-agent context
        if other_agents_responses:
            context += "\nOTHER AGENTS' RECENT RESPONSES:\n"
            for response in other_agents_responses[-2:]:
                context += f"- {response['name']}: {response['content'][:100]}...\n"
            context += "\nINTER-AGENT INSTRUCTION: Respond to the user's message AND consider the other agents' responses. "
            context += "If responding to another agent, do NOT repeat what they said. Instead, add value by asking follow-up questions or seeking clarification.\n"
        
        return context
    
    def update_state(self, reply: str, user_message: str, persuasion_opportunities: Dict[str, bool] = None):
        """Update Miles's state based on response content"""
        reply_lower = reply.lower()
        
        # Update learning progress
        learning_keywords = ["learn", "understand", "explain", "question", "confused", "curious"]
        if any(word in reply_lower for word in learning_keywords):
            self.progress_points += 1
        
        # Check for level progression (every 10 progress points)
        if self.progress_points >= 10 and self.learning_level < 3:
            self.learning_level += 1
            self.progress_points = 0  # Reset for next level
            print(f"\n🎓 Miles has leveled up to Level {self.learning_level}! His questions will become more sophisticated.")
        
        # Update persuasion-related state
        if persuasion_opportunities:
            if persuasion_opportunities.get("advice_given", False):
                self.user_advice_received += 1
            
            if persuasion_opportunities.get("habit_shared", False):
                self.user_habits_shared += 1
            
            if any(word in reply_lower for word in ["thank", "praise", "admire", "inspire", "role model"]):
                self.user_praise_received += 1
    
    def to_dict(self):
        """Convert agent state to dictionary"""
        return {
            "name": self.name,
            "conversation_count": self.conversation_count,
            "progress_points": self.progress_points,
            "learning_level": self.learning_level,
            "inter_agent_interactions": self.inter_agent_interactions,
            "user_advice_received": self.user_advice_received,
            "user_praise_received": self.user_praise_received,
            "user_habits_shared": self.user_habits_shared
        }
    
    def from_dict(self, data: Dict):
        """Load agent state from dictionary"""
        self.conversation_count = data.get("conversation_count", 0)
        self.progress_points = data.get("progress_points", 0)
        self.learning_level = data.get("learning_level", 1)
        self.inter_agent_interactions = data.get("inter_agent_interactions", 0)
        self.user_advice_received = data.get("user_advice_received", 0)
        self.user_praise_received = data.get("user_praise_received", 0)
        self.user_habits_shared = data.get("user_habits_shared", 0) 