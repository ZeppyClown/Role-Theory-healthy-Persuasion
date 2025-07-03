"""
Conversation Manager
Handles inter-agent interactions and conversation flow
"""

import random
from typing import Dict, List, Any
from datetime import datetime

def analyze_user_persuasion_opportunities(user_message: str) -> Dict[str, bool]:
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

def generate_inter_agent_interactions(agent_responses: List[Dict]) -> List[tuple]:
    """Generate inter-agent interaction pairs based on agent personalities and content"""
    interaction_pairs = []
    
    # Get the most recent responses for each agent
    agent_latest_responses = {}
    for response in agent_responses:
        agent_name = response['name'].capitalize()
        if agent_name not in agent_latest_responses:
            agent_latest_responses[agent_name] = response
    
    # Lila should correct Miles if he made a mistake (high priority)
    miles_response = agent_latest_responses.get("Miles")
    if miles_response and should_trigger_inter_agent_correction("", agent_responses):
        interaction_pairs.append(("Lila", "Miles", "correction"))
    
    # Momo might ask for help from Lila (if Momo mentioned struggles)
    momo_response = agent_latest_responses.get("Momo")
    if momo_response and any(word in momo_response['content'].lower() for word in ["help", "struggle", "difficult", "confused", "mistake"]):
        if random.random() < 0.6:  # 60% chance if Momo is struggling
            interaction_pairs.append(("Momo", "Lila", "help_request"))
    
    # Miles might ask Lila for clarification (if Miles asked a question)
    miles_response = agent_latest_responses.get("Miles")
    if miles_response and "?" in miles_response['content']:
        if random.random() < 0.7:  # 70% chance if Miles asked a question
            interaction_pairs.append(("Miles", "Lila", "clarification"))
    
    # Lila might check on Momo's progress (if Momo mentioned progress or setbacks)
    momo_response = agent_latest_responses.get("Momo")
    if momo_response and any(word in momo_response['content'].lower() for word in ["progress", "lost", "gained", "better", "worse", "mistake"]):
        if random.random() < 0.5:  # 50% chance if Momo mentioned progress-related content
            interaction_pairs.append(("Lila", "Momo", "progress_check"))
    
    # Ensure we don't have too many interactions (max 2 per round)
    if len(interaction_pairs) > 2:
        # Prioritize corrections and help requests
        priority_interactions = []
        for agent1, agent2, interaction_type in interaction_pairs:
            if interaction_type in ["correction", "help_request"]:
                priority_interactions.append((agent1, agent2, interaction_type))
        
        # Add other interactions if space allows
        other_interactions = [pair for pair in interaction_pairs if pair[2] not in ["correction", "help_request"]]
        interaction_pairs = priority_interactions + other_interactions[:2-len(priority_interactions)]
    
    return interaction_pairs

def create_interaction_prompt(agent1: str, agent2: str, interaction_type: str, other_response: Dict) -> str:
    """Create a prompt for inter-agent interaction with anti-repetition instructions"""
    
    # Base anti-repetition instruction
    anti_repetition = (
        f"IMPORTANT: Do NOT repeat what {agent2} just said. "
        "Instead, respond by correcting, asking a follow-up, encouraging, or adding new information. "
        "Acknowledge the previous statement briefly, but do not restate it."
    )
    
    if interaction_type == "correction":
        return (
            f"{agent2} said: '{other_response['content']}'. "
            f"As {agent1}, you should correct any wrong information and provide accurate health guidance. "
            f"{anti_repetition}"
        )
    elif interaction_type == "help_request":
        return (
            f"{agent2} shared: '{other_response['content']}'. "
            f"As {agent1}, offer specific help or advice based on your expertise. "
            f"{anti_repetition}"
        )
    elif interaction_type == "clarification":
        return (
            f"{agent2} mentioned: '{other_response['content']}'. "
            f"As {agent1}, ask for clarification or more details to better understand. "
            f"{anti_repetition}"
        )
    elif interaction_type == "progress_check":
        return (
            f"{agent2} reported: '{other_response['content']}'. "
            f"As {agent1}, check on their progress and offer specific encouragement or suggestions. "
            f"{anti_repetition}"
        )
    else:
        return (
            f"{agent2} said: '{other_response['content']}'. "
            f"As {agent1}, respond appropriately by adding value to the conversation. "
            f"{anti_repetition}"
        )

def check_response_similarity(response1: str, response2: str, threshold: float = 0.7) -> bool:
    """Check if two responses are too similar (simple word overlap check)"""
    words1 = set(response1.lower().split())
    words2 = set(response2.lower().split())
    
    if not words1 or not words2:
        return False
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    similarity = intersection / union if union > 0 else 0
    return similarity > threshold

def run_inter_agent_conversation(user_message: str, history: List[Dict], agents: Dict, run_agent_func) -> List[Dict]:
    """Run a multi-turn conversation where agents respond to each other"""
    agent_responses = []
    
    # First round: All agents respond to user
    for agent_name, agent in agents.items():
        reply = run_agent_func(agent, user_message, history, [])  # Empty list for first round
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
        
        # Generate interaction pairs
        interaction_pairs = generate_inter_agent_interactions(agent_responses)
        
        # Execute inter-agent interactions
        for agent1_name, agent2_name, interaction_type in interaction_pairs:
            # Get the other agent's recent response
            other_response = next((r for r in agent_responses if r['name'] == agent2_name.lower()), None)
            
            if other_response:
                # Create a prompt for the inter-agent interaction
                interaction_prompt = create_interaction_prompt(agent1_name, agent2_name, interaction_type, other_response)
                
                # Get the inter-agent response
                agent1 = agents[agent1_name]
                inter_response = run_agent_func(agent1, interaction_prompt, history, [other_response])
                
                # Check if response is too similar to the original
                if check_response_similarity(inter_response, other_response['content']):
                    print(f"⚠️  {agent1_name} → {agent2_name}: [Response too similar, skipping]")
                    continue
                
                print(f"🤖 {agent1_name} → {agent2_name}: {inter_response}")
                
                # Add to agent responses
                agent_responses.append({
                    "role": "assistant",
                    "name": agent1_name.lower(),
                    "content": inter_response,
                    "interaction_type": interaction_type,
                    "target_agent": agent2_name.lower()
                })
                
                # Update inter-agent interaction count
                agent1.inter_agent_interactions += 1
    
    return agent_responses

class ConversationManager:
    """Manages conversation flow and inter-agent interactions"""
    
    def __init__(self):
        self.conversation_history = []
        self.inter_agent_history = []
        self.user_persuasion_state = {
            "advice_given": 0,
            "habits_shared": 0,
            "praise_received": 0,
            "role_model_moments": 0,
            "social_value_created": 0
        }
    
    def add_to_history(self, message: Dict):
        """Add message to conversation history"""
        self.conversation_history.append(message)
        
        # Keep conversation history manageable
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-30:]
    
    def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:] if self.conversation_history else []
    
    def update_persuasion_state(self, opportunities: Dict[str, bool]):
        """Update user persuasion state based on opportunities"""
        if opportunities.get("advice_given", False):
            self.user_persuasion_state["advice_given"] += 1
        
        if opportunities.get("habit_shared", False):
            self.user_persuasion_state["habits_shared"] += 1
        
        if opportunities.get("motivation_provided", False):
            self.user_persuasion_state["role_model_moments"] += 1
    
    def get_persuasion_metrics(self) -> Dict[str, int]:
        """Get current persuasion metrics"""
        return self.user_persuasion_state.copy()
    
    def reset_conversation(self):
        """Reset conversation state"""
        self.conversation_history = []
        self.inter_agent_history = []
        self.user_persuasion_state = {
            "advice_given": 0,
            "habits_shared": 0,
            "praise_received": 0,
            "role_model_moments": 0,
            "social_value_created": 0
        } 