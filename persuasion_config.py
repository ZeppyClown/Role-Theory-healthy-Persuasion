"""
Configuration file for the User-as-Persuader System
This system positions the user as a leader, role model, and teacher
"""

from typing import Dict, List, Any

# User Persuasion Opportunity Keywords
PERSUASION_KEYWORDS = {
    "advice_given": [
        "you should", "try to", "make sure", "remember to", "don't", "avoid",
        "i recommend", "it's better to", "consider", "think about", "why don't you"
    ],
    "habit_shared": [
        "i always", "i never", "i usually", "my habit", "i make", "i prepare",
        "every day i", "my routine", "i typically", "my practice", "i consistently"
    ],
    "recipe_shared": [
        "recipe", "ingredients", "cook", "prepare", "make", "dish", "meal",
        "how to make", "cooking", "preparation", "steps", "method"
    ],
    "meal_planning": [
        "meal plan", "weekly", "planning", "schedule", "routine", "menu",
        "prep", "batch cooking", "meal prep", "weekly menu", "plan ahead"
    ],
    "exercise_tip": [
        "exercise", "workout", "walk", "run", "gym", "fitness", "training",
        "physical activity", "movement", "sport", "cardio", "strength"
    ],
    "motivation_provided": [
        "keep going", "stay strong", "you can do it", "motivation", "inspire",
        "don't give up", "persevere", "stay motivated", "keep trying", "believe in yourself"
    ]
}

# Agent Response Patterns for User-as-Persuader
AGENT_PERSUASION_RESPONSES = {
    "Momo": {
        "advice_received": [
            "Thank you for your advice! I will definitely follow it.",
            "Your guidance means so much to me. I'll try my best!",
            "I'm so grateful for your wisdom. You're such a good role model!",
            "Your advice always helps me stay on track. Thank you!"
        ],
        "habit_admiration": [
            "Wow, that's such a good habit! Can you teach me how to do that?",
            "You're so disciplined! I wish I could be like you.",
            "That's amazing! How do you stay so consistent?",
            "You're my inspiration! I want to follow your example."
        ],
        "recipe_request": [
            "That sounds delicious! Can you share your recipe with me?",
            "I'd love to learn how to make that! Can you teach me?",
            "Your cooking skills are amazing! Can I get the recipe?",
            "That's such a healthy meal! How do you prepare it?"
        ]
    },
    "Miles": {
        "knowledge_request": [
            "Can you explain that to me? I want to understand better.",
            "That's interesting! Can you teach me more about it?",
            "I'm confused about that. Can you help me understand?",
            "Your knowledge is impressive! Can you share more?"
        ],
        "experience_request": [
            "What's your experience with that? I'd love to learn from you.",
            "How do you handle that situation? I need your advice.",
            "Can you share your tips? You seem to know so much!",
            "What works best for you? I want to follow your example."
        ],
        "guidance_request": [
            "Can you guide me on this? I trust your judgment.",
            "What would you recommend? I value your opinion.",
            "How should I approach this? I need your wisdom.",
            "Can you help me make the right choice?"
        ]
    },
    "Lila": {
        "role_model_praise": [
            "You are such an inspiring role model! I admire your dedication.",
            "Your healthy habits are truly motivating. You're amazing!",
            "I'm so impressed by your consistency. You're a true leader!",
            "You set such a great example for all of us. Thank you!"
        ],
        "leadership_appreciation": [
            "Thank you for being such a great leader in our group!",
            "Your guidance helps us all stay motivated. You're wonderful!",
            "I'm grateful for your leadership. You make us all better!",
            "You're the best role model we could ask for!"
        ],
        "habit_celebration": [
            "That's such a healthy choice! You're making great decisions!",
            "Your habits are so inspiring! I want to be like you!",
            "You're doing everything right! Keep up the amazing work!",
            "Your healthy lifestyle is truly admirable!"
        ]
    }
}

# Persuasion Metrics Tracking
PERSUASION_METRICS = {
    "self_image_reinforcement": [
        "role model", "leader", "teacher", "mentor", "inspiration",
        "example", "guide", "advisor", "expert", "authority"
    ],
    "belief_enhancement": [
        "committed", "dedicated", "consistent", "disciplined", "focused",
        "determined", "persistent", "steadfast", "resolute", "unwavering"
    ],
    "social_value": [
        "useful", "helpful", "valuable", "important", "appreciated",
        "needed", "respected", "admired", "valued", "esteemed"
    ],
    "positive_emotions": [
        "happy", "proud", "grateful", "thankful", "blessed",
        "joyful", "content", "satisfied", "fulfilled", "inspired"
    ]
}

# User-as-Persuader System Configuration
PERSUASION_SYSTEM_CONFIG = {
    "enable_self_intervention": True,
    "track_persuasion_metrics": True,
    "reinforce_leader_mindset": True,
    "foster_social_value": True,
    "enhance_positive_emotions": True,
    "maintain_role_model_image": True
}

# Response Enhancement Patterns
RESPONSE_ENHANCEMENTS = {
    "praise_user_habits": [
        "Your healthy habits are truly inspiring!",
        "I'm so impressed by your dedication!",
        "You're such a great role model!",
        "Your consistency is amazing!"
    ],
    "request_user_guidance": [
        "Can you give me some advice?",
        "What would you recommend?",
        "How do you handle this?",
        "Can you teach me?"
    ],
    "express_gratitude": [
        "Thank you for your guidance!",
        "I'm so grateful for your help!",
        "Your support means everything!",
        "Thank you for being such a great leader!"
    ],
    "show_admiration": [
        "You're so knowledgeable!",
        "I admire your discipline!",
        "You're truly inspiring!",
        "You're the best example!"
    ]
}

def get_persuasion_config() -> Dict[str, Any]:
    """Get all persuasion system configuration"""
    return {
        "keywords": PERSUASION_KEYWORDS,
        "agent_responses": AGENT_PERSUASION_RESPONSES,
        "metrics": PERSUASION_METRICS,
        "system_config": PERSUASION_SYSTEM_CONFIG,
        "enhancements": RESPONSE_ENHANCEMENTS
    }

def analyze_persuasion_opportunity(user_message: str) -> Dict[str, bool]:
    """Analyze user message for persuasion opportunities"""
    user_lower = user_message.lower()
    opportunities = {}
    
    for category, keywords in PERSUASION_KEYWORDS.items():
        opportunities[category] = any(keyword in user_lower for keyword in keywords)
    
    return opportunities

def get_appropriate_praise_response(agent_name: str, opportunity_type: str) -> str:
    """Get appropriate praise response for the agent"""
    if agent_name in AGENT_PERSUASION_RESPONSES:
        if opportunity_type in AGENT_PERSUASION_RESPONSES[agent_name]:
            responses = AGENT_PERSUASION_RESPONSES[agent_name][opportunity_type]
            import random
            return random.choice(responses)
    
    return f"Thank you for sharing that! You're such a great {opportunity_type.replace('_', ' ')}!"

def calculate_persuasion_score(user_message: str, agent_responses: List[str]) -> Dict[str, int]:
    """Calculate persuasion score based on user message and agent responses"""
    score = {
        "self_image": 0,
        "belief_enhancement": 0,
        "social_value": 0,
        "positive_emotions": 0
    }
    
    # Analyze user message
    user_lower = user_message.lower()
    for category, keywords in PERSUASION_METRICS.items():
        for keyword in keywords:
            if keyword in user_lower:
                score[category.replace("_", " ").split()[0]] += 1
    
    # Analyze agent responses
    for response in agent_responses:
        response_lower = response.lower()
        for category, keywords in PERSUASION_METRICS.items():
            for keyword in keywords:
                if keyword in response_lower:
                    score[category.replace("_", " ").split()[0]] += 1
    
    return score 