#!/usr/bin/env python3
"""
Demo Script for Research and Evaluation Features
This script demonstrates the enhanced multi-agent system with:
- Structured outputs for research analysis
- Expanded health domains beyond sugar intake
- Long-term engagement tracking
- Performance metrics and evaluation
"""

import json
import time
from datetime import datetime
from agent import (
    run_inter_agent_conversation, 
    analyze_research_data, 
    save_research_data,
    display_agent_status,
    conversation_history,
    session_id
)

def demo_research_features():
    """Demonstrate the research and evaluation features"""
    
    print("🔬 RESEARCH & EVALUATION FEATURES DEMO")
    print("="*60)
    print("This demo showcases the enhanced multi-agent system with:")
    print("• Structured data collection for research analysis")
    print("• Expanded health domains (nutrition, exercise, sleep, stress, etc.)")
    print("• Long-term engagement tracking and evaluation")
    print("• Performance metrics and persona adherence analysis")
    print("• User-as-persuader dynamics measurement")
    print("="*60)
    
    # Demo conversation scenarios
    demo_scenarios = [
        {
            "title": "Nutrition & Meal Planning",
            "user_input": "I always prepare my meals on Sundays for the week. I make grilled chicken, quinoa, and roasted vegetables. It helps me stay on track with my health goals.",
            "expected_domains": ["nutrition", "meal_planning", "healthy_habits"]
        },
        {
            "title": "Exercise & Fitness",
            "user_input": "I've been doing 30 minutes of cardio every morning before work. It really helps with my energy levels throughout the day.",
            "expected_domains": ["exercise", "fitness", "energy_management"]
        },
        {
            "title": "Sleep & Stress Management",
            "user_input": "I've been practicing meditation before bed and it's really improved my sleep quality. I feel much more rested now.",
            "expected_domains": ["sleep", "stress_management", "mental_health"]
        },
        {
            "title": "Weight Management & Progress",
            "user_input": "I've lost 5 pounds this month by tracking my calories and staying consistent with my workout routine.",
            "expected_domains": ["weight_management", "progress_tracking", "consistency"]
        },
        {
            "title": "Hydration & Wellness",
            "user_input": "I make sure to drink 8 glasses of water daily and take regular breaks from my computer to stretch.",
            "expected_domains": ["hydration", "general_wellness", "work_life_balance"]
        }
    ]
    
    print("\n🚀 Starting Demo Conversations...")
    print("-" * 40)
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n📝 Scenario {i}: {scenario['title']}")
        print(f"User: {scenario['user_input']}")
        print("-" * 40)
        
        # Run the conversation
        agent_responses = run_inter_agent_conversation(scenario['user_input'], conversation_history)
        
        # Display responses
        for response in agent_responses:
            if 'interaction_type' not in response:  # Direct responses only
                print(f"🤖 {response['name'].capitalize()}: {response['content'][:100]}...")
        
        # Add to conversation history
        conversation_history.append({"role": "user", "content": scenario['user_input']})
        for response in agent_responses:
            conversation_history.append(response)
        
        print(f"✅ Completed scenario {i}")
        time.sleep(1)  # Brief pause between scenarios
    
    print("\n" + "="*60)
    print("📊 RESEARCH DATA ANALYSIS")
    print("="*60)
    
    # Analyze the collected data
    analysis = analyze_research_data()
    
    if "error" not in analysis:
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"  Total Responses: {analysis['total_responses']}")
        print(f"  Average Response Time: {analysis['performance_metrics']['avg_response_time']:.2f} seconds")
        print(f"  Total Conversation Turns: {analysis['performance_metrics']['total_conversation_turns']}")
        
        print(f"\n🤖 AGENT DISTRIBUTION:")
        for agent, count in analysis['agent_distribution'].items():
            percentage = (count / analysis['total_responses']) * 100
            print(f"  {agent}: {count} responses ({percentage:.1f}%)")
        
        print(f"\n🎭 PERSONA ADHERENCE SCORES:")
        for agent, score in analysis['persona_adherence_scores'].items():
            print(f"  {agent}: {score:.2f}/1.0")
        
        print(f"\n🏥 HEALTH DOMAIN COVERAGE:")
        for domain, count in analysis['health_domain_coverage'].items():
            print(f"  {domain}: {count} mentions")
        
        print(f"\n🎯 PERSUASION TECHNIQUES USED:")
        for technique, count in analysis['persuasion_techniques_used'].items():
            print(f"  {technique}: {count} instances")
        
        print(f"\n📊 ENGAGEMENT METRICS:")
        print(f"  Average Interactivity: {analysis['engagement_metrics']['avg_interactivity']:.2f}/1.0")
        print(f"  Average Emotional Intensity: {analysis['engagement_metrics']['avg_emotional_intensity']:.2f}/1.0")
        print(f"  Average Response Length: {analysis['engagement_metrics']['avg_response_length']:.0f} words")
        
    else:
        print("❌ No research data available for analysis")
    
    print("\n" + "="*60)
    print("💾 SAVING RESEARCH DATA")
    print("="*60)
    
    # Save the research data
    save_research_data()
    
    print(f"\n📁 Research data saved to: research_data_{session_id}.json")
    print("This file contains structured data for further analysis including:")
    print("• Agent response patterns and persona adherence")
    print("• Health domain coverage and topic evolution")
    print("• Persuasion technique effectiveness")
    print("• Engagement metrics and user interaction patterns")
    print("• Performance timing and response quality")
    
    print("\n" + "="*60)
    print("🔍 RESEARCH APPLICATIONS")
    print("="*60)
    print("The collected data can be used for:")
    print("• Academic research on AI agent effectiveness")
    print("• User engagement pattern analysis")
    print("• Persuasion technique optimization")
    print("• Health intervention effectiveness studies")
    print("• Long-term behavior change research")
    print("• Multi-agent system performance evaluation")
    
    print("\n" + "="*60)
    print("🎯 KEY RESEARCH INSIGHTS")
    print("="*60)
    print("1. EXPANDED HEALTH SCOPE: System now covers 8 health domains")
    print("2. STRUCTURED DATA: JSON-formatted responses for systematic analysis")
    print("3. PERFORMANCE TRACKING: Response times, engagement scores, persona adherence")
    print("4. USER-AS-PERSUADER: Metrics on user guidance and role model reinforcement")
    print("5. INTER-AGENT DYNAMICS: Collaboration patterns and knowledge sharing")
    print("6. LONG-TERM ENGAGEMENT: Progressive learning and adaptive interactions")
    
    print("\n✅ Demo completed successfully!")
    print("The enhanced system is ready for research and long-term health intervention studies.")

def demo_health_domain_expansion():
    """Demonstrate the expanded health domains"""
    
    print("\n🏥 HEALTH DOMAIN EXPANSION DEMO")
    print("="*50)
    print("The system now covers multiple health domains beyond sugar intake:")
    
    health_domains = {
        "Nutrition": "Food choices, meal planning, dietary patterns",
        "Exercise": "Physical activity, fitness routines, workout plans",
        "Sleep": "Sleep hygiene, rest patterns, energy management",
        "Stress Management": "Relaxation techniques, meditation, mindfulness",
        "Weight Management": "Weight goals, body composition, progress tracking",
        "Mental Health": "Mood, emotional well-being, psychological health",
        "Hydration": "Water intake, fluid balance, hydration habits",
        "General Wellness": "Overall lifestyle, healthy habits, well-being"
    }
    
    for domain, description in health_domains.items():
        print(f"• {domain}: {description}")
    
    print("\nThis expansion allows for:")
    print("• More comprehensive health coaching")
    print("• Broader user engagement opportunities")
    print("• Diverse research applications")
    print("• Sustained long-term interactions")

def demo_long_term_features():
    """Demonstrate long-term engagement features"""
    
    print("\n📈 LONG-TERM ENGAGEMENT FEATURES")
    print("="*50)
    print("Features designed for sustained user engagement:")
    
    features = [
        "Progressive Learning: Miles's knowledge evolves over time",
        "Dynamic Interactions: Agents adapt based on conversation history",
        "Health Domain Expansion: Broader scope beyond sugar intake",
        "Research Tracking: Comprehensive data collection for analysis",
        "Performance Metrics: Response times, engagement scores",
        "Structured Outputs: JSON-formatted data for research",
        "User-as-Persuader: Reinforces user's role as leader and teacher",
        "Inter-Agent Dynamics: Collaborative learning and support"
    ]
    
    for feature in features:
        print(f"• {feature}")
    
    print("\nBenefits for long-term engagement:")
    print("• Prevents conversation monotony")
    print("• Maintains user interest through variety")
    print("• Enables research on sustained behavior change")
    print("• Supports academic studies and clinical applications")

if __name__ == "__main__":
    print("🔬 Multi-Agent System Research Features Demo")
    print("="*60)
    
    # Run the main demo
    demo_research_features()
    
    # Additional feature demonstrations
    demo_health_domain_expansion()
    demo_long_term_features()
    
    print("\n" + "="*60)
    print("🎉 Demo completed! The enhanced system is ready for research use.")
    print("="*60) 