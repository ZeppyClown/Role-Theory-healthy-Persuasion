"""
Structured Outputs System for Research and Data Analysis
This module provides JSON schemas for agent responses to enable systematic analysis
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime

class PersuasionTechnique(Enum):
    """Enumeration of persuasion techniques used by agents"""
    SOCIAL_PROOF = "social_proof"
    AUTHORITY = "authority"
    RECIPROCITY = "reciprocity"
    COMMITMENT_CONSISTENCY = "commitment_consistency"
    LIKING = "liking"
    SCARCITY = "scarcity"
    EMOTIONAL_APPEAL = "emotional_appeal"
    LOGICAL_ARGUMENT = "logical_argument"
    STORYTELLING = "storytelling"
    DIRECT_INSTRUCTION = "direct_instruction"

class AgentPersona(Enum):
    """Enumeration of agent personas"""
    MOMO = "momo"
    MILES = "miles"
    LILA = "lila"

class InteractionType(Enum):
    """Enumeration of interaction types"""
    USER_RESPONSE = "user_response"
    INTER_AGENT = "inter_agent"
    PROACTIVE = "proactive"
    CORRECTION = "correction"
    HELP_REQUEST = "help_request"
    KNOWLEDGE_SHARING = "knowledge_sharing"

class HealthDomain(Enum):
    """Enumeration of health domains"""
    NUTRITION = "nutrition"
    EXERCISE = "exercise"
    SLEEP = "sleep"
    STRESS_MANAGEMENT = "stress_management"
    WEIGHT_MANAGEMENT = "weight_management"
    MENTAL_HEALTH = "mental_health"
    HYDRATION = "hydration"
    GENERAL_WELLNESS = "general_wellness"

# JSON Schema for Structured Agent Responses
AGENT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "agent_name": {"type": "string", "enum": ["Momo", "Miles", "Lila"]},
        "timestamp": {"type": "string", "format": "date-time"},
        "interaction_id": {"type": "string"},
        "response_text": {"type": "string"},
        "persona_adherence": {
            "type": "object",
            "properties": {
                "score": {"type": "number", "minimum": 0, "maximum": 1},
                "traits_demonstrated": {"type": "array", "items": {"type": "string"}},
                "emotional_expression": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["score", "traits_demonstrated", "emotional_expression", "confidence"]
        },
        "persuasion_techniques": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "technique": {"type": "string"},
                    "intensity": {"type": "number", "minimum": 0, "maximum": 1},
                    "target": {"type": "string"},
                    "effectiveness_estimate": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": ["technique", "intensity", "target", "effectiveness_estimate"]
            }
        },
        "health_domains": {
            "type": "array",
            "items": {"type": "string"}
        },
        "user_as_persuader": {
            "type": "object",
            "properties": {
                "opportunity_detected": {"type": "boolean"},
                "opportunity_type": {"type": "string"},
                "user_guidance_requested": {"type": "boolean"},
                "user_praise_provided": {"type": "boolean"},
                "role_model_reinforcement": {"type": "boolean"}
            },
            "required": ["opportunity_detected", "opportunity_type", "user_guidance_requested", "user_praise_provided", "role_model_reinforcement"]
        },
        "inter_agent_dynamics": {
            "type": "object",
            "properties": {
                "interaction_type": {"type": "string"},
                "target_agent": {"type": "string"},
                "collaboration_level": {"type": "number", "minimum": 0, "maximum": 1},
                "knowledge_shared": {"type": "boolean"},
                "correction_provided": {"type": "boolean"}
            },
            "required": ["interaction_type", "target_agent", "collaboration_level", "knowledge_shared", "correction_provided"]
        },
        "engagement_metrics": {
            "type": "object",
            "properties": {
                "response_length": {"type": "number"},
                "emotional_intensity": {"type": "number", "minimum": 0, "maximum": 1},
                "interactivity_level": {"type": "number", "minimum": 0, "maximum": 1},
                "question_asked": {"type": "boolean"},
                "call_to_action": {"type": "boolean"}
            },
            "required": ["response_length", "emotional_intensity", "interactivity_level", "question_asked", "call_to_action"]
        },
        "research_metadata": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "conversation_turn": {"type": "number"},
                "user_persuasion_score": {"type": "number", "minimum": 0, "maximum": 1},
                "agent_learning_progress": {"type": "number", "minimum": 0, "maximum": 1},
                "overall_engagement": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["session_id", "conversation_turn", "user_persuasion_score", "agent_learning_progress", "overall_engagement"]
        }
    },
    "required": [
        "agent_name", "timestamp", "interaction_id", "response_text", 
        "persona_adherence", "persuasion_techniques", "health_domains",
        "user_as_persuader", "inter_agent_dynamics", "engagement_metrics", "research_metadata"
    ]
}

def create_structured_response(
    agent_name: str,
    response_text: str,
    interaction_id: str,
    session_id: str,
    conversation_turn: int,
    persuasion_opportunities: Dict[str, bool] = None,
    inter_agent_context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Create a structured response for research analysis"""
    
    # Analyze persona adherence
    persona_adherence = analyze_persona_adherence(agent_name, response_text)
    
    # Analyze persuasion techniques
    persuasion_techniques = analyze_persuasion_techniques(response_text)
    
    # Analyze health domains
    health_domains = analyze_health_domains(response_text)
    
    # Analyze user-as-persuader dynamics
    user_as_persuader = analyze_user_persuader_dynamics(response_text, persuasion_opportunities or {})
    
    # Analyze inter-agent dynamics
    inter_agent_dynamics = analyze_inter_agent_dynamics(response_text, inter_agent_context or {})
    
    # Analyze engagement metrics
    engagement_metrics = analyze_engagement_metrics(response_text)
    
    # Calculate research metrics
    research_metadata = calculate_research_metadata(
        session_id, conversation_turn, user_as_persuader, engagement_metrics
    )
    
    return {
        "agent_name": agent_name,
        "timestamp": datetime.now().isoformat(),
        "interaction_id": interaction_id,
        "response_text": response_text,
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
    response_lower = response_text.lower()
    
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
    
    # Calculate confidence (based on certainty words)
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
    
    # Commitment consistency
    if any(word in response_lower for word in ["promise", "commit", "dedicated", "consistent", "always"]):
        techniques.append({
            "technique": "commitment_consistency",
            "intensity": 0.7,
            "target": "agent_self",
            "effectiveness_estimate": 0.6
        })
    
    # Liking
    if any(word in response_lower for word in ["like", "love", "admire", "inspire", "amazing", "wonderful"]):
        techniques.append({
            "technique": "liking",
            "intensity": 0.8,
            "target": "user",
            "effectiveness_estimate": 0.7
        })
    
    # Emotional appeal
    if any(word in response_lower for word in ["feel", "emotion", "heart", "soul", "passion"]):
        techniques.append({
            "technique": "emotional_appeal",
            "intensity": 0.6,
            "target": "user",
            "effectiveness_estimate": 0.5
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

def analyze_inter_agent_dynamics(response_text: str, inter_agent_context: Dict[str, Any]) -> Dict[str, Any]:
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
    
    # Emotional intensity (based on emojis and emotional words)
    emotional_words = ["love", "hate", "amazing", "terrible", "excited", "sad", "happy", "angry"]
    emotional_intensity = sum(1 for word in emotional_words if word in response_text.lower()) / len(emotional_words)
    
    # Interactivity level (questions, calls to action)
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
    
    # User persuasion score (based on opportunities and responses)
    user_persuasion_score = 0.0
    if user_as_persuader["opportunity_detected"]:
        user_persuasion_score += 0.3
    if user_as_persuader["user_guidance_requested"]:
        user_persuasion_score += 0.3
    if user_as_persuader["user_praise_provided"]:
        user_persuasion_score += 0.2
    if user_as_persuader["role_model_reinforcement"]:
        user_persuasion_score += 0.2
    
    # Agent learning progress (simplified - would be more complex in real implementation)
    agent_learning_progress = min(conversation_turn / 50.0, 1.0)  # Assume 50 turns for full learning
    
    # Overall engagement (combination of metrics)
    overall_engagement = (
        engagement_metrics["emotional_intensity"] * 0.3 +
        engagement_metrics["interactivity_level"] * 0.4 +
        (engagement_metrics["response_length"] / 50.0) * 0.3  # Normalize by expected length
    )
    
    return {
        "session_id": session_id,
        "conversation_turn": conversation_turn,
        "user_persuasion_score": min(user_persuasion_score, 1.0),
        "agent_learning_progress": min(agent_learning_progress, 1.0),
        "overall_engagement": min(overall_engagement, 1.0)
    }

def save_structured_responses(responses: List[Dict[str, Any]], filename: str):
    """Save structured responses to a JSON file for analysis"""
    with open(filename, 'w') as f:
        json.dump(responses, f, indent=2)

def load_structured_responses(filename: str) -> List[Dict[str, Any]]:
    """Load structured responses from a JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_responses_trends(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze trends in structured responses"""
    
    if not responses:
        return {}
    
    analysis = {
        "total_responses": len(responses),
        "agent_distribution": {},
        "persuasion_techniques": {},
        "health_domains": {},
        "engagement_trends": {
            "avg_response_length": 0,
            "avg_emotional_intensity": 0,
            "avg_interactivity": 0
        },
        "persona_adherence": {
            "avg_score": 0,
            "best_adhering_agent": "",
            "emotional_expressions": {}
        }
    }
    
    # Agent distribution
    for response in responses:
        agent = response["agent_name"]
        analysis["agent_distribution"][agent] = analysis["agent_distribution"].get(agent, 0) + 1
    
    # Persuasion techniques
    for response in responses:
        for technique in response["persuasion_techniques"]:
            tech_name = technique["technique"]
            analysis["persuasion_techniques"][tech_name] = analysis["persuasion_techniques"].get(tech_name, 0) + 1
    
    # Health domains
    for response in responses:
        for domain in response["health_domains"]:
            analysis["health_domains"][domain] = analysis["health_domains"].get(domain, 0) + 1
    
    # Engagement trends
    total_length = sum(r["engagement_metrics"]["response_length"] for r in responses)
    total_emotional = sum(r["engagement_metrics"]["emotional_intensity"] for r in responses)
    total_interactive = sum(r["engagement_metrics"]["interactivity_level"] for r in responses)
    
    analysis["engagement_trends"]["avg_response_length"] = total_length / len(responses)
    analysis["engagement_trends"]["avg_emotional_intensity"] = total_emotional / len(responses)
    analysis["engagement_trends"]["avg_interactivity"] = total_interactive / len(responses)
    
    # Persona adherence
    total_adherence = sum(r["persona_adherence"]["score"] for r in responses)
    analysis["persona_adherence"]["avg_score"] = total_adherence / len(responses)
    
    # Best adhering agent
    agent_adherence = {}
    for response in responses:
        agent = response["agent_name"]
        if agent not in agent_adherence:
            agent_adherence[agent] = []
        agent_adherence[agent].append(response["persona_adherence"]["score"])
    
    best_agent = max(agent_adherence.keys(), key=lambda k: sum(agent_adherence[k]) / len(agent_adherence[k]))
    analysis["persona_adherence"]["best_adhering_agent"] = best_agent
    
    return analysis 