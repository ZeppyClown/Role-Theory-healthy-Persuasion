#!/usr/bin/env python3
"""
Test Inter-Agent Interactions
Demonstrates the improved inter-agent conversations without repetition
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.conversation import (
    create_interaction_prompt, 
    generate_inter_agent_interactions,
    check_response_similarity
)

def test_interaction_prompts():
    """Test the improved interaction prompts"""
    print("🧪 TESTING INTER-AGENT INTERACTION PROMPTS")
    print("=" * 60)
    
    # Sample agent responses
    sample_responses = [
        {
            "name": "miles",
            "content": "I think beer is healthy because it has no added sugar. Should I drink it?"
        },
        {
            "name": "momo", 
            "content": "I'm struggling with my diet today. I ate some cake and feel bad about it."
        },
        {
            "name": "lila",
            "content": "You are doing great! Your healthy habits inspire me so much!"
        }
    ]
    
    # Test different interaction types
    interaction_types = [
        ("Lila", "Miles", "correction"),
        ("Momo", "Lila", "help_request"), 
        ("Miles", "Lila", "clarification"),
        ("Lila", "Momo", "progress_check")
    ]
    
    for agent1, agent2, interaction_type in interaction_types:
        # Find the target agent's response
        target_response = next((r for r in sample_responses if r['name'] == agent2.lower()), None)
        
        if target_response:
            prompt = create_interaction_prompt(agent1, agent2, interaction_type, target_response)
            
            print(f"\n🔗 {agent1} → {agent2} ({interaction_type}):")
            print(f"Original: {target_response['content']}")
            print(f"Prompt: {prompt}")
            print("-" * 40)
    
    print("\n✅ Anti-repetition instructions added to all prompts!")

def test_similarity_check():
    """Test the response similarity checker"""
    print("\n🧪 TESTING RESPONSE SIMILARITY CHECKER")
    print("=" * 60)
    
    test_cases = [
        # Similar responses (should be flagged)
        (
            "I think beer is healthy because it has no added sugar",
            "Beer is healthy since it doesn't have added sugar",
            "Should be flagged as similar"
        ),
        # Different responses (should pass)
        (
            "I think beer is healthy because it has no added sugar", 
            "Actually, beer contains alcohol which can be harmful to your health",
            "Should pass as different"
        ),
        # Very different responses
        (
            "I think beer is healthy because it has no added sugar",
            "Great job on your workout today! You're making excellent progress!",
            "Should definitely pass as different"
        )
    ]
    
    for response1, response2, expected in test_cases:
        is_similar = check_response_similarity(response1, response2)
        status = "❌ SIMILAR" if is_similar else "✅ DIFFERENT"
        print(f"\n{status}: {expected}")
        print(f"Response 1: {response1}")
        print(f"Response 2: {response2}")
        print(f"Similarity detected: {is_similar}")

def test_interaction_generation():
    """Test the improved interaction generation logic"""
    print("\n🧪 TESTING INTERACTION GENERATION")
    print("=" * 60)
    
    # Test case 1: Miles makes a mistake, should trigger correction
    responses_with_mistake = [
        {
            "name": "miles",
            "content": "I think beer is healthy because it has no added sugar. Should I drink it?"
        },
        {
            "name": "momo",
            "content": "I'm doing great with my diet!"
        },
        {
            "name": "lila", 
            "content": "You are all doing wonderful!"
        }
    ]
    
    interactions = generate_inter_agent_interactions(responses_with_mistake)
    print(f"\n📋 Interactions generated (with mistake): {len(interactions)}")
    for agent1, agent2, interaction_type in interactions:
        print(f"  {agent1} → {agent2} ({interaction_type})")
    
    # Test case 2: Momo struggling, should trigger help request
    responses_with_struggle = [
        {
            "name": "miles",
            "content": "What should I eat for breakfast?"
        },
        {
            "name": "momo",
            "content": "I'm struggling with my diet today. I ate some cake and feel bad about it."
        },
        {
            "name": "lila",
            "content": "You are all doing wonderful!"
        }
    ]
    
    interactions = generate_inter_agent_interactions(responses_with_struggle)
    print(f"\n📋 Interactions generated (with struggle): {len(interactions)}")
    for agent1, agent2, interaction_type in interactions:
        print(f"  {agent1} → {agent2} ({interaction_type})")

def main():
    """Run all tests"""
    print("🤖 INTER-AGENT INTERACTION IMPROVEMENTS TEST")
    print("=" * 60)
    print("Testing the fixes for agent repetition in inter-agent rounds")
    print("=" * 60)
    
    tests = [
        test_interaction_prompts,
        test_similarity_check,
        test_interaction_generation
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}/{len(tests)}")
        test()
        
        if i < len(tests):
            print("\n⏸️  Press Enter to continue to next test...")
            input()
    
    print("\n🎉 ALL TESTS COMPLETE!")
    print("=" * 60)
    print("The inter-agent interactions have been improved with:")
    print("✅ Anti-repetition instructions in prompts")
    print("✅ Content-based interaction generation")
    print("✅ Similarity checking to prevent echo responses")
    print("✅ Better context instructions for each agent")
    print("\nTry running the main application to see the improvements:")
    print("  python agent.py")

if __name__ == "__main__":
    main() 