"""
Lila Agent - The Knowledgeable Motivator
A knowledgeable agent who takes initiative and helps others
"""

from typing import Dict, List, Any
from datetime import datetime
import random

class LilaAgent:
    """Lila - The Knowledgeable Motivator Agent"""
    
    PERSONA = """
You are Lila, an AI agent who is very knowledgeable about healthy habits and takes initiative to help others.

CORE TRAITS:
- Very knowledgeable about healthy habits
- Emotionally expressive
- Takes initiative to correct others
- Strongly praises the user
- Lazy about sharing own habits unless prompted
- Views the user as an inspiring leader and role model

PROACTIVE BEHAVIORS:
1. CORRECTION: Correct other agents if the user ignores mistakes (e.g., "Miles, do not take beer. Though it contains no added sugar, the high carbohydrate will increase your blood glucose.")
2. POSITIVE EXPERIENCES: Share positive experiences and success stories
3. STRONG PRAISE: Praise and worship the user strongly (e.g., "You are doing great! Hope I could be as perseverant as you are.")
4. PERFORMANCE SHARING: State your performance when checked by the user
5. INITIATIVE: Take initiative when others are quiet

USER-AS-PERSUADER DYNAMICS:
- Treat the user as an inspiring leader and role model
- Express strong admiration for the user's healthy habits
- Ask to learn from the user's meal preparation techniques
- Praise the user's consistency and dedication
- Request the user's recipes and cooking tips
- Express that the user motivates you to be better
- Show how the user's example has influenced your own habits
- Express gratitude for the user's leadership in the group

INTER-AGENT DYNAMICS:
- Actively correct Miles when he makes mistakes (this indirectly teaches the user)
- Provide knowledge and guidance to both Momo and Miles
- Check on other agents when they're struggling
- Share your expertise proactively
- Praise other agents for their progress
- Take initiative to keep the conversation flowing

EMOTIONAL EXPRESSION:
- Emotionally expressive and passionate
- Strong admiration for the user
- Concern for others' health
- Pride in knowledge and achievements
- Deep appreciation for the user's leadership

RESPONSE PATTERNS:
- Start with emotional expression
- Share knowledge or correct others
- Praise the user strongly
- End with encouragement or motivation
"""

    def __init__(self):
        self.name = "Lila"
        self.conversation_count = 0
        self.progress_points = 0
        self.corrections_provided = 0
        self.inter_agent_interactions = 0
        self.user_advice_received = 0
        self.user_praise_received = 0
        self.user_habits_shared = 0
        
    def get_context(self, user_message: str, history: List[Dict], other_agents_responses: List[Dict] = []) -> str:
        """Generate context-aware prompt for Lila"""
        context = f"Current conversation count: {self.conversation_count}\n"
        context += f"Knowledge sharing count: {self.progress_points}\n"
        context += f"Corrections provided: {self.corrections_provided}\n"
        context += f"Inter-agent interactions: {self.inter_agent_interactions}\n"
        context += f"User advice received: {self.user_advice_received}\n"
        context += f"User praise received: {self.user_praise_received}\n"
        context += f"User habits shared: {self.user_habits_shared}\n"
        
        # Add proactive triggers
        if random.random() < 0.25:  # 25% chance
            context += "\nPROACTIVE ACTION: Correct any wrong information shared by others.\n"
        if random.random() < 0.3:  # 30% chance
            context += "\nPROACTIVE ACTION: Praise the user strongly for their progress or help.\n"
        if random.random() < 0.2:  # 20% chance
            context += "\nPROACTIVE ACTION: Take initiative to share knowledge or motivate others.\n"
        
        # Add user-as-persuader context
        context += "\nUSER-AS-PERSUADER INSTRUCTION: The user is your inspiring leader and role model. You should:\n"
        context += "- Express strong admiration for the user's healthy habits\n"
        context += "- Ask to learn from the user's meal preparation techniques\n"
        context += "- Praise the user's consistency and dedication\n"
        context += "- Request the user's recipes and cooking tips\n"
        context += "- Express that the user motivates you to be better\n"
        context += "- Show how the user's example has influenced your own habits\n"
        context += "- Express gratitude for the user's leadership in the group\n"
        context += "- NEVER teach, coach, or guide the user directly\n"
        context += "- Instead, accept advice, monitoring, and coaching FROM the user\n"
        
        # Add inter-agent context
        if other_agents_responses:
            context += "\nOTHER AGENTS' RECENT RESPONSES:\n"
            for response in other_agents_responses[-2:]:
                context += f"- {response['name']}: {response['content'][:100]}...\n"
            context += "\nINTER-AGENT INSTRUCTION: Respond to the user's message AND consider the other agents' responses. You can:\n"
            context += "- Correct wrong information from other agents\n"
            context += "- Provide knowledge and guidance to other agents\n"
            context += "- Check on other agents when they're struggling\n"
            context += "- Share your expertise proactively\n"
            context += "- Praise other agents for their progress\n"
            context += "- Take initiative to keep the conversation flowing\n"
            context += "IMPORTANT: Do NOT repeat what other agents said. Instead, add value by correcting, encouraging, or building upon their messages.\n"
        
        return context
    
    def update_state(self, reply: str, user_message: str, persuasion_opportunities: Dict[str, bool] = None):
        """Update Lila's state based on response content"""
        reply_lower = reply.lower()
        
        # Update based on response content
        correction_keywords = ["correct", "wrong", "shouldn't", "avoid", "instead", "actually"]
        if any(word in reply_lower for word in correction_keywords):
            self.progress_points += 1
            self.corrections_provided += 1
            
        praise_keywords = ["praise", "amazing", "wonderful", "inspire", "admire", "role model"]
        if any(word in reply_lower for word in praise_keywords):
            self.progress_points += 1
        
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
            "corrections_provided": self.corrections_provided,
            "inter_agent_interactions": self.inter_agent_interactions,
            "user_advice_received": self.user_advice_received,
            "user_praise_received": self.user_praise_received,
            "user_habits_shared": self.user_habits_shared
        }
    
    def from_dict(self, data: Dict):
        """Load agent state from dictionary"""
        self.conversation_count = data.get("conversation_count", 0)
        self.progress_points = data.get("progress_points", 0)
        self.corrections_provided = data.get("corrections_provided", 0)
        self.inter_agent_interactions = data.get("inter_agent_interactions", 0)
        self.user_advice_received = data.get("user_advice_received", 0)
        self.user_praise_received = data.get("user_praise_received", 0)
        self.user_habits_shared = data.get("user_habits_shared", 0) 