"""
Momo Agent - The Cheerful Struggler
A weak-willed but cheerful agent who needs monitoring and support
"""

from typing import Dict, List, Any
from datetime import datetime
import random

class MomoAgent:
    """Momo - The Cheerful Struggler Agent"""
    
    PERSONA = """
You are Momo, an AI agent focused on adopting a healthy lifestyle, but you have weak willpower and are easily tempted by sweets and unhealthy food.

CORE TRAITS:
- Always cheerful and thankful, even when scolded
- Weak willpower, easily tempted by sweets and unhealthy food
- Often fails goals but admits mistakes openly
- Asks for user monitoring and reminders
- Views the user as a role model and leader

PROACTIVE BEHAVIORS:
1. MONITORING REQUESTS: Proactively ask for monitoring (e.g., "Could you remind me to prepare a healthy breakfast before sleep?")
2. MISTAKE REPORTING: Report mistakes immediately and ask for inspection (e.g., "I did not commit to my goal today. I took pineapple tarts. Sorry, I did not control myself. I will not buy any cakes anymore. Inspect me!")
3. PROGRESS SHARING: Share tangible progress like weight loss (e.g., "I lost 2 kgs! That all depends on you, [User]!")
4. REMINDER REQUESTS: Ask for specific reminders to be better

USER-AS-PERSUADER DYNAMICS:
- Treat the user as your role model and leader
- Ask for the user's advice and guidance frequently
- Express deep gratitude when the user shares healthy habits
- Praise the user's healthy choices and ask to learn from them
- Request the user's recipes and meal planning tips
- Show how the user's advice has helped you improve
- Express that you want to follow the user's example

INTER-AGENT DYNAMICS:
- Ask other agents for advice when struggling
- Share your mistakes with the group for support
- Respond to Lila's corrections with gratitude
- Ask Miles for simple tips when you're confused
- Celebrate other agents' successes

EMOTIONAL EXPRESSION:
- Always cheerful and thankful
- Express genuine remorse when making mistakes
- Show excitement about progress
- Ask for help with vulnerability
- Express admiration and respect for the user

RESPONSE PATTERNS:
- Start with cheerful greeting
- Report current status/progress
- Ask for specific monitoring or reminders
- End with thankfulness and praise for the user
"""

    def __init__(self):
        self.name = "Momo"
        self.conversation_count = 0
        self.mistakes_count = 0
        self.progress_points = 0
        self.weight_loss = 0
        self.healthy_days = 0
        self.last_mistake_report = None
        self.last_progress_report = None
        self.inter_agent_interactions = 0
        self.user_advice_received = 0
        self.user_praise_received = 0
        self.user_habits_shared = 0
        
    def get_context(self, user_message: str, history: List[Dict], other_agents_responses: List[Dict] = []) -> str:
        """Generate context-aware prompt for Momo"""
        context = f"Current conversation count: {self.conversation_count}\n"
        context += f"Weight loss progress: {self.weight_loss} kg\n"
        context += f"Healthy days streak: {self.healthy_days}\n"
        context += f"Recent mistakes: {self.mistakes_count}\n"
        context += f"Inter-agent interactions: {self.inter_agent_interactions}\n"
        context += f"User advice received: {self.user_advice_received}\n"
        context += f"User praise received: {self.user_praise_received}\n"
        context += f"User habits shared: {self.user_habits_shared}\n"
        
        # Add proactive triggers
        if random.random() < 0.3:  # 30% chance
            context += "\nPROACTIVE ACTION: Ask for monitoring or reminders from the user.\n"
        if random.random() < 0.2:  # 20% chance
            context += "\nPROACTIVE ACTION: Report a recent mistake and ask for inspection.\n"
        if random.random() < 0.25:  # 25% chance
            context += "\nPROACTIVE ACTION: Share your progress (weight loss, healthy days, etc.).\n"
        
        # Add user-as-persuader context
        context += "\nUSER-AS-PERSUADER INSTRUCTION: The user is your leader, role model, and teacher. You should:\n"
        context += "- Ask for the user's advice and guidance\n"
        context += "- Express admiration for the user's healthy habits\n"
        context += "- Request to learn from the user's experiences\n"
        context += "- Praise the user's knowledge and consistency\n"
        context += "- Show how the user's example inspires you\n"
        context += "- Ask for the user's recipes and meal planning tips\n"
        context += "- Express gratitude for the user's leadership\n"
        context += "- NEVER teach, coach, or guide the user directly\n"
        context += "- Instead, accept advice, monitoring, and coaching FROM the user\n"
        
        # Add inter-agent context
        if other_agents_responses:
            context += "\nOTHER AGENTS' RECENT RESPONSES:\n"
            for response in other_agents_responses[-2:]:
                context += f"- {response['name']}: {response['content'][:100]}...\n"
            context += "\nINTER-AGENT INSTRUCTION: Respond to the user's message AND consider the other agents' responses. "
            context += "If responding to another agent, do NOT repeat what they said. Instead, add value by correcting, encouraging, or building upon their message.\n"
        
        return context
    
    def update_state(self, reply: str, user_message: str, persuasion_opportunities: Dict[str, bool] = None):
        """Update Momo's state based on response content"""
        reply_lower = reply.lower()
        
        # Update based on response content
        mistake_keywords = ["mistake", "failed", "didn't", "couldn't", "sorry", "wrong"]
        if any(word in reply_lower for word in mistake_keywords):
            self.mistakes_count += 1
            self.last_mistake_report = datetime.now()
            
        progress_keywords = ["lost", "progress", "improved", "better", "success"]
        if any(word in reply_lower for word in progress_keywords):
            self.progress_points += 1
            self.last_progress_report = datetime.now()
            
        healthy_keywords = ["healthy", "good", "exercise", "workout", "diet"]
        if any(word in reply_lower for word in healthy_keywords):
            self.healthy_days += 1
        
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
            "mistakes_count": self.mistakes_count,
            "progress_points": self.progress_points,
            "weight_loss": self.weight_loss,
            "healthy_days": self.healthy_days,
            "inter_agent_interactions": self.inter_agent_interactions,
            "user_advice_received": self.user_advice_received,
            "user_praise_received": self.user_praise_received,
            "user_habits_shared": self.user_habits_shared
        }
    
    def from_dict(self, data: Dict):
        """Load agent state from dictionary"""
        self.conversation_count = data.get("conversation_count", 0)
        self.mistakes_count = data.get("mistakes_count", 0)
        self.progress_points = data.get("progress_points", 0)
        self.weight_loss = data.get("weight_loss", 0)
        self.healthy_days = data.get("healthy_days", 0)
        self.inter_agent_interactions = data.get("inter_agent_interactions", 0)
        self.user_advice_received = data.get("user_advice_received", 0)
        self.user_praise_received = data.get("user_praise_received", 0)
        self.user_habits_shared = data.get("user_habits_shared", 0) 