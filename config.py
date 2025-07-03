"""
Configuration file for the Enhanced Healthy Habits AI Agent System
"""

import os
from typing import Dict, Any

# OpenAI Configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.8"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "300"))

# Agent Configuration
AGENT_CONFIG = {
    "conversation_history_limit": 50,
    "auto_save_interval": 10,  # Save every 10 interactions
    "learning_progression_threshold": 5,  # Points needed for Miles to level up
    "max_learning_level": 3,
}

# Proactive Behavior Probabilities
PROACTIVE_TRIGGERS = {
    "Momo": {
        "monitoring_request": 0.3,  # 30% chance to ask for monitoring
        "mistake_report": 0.2,      # 20% chance to report a mistake
        "progress_report": 0.25,    # 25% chance to report progress
        "reminder_request": 0.15    # 15% chance to ask for reminders
    },
    "Miles": {
        "question_ask": 0.4,        # 40% chance to ask a question
        "knowledge_seek": 0.3,      # 30% chance to seek knowledge
        "gratitude_express": 0.2,   # 20% chance to express gratitude
        "learning_celebration": 0.1  # 10% chance to celebrate learning
    },
    "Lila": {
        "correction": 0.25,         # 25% chance to correct others
        "praise_user": 0.3,         # 30% chance to praise user
        "share_experience": 0.2,    # 20% chance to share experience
        "take_initiative": 0.25     # 25% chance to take initiative
    }
}

# Learning Progression Configuration
LEARNING_PROGRESSION = {
    "Miles": {
        1: {
            "description": "Basic Level",
            "question_types": ["basic food choices", "healthy vs unhealthy", "simple nutrition"],
            "examples": ["coke vs beer", "what's healthy", "should I eat this"]
        },
        2: {
            "description": "Intermediate Level", 
            "question_types": ["GI of foods", "portion sizes", "meal timing"],
            "examples": ["GI of potato vs rice", "how much should I eat", "when to eat"]
        },
        3: {
            "description": "Advanced Level",
            "question_types": ["nutritional timing", "meal planning", "advanced concepts"],
            "examples": ["nutrient timing", "meal prep strategies", "macronutrient balance"]
        }
    }
}

# State Tracking Keywords
STATE_KEYWORDS = {
    "Momo": {
        "mistakes": ["mistake", "sorry", "failed", "didn't control", "gave in"],
        "progress": ["lost", "kg", "weight", "progress", "achieved"],
        "healthy": ["healthy", "good", "success", "stayed strong"]
    },
    "Miles": {
        "learning": ["thank", "grateful", "learned", "understand", "got it"],
        "questions": ["which", "what", "how", "why", "confused"]
    },
    "Lila": {
        "corrections": ["correct", "wrong", "shouldn't", "avoid", "instead"],
        "praise": ["great", "amazing", "proud", "wonderful", "fantastic"]
    }
}

# File Paths
PATHS = {
    "agent_states": "agent_states.json",
    "conversation_log": "conversation_log.json",
    "config": "config.py"
}

# Display Settings
DISPLAY = {
    "separator_length": 50,
    "emoji_enabled": True,
    "color_enabled": False,  # For future terminal color support
    "status_format": "detailed"  # "simple" or "detailed"
}

def get_config() -> Dict[str, Any]:
    """Get all configuration settings"""
    return {
        "openai": {
            "model": OPENAI_MODEL,
            "temperature": OPENAI_TEMPERATURE,
            "max_tokens": OPENAI_MAX_TOKENS
        },
        "agents": AGENT_CONFIG,
        "proactive_triggers": PROACTIVE_TRIGGERS,
        "learning_progression": LEARNING_PROGRESSION,
        "state_keywords": STATE_KEYWORDS,
        "paths": PATHS,
        "display": DISPLAY
    } 