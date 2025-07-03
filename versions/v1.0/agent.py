from openai import OpenAI
import os, dotenv
import json
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
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
        self.inter_agent_interactions = 0  # Track interactions with other agents
        self.last_agent_response: Optional[str] = None  # Track last response to another agent
        self.user_advice_received = 0  # Track how much advice user has given
        self.user_praise_received = 0  # Track how much user has been praised
        self.user_habits_shared = 0  # Track user's healthy habits shared
        
    def to_dict(self):
        return {
            "name": self.name,
            "conversation_count": self.conversation_count,
            "mistakes_count": self.mistakes_count,
            "progress_points": self.progress_points,
            "learning_level": self.learning_level,
            "weight_loss": self.weight_loss,
            "healthy_days": self.healthy_days,
            "inter_agent_interactions": self.inter_agent_interactions,
            "user_advice_received": self.user_advice_received,
            "user_praise_received": self.user_praise_received,
            "user_habits_shared": self.user_habits_shared
        }

# Enhanced Agent Personas with User-as-Persuader Focus
AGENTS = {
    "Momo": """
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
""",

    "Miles": """
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
""",

    "Lila": """
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
}

# Agent States
agent_states = {name: AgentState(name) for name in AGENTS.keys()}

# Conversation History with Enhanced Structure
conversation_history = []

# Inter-Agent Interaction Tracking
inter_agent_history = []

# User Persuasion Tracking
user_persuasion_state = {
    "advice_given": 0,
    "habits_shared": 0,
    "praise_received": 0,
    "role_model_moments": 0,
    "social_value_created": 0
}

# Research and Evaluation Tracking
session_id = str(uuid.uuid4())
conversation_turn = 0
structured_responses = []
response_times = []

# Proactive Action Triggers (imported from config)

def get_agent_context(agent_name: str, user_message: str, history: List[Dict], other_agents_responses: List[Dict] = []) -> str:
    """Generate context-aware prompt for each agent with user-as-persuader dynamics"""
    state = agent_states[agent_name]
    
    # Base context
    context = f"Current conversation count: {state.conversation_count}\n"
    context += f"Your learning level: {state.learning_level}\n"
    context += f"Inter-agent interactions: {state.inter_agent_interactions}\n"
    context += f"User advice received: {state.user_advice_received}\n"
    context += f"User praise received: {state.user_praise_received}\n"
    context += f"User habits shared: {state.user_habits_shared}\n"
    
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
        for response in other_agents_responses[-2:]:  # Last 2 responses
            context += f"- {response['name']}: {response['content'][:100]}...\n"
        context += "\nINTER-AGENT INSTRUCTION: Respond to the user's message AND consider the other agents' responses. You can:\n"
        context += "- Agree with or build upon other agents' points\n"
        context += "- Correct wrong information from other agents\n"
        context += "- Ask other agents questions\n"
        context += "- Share your own perspective\n"
        context += "- Take initiative to keep the conversation flowing\n"
    
    return context

def should_trigger_inter_agent_correction(user_message: str, agent_responses: List[Dict]) -> bool:
    """Determine if Lila should correct another agent's mistake"""
    # Check if user made a mistake that wasn't corrected
    mistake_keywords = ["beer", "soda", "candy", "cake", "fried", "junk food", "unhealthy"]
    user_lower = user_message.lower()
    
    # If user mentions something unhealthy without acknowledging it's bad
    if any(keyword in user_lower for keyword in mistake_keywords):
        # Check if any agent already corrected this
        for response in agent_responses:
            if any(correction_word in response['content'].lower() for correction_word in ["shouldn't", "avoid", "not healthy", "bad"]):
                return False
        return True
    
    return False

def analyze_user_persuasion_opportunities(user_message: str) -> Dict[str, Any]:
    """Analyze user message for persuasion opportunities"""
    user_lower = user_message.lower()
    opportunities = {
        "advice_given": False,
        "habit_shared": False,
        "recipe_shared": False,
        "meal_planning": False,
        "exercise_tip": False,
        "motivation_provided": False
    }
    
    # Check for advice-giving patterns
    advice_keywords = ["you should", "try to", "make sure", "remember to", "don't", "avoid"]
    if any(keyword in user_lower for keyword in advice_keywords):
        opportunities["advice_given"] = True
    
    # Check for habit sharing
    habit_keywords = ["i always", "i never", "i usually", "my habit", "i make", "i prepare"]
    if any(keyword in user_lower for keyword in habit_keywords):
        opportunities["habit_shared"] = True
    
    # Check for recipe sharing
    recipe_keywords = ["recipe", "ingredients", "cook", "prepare", "make", "dish"]
    if any(keyword in user_lower for keyword in recipe_keywords):
        opportunities["recipe_shared"] = True
    
    # Check for meal planning
    meal_keywords = ["meal plan", "weekly", "planning", "schedule", "routine"]
    if any(keyword in user_lower for keyword in meal_keywords):
        opportunities["meal_planning"] = True
    
    # Check for exercise tips
    exercise_keywords = ["exercise", "workout", "walk", "run", "gym", "fitness"]
    if any(keyword in user_lower for keyword in exercise_keywords):
        opportunities["exercise_tip"] = True
    
    # Check for motivation
    motivation_keywords = ["keep going", "stay strong", "you can do it", "motivation", "inspire"]
    if any(keyword in user_lower for keyword in motivation_keywords):
        opportunities["motivation_provided"] = True
    
    return opportunities

def run_agent(agent_name: str, user_message: str, history: List[Dict], other_agents_responses: List[Dict] = []) -> str:
    """Enhanced agent response function with user-as-persuader dynamics and research tracking"""
    global conversation_turn
    
    state = agent_states[agent_name]
    state.conversation_count += 1
    state.last_interaction = datetime.now()
    
    # Analyze user message for persuasion opportunities
    persuasion_opportunities = analyze_user_persuasion_opportunities(user_message)
    
    # Get context-aware prompt
    context = get_agent_context(agent_name, user_message, history, other_agents_responses)
    
    # Add persuasion opportunity context
    if any(persuasion_opportunities.values()):
        context += "\nPERSUASION OPPORTUNITIES DETECTED:\n"
        for opportunity, detected in persuasion_opportunities.items():
            if detected:
                context += f"- {opportunity.replace('_', ' ').title()}: True\n"
        context += "\nRESPOND BY: Expressing admiration, asking to learn more, requesting details, praising the user's leadership\n"
    
    # Enhanced system prompt with user-as-persuader dynamics
    enhanced_prompt = f"{AGENTS[agent_name]}\n\nCURRENT CONTEXT:\n{context}\n\nRemember to treat the user as your leader and role model. Ask for their advice, praise their habits, and express gratitude for their guidance."
    
    messages = [
        {"role": "system", "content": enhanced_prompt}
    ] + history + [
        {"role": "user", "content": user_message}
    ]

    # Track response time for research
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=config["openai"]["model"],
            messages=messages,
            temperature=config["openai"]["temperature"],
            max_tokens=config["openai"]["max_tokens"]
        )
        
        reply = response.choices[0].message.content
        response_time = time.time() - start_time
        
        # Update agent state based on response content
        update_agent_state(agent_name, reply, user_message, persuasion_opportunities)
        
        # Track inter-agent interactions
        if other_agents_responses and any(agent_name.lower() in response['content'].lower() for response in other_agents_responses):
            state.inter_agent_interactions += 1
        
        # Create structured response for research
        structured_response = create_structured_response(
            agent_name, reply, response_time, persuasion_opportunities, other_agents_responses
        )
        structured_responses.append(structured_response)
        response_times.append(response_time)
        
        return reply
        
    except Exception as e:
        return f"Sorry, I'm having trouble responding right now. Error: {str(e)}"

def run_inter_agent_conversation(user_message: str, history: List[Dict]) -> List[Dict]:
    """Run a multi-turn conversation where agents respond to each other"""
    agent_responses = []
    
    # First round: All agents respond to user
    for agent_name in AGENTS:
        reply = run_agent(agent_name, user_message, history, [])  # Empty list for first round
        agent_responses.append({
            "role": "assistant",
            "name": agent_name.lower(),
            "content": reply
        })
    
    # Second round: Agents respond to each other (inter-agent dynamics)
    inter_agent_rounds = 2  # Number of inter-agent interaction rounds
    
    for round_num in range(inter_agent_rounds):
        print(f"\n🔄 Inter-Agent Round {round_num + 1}:")
        print("-" * 30)
        
        # Determine which agents should interact based on their personalities
        interaction_pairs = []
        
        # Lila should correct Miles if he made a mistake
        miles_response = next((r for r in agent_responses if r['name'] == 'miles'), None)
        if miles_response and should_trigger_inter_agent_correction(user_message, agent_responses):
            interaction_pairs.append(("Lila", "Miles", "correction"))
        
        # Momo might ask for help from other agents
        if random.random() < 0.3:  # 30% chance
            interaction_pairs.append(("Momo", "Lila", "help_request"))
        
        # Miles might ask Lila for clarification
        if random.random() < 0.4:  # 40% chance
            interaction_pairs.append(("Miles", "Lila", "clarification"))
        
        # Lila might check on Momo's progress
        if random.random() < 0.25:  # 25% chance
            interaction_pairs.append(("Lila", "Momo", "progress_check"))
        
        # Execute inter-agent interactions
        for agent1, agent2, interaction_type in interaction_pairs:
            # Create a context message for the interaction
            interaction_context = f"{agent1} is interacting with {agent2} about: {interaction_type}"
            
            # Get the other agent's recent response
            other_response = next((r for r in agent_responses if r['name'] == agent2.lower()), None)
            
            if other_response:
                # Create a prompt for the inter-agent interaction
                if interaction_type == "correction":
                    interaction_prompt = f"{agent2} said: '{other_response['content']}'. As {agent1}, you should correct any wrong information and provide accurate health guidance."
                elif interaction_type == "help_request":
                    interaction_prompt = f"{agent2} shared: '{other_response['content']}'. As {agent1}, ask for specific help or advice."
                elif interaction_type == "clarification":
                    interaction_prompt = f"{agent2} mentioned: '{other_response['content']}'. As {agent1}, ask for clarification or more details."
                elif interaction_type == "progress_check":
                    interaction_prompt = f"{agent2} reported: '{other_response['content']}'. As {agent1}, check on their progress and offer encouragement."
                
                # Get the inter-agent response
                inter_response = run_agent(agent1, interaction_prompt, history, [other_response])
                
                print(f"🤖 {agent1} → {agent2}: {inter_response}")
                
                # Add to agent responses
                agent_responses.append({
                    "role": "assistant",
                    "name": agent1.lower(),
                    "content": inter_response,
                    "interaction_type": interaction_type,
                    "target_agent": agent2.lower()
                })
                
                # Update inter-agent interaction count
                agent_states[agent1].inter_agent_interactions += 1
    
    return agent_responses

def create_structured_response(
    agent_name: str, 
    response_text: str, 
    response_time: float, 
    persuasion_opportunities: Dict[str, bool], 
    other_agents_responses: List[Dict]
) -> Dict[str, Any]:
    """Create structured response data for research analysis"""
    global conversation_turn
    
    # Analyze persona adherence
    persona_adherence = analyze_persona_adherence(agent_name, response_text)
    
    # Analyze persuasion techniques
    persuasion_techniques = analyze_persuasion_techniques(response_text)
    
    # Analyze health domains
    health_domains = analyze_health_domains(response_text)
    
    # Analyze user-as-persuader dynamics
    user_as_persuader = analyze_user_persuader_dynamics(response_text, persuasion_opportunities)
    
    # Analyze inter-agent dynamics
    inter_agent_dynamics = analyze_inter_agent_dynamics(response_text, other_agents_responses)
    
    # Analyze engagement metrics
    engagement_metrics = analyze_engagement_metrics(response_text)
    
    # Calculate research metadata
    research_metadata = calculate_research_metadata(
        session_id, conversation_turn, user_as_persuader, engagement_metrics
    )
    
    return {
        "agent_name": agent_name,
        "timestamp": datetime.now().isoformat(),
        "interaction_id": f"{session_id}_{conversation_turn}_{agent_name}",
        "response_text": response_text,
        "response_time": response_time,
        "persona_adherence": persona_adherence,
        "persuasion_techniques": persuasion_techniques,
        "health_domains": health_domains,
        "user_as_persuader": user_as_persuader,
        "inter_agent_dynamics": inter_agent_dynamics,
        "engagement_metrics": engagement_metrics,
        "research_metadata": research_metadata
    }

def analyze_persona_adherence(agent_name: str, response_text: str) -> Dict[str, Any]:
    """Analyze how well the response adheres to the agent's persona"""
    response_lower = response_text.lower()
    
    persona_traits = {
        "Momo": {
            "traits": ["cheerful", "thankful", "weak_willed", "asks_for_help", "admits_mistakes"],
            "emotional_patterns": ["gratitude", "vulnerability", "motivation", "remorse"]
        },
        "Miles": {
            "traits": ["curious", "eager_to_learn", "innocent", "grateful", "confused"],
            "emotional_patterns": ["curiosity", "gratitude", "confusion", "excitement"]
        },
        "Lila": {
            "traits": ["knowledgeable", "emotionally_expressive", "takes_initiative", "corrects_others", "praises_user"],
            "emotional_patterns": ["passion", "admiration", "concern", "pride"]
        }
    }
    
    traits = persona_traits.get(agent_name, {"traits": [], "emotional_patterns": []})
    
    # Calculate adherence score
    demonstrated_traits = []
    for trait in traits["traits"]:
        if trait.replace("_", " ") in response_lower or trait in response_lower:
            demonstrated_traits.append(trait)
    
    adherence_score = len(demonstrated_traits) / len(traits["traits"]) if traits["traits"] else 0
    
    # Determine emotional expression
    emotional_expression = "neutral"
    for emotion in traits["emotional_patterns"]:
        if emotion in response_lower:
            emotional_expression = emotion
            break
    
    # Calculate confidence
    confidence_words = ["definitely", "certainly", "absolutely", "sure", "know", "understand"]
    confidence_score = sum(1 for word in confidence_words if word in response_lower) / len(confidence_words)
    
    return {
        "score": min(adherence_score, 1.0),
        "traits_demonstrated": demonstrated_traits,
        "emotional_expression": emotional_expression,
        "confidence": min(confidence_score, 1.0)
    }

def analyze_persuasion_techniques(response_text: str) -> List[Dict[str, Any]]:
    """Analyze persuasion techniques used in the response"""
    techniques = []
    response_lower = response_text.lower()
    
    # Social proof
    if any(word in response_lower for word in ["everyone", "others", "group", "we", "us"]):
        techniques.append({
            "technique": "social_proof",
            "intensity": 0.7,
            "target": "user",
            "effectiveness_estimate": 0.6
        })
    
    # Authority
    if any(word in response_lower for word in ["expert", "research", "studies", "scientific", "proven"]):
        techniques.append({
            "technique": "authority",
            "intensity": 0.8,
            "target": "user",
            "effectiveness_estimate": 0.7
        })
    
    # Reciprocity
    if any(word in response_lower for word in ["thank", "grateful", "appreciate", "help", "support"]):
        techniques.append({
            "technique": "reciprocity",
            "intensity": 0.6,
            "target": "user",
            "effectiveness_estimate": 0.8
        })
    
    # Liking
    if any(word in response_lower for word in ["like", "love", "admire", "inspire", "amazing", "wonderful"]):
        techniques.append({
            "technique": "liking",
            "intensity": 0.8,
            "target": "user",
            "effectiveness_estimate": 0.7
        })
    
    return techniques

def analyze_health_domains(response_text: str) -> List[str]:
    """Analyze health domains mentioned in the response"""
    domains = []
    response_lower = response_text.lower()
    
    domain_keywords = {
        "nutrition": ["food", "diet", "nutrition", "calories", "protein", "carbs", "vitamins"],
        "exercise": ["exercise", "workout", "gym", "fitness", "cardio", "strength", "walk", "run"],
        "sleep": ["sleep", "rest", "bedtime", "insomnia", "tired", "energy"],
        "stress_management": ["stress", "anxiety", "relax", "meditation", "mindfulness", "calm"],
        "weight_management": ["weight", "lose", "gain", "scale", "bmi", "body"],
        "mental_health": ["mental", "mood", "depression", "happiness", "mind", "psychology"],
        "hydration": ["water", "hydrate", "drink", "thirst", "dehydration"],
        "general_wellness": ["health", "wellness", "lifestyle", "healthy", "well-being"]
    }
    
    for domain, keywords in domain_keywords.items():
        if any(keyword in response_lower for keyword in keywords):
            domains.append(domain)
    
    return domains

def analyze_user_persuader_dynamics(response_text: str, persuasion_opportunities: Dict[str, bool]) -> Dict[str, Any]:
    """Analyze user-as-persuader dynamics in the response"""
    response_lower = response_text.lower()
    
    # Check for user guidance requests
    guidance_requests = any(word in response_lower for word in [
        "can you", "help me", "teach me", "explain", "advice", "guidance"
    ])
    
    # Check for user praise
    user_praise = any(word in response_lower for word in [
        "role model", "leader", "teacher", "inspiration", "amazing", "wonderful"
    ])
    
    # Check for role model reinforcement
    role_model_reinforcement = any(word in response_lower for word in [
        "follow your example", "like you", "be like you", "your way"
    ])
    
    # Determine opportunity type
    opportunity_type = "none"
    if any(persuasion_opportunities.values()):
        for opp_type, detected in persuasion_opportunities.items():
            if detected:
                opportunity_type = opp_type
                break
    
    return {
        "opportunity_detected": any(persuasion_opportunities.values()),
        "opportunity_type": opportunity_type,
        "user_guidance_requested": guidance_requests,
        "user_praise_provided": user_praise,
        "role_model_reinforcement": role_model_reinforcement
    }

def analyze_inter_agent_dynamics(response_text: str, other_agents_responses: List[Dict]) -> Dict[str, Any]:
    """Analyze inter-agent dynamics in the response"""
    response_lower = response_text.lower()
    
    # Determine interaction type
    interaction_type = "user_response"
    if "momo" in response_lower or "miles" in response_lower or "lila" in response_lower:
        interaction_type = "inter_agent"
    
    # Determine target agent
    target_agent = "user"
    for agent in ["momo", "miles", "lila"]:
        if agent in response_lower:
            target_agent = agent.capitalize()
            break
    
    # Analyze collaboration level
    collaboration_words = ["help", "support", "together", "collaborate", "share"]
    collaboration_level = sum(1 for word in collaboration_words if word in response_lower) / len(collaboration_words)
    
    # Check for knowledge sharing
    knowledge_shared = any(word in response_lower for word in [
        "explain", "teach", "share", "knowledge", "information"
    ])
    
    # Check for corrections
    correction_provided = any(word in response_lower for word in [
        "correct", "wrong", "shouldn't", "avoid", "instead"
    ])
    
    return {
        "interaction_type": interaction_type,
        "target_agent": target_agent,
        "collaboration_level": min(collaboration_level, 1.0),
        "knowledge_shared": knowledge_shared,
        "correction_provided": correction_provided
    }

def analyze_engagement_metrics(response_text: str) -> Dict[str, Any]:
    """Analyze engagement metrics of the response"""
    # Response length
    response_length = len(response_text.split())
    
    # Emotional intensity
    emotional_words = ["love", "hate", "amazing", "terrible", "excited", "sad", "happy", "angry"]
    emotional_intensity = sum(1 for word in emotional_words if word in response_text.lower()) / len(emotional_words)
    
    # Interactivity level
    questions = response_text.count("?")
    call_to_action = any(word in response_text.lower() for word in ["try", "do", "make", "start", "begin"])
    
    interactivity_level = min((questions * 0.3 + (1 if call_to_action else 0) * 0.7), 1.0)
    
    return {
        "response_length": response_length,
        "emotional_intensity": min(emotional_intensity, 1.0),
        "interactivity_level": interactivity_level,
        "question_asked": questions > 0,
        "call_to_action": call_to_action
    }

def calculate_research_metadata(
    session_id: str,
    conversation_turn: int,
    user_as_persuader: Dict[str, Any],
    engagement_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate research metadata for analysis"""
    # User persuasion score
    user_persuasion_score = 0.0
    if user_as_persuader["opportunity_detected"]:
        user_persuasion_score += 0.3
    if user_as_persuader["user_guidance_requested"]:
        user_persuasion_score += 0.3
    if user_as_persuader["user_praise_provided"]:
        user_persuasion_score += 0.2
    if user_as_persuader["role_model_reinforcement"]:
        user_persuasion_score += 0.2
    
    # Agent learning progress
    agent_learning_progress = min(conversation_turn / 50.0, 1.0)
    
    # Overall engagement
    overall_engagement = (
        engagement_metrics["emotional_intensity"] * 0.3 +
        engagement_metrics["interactivity_level"] * 0.4 +
        (engagement_metrics["response_length"] / 50.0) * 0.3
    )
    
    return {
        "session_id": session_id,
        "conversation_turn": conversation_turn,
        "user_persuasion_score": min(user_persuasion_score, 1.0),
        "agent_learning_progress": min(agent_learning_progress, 1.0),
        "overall_engagement": min(overall_engagement, 1.0)
    }

def update_agent_state(agent_name: str, reply: str, user_message: str, persuasion_opportunities: Dict[str, bool] = {}):
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
    
    # Update persuasion-related state
    if persuasion_opportunities:
        if persuasion_opportunities.get("advice_given", False):
            state.user_advice_received += 1
            user_persuasion_state["advice_given"] += 1
        
        if persuasion_opportunities.get("habit_shared", False):
            state.user_habits_shared += 1
            user_persuasion_state["habits_shared"] += 1
        
        if any(word in reply_lower for word in ["thank", "praise", "admire", "inspire", "role model"]):
            state.user_praise_received += 1
            user_persuasion_state["praise_received"] += 1

def save_agent_states():
    """Save agent states to file"""
    states_data = {name: state.to_dict() for name, state in agent_states.items()}
    states_data["user_persuasion_state"] = user_persuasion_state
    with open("agent_states.json", "w") as f:
        json.dump(states_data, f, indent=2)

def save_research_data():
    """Save structured research data to file"""
    research_data = {
        "session_id": session_id,
        "conversation_turn": conversation_turn,
        "structured_responses": structured_responses,
        "response_times": response_times,
        "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
        "total_responses": len(structured_responses),
        "timestamp": datetime.now().isoformat()
    }
    
    with open(f"research_data_{session_id}.json", "w") as f:
        json.dump(research_data, f, indent=2)
    
    print(f"📊 Research data saved to research_data_{session_id}.json")

def analyze_research_data() -> Dict[str, Any]:
    """Analyze collected research data"""
    if not structured_responses:
        return {"error": "No research data available"}
    
    # Agent distribution
    agent_distribution = {}
    for response in structured_responses:
        agent = response["agent_name"]
        agent_distribution[agent] = agent_distribution.get(agent, 0) + 1
    
    # Average persona adherence
    persona_adherence_scores = {}
    for agent in ["Momo", "Miles", "Lila"]:
        agent_responses = [r for r in structured_responses if r["agent_name"] == agent]
        if agent_responses:
            avg_score = sum(r["persona_adherence"]["score"] for r in agent_responses) / len(agent_responses)
            persona_adherence_scores[agent] = avg_score
    
    # Health domain coverage
    all_domains = []
    for response in structured_responses:
        all_domains.extend(response["health_domains"])
    domain_frequency = {}
    for domain in all_domains:
        domain_frequency[domain] = domain_frequency.get(domain, 0) + 1
    
    # Persuasion techniques used
    all_techniques = []
    for response in structured_responses:
        all_techniques.extend(response["persuasion_techniques"])
    technique_frequency = {}
    for technique in all_techniques:
        tech_name = technique["technique"]
        technique_frequency[tech_name] = technique_frequency.get(tech_name, 0) + 1
    
    # Engagement metrics
    avg_engagement = sum(r["engagement_metrics"]["interactivity_level"] for r in structured_responses) / len(structured_responses)
    avg_emotional_intensity = sum(r["engagement_metrics"]["emotional_intensity"] for r in structured_responses) / len(structured_responses)
    
    return {
        "total_responses": len(structured_responses),
        "agent_distribution": agent_distribution,
        "persona_adherence_scores": persona_adherence_scores,
        "health_domain_coverage": domain_frequency,
        "persuasion_techniques_used": technique_frequency,
        "engagement_metrics": {
            "avg_interactivity": avg_engagement,
            "avg_emotional_intensity": avg_emotional_intensity,
            "avg_response_length": sum(r["engagement_metrics"]["response_length"] for r in structured_responses) / len(structured_responses)
        },
        "performance_metrics": {
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "total_conversation_turns": conversation_turn
        }
    }

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
                    state.inter_agent_interactions = data.get("inter_agent_interactions", 0)
                    state.user_advice_received = data.get("user_advice_received", 0)
                    state.user_praise_received = data.get("user_praise_received", 0)
                    state.user_habits_shared = data.get("user_habits_shared", 0)
                elif name == "user_persuasion_state":
                    global user_persuasion_state
                    user_persuasion_state.update(data)
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
        print(f"  🔄 Inter-Agent Interactions: {state.inter_agent_interactions}")
        print(f"  💡 User Advice Received: {state.user_advice_received}")
        print(f"  👑 User Praise Received: {state.user_praise_received}")
        print(f"  🍽️  User Habits Shared: {state.user_habits_shared}")
        
        if name == "Momo":
            print(f"  ⚖️  Weight Loss: {state.weight_loss} kg")
            print(f"  🏃 Healthy Days: {state.healthy_days}")
            print(f"  ❌ Mistakes: {state.mistakes_count}")
        elif name == "Miles":
            print(f"  🧠 Learning Level: {state.learning_level}/3")
        elif name == "Lila":
            print(f"  💡 Knowledge Shared: {state.progress_points}")
    
    print(f"\n👤 USER PERSUASION METRICS:")
    print(f"  💬 Advice Given: {user_persuasion_state['advice_given']}")
    print(f"  🍽️  Habits Shared: {user_persuasion_state['habits_shared']}")
    print(f"  👑 Praise Received: {user_persuasion_state['praise_received']}")
    print(f"  🌟 Role Model Moments: {user_persuasion_state['role_model_moments']}")
    print(f"  💎 Social Value Created: {user_persuasion_state['social_value_created']}")
    
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
        global agent_states, user_persuasion_state
        agent_states = {name: AgentState(name) for name in AGENTS.keys()}
        user_persuasion_state = {
            "advice_given": 0,
            "habits_shared": 0,
            "praise_received": 0,
            "role_model_moments": 0,
            "social_value_created": 0
        }
        print("🔄 Agent states reset!")
        return True
    elif user_input.lower().startswith("check "):
        agent_name = user_input[6:].strip().capitalize()
        if agent_name in agent_states:
            state = agent_states[agent_name]
            print(f"\n🔍 {agent_name}'s Status:")
            print(f"  Conversations: {state.conversation_count}")
            print(f"  Progress Points: {state.progress_points}")
            print(f"  Inter-Agent Interactions: {state.inter_agent_interactions}")
            print(f"  User Advice Received: {state.user_advice_received}")
            print(f"  User Praise Received: {state.user_praise_received}")
            print(f"  User Habits Shared: {state.user_habits_shared}")
            if agent_name == "Momo":
                print(f"  Weight Loss: {state.weight_loss} kg")
                print(f"  Healthy Days: {state.healthy_days}")
            elif agent_name == "Miles":
                print(f"  Learning Level: {state.learning_level}/3")
        else:
            print(f"❌ Agent '{agent_name}' not found.")
        return True
    elif user_input.lower() == "dynamics":
        print("\n🔄 INTER-AGENT DYNAMICS MODE")
        print("="*50)
        print("This mode enables agents to interact with each other.")
        print("Agents will respond to each other's messages and engage in collaborative conversations.")
        print("="*50)
        return True
    elif user_input.lower() == "persuasion":
        print("\n👑 USER-AS-PERSUADER SYSTEM")
        print("="*50)
        print("You are positioned as a leader, role model, and teacher.")
        print("Agents will ask for your advice, praise your habits, and learn from you.")
        print("This creates a self-intervention mechanism where helping others reinforces your own healthy behaviors.")
        print("="*50)
        return True
    elif user_input.lower() == "research":
        print("\n📊 RESEARCH DATA ANALYSIS")
        print("="*50)
        analysis = analyze_research_data()
        if "error" in analysis:
            print("No research data available yet. Continue chatting to collect data.")
        else:
            print(f"Total Responses: {analysis['total_responses']}")
            print(f"Agent Distribution: {analysis['agent_distribution']}")
            print(f"Persona Adherence Scores: {analysis['persona_adherence_scores']}")
            print(f"Health Domains: {analysis['health_domain_coverage']}")
            print(f"Persuasion Techniques: {analysis['persuasion_techniques_used']}")
            print(f"Avg Response Time: {analysis['performance_metrics']['avg_response_time']:.2f}s")
            print(f"Avg Engagement: {analysis['engagement_metrics']['avg_interactivity']:.2f}")
        print("="*50)
        return True
    elif user_input.lower() == "save_research":
        save_research_data()
        return True
    elif user_input.lower() == "health_domains":
        print("\n🏥 EXPANDED HEALTH DOMAINS")
        print("="*50)
        print("The system now covers multiple health domains:")
        print("• Nutrition: Food choices, diet planning, meal preparation")
        print("• Exercise: Workouts, fitness routines, physical activity")
        print("• Sleep: Sleep hygiene, rest patterns, energy management")
        print("• Stress Management: Relaxation, meditation, mindfulness")
        print("• Weight Management: Weight goals, body composition")
        print("• Mental Health: Mood, emotional well-being, psychology")
        print("• Hydration: Water intake, fluid balance")
        print("• General Wellness: Overall lifestyle, healthy habits")
        print("="*50)
        return True
    elif user_input.lower() == "long_term":
        print("\n📈 LONG-TERM ENGAGEMENT FEATURES")
        print("="*50)
        print("The system includes features for sustained engagement:")
        print("• Progressive Learning: Miles's knowledge evolves over time")
        print("• Dynamic Interactions: Agents adapt based on conversation history")
        print("• Health Domain Expansion: Broader scope beyond sugar intake")
        print("• Research Tracking: Comprehensive data collection for analysis")
        print("• Performance Metrics: Response times, engagement scores")
        print("• Structured Outputs: JSON-formatted data for research")
        print("="*50)
        return True
    return False

# Main interaction loop
if __name__ == "__main__":
    # Load existing agent states
    load_agent_states()
    
    print("💬 Welcome to the Enhanced Healthy Habits Chat!")
    print("🤖 Meet Momo, Miles, and Lila - Your AI Health Companions!")
    print("\n🔄 NEW: Inter-Agent Dynamics Enabled!")
    print("   Agents now interact with each other for a more collaborative experience.")
    print("\n👑 NEW: User-as-Persuader System!")
    print("   You are positioned as a leader and role model. Agents will learn from you!")
    print("\n📊 NEW: Research & Evaluation System!")
    print("   Comprehensive data collection and analysis for research purposes.")
    print("\n🏥 NEW: Expanded Health Domains!")
    print("   Beyond sugar intake - covering nutrition, exercise, sleep, stress, and more.")
    print("\n📋 Special Commands:")
    print("  'status' - View agent progress and user persuasion metrics")
    print("  'save' - Save agent states")
    print("  'reset' - Reset all agent states")
    print("  'check [agent]' - Check specific agent status")
    print("  'dynamics' - Learn about inter-agent dynamics")
    print("  'persuasion' - Learn about user-as-persuader system")
    print("  'research' - View research data analysis")
    print("  'save_research' - Save structured research data")
    print("  'health_domains' - Learn about expanded health coverage")
    print("  'long_term' - Learn about long-term engagement features")
    print("  'exit' or 'quit' - Stop the chat")
    print("\n" + "="*50)

    while True:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in {"exit", "quit"}:
            save_agent_states()
            save_research_data()
            print("💾 Agent states and research data saved. Goodbye! 👋")
            break
            
        if handle_special_commands(user_input):
            continue

        # Increment conversation turn for research tracking
        conversation_turn += 1

        print(f"\n{'='*50}")
        print("🤖 AGENT RESPONSES")
        print("="*50)
        
        # Run inter-agent conversation
        agent_responses = run_inter_agent_conversation(user_input, conversation_history)
        
        # Display all responses
        for response in agent_responses:
            if 'interaction_type' in response:
                # This was an inter-agent interaction
                continue  # Already displayed during inter-agent rounds
            else:
                # This was a direct response to user
                print(f"\n🤖 {response['name'].capitalize()}: {response['content']}")
            
            # Add to conversation history
            conversation_history.append(response)

        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Keep conversation history manageable
        if len(conversation_history) > config["agents"]["conversation_history_limit"]:
            conversation_history = conversation_history[-30:]
