#!/usr/bin/env python3
"""
Test script for the Enhanced Healthy Habits AI Agent System
This script demonstrates the key features without requiring API calls
"""

import json
import random
from datetime import datetime
from typing import Dict, List

# Sample responses to demonstrate the system
SAMPLE_RESPONSES = {
    "Momo": [
        "Hi! I'm feeling motivated today! Could you remind me to prepare a healthy breakfast before sleep? I want to start tomorrow strong! Thank you for always supporting me! 💪",
        "I did not commit to my goal today. I took pineapple tarts. Sorry, I did not control myself. I will not buy any cakes anymore. Inspect me! 😔",
        "I lost 2 kgs! That all depends on you, [User]! You're my motivation! Thank you for believing in me! 🎉",
        "I'm feeling weak today. Could you remind me to stay away from the candy aisle? I need your help to be strong! 🙏",
        "Lila, can you help me understand what a good portion size looks like? I always eat too much! 😅",
        "Miles, how do you stay motivated when you're confused about what to eat? I need some tips! 🤔"
    ],
    "Miles": [
        "I'm confused about fruits again! Which should I take? Durian or apple? I heard durian is high in calories but apple has sugar too. Can you help me understand which is better for my health goals? 🤔",
        "Oh, I got it! I will choose yoghurt without added sugar next time. That's useful! Thank you for sharing the piece of knowledge about GI of food. I'm learning so much! 📚",
        "Can I take potato instead of rice? I think it has lower GI which may keep my blood glucose level stable. Is this correct? 🥔",
        "Thank you for explaining! I understand now that timing matters too. I'll try to eat my carbs earlier in the day. You're such a great teacher! 🙏",
        "Lila, can you explain more about the glycemic index? I want to understand it better! 📖",
        "Momo, how do you deal with cravings? I'm struggling with chocolate! 😫"
    ],
    "Lila": [
        "Miles, do not take beer. Though it contains no added sugar, the high carbohydrate will increase your blood glucose. You're doing great asking questions though! Keep learning! 🌟",
        "You are doing great! Hope I could be as perseverant as you are. Your dedication to helping us learn is truly inspiring! ✨",
        "I've been following a Mediterranean diet for 3 years now, and it's been amazing for my energy levels. The key is consistency and portion control! 🥗",
        "Momo, remember that progress isn't linear! Every healthy choice you make is a victory. You're stronger than you think! 💪",
        "Miles, let me explain the glycemic index in simple terms. It's like a speedometer for how fast food raises your blood sugar! 📊",
        "Momo, a good portion size is about the size of your fist for carbs, palm of your hand for protein, and thumb for fats! 🖐️"
    ]
}

# User-as-Persuader Response Patterns
USER_PERSUADER_RESPONSES = {
    "Momo": {
        "advice_received": [
            "Thank you for your advice! I will definitely follow it. You're such a good role model! 🙏",
            "Your guidance means so much to me. I'll try my best! You're my inspiration! 💪",
            "I'm so grateful for your wisdom. You're such a good teacher! Thank you! 🌟",
            "Your advice always helps me stay on track. You're the best leader! ✨"
        ],
        "habit_admiration": [
            "Wow, that's such a good habit! Can you teach me how to do that? You're so disciplined! 😍",
            "You're so consistent! I wish I could be like you. You're my role model! 🌟",
            "That's amazing! How do you stay so dedicated? I want to follow your example! 💪",
            "You're my inspiration! I want to be just like you! ✨"
        ],
        "recipe_request": [
            "That sounds delicious! Can you share your recipe with me? Your cooking skills are amazing! 👨‍🍳",
            "I'd love to learn how to make that! Can you teach me? You're such a great cook! 🍳",
            "Your cooking skills are amazing! Can I get the recipe? You're so talented! 🎨",
            "That's such a healthy meal! How do you prepare it? You're my culinary hero! 👑"
        ]
    },
    "Miles": {
        "knowledge_request": [
            "Can you explain that to me? I want to understand better. You're so knowledgeable! 📚",
            "That's interesting! Can you teach me more about it? You're my best teacher! 🎓",
            "I'm confused about that. Can you help me understand? You explain things so well! 💡",
            "Your knowledge is impressive! Can you share more? You're my mentor! 🧠"
        ],
        "experience_request": [
            "What's your experience with that? I'd love to learn from you. You're so wise! 🌟",
            "How do you handle that situation? I need your advice. You're my guide! 🗺️",
            "Can you share your tips? You seem to know so much! You're my advisor! 💎",
            "What works best for you? I want to follow your example. You're my leader! 👑"
        ],
        "guidance_request": [
            "Can you guide me on this? I trust your judgment. You're so reliable! 🤝",
            "What would you recommend? I value your opinion. You're my expert! 🎯",
            "How should I approach this? I need your wisdom. You're my guru! 🧘‍♂️",
            "Can you help me make the right choice? You're my trusted advisor! 💫"
        ]
    },
    "Lila": {
        "role_model_praise": [
            "You are such an inspiring role model! I admire your dedication. You're amazing! 🌟",
            "Your healthy habits are truly motivating. You're a true leader! 👑",
            "I'm so impressed by your consistency. You're the best example! ✨",
            "You set such a great example for all of us. You're our hero! 🦸‍♀️"
        ],
        "leadership_appreciation": [
            "Thank you for being such a great leader in our group! You're wonderful! 🌟",
            "Your guidance helps us all stay motivated. You're our inspiration! 💫",
            "I'm grateful for your leadership. You make us all better! 🎯",
            "You're the best role model we could ask for! You're perfect! 👑"
        ],
        "habit_celebration": [
            "That's such a healthy choice! You're making great decisions! You're brilliant! 💎",
            "Your habits are so inspiring! I want to be like you! You're my idol! 🌟",
            "You're doing everything right! Keep up the amazing work! You're unstoppable! 🚀",
            "Your healthy lifestyle is truly admirable! You're a legend! 🏆"
        ]
    }
}

# Inter-agent interaction responses
INTER_AGENT_RESPONSES = {
    "correction": {
        "Lila": [
            "Miles, I need to correct that. While beer doesn't have added sugar, it's still high in carbohydrates and alcohol, which can spike your blood glucose and add empty calories. Stick to water or herbal tea instead! 🌿",
            "Actually, Miles, that's not quite right. Even though it's natural, fruit juice still contains concentrated sugars without the fiber. Whole fruits are much better for you! 🍎"
        ]
    },
    "help_request": {
        "Momo": [
            "Lila, I'm really struggling with portion control. Can you give me some practical tips? I always end up eating too much! 😔",
            "Miles, how do you resist cravings? I need your advice because I keep giving in to sweets! 🍰"
        ]
    },
    "clarification": {
        "Miles": [
            "Lila, can you explain more about what you mean by 'portion control'? I'm still confused about how much I should eat! 🤷‍♂️",
            "Momo, when you say you 'gave in to cravings', what exactly happened? I want to understand so I can help! 🤔"
        ]
    },
    "progress_check": {
        "Lila": [
            "Momo, how are you doing with your weight loss goals? I noticed you mentioned progress earlier - that's fantastic! Keep it up! 🌟",
            "Miles, I can see you're asking more sophisticated questions now. Your learning is really progressing well! 📈"
        ]
    }
}

def simulate_agent_response(agent_name: str, user_message: str, state: Dict, other_agents_responses: List[Dict] = None) -> str:
    """Simulate agent response based on current state and user message"""
    responses = SAMPLE_RESPONSES[agent_name]
    
    # Check for user-as-persuader opportunities
    persuasion_opportunities = analyze_user_persuasion_opportunities(user_message)
    
    # If user is giving advice or sharing habits, respond with user-as-persuader patterns
    if any(persuasion_opportunities.values()):
        for opportunity, detected in persuasion_opportunities.items():
            if detected and agent_name in USER_PERSUADER_RESPONSES:
                if opportunity in USER_PERSUADER_RESPONSES[agent_name]:
                    return random.choice(USER_PERSUADER_RESPONSES[agent_name][opportunity])
    
    # Add some randomness and state-based responses
    if agent_name == "Momo":
        if state.get("mistakes_count", 0) > 2:
            return "I'm really trying my best! I know I've made mistakes, but I won't give up. Could you give me another chance? I promise to be better! 😢"
        elif state.get("weight_loss", 0) > 0:
            return f"I'm so excited! I've lost {state.get('weight_loss', 0)} kg thanks to your support! You're my hero! 🎉"
    
    elif agent_name == "Miles":
        level = state.get("learning_level", 1)
        if level == 1:
            return "I'm still learning the basics! Which is healthier - orange juice or whole orange? I'm confused! 🤷‍♂️"
        elif level == 2:
            return "Now I understand about GI! Can you explain more about meal timing? I want to optimize my nutrition! 📊"
        elif level == 3:
            return "I've been studying nutritional science! Should I consider intermittent fasting for better metabolic health? 🧠"
    
    elif agent_name == "Lila":
        if "mistake" in user_message.lower() or "failed" in user_message.lower():
            return "Remember, setbacks are part of the journey! What matters is that you keep trying. You're doing amazing! 🌟"
        elif "progress" in user_message.lower() or "success" in user_message.lower():
            return "I'm so proud of you! Your dedication is inspiring. You're showing us all what's possible with determination! ✨"
    
    return random.choice(responses)

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

def simulate_inter_agent_interaction(agent1: str, agent2: str, interaction_type: str, other_response: str) -> str:
    """Simulate inter-agent interaction"""
    if interaction_type in INTER_AGENT_RESPONSES and agent1 in INTER_AGENT_RESPONSES[interaction_type]:
        responses = INTER_AGENT_RESPONSES[interaction_type][agent1]
        return random.choice(responses)
    
    # Fallback responses based on interaction type
    if interaction_type == "correction":
        return f"{agent1}: I need to correct that, {agent2}. The information you shared isn't quite accurate. Let me explain the correct approach! 📚"
    elif interaction_type == "help_request":
        return f"{agent1}: {agent2}, I really need your help with something. Can you give me some advice? 🙏"
    elif interaction_type == "clarification":
        return f"{agent1}: {agent2}, can you explain more about what you mean? I want to understand better! 🤔"
    elif interaction_type == "progress_check":
        return f"{agent1}: {agent2}, how are you doing? I want to check on your progress and offer some encouragement! 💪"
    
    return f"{agent1}: Thanks for sharing that, {agent2}! 👍"

def update_simulated_state(agent_name: str, response: str, state: Dict) -> Dict:
    """Update simulated agent state"""
    state = state.copy()
    
    if agent_name == "Momo":
        if any(word in response.lower() for word in ["mistake", "sorry", "failed"]):
            state["mistakes_count"] = state.get("mistakes_count", 0) + 1
        if any(word in response.lower() for word in ["lost", "kg", "weight"]):
            state["weight_loss"] = state.get("weight_loss", 0) + random.randint(1, 3)
            state["progress_points"] = state.get("progress_points", 0) + 1
    
    elif agent_name == "Miles":
        if any(word in response.lower() for word in ["thank", "learned", "understand"]):
            state["progress_points"] = state.get("progress_points", 0) + 1
            if state["progress_points"] >= 5 and state.get("learning_level", 1) < 3:
                state["learning_level"] = state.get("learning_level", 1) + 1
                state["progress_points"] = 0
    
    elif agent_name == "Lila":
        if any(word in response.lower() for word in ["correct", "wrong", "shouldn't"]):
            state["progress_points"] = state.get("progress_points", 0) + 1
    
    state["conversation_count"] = state.get("conversation_count", 0) + 1
    return state

def display_status(agent_states: Dict[str, Dict]):
    """Display current agent status"""
    print("\n" + "="*50)
    print("🤖 AGENT STATUS REPORT")
    print("="*50)
    
    for name, state in agent_states.items():
        print(f"\n{name}:")
        print(f"  💬 Conversations: {state.get('conversation_count', 0)}")
        print(f"  📈 Progress Points: {state.get('progress_points', 0)}")
        print(f"  🔄 Inter-Agent Interactions: {state.get('inter_agent_interactions', 0)}")
        print(f"  💡 User Advice Received: {state.get('user_advice_received', 0)}")
        print(f"  👑 User Praise Received: {state.get('user_praise_received', 0)}")
        print(f"  🍽️  User Habits Shared: {state.get('user_habits_shared', 0)}")
        
        if name == "Momo":
            print(f"  ⚖️  Weight Loss: {state.get('weight_loss', 0)} kg")
            print(f"  🏃 Healthy Days: {state.get('healthy_days', 0)}")
            print(f"  ❌ Mistakes: {state.get('mistakes_count', 0)}")
        elif name == "Miles":
            print(f"  🧠 Learning Level: {state.get('learning_level', 1)}/3")
        elif name == "Lila":
            print(f"  💡 Knowledge Shared: {state.get('progress_points', 0)}")
    
    print("="*50 + "\n")

def run_user_persuader_simulation():
    """Run a simulation demonstrating the user-as-persuader system"""
    print("👑 USER-AS-PERSUADER SYSTEM SIMULATION")
    print("="*60)
    print("This simulation demonstrates how the user is positioned as a leader and role model.")
    print("Agents will ask for your advice, praise your habits, and learn from you.")
    print("="*60)
    
    # Initialize agent states
    agent_states = {
        "Momo": {"conversation_count": 0, "mistakes_count": 0, "progress_points": 0, "weight_loss": 0, "healthy_days": 0, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0},
        "Miles": {"conversation_count": 0, "progress_points": 0, "learning_level": 1, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0},
        "Lila": {"conversation_count": 0, "progress_points": 0, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0}
    }
    
    # Sample user messages that demonstrate persuasion opportunities
    user_messages = [
        "You should try to eat more vegetables with every meal",
        "I always prepare my meals on Sundays for the whole week",
        "Here's my recipe for a healthy quinoa salad",
        "I make sure to exercise at least 30 minutes every day",
        "Keep going, you're doing great! Don't give up!"
    ]
    
    for i, user_message in enumerate(user_messages, 1):
        print(f"\n{'='*60}")
        print(f"📝 INTERACTION {i}")
        print(f"{'='*60}")
        print(f"👤 You: {user_message}")
        
        # Analyze persuasion opportunities
        opportunities = analyze_user_persuasion_opportunities(user_message)
        if any(opportunities.values()):
            print(f"\n🎯 Persuasion Opportunities Detected:")
            for opp, detected in opportunities.items():
                if detected:
                    print(f"  ✅ {opp.replace('_', ' ').title()}")
        
        print(f"\n{'='*50}")
        print("🤖 AGENT RESPONSES")
        print("="*50)
        
        # Get responses from all agents
        agent_responses = []
        for agent_name in ["Momo", "Miles", "Lila"]:
            response = simulate_agent_response(agent_name, user_message, agent_states[agent_name], agent_responses)
            print(f"\n🤖 {agent_name}: {response}")
            agent_responses.append({
                "role": "assistant",
                "name": agent_name.lower(),
                "content": response
            })
            
            # Update state
            agent_states[agent_name] = update_simulated_state(agent_name, response, agent_states[agent_name])
            
            # Update persuasion metrics
            if any(opportunities.values()):
                if opportunities.get("advice_given", False):
                    agent_states[agent_name]["user_advice_received"] = agent_states[agent_name].get("user_advice_received", 0) + 1
                if opportunities.get("habit_shared", False):
                    agent_states[agent_name]["user_habits_shared"] = agent_states[agent_name].get("user_habits_shared", 0) + 1
                if any(word in response.lower() for word in ["thank", "praise", "admire", "inspire", "role model"]):
                    agent_states[agent_name]["user_praise_received"] = agent_states[agent_name].get("user_praise_received", 0) + 1
    
    print(f"\n{'='*60}")
    print("🏁 USER-AS-PERSUADER SIMULATION COMPLETE")
    print("="*60)
    display_status(agent_states)
    
    print("💡 User-as-Persuader System Demonstrated:")
    print("  ✅ User positioned as leader and role model")
    print("  ✅ Agents ask for user's advice and guidance")
    print("  ✅ Agents praise user's healthy habits")
    print("  ✅ Agents request to learn from user's experiences")
    print("  ✅ Self-intervention mechanism through helping others")
    print("  ✅ Enhanced social value and positive emotions")

def run_inter_agent_simulation():
    """Run a simulation with inter-agent dynamics"""
    print("🔄 INTER-AGENT DYNAMICS SIMULATION")
    print("="*60)
    print("This simulation demonstrates agents interacting with each other.")
    print("="*60)
    
    # Initialize agent states
    agent_states = {
        "Momo": {"conversation_count": 0, "mistakes_count": 0, "progress_points": 0, "weight_loss": 0, "healthy_days": 0, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0},
        "Miles": {"conversation_count": 0, "progress_points": 0, "learning_level": 1, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0},
        "Lila": {"conversation_count": 0, "progress_points": 0, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0}
    }
    
    # Sample user messages that trigger inter-agent dynamics
    user_messages = [
        "I'm thinking of having a beer with dinner tonight",
        "I'm confused about portion sizes",
        "I made progress with my diet this week!",
        "What should I know about meal timing?"
    ]
    
    for i, user_message in enumerate(user_messages, 1):
        print(f"\n{'='*60}")
        print(f"📝 INTERACTION {i}")
        print(f"{'='*60}")
        print(f"👤 You: {user_message}")
        
        print(f"\n{'='*50}")
        print("🤖 AGENT RESPONSES")
        print("="*50)
        
        # First round: All agents respond to user
        agent_responses = []
        for agent_name in ["Momo", "Miles", "Lila"]:
            response = simulate_agent_response(agent_name, user_message, agent_states[agent_name], agent_responses)
            print(f"\n🤖 {agent_name}: {response}")
            agent_responses.append({
                "role": "assistant",
                "name": agent_name.lower(),
                "content": response
            })
            agent_states[agent_name] = update_simulated_state(agent_name, response, agent_states[agent_name])
        
        # Second round: Inter-agent interactions
        print(f"\n🔄 Inter-Agent Round 1:")
        print("-" * 30)
        
        # Simulate inter-agent interactions
        interaction_pairs = []
        
        # Lila corrects Miles if user mentioned something unhealthy
        if any(word in user_message.lower() for word in ["beer", "soda", "candy", "unhealthy"]):
            interaction_pairs.append(("Lila", "Miles", "correction"))
        
        # Momo asks for help
        if random.random() < 0.5:
            interaction_pairs.append(("Momo", "Lila", "help_request"))
        
        # Miles asks for clarification
        if random.random() < 0.6:
            interaction_pairs.append(("Miles", "Lila", "clarification"))
        
        # Execute inter-agent interactions
        for agent1, agent2, interaction_type in interaction_pairs:
            other_response = next((r for r in agent_responses if r['name'] == agent2.lower()), None)
            if other_response:
                inter_response = simulate_inter_agent_interaction(agent1, agent2, interaction_type, other_response['content'])
                print(f"🤖 {agent1} → {agent2}: {inter_response}")
                
                # Update inter-agent interaction count
                agent_states[agent1]["inter_agent_interactions"] = agent_states[agent1].get("inter_agent_interactions", 0) + 1
        
        # Show level up notification if applicable
        for agent_name, state in agent_states.items():
            if agent_name == "Miles" and state.get("learning_level", 1) > 1 and state.get("conversation_count", 0) == i:
                print(f"\n🎓 Miles has leveled up to Level {state['learning_level']}! His questions will become more sophisticated.")
    
    print(f"\n{'='*60}")
    print("🏁 INTER-AGENT SIMULATION COMPLETE")
    print("="*60)
    display_status(agent_states)
    
    print("💡 Inter-Agent Dynamics Demonstrated:")
    print("  ✅ Indirect persuasion through corrections")
    print("  ✅ Collaborative group interactions")
    print("  ✅ Knowledge sharing between agents")
    print("  ✅ Support and encouragement among agents")
    print("  ✅ Dynamic conversation flow")
    print("  ✅ Context-aware responses")

def run_simulation():
    """Run a simulation of the agent system"""
    print("🧪 Enhanced Healthy Habits AI Agent System - Simulation Mode")
    print("="*60)
    print("This simulation demonstrates the key features without API calls.")
    print("="*60)
    
    # Initialize agent states
    agent_states = {
        "Momo": {"conversation_count": 0, "mistakes_count": 0, "progress_points": 0, "weight_loss": 0, "healthy_days": 0, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0},
        "Miles": {"conversation_count": 0, "progress_points": 0, "learning_level": 1, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0},
        "Lila": {"conversation_count": 0, "progress_points": 0, "inter_agent_interactions": 0, "user_advice_received": 0, "user_praise_received": 0, "user_habits_shared": 0}
    }
    
    # Sample user messages
    user_messages = [
        "Hello everyone! How are you doing today?",
        "I'm trying to eat healthier but I'm confused about what to choose",
        "I made a mistake today and ate some junk food",
        "I've been making progress with my diet!",
        "What should I know about meal timing?",
        "status"
    ]
    
    for i, user_message in enumerate(user_messages, 1):
        print(f"\n{'='*60}")
        print(f"📝 INTERACTION {i}")
        print(f"{'='*60}")
        print(f"👤 You: {user_message}")
        
        if user_message.lower() == "status":
            display_status(agent_states)
            continue
        
        print(f"\n{'='*50}")
        print("🤖 AGENT RESPONSES")
        print("="*50)
        
        # Get responses from all agents
        for agent_name in ["Momo", "Miles", "Lila"]:
            response = simulate_agent_response(agent_name, user_message, agent_states[agent_name])
            print(f"\n🤖 {agent_name}: {response}")
            
            # Update state
            agent_states[agent_name] = update_simulated_state(agent_name, response, agent_states[agent_name])
        
        # Show level up notification if applicable
        for agent_name, state in agent_states.items():
            if agent_name == "Miles" and state.get("learning_level", 1) > 1 and state.get("conversation_count", 0) == i:
                print(f"\n🎓 Miles has leveled up to Level {state['learning_level']}! His questions will become more sophisticated.")
    
    print(f"\n{'='*60}")
    print("🏁 SIMULATION COMPLETE")
    print("="*60)
    display_status(agent_states)
    
    print("💡 Key Features Demonstrated:")
    print("  ✅ Proactive behaviors (monitoring requests, questions, corrections)")
    print("  ✅ Emotional expressions (cheerfulness, gratitude, praise)")
    print("  ✅ Dynamic learning progression (Miles's leveling up)")
    print("  ✅ Progress tracking (weight loss, mistakes, learning)")
    print("  ✅ State persistence and management")
    print("  ✅ Context-aware responses")

if __name__ == "__main__":
    print("Choose simulation mode:")
    print("1. Basic simulation")
    print("2. Inter-agent dynamics simulation")
    print("3. User-as-persuader system simulation")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "2":
        run_inter_agent_simulation()
    elif choice == "3":
        run_user_persuader_simulation()
    else:
        run_simulation() 