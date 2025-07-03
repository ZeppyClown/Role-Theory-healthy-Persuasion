"""
Research Utilities
Provides tools for data analysis and structured outputs
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
import uuid

def create_structured_response(
    agent_name: str, 
    response_text: str, 
    response_time: float, 
    persuasion_opportunities: Dict[str, bool], 
    other_agents_responses: List[Dict]
) -> Dict[str, Any]:
    """Create structured response data for research analysis"""
    
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
    
    return {
        "agent_name": agent_name,
        "timestamp": datetime.now().isoformat(),
        "response_text": response_text,
        "response_time": response_time,
        "persona_adherence": persona_adherence,
        "persuasion_techniques": persuasion_techniques,
        "health_domains": health_domains,
        "user_as_persuader": user_as_persuader,
        "inter_agent_dynamics": inter_agent_dynamics,
        "engagement_metrics": engagement_metrics
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

def save_research_data(structured_responses: List[Dict], session_id: str, conversation_turn: int, response_times: List[float]) -> None:
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

def analyze_research_data(structured_responses: List[Dict], response_times: List[float], conversation_turn: int) -> Dict[str, Any]:
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