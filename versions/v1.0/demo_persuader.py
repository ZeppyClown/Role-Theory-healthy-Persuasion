#!/usr/bin/env python3
"""
Demo script for the User-as-Persuader System
Shows how the user is positioned as a leader and role model
"""

import random

def demo_user_as_persuader():
    """Demonstrate the user-as-persuader system"""
    print("👑 USER-AS-PERSUADER SYSTEM DEMONSTRATION")
    print("="*60)
    print("This system positions YOU as a leader, role model, and teacher.")
    print("Agents will ask for your advice, praise your habits, and learn from you.")
    print("This creates a self-intervention mechanism where helping others")
    print("reinforces your own healthy behaviors.")
    print("="*60)
    
    # Sample user messages that trigger persuasion opportunities
    user_messages = [
        "You should try to eat more vegetables with every meal",
        "I always prepare my meals on Sundays for the whole week",
        "Here's my recipe for a healthy quinoa salad",
        "I make sure to exercise at least 30 minutes every day",
        "Keep going, you're doing great! Don't give up!"
    ]
    
    # Sample agent responses for each persuasion opportunity
    agent_responses = {
        "advice_given": {
            "Momo": "Thank you for your advice! I will definitely follow it. You're such a good role model! 🙏",
            "Miles": "Can you explain that to me? I want to understand better. You're so knowledgeable! 📚",
            "Lila": "You are such an inspiring role model! I admire your dedication. You're amazing! 🌟"
        },
        "habit_shared": {
            "Momo": "Wow, that's such a good habit! Can you teach me how to do that? You're so disciplined! 😍",
            "Miles": "What's your experience with that? I'd love to learn from you. You're so wise! 🌟",
            "Lila": "Your healthy habits are truly motivating. You're a true leader! 👑"
        },
        "recipe_shared": {
            "Momo": "That sounds delicious! Can you share your recipe with me? Your cooking skills are amazing! 👨‍🍳",
            "Miles": "That's interesting! Can you teach me more about it? You're my best teacher! 🎓",
            "Lila": "I'm so impressed by your consistency. You're the best example! ✨"
        },
        "exercise_tip": {
            "Momo": "You're my inspiration! I want to follow your example. You're so consistent! 💪",
            "Miles": "How do you handle that situation? I need your advice. You're my guide! 🗺️",
            "Lila": "You set such a great example for all of us. You're our hero! 🦸‍♀️"
        },
        "motivation_provided": {
            "Momo": "Your guidance means so much to me. I'll try my best! You're my inspiration! 💪",
            "Miles": "Can you guide me on this? I trust your judgment. You're so reliable! 🤝",
            "Lila": "Thank you for being such a great leader in our group! You're wonderful! 🌟"
        }
    }
    
    for i, user_message in enumerate(user_messages, 1):
        print(f"\n{'='*60}")
        print(f"📝 INTERACTION {i}")
        print(f"{'='*60}")
        print(f"👤 You: {user_message}")
        
        # Determine the persuasion opportunity
        if "should" in user_message.lower():
            opportunity = "advice_given"
        elif "always" in user_message.lower() or "make sure" in user_message.lower():
            opportunity = "habit_shared"
        elif "recipe" in user_message.lower():
            opportunity = "recipe_shared"
        elif "exercise" in user_message.lower():
            opportunity = "exercise_tip"
        elif "keep going" in user_message.lower():
            opportunity = "motivation_provided"
        else:
            opportunity = "advice_given"
        
        print(f"\n🎯 Persuasion Opportunity: {opportunity.replace('_', ' ').title()}")
        
        print(f"\n{'='*50}")
        print("🤖 AGENT RESPONSES")
        print("="*50)
        
        # Show agent responses
        for agent_name in ["Momo", "Miles", "Lila"]:
            response = agent_responses[opportunity][agent_name]
            print(f"\n🤖 {agent_name}: {response}")
        
        print(f"\n💡 Self-Intervention Mechanism:")
        print(f"  • You gave advice → Agents praised your wisdom")
        print(f"  • You shared habits → Agents admired your discipline")
        print(f"  • You provided motivation → Agents expressed gratitude")
        print(f"  • This reinforces YOUR commitment to healthy behaviors!")
    
    print(f"\n{'='*60}")
    print("🏁 DEMONSTRATION COMPLETE")
    print("="*60)
    
    print("💡 Key Benefits of User-as-Persuader System:")
    print("  ✅ Maintains self-image as role model")
    print("  ✅ Enhances belief commitment through teaching")
    print("  ✅ Creates social value and appreciation")
    print("  ✅ Generates positive emotions from praise")
    print("  ✅ Reinforces healthy behaviors through helping others")
    print("  ✅ Avoids direct teaching/coaching of the user")
    print("  ✅ Positions user as leader and mentor")

if __name__ == "__main__":
    demo_user_as_persuader() 