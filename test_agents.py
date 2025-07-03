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
        "I'm feeling weak today. Could you remind me to stay away from the candy aisle? I need your help to be strong! 🙏"
    ],
    "Miles": [
        "I'm confused about fruits again! Which should I take? Durian or apple? I heard durian is high in calories but apple has sugar too. Can you help me understand which is better for my health goals? 🤔",
        "Oh, I got it! I will choose yoghurt without added sugar next time. That's useful! Thank you for sharing the piece of knowledge about GI of food. I'm learning so much! 📚",
        "Can I take potato instead of rice? I think it has lower GI which may keep my blood glucose level stable. Is this correct? 🥔",
        "Thank you for explaining! I understand now that timing matters too. I'll try to eat my carbs earlier in the day. You're such a great teacher! 🙏"
    ],
    "Lila": [
        "Miles, do not take beer. Though it contains no added sugar, the high carbohydrate will increase your blood glucose. You're doing great asking questions though! Keep learning! 🌟",
        "You are doing great! Hope I could be as perseverant as you are. Your dedication to helping us learn is truly inspiring! ✨",
        "I've been following a Mediterranean diet for 3 years now, and it's been amazing for my energy levels. The key is consistency and portion control! 🥗",
        "Momo, remember that progress isn't linear! Every healthy choice you make is a victory. You're stronger than you think! 💪"
    ]
}

def simulate_agent_response(agent_name: str, user_message: str, state: Dict) -> str:
    """Simulate agent response based on current state and user message"""
    responses = SAMPLE_RESPONSES[agent_name]
    
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
        
        if name == "Momo":
            print(f"  ⚖️  Weight Loss: {state.get('weight_loss', 0)} kg")
            print(f"  🏃 Healthy Days: {state.get('healthy_days', 0)}")
            print(f"  ❌ Mistakes: {state.get('mistakes_count', 0)}")
        elif name == "Miles":
            print(f"  🧠 Learning Level: {state.get('learning_level', 1)}/3")
        elif name == "Lila":
            print(f"  💡 Knowledge Shared: {state.get('progress_points', 0)}")
    
    print("="*50 + "\n")

def run_simulation():
    """Run a simulation of the agent system"""
    print("🧪 Enhanced Healthy Habits AI Agent System - Simulation Mode")
    print("="*60)
    print("This simulation demonstrates the key features without API calls.")
    print("="*60)
    
    # Initialize agent states
    agent_states = {
        "Momo": {"conversation_count": 0, "mistakes_count": 0, "progress_points": 0, "weight_loss": 0, "healthy_days": 0},
        "Miles": {"conversation_count": 0, "progress_points": 0, "learning_level": 1},
        "Lila": {"conversation_count": 0, "progress_points": 0}
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
    run_simulation() 