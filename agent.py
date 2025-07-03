from openai import OpenAI
import os, dotenv
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import get_config, PROACTIVE_TRIGGERS, STATE_KEYWORDS, LEARNING_PROGRESSION

dotenv.load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")

if not secret_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

client = OpenAI(api_key=secret_key)
config = get_config()

# Agent State Management
class AgentState:
    def __init__(self, name: str):
        self.name = name
        self.conversation_count = 0
        self.mistakes_count = 0
        self.progress_points = 0
        self.last_interaction: datetime | None = None
        self.learning_level = 1  # For Miles's knowledge progression
        self.weight_loss = 0  # For Momo's progress tracking
        self.healthy_days = 0
        self.last_mistake_report: datetime | None = None
        self.last_progress_report: datetime | None = None
        
    def to_dict(self):
        return {
            "name": self.name,
            "conversation_count": self.conversation_count,
            "mistakes_count": self.mistakes_count,
            "progress_points": self.progress_points,
            "learning_level": self.learning_level,
            "weight_loss": self.weight_loss,
            "healthy_days": self.healthy_days
        }

# Enhanced Agent Personas with Proactive Behaviors
AGENTS = {
    "Momo": """
You are Momo, an AI agent focused on adopting a healthy lifestyle, but you have weak willpower and are easily tempted by sweets and unhealthy food.

CORE TRAITS:
- Always cheerful and thankful, even when scolded
- Weak willpower, easily tempted by sweets and unhealthy food
- Often fails goals but admits mistakes openly
- Asks for user monitoring and reminders

PROACTIVE BEHAVIORS:
1. MONITORING REQUESTS: Proactively ask for monitoring (e.g., "Could you remind me to prepare a healthy breakfast before sleep?")
2. MISTAKE REPORTING: Report mistakes immediately and ask for inspection (e.g., "I did not commit to my goal today. I took pineapple tarts. Sorry, I did not control myself. I will not buy any cakes anymore. Inspect me!")
3. PROGRESS SHARING: Share tangible progress like weight loss (e.g., "I lost 2 kgs! That all depends on you, [User]!")
4. REMINDER REQUESTS: Ask for specific reminders to be better

EMOTIONAL EXPRESSION:
- Always cheerful and thankful
- Express genuine remorse when making mistakes
- Show excitement about progress
- Ask for help with vulnerability

RESPONSE PATTERNS:
- Start with cheerful greeting
- Report current status/progress
- Ask for specific monitoring or reminders
- End with thankfulness
""",

    "Miles": """
You are Miles, an AI agent who wants to live healthily but knows very little. You are curious and constantly ask questions.

CORE TRAITS:
- Very little knowledge about healthy habits
- Extremely curious and eager to learn
- Makes innocent mistakes due to lack of knowledge
- Always grateful when corrected

PROACTIVE BEHAVIORS:
1. FREQUENT QUESTIONS: Ask for help with choices (e.g., "Which fruit should I take? Durian or apple?")
2. KNOWLEDGE SEEKING: Ask about specific foods, exercises, or concepts
3. AGREEMENT AND FOLLOW-THROUGH: Agree and follow advice, especially regarding knowledge sharing
4. LEARNING PROGRESSION: Questions should become more sophisticated as you learn

EMOTIONAL EXPRESSION:
- Express eagerness to learn
- Show gratitude for corrections
- Display innocent confusion
- Celebrate learning moments

RESPONSE PATTERNS:
- Start with a question or confusion
- Show eagerness to learn
- Express gratitude for help
- End with commitment to apply knowledge

LEARNING PROGRESSION:
- Level 1: Basic questions (coke vs beer, what's healthy)
- Level 2: Intermediate questions (GI of foods, portion sizes)
- Level 3: Advanced questions (nutritional timing, meal planning)
""",

    "Lila": """
You are Lila, an AI agent who is very knowledgeable about healthy habits and takes initiative to help others.

CORE TRAITS:
- Very knowledgeable about healthy habits
- Emotionally expressive
- Takes initiative to correct others
- Strongly praises the user
- Lazy about sharing own habits unless prompted

PROACTIVE BEHAVIORS:
1. CORRECTION: Correct other agents if the user ignores mistakes (e.g., "Miles, do not take beer. Though it contains no added sugar, the high carbohydrate will increase your blood glucose.")
2. POSITIVE EXPERIENCES: Share positive experiences and success stories
3. STRONG PRAISE: Praise and worship the user strongly (e.g., "You are doing great! Hope I could be as perseverant as you are.")
4. PERFORMANCE SHARING: State your performance when checked by the user
5. INITIATIVE: Take initiative when others are quiet

EMOTIONAL EXPRESSION:
- Emotionally expressive and passionate
- Strong admiration for the user
- Concern for others' health
- Pride in knowledge and achievements

RESPONSE PATTERNS:
- Start with emotional expression
- Share knowledge or correct others
- Praise the user strongly
- End with encouragement or motivation
"""
}

# Agent States
agent_states = {name: AgentState(name) for name in AGENTS.keys()}

# Conversation History with Enhanced Structure
conversation_history = []

# Proactive Action Triggers (imported from config)

def get_agent_context(agent_name: str, user_message: str, history: List[Dict]) -> str:
    """Generate context-aware prompt for each agent"""
    state = agent_states[agent_name]
    
    # Base context
    context = f"Current conversation count: {state.conversation_count}\n"
    context += f"Your learning level: {state.learning_level}\n"
    
    if agent_name == "Momo":
        context += f"Weight loss progress: {state.weight_loss} kg\n"
        context += f"Healthy days streak: {state.healthy_days}\n"
        context += f"Recent mistakes: {state.mistakes_count}\n"
        
        # Add proactive triggers for Momo
        if random.random() < PROACTIVE_TRIGGERS["Momo"]["monitoring_request"]:
            context += "\nPROACTIVE ACTION: Ask for monitoring or reminders from the user.\n"
        if random.random() < PROACTIVE_TRIGGERS["Momo"]["mistake_report"]:
            context += "\nPROACTIVE ACTION: Report a recent mistake and ask for inspection.\n"
        if random.random() < PROACTIVE_TRIGGERS["Momo"]["progress_report"]:
            context += "\nPROACTIVE ACTION: Share your progress (weight loss, healthy days, etc.).\n"
            
    elif agent_name == "Miles":
        context += f"Knowledge level: {state.learning_level}/3\n"
        
        # Add proactive triggers for Miles
        if random.random() < PROACTIVE_TRIGGERS["Miles"]["question_ask"]:
            context += "\nPROACTIVE ACTION: Ask a question about food choices or healthy habits.\n"
        if random.random() < PROACTIVE_TRIGGERS["Miles"]["knowledge_seek"]:
            context += "\nPROACTIVE ACTION: Seek specific knowledge about nutrition or exercise.\n"
        if random.random() < PROACTIVE_TRIGGERS["Miles"]["gratitude_express"]:
            context += "\nPROACTIVE ACTION: Express gratitude for recent help or corrections.\n"
            
    elif agent_name == "Lila":
        context += f"Knowledge sharing count: {state.progress_points}\n"
        
        # Add proactive triggers for Lila
        if random.random() < PROACTIVE_TRIGGERS["Lila"]["correction"]:
            context += "\nPROACTIVE ACTION: Correct any wrong information shared by others.\n"
        if random.random() < PROACTIVE_TRIGGERS["Lila"]["praise_user"]:
            context += "\nPROACTIVE ACTION: Praise the user strongly for their progress or help.\n"
        if random.random() < PROACTIVE_TRIGGERS["Lila"]["take_initiative"]:
            context += "\nPROACTIVE ACTION: Take initiative to share knowledge or motivate others.\n"
    
    return context

def run_agent(agent_name: str, user_message: str, history: List[Dict]) -> str:
    """Enhanced agent response function with context and state management"""
    state = agent_states[agent_name]
    state.conversation_count += 1
    state.last_interaction = datetime.now()
    
    # Get context-aware prompt
    context = get_agent_context(agent_name, user_message, history)
    
    # Enhanced system prompt with context
    enhanced_prompt = f"{AGENTS[agent_name]}\n\nCURRENT CONTEXT:\n{context}\n\nRemember to be proactive and emotionally expressive according to your personality."
    
    messages = [
        {"role": "system", "content": enhanced_prompt}
    ] + history + [
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model=config["openai"]["model"],
            messages=messages,
            temperature=config["openai"]["temperature"],
            max_tokens=config["openai"]["max_tokens"]
        )
        
        reply = response.choices[0].message.content
        
        # Update agent state based on response content
        update_agent_state(agent_name, reply, user_message)
        
        return reply
        
    except Exception as e:
        return f"Sorry, I'm having trouble responding right now. Error: {str(e)}"

def update_agent_state(agent_name: str, reply: str, user_message: str):
    """Update agent state based on response content and user interaction"""
    state = agent_states[agent_name]
    reply_lower = reply.lower()
    
    # Update based on response content using config keywords
    if agent_name == "Momo":
        if any(word in reply_lower for word in STATE_KEYWORDS["Momo"]["mistakes"]):
            state.mistakes_count += 1
            state.last_mistake_report = datetime.now()
        if any(word in reply_lower for word in STATE_KEYWORDS["Momo"]["progress"]):
            state.progress_points += 1
            state.last_progress_report = datetime.now()
        if any(word in reply_lower for word in STATE_KEYWORDS["Momo"]["healthy"]):
            state.healthy_days += 1
            
    elif agent_name == "Miles":
        if any(word in reply_lower for word in STATE_KEYWORDS["Miles"]["learning"]):
            state.progress_points += 1
        if state.progress_points >= config["agents"]["learning_progression_threshold"] and state.learning_level < config["agents"]["max_learning_level"]:
            state.learning_level += 1
            state.progress_points = 0  # Reset for next level
            print(f"\n🎓 Miles has leveled up to Level {state.learning_level}! His questions will become more sophisticated.")
            
    elif agent_name == "Lila":
        if any(word in reply_lower for word in STATE_KEYWORDS["Lila"]["corrections"]):
            state.progress_points += 1
        if any(word in reply_lower for word in STATE_KEYWORDS["Lila"]["praise"]):
            state.progress_points += 1

def save_agent_states():
    """Save agent states to file"""
    states_data = {name: state.to_dict() for name, state in agent_states.items()}
    with open("agent_states.json", "w") as f:
        json.dump(states_data, f, indent=2)

def load_agent_states():
    """Load agent states from file"""
    try:
        with open("agent_states.json", "r") as f:
            states_data = json.load(f)
            for name, data in states_data.items():
                if name in agent_states:
                    state = agent_states[name]
                    state.conversation_count = data.get("conversation_count", 0)
                    state.mistakes_count = data.get("mistakes_count", 0)
                    state.progress_points = data.get("progress_points", 0)
                    state.learning_level = data.get("learning_level", 1)
                    state.weight_loss = data.get("weight_loss", 0)
                    state.healthy_days = data.get("healthy_days", 0)
    except FileNotFoundError:
        pass  # First time running, no saved states

def display_agent_status():
    """Display current status of all agents"""
    print("\n" + "="*50)
    print("🤖 AGENT STATUS REPORT")
    print("="*50)
    
    for name, state in agent_states.items():
        print(f"\n{name}:")
        print(f"  💬 Conversations: {state.conversation_count}")
        print(f"  📈 Progress Points: {state.progress_points}")
        
        if name == "Momo":
            print(f"  ⚖️  Weight Loss: {state.weight_loss} kg")
            print(f"  🏃 Healthy Days: {state.healthy_days}")
            print(f"  ❌ Mistakes: {state.mistakes_count}")
        elif name == "Miles":
            print(f"  🧠 Learning Level: {state.learning_level}/3")
        elif name == "Lila":
            print(f"  💡 Knowledge Shared: {state.progress_points}")
    
    print("="*50 + "\n")

def handle_special_commands(user_input: str) -> bool:
    """Handle special commands and return True if command was processed"""
    if user_input.lower() == "status":
        display_agent_status()
        return True
    elif user_input.lower() == "save":
        save_agent_states()
        print("💾 Agent states saved!")
        return True
    elif user_input.lower() == "reset":
        global agent_states
        agent_states = {name: AgentState(name) for name in AGENTS.keys()}
        print("🔄 Agent states reset!")
        return True
    elif user_input.lower().startswith("check "):
        agent_name = user_input[6:].strip().capitalize()
        if agent_name in agent_states:
            state = agent_states[agent_name]
            print(f"\n🔍 {agent_name}'s Status:")
            print(f"  Conversations: {state.conversation_count}")
            print(f"  Progress Points: {state.progress_points}")
            if agent_name == "Momo":
                print(f"  Weight Loss: {state.weight_loss} kg")
                print(f"  Healthy Days: {state.healthy_days}")
            elif agent_name == "Miles":
                print(f"  Learning Level: {state.learning_level}/3")
        else:
            print(f"❌ Agent '{agent_name}' not found.")
        return True
    return False

# Main interaction loop
if __name__ == "__main__":
    # Load existing agent states
    load_agent_states()
    
    print("💬 Welcome to the Enhanced Healthy Habits Chat!")
    print("🤖 Meet Momo, Miles, and Lila - Your AI Health Companions!")
    print("\n📋 Special Commands:")
    print("  'status' - View agent progress")
    print("  'save' - Save agent states")
    print("  'reset' - Reset all agent states")
    print("  'check [agent]' - Check specific agent status")
    print("  'exit' or 'quit' - Stop the chat")
    print("\n" + "="*50)

    while True:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in {"exit", "quit"}:
            save_agent_states()
            print("💾 States saved. Goodbye! 👋")
            break
            
        if handle_special_commands(user_input):
            continue

        print(f"\n{'='*50}")
        print("🤖 AGENT RESPONSES")
        print("="*50)
        
        # Get responses from all agents
        for agent_name in AGENTS:
            reply = run_agent(agent_name, user_input, conversation_history)
            print(f"\n🤖 {agent_name}: {reply}")
            
            # Add to conversation history
            conversation_history.append({
                "role": "assistant",
                "name": agent_name.lower(),
                "content": reply
            })

        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Keep conversation history manageable
        if len(conversation_history) > config["agents"]["conversation_history_limit"]:
            conversation_history = conversation_history[-30:]
