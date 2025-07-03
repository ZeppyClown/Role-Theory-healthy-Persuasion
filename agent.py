"""
Enhanced Multi-Agent System with Streaming
A modular implementation with separate agent files and real-time streaming
"""

from openai import OpenAI
import os, dotenv
import json
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Import our modular components
from agents import MomoAgent, MilesAgent, LilaAgent
from utils import (
    streaming_manager, stream_agent_response, stream_inter_agent_interaction,
    create_structured_response, save_research_data, analyze_research_data,
    analyze_user_persuasion_opportunities, run_inter_agent_conversation,
    ConversationManager
)
from config import get_config

dotenv.load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")

if not secret_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

client = OpenAI(api_key=secret_key)
config = get_config()

# Initialize agents
agents = {
    "Momo": MomoAgent(),
    "Miles": MilesAgent(),
    "Lila": LilaAgent()
}

# Initialize conversation manager
conversation_manager = ConversationManager()

# Research and Evaluation Tracking
session_id = str(uuid.uuid4())
conversation_turn = 0
structured_responses = []
response_times = []

def run_agent(agent, user_message: str, history: List[Dict], other_agents_responses: List[Dict] = []) -> str:
    """Enhanced agent response function with streaming and research tracking"""
    global conversation_turn
    
    agent.conversation_count += 1
    
    # Analyze user message for persuasion opportunities
    persuasion_opportunities = analyze_user_persuasion_opportunities(user_message)
    
    # Get context-aware prompt
    context = agent.get_context(user_message, history, other_agents_responses)
    
    # Add persuasion opportunity context
    if any(persuasion_opportunities.values()):
        context += "\nPERSUASION OPPORTUNITIES DETECTED:\n"
        for opportunity, detected in persuasion_opportunities.items():
            if detected:
                context += f"- {opportunity.replace('_', ' ').title()}: True\n"
        context += "\nRESPOND BY: Expressing admiration, asking to learn more, requesting details, praising the user's leadership\n"
    
    # Enhanced system prompt with user-as-persuader dynamics
    enhanced_prompt = f"{agent.PERSONA}\n\nCURRENT CONTEXT:\n{context}\n\nRemember to treat the user as your leader and role model. Ask for their advice, praise their habits, and express gratitude for their guidance."
    
    messages = [
        {"role": "system", "content": enhanced_prompt}
    ] + history + [
        {"role": "user", "content": user_message}
    ]

    # Track response time for research
    start_time = time.time()
    
    try:
        # Use streaming for better user experience
        response = client.chat.completions.create(
            model=config["openai"]["model"],
            messages=messages,
            temperature=config["openai"]["temperature"],
            max_tokens=config["openai"]["max_tokens"],
            stream=True  # Enable streaming
        )
        
        # Stream the response
        full_response = ""
        print(f"\n🤖 {agent.name}: ", end='', flush=True)
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)
                full_response += content
                time.sleep(0.02)  # Small delay for typing effect
        
        print()  # New line at the end
        
        response_time = time.time() - start_time
        
        # Update agent state based on response content
        agent.update_state(full_response, user_message, persuasion_opportunities)
        
        # Track inter-agent interactions
        if other_agents_responses and any(agent.name.lower() in response['content'].lower() for response in other_agents_responses):
            agent.inter_agent_interactions += 1
        
        # Create structured response for research
        structured_response = create_structured_response(
            agent.name, full_response, response_time, persuasion_opportunities, other_agents_responses
        )
        structured_responses.append(structured_response)
        response_times.append(response_time)
        
        return full_response
        
    except Exception as e:
        error_msg = f"Sorry, I'm having trouble responding right now. Error: {str(e)}"
        print(f"\n❌ {agent.name}: {error_msg}")
        return error_msg

def save_agent_states():
    """Save agent states to file"""
    states_data = {name: agent.to_dict() for name, agent in agents.items()}
    states_data["user_persuasion_state"] = conversation_manager.get_persuasion_metrics()
    with open("agent_states.json", "w") as f:
        json.dump(states_data, f, indent=2)

def load_agent_states():
    """Load agent states from file"""
    try:
        with open("agent_states.json", "r") as f:
            states_data = json.load(f)
            for name, data in states_data.items():
                if name in agents:
                    agents[name].from_dict(data)
                elif name == "user_persuasion_state":
                    conversation_manager.user_persuasion_state.update(data)
    except FileNotFoundError:
        pass  # First time running, no saved states

def display_agent_status():
    """Display current status of all agents"""
    print("\n" + "="*50)
    print("🤖 AGENT STATUS REPORT")
    print("="*50)
    
    for name, agent in agents.items():
        print(f"\n{name}:")
        print(f"  💬 Conversations: {agent.conversation_count}")
        print(f"  📈 Progress Points: {agent.progress_points}")
        print(f"  🔄 Inter-Agent Interactions: {agent.inter_agent_interactions}")
        print(f"  💡 User Advice Received: {agent.user_advice_received}")
        print(f"  👑 User Praise Received: {agent.user_praise_received}")
        print(f"  🍽️  User Habits Shared: {agent.user_habits_shared}")
        
        if name == "Momo":
            print(f"  ⚖️  Weight Loss: {agent.weight_loss} kg")
            print(f"  🏃 Healthy Days: {agent.healthy_days}")
            print(f"  ❌ Mistakes: {agent.mistakes_count}")
        elif name == "Miles":
            print(f"  🧠 Learning Level: {agent.learning_level}/3")
        elif name == "Lila":
            print(f"  💡 Knowledge Shared: {agent.progress_points}")
            print(f"  ✅ Corrections Provided: {agent.corrections_provided}")
    
    persuasion_metrics = conversation_manager.get_persuasion_metrics()
    print(f"\n👤 USER PERSUASION METRICS:")
    print(f"  💬 Advice Given: {persuasion_metrics['advice_given']}")
    print(f"  🍽️  Habits Shared: {persuasion_metrics['habits_shared']}")
    print(f"  👑 Praise Received: {persuasion_metrics['praise_received']}")
    print(f"  🌟 Role Model Moments: {persuasion_metrics['role_model_moments']}")
    print(f"  💎 Social Value Created: {persuasion_metrics['social_value_created']}")
    
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
        global agents, conversation_manager
        agents = {
            "Momo": MomoAgent(),
            "Miles": MilesAgent(),
            "Lila": LilaAgent()
        }
        conversation_manager.reset_conversation()
        print("🔄 Agent states reset!")
        return True
    elif user_input.lower().startswith("check "):
        agent_name = user_input[6:].strip().capitalize()
        if agent_name in agents:
            agent = agents[agent_name]
            print(f"\n🔍 {agent_name}'s Status:")
            print(f"  Conversations: {agent.conversation_count}")
            print(f"  Progress Points: {agent.progress_points}")
            print(f"  Inter-Agent Interactions: {agent.inter_agent_interactions}")
            print(f"  User Advice Received: {agent.user_advice_received}")
            print(f"  User Praise Received: {agent.user_praise_received}")
            print(f"  User Habits Shared: {agent.user_habits_shared}")
            if agent_name == "Momo":
                print(f"  Weight Loss: {agent.weight_loss} kg")
                print(f"  Healthy Days: {agent.healthy_days}")
            elif agent_name == "Miles":
                print(f"  Learning Level: {agent.learning_level}/3")
            elif agent_name == "Lila":
                print(f"  Corrections Provided: {agent.corrections_provided}")
        else:
            print(f"❌ Agent '{agent_name}' not found.")
        return True
    elif user_input.lower() == "streaming":
        print("\n⚡ STREAMING SETTINGS")
        print("="*50)
        print(f"Streaming enabled: {streaming_manager.enabled}")
        print(f"Delay: {streaming_manager.delay}s")
        print("Commands:")
        print("  'streaming on' - Enable streaming")
        print("  'streaming off' - Disable streaming")
        print("  'delay [seconds]' - Set typing delay")
        print("="*50)
        return True
    elif user_input.lower() == "streaming on":
        streaming_manager.set_streaming(True)
        print("✅ Streaming enabled!")
        return True
    elif user_input.lower() == "streaming off":
        streaming_manager.set_streaming(False)
        print("❌ Streaming disabled!")
        return True
    elif user_input.lower().startswith("delay "):
        try:
            delay = float(user_input[6:])
            streaming_manager.set_delay(delay)
            print(f"⏱️  Typing delay set to {delay}s")
        except ValueError:
            print("❌ Invalid delay value. Use a number like 'delay 0.03'")
        return True
    elif user_input.lower() == "research":
        print("\n📊 RESEARCH DATA ANALYSIS")
        print("="*50)
        analysis = analyze_research_data(structured_responses, response_times, conversation_turn)
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
        save_research_data(structured_responses, session_id, conversation_turn, response_times)
        return True
    elif user_input.lower() == "help":
        print("\n📋 AVAILABLE COMMANDS:")
        print("="*50)
        print("  'status' - View agent progress and user persuasion metrics")
        print("  'save' - Save agent states")
        print("  'reset' - Reset all agent states")
        print("  'check [agent]' - Check specific agent status")
        print("  'streaming' - View streaming settings")
        print("  'streaming on/off' - Enable/disable streaming")
        print("  'delay [seconds]' - Set typing delay")
        print("  'research' - View research data analysis")
        print("  'save_research' - Save structured research data")
        print("  'help' - Show this help message")
        print("  'exit' or 'quit' - Stop the chat")
        print("="*50)
        return True
    return False

# Main interaction loop
if __name__ == "__main__":
    # Load existing agent states
    load_agent_states()
    
    print("💬 Welcome to the Enhanced Healthy Habits Chat!")
    print("🤖 Meet Momo, Miles, and Lila - Your AI Health Companions!")
    print("\n🔄 NEW: Modular Architecture!")
    print("   Clean, organized code with separate agent files.")
    print("\n⚡ NEW: Real-time Streaming!")
    print("   Watch agents type their responses in real-time.")
    print("\n👑 NEW: User-as-Persuader System!")
    print("   You are positioned as a leader and role model. Agents will learn from you!")
    print("\n📊 NEW: Research & Evaluation System!")
    print("   Comprehensive data collection and analysis for research purposes.")
    print("\n🏥 NEW: Expanded Health Domains!")
    print("   Beyond sugar intake - covering nutrition, exercise, sleep, stress, and more.")
    print("\n📋 Type 'help' for available commands")
    print("\n" + "="*50)

    while True:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in {"exit", "quit"}:
            save_agent_states()
            save_research_data(structured_responses, session_id, conversation_turn, response_times)
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
        agent_responses = run_inter_agent_conversation(user_input, conversation_manager.get_recent_history(), agents, run_agent)
        
        # Display all responses (already streamed, just add to history)
        for response in agent_responses:
            # Add to conversation history
            conversation_manager.add_to_history(response)

        # Add user message to history
        conversation_manager.add_to_history({
            "role": "user",
            "content": user_input
        }) 