"""
Evaluation System for Agent Effectiveness and User Engagement
This module provides tools for measuring and analyzing the performance of the multi-agent system
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid

class EvaluationMetrics:
    """Class for tracking and calculating evaluation metrics"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.metrics = {
            "conversation_turns": 0,
            "agent_responses": 0,
            "inter_agent_interactions": 0,
            "user_persuasion_opportunities": 0,
            "user_guidance_requests": 0,
            "user_praise_instances": 0,
            "health_domains_covered": set(),
            "persuasion_techniques_used": {},
            "engagement_scores": [],
            "persona_adherence_scores": [],
            "response_times": [],
            "user_satisfaction_indicators": []
        }
    
    def record_conversation_turn(self):
        """Record a new conversation turn"""
        self.metrics["conversation_turns"] += 1
    
    def record_agent_response(self, agent_name: str, response_time: float):
        """Record an agent response with timing"""
        self.metrics["agent_responses"] += 1
        self.metrics["response_times"].append(response_time)
    
    def record_inter_agent_interaction(self):
        """Record an inter-agent interaction"""
        self.metrics["inter_agent_interactions"] += 1
    
    def record_persuasion_opportunity(self, opportunity_type: str):
        """Record a user persuasion opportunity"""
        self.metrics["user_persuasion_opportunities"] += 1
    
    def record_user_guidance_request(self):
        """Record when user provides guidance"""
        self.metrics["user_guidance_requests"] += 1
    
    def record_user_praise(self):
        """Record when user receives praise"""
        self.metrics["user_praise_instances"] += 1
    
    def record_health_domain(self, domain: str):
        """Record a health domain being discussed"""
        self.metrics["health_domains_covered"].add(domain)
    
    def record_persuasion_technique(self, technique: str):
        """Record a persuasion technique being used"""
        self.metrics["persuasion_techniques_used"][technique] = \
            self.metrics["persuasion_techniques_used"].get(technique, 0) + 1
    
    def record_engagement_score(self, score: float):
        """Record an engagement score (0-1)"""
        self.metrics["engagement_scores"].append(score)
    
    def record_persona_adherence(self, agent: str, score: float):
        """Record persona adherence score for an agent"""
        self.metrics["persona_adherence_scores"].append({
            "agent": agent,
            "score": score,
            "timestamp": datetime.now().isoformat()
        })
    
    def record_user_satisfaction(self, indicator: str):
        """Record user satisfaction indicators"""
        self.metrics["user_satisfaction_indicators"].append({
            "indicator": indicator,
            "timestamp": datetime.now().isoformat()
        })
    
    def calculate_summary_metrics(self) -> Dict[str, Any]:
        """Calculate summary metrics for the session"""
        session_duration = (datetime.now() - self.start_time).total_seconds()
        
        avg_response_time = (
            sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
            if self.metrics["response_times"] else 0
        )
        
        avg_engagement = (
            sum(self.metrics["engagement_scores"]) / len(self.metrics["engagement_scores"])
            if self.metrics["engagement_scores"] else 0
        )
        
        avg_persona_adherence = (
            sum(score["score"] for score in self.metrics["persona_adherence_scores"]) / 
            len(self.metrics["persona_adherence_scores"])
            if self.metrics["persona_adherence_scores"] else 0
        )
        
        return {
            "session_id": self.session_id,
            "session_duration_seconds": session_duration,
            "conversation_turns": self.metrics["conversation_turns"],
            "agent_responses": self.metrics["agent_responses"],
            "inter_agent_interactions": self.metrics["inter_agent_interactions"],
            "user_persuasion_opportunities": self.metrics["user_persuasion_opportunities"],
            "user_guidance_requests": self.metrics["user_guidance_requests"],
            "user_praise_instances": self.metrics["user_praise_instances"],
            "health_domains_covered": list(self.metrics["health_domains_covered"]),
            "persuasion_techniques_used": self.metrics["persuasion_techniques_used"],
            "avg_response_time_seconds": avg_response_time,
            "avg_engagement_score": avg_engagement,
            "avg_persona_adherence_score": avg_persona_adherence,
            "user_satisfaction_indicators": self.metrics["user_satisfaction_indicators"],
            "conversation_rate": self.metrics["conversation_turns"] / (session_duration / 60) if session_duration > 0 else 0,
            "inter_agent_interaction_rate": self.metrics["inter_agent_interactions"] / self.metrics["conversation_turns"] if self.metrics["conversation_turns"] > 0 else 0,
            "persuasion_opportunity_rate": self.metrics["user_persuasion_opportunities"] / self.metrics["conversation_turns"] if self.metrics["conversation_turns"] > 0 else 0
        }
    
    def save_metrics(self, filename: str):
        """Save metrics to a JSON file"""
        summary = self.calculate_summary_metrics()
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)

class LongTermEngagementTracker:
    """Class for tracking long-term engagement patterns"""
    
    def __init__(self):
        self.sessions = []
        self.user_progress = {
            "total_sessions": 0,
            "total_conversation_turns": 0,
            "engagement_trend": [],
            "health_domains_evolution": {},
            "persuasion_effectiveness": []
        }
    
    def add_session(self, session_metrics: Dict[str, Any]):
        """Add a new session to the tracker"""
        self.sessions.append(session_metrics)
        self.user_progress["total_sessions"] += 1
        self.user_progress["total_conversation_turns"] += session_metrics["conversation_turns"]
        
        # Track engagement trend
        self.user_progress["engagement_trend"].append({
            "session_number": self.user_progress["total_sessions"],
            "avg_engagement": session_metrics["avg_engagement_score"],
            "conversation_turns": session_metrics["conversation_turns"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Track health domains evolution
        for domain in session_metrics["health_domains_covered"]:
            if domain not in self.user_progress["health_domains_evolution"]:
                self.user_progress["health_domains_evolution"][domain] = []
            self.user_progress["health_domains_evolution"][domain].append({
                "session_number": self.user_progress["total_sessions"],
                "timestamp": datetime.now().isoformat()
            })
        
        # Track persuasion effectiveness
        persuasion_score = (
            session_metrics["user_guidance_requests"] + 
            session_metrics["user_praise_instances"]
        ) / session_metrics["conversation_turns"] if session_metrics["conversation_turns"] > 0 else 0
        
        self.user_progress["persuasion_effectiveness"].append({
            "session_number": self.user_progress["total_sessions"],
            "persuasion_score": persuasion_score,
            "opportunities": session_metrics["user_persuasion_opportunities"],
            "timestamp": datetime.now().isoformat()
        })
    
    def analyze_engagement_patterns(self) -> Dict[str, Any]:
        """Analyze long-term engagement patterns"""
        if not self.sessions:
            return {}
        
        # Calculate engagement trend
        recent_sessions = self.sessions[-5:] if len(self.sessions) >= 5 else self.sessions
        recent_avg_engagement = sum(s["avg_engagement_score"] for s in recent_sessions) / len(recent_sessions)
        
        # Determine engagement trend direction
        if len(self.sessions) >= 2:
            first_half = self.sessions[:len(self.sessions)//2]
            second_half = self.sessions[len(self.sessions)//2:]
            
            first_avg = sum(s["avg_engagement_score"] for s in first_half) / len(first_half)
            second_avg = sum(s["avg_engagement_score"] for s in second_half) / len(second_half)
            
            engagement_trend = "improving" if second_avg > first_avg else "declining" if second_avg < first_avg else "stable"
        else:
            engagement_trend = "insufficient_data"
        
        # Analyze health domain preferences
        domain_frequency = {}
        for session in self.sessions:
            for domain in session["health_domains_covered"]:
                domain_frequency[domain] = domain_frequency.get(domain, 0) + 1
        
        preferred_domains = sorted(domain_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_sessions": self.user_progress["total_sessions"],
            "total_conversation_turns": self.user_progress["total_conversation_turns"],
            "avg_session_length": self.user_progress["total_conversation_turns"] / self.user_progress["total_sessions"],
            "recent_engagement_score": recent_avg_engagement,
            "engagement_trend": engagement_trend,
            "preferred_health_domains": preferred_domains[:3],  # Top 3
            "persuasion_effectiveness_trend": self.user_progress["persuasion_effectiveness"][-5:] if len(self.user_progress["persuasion_effectiveness"]) >= 5 else self.user_progress["persuasion_effectiveness"]
        }
    
    def save_long_term_data(self, filename: str):
        """Save long-term engagement data"""
        analysis = self.analyze_engagement_patterns()
        with open(filename, 'w') as f:
            json.dump({
                "user_progress": self.user_progress,
                "analysis": analysis
            }, f, indent=2)

class AgentEffectivenessEvaluator:
    """Class for evaluating individual agent effectiveness"""
    
    def __init__(self):
        self.agent_metrics = {
            "Momo": {"responses": 0, "persona_adherence": [], "user_interactions": 0},
            "Miles": {"responses": 0, "persona_adherence": [], "learning_progress": []},
            "Lila": {"responses": 0, "persona_adherence": [], "corrections_provided": 0}
        }
    
    def record_agent_response(self, agent_name: str, persona_adherence_score: float, additional_metrics: Dict[str, Any] = None):
        """Record metrics for an agent response"""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name]["responses"] += 1
            self.agent_metrics[agent_name]["persona_adherence"].append(persona_adherence_score)
            
            if additional_metrics:
                if agent_name == "Miles" and "learning_progress" in additional_metrics:
                    self.agent_metrics[agent_name]["learning_progress"].append(additional_metrics["learning_progress"])
                elif agent_name == "Lila" and "corrections_provided" in additional_metrics:
                    self.agent_metrics[agent_name]["corrections_provided"] += additional_metrics["corrections_provided"]
    
    def calculate_agent_effectiveness(self) -> Dict[str, Any]:
        """Calculate effectiveness metrics for each agent"""
        effectiveness = {}
        
        for agent_name, metrics in self.agent_metrics.items():
            avg_persona_adherence = (
                sum(metrics["persona_adherence"]) / len(metrics["persona_adherence"])
                if metrics["persona_adherence"] else 0
            )
            
            effectiveness[agent_name] = {
                "total_responses": metrics["responses"],
                "avg_persona_adherence": avg_persona_adherence,
                "consistency_score": self._calculate_consistency(metrics["persona_adherence"]),
                "specialized_metrics": self._get_specialized_metrics(agent_name, metrics)
            }
        
        return effectiveness
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calculate consistency of scores (lower variance = higher consistency)"""
        if len(scores) < 2:
            return 1.0
        
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        return max(0, 1 - variance)  # Higher consistency = lower variance
    
    def _get_specialized_metrics(self, agent_name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Get agent-specific effectiveness metrics"""
        if agent_name == "Miles":
            learning_progress = metrics.get("learning_progress", [])
            return {
                "learning_progress": learning_progress[-1] if learning_progress else 0,
                "learning_consistency": self._calculate_consistency(learning_progress)
            }
        elif agent_name == "Lila":
            return {
                "corrections_provided": metrics.get("corrections_provided", 0),
                "correction_rate": metrics.get("corrections_provided", 0) / metrics["responses"] if metrics["responses"] > 0 else 0
            }
        elif agent_name == "Momo":
            return {
                "user_interactions": metrics.get("user_interactions", 0),
                "interaction_rate": metrics.get("user_interactions", 0) / metrics["responses"] if metrics["responses"] > 0 else 0
            }
        return {}

def create_evaluation_report(metrics: EvaluationMetrics, long_term_tracker: LongTermEngagementTracker, agent_evaluator: AgentEffectivenessEvaluator) -> Dict[str, Any]:
    """Create a comprehensive evaluation report"""
    
    session_summary = metrics.calculate_summary_metrics()
    long_term_analysis = long_term_tracker.analyze_engagement_patterns()
    agent_effectiveness = agent_evaluator.calculate_agent_effectiveness()
    
    return {
        "session_report": session_summary,
        "long_term_analysis": long_term_analysis,
        "agent_effectiveness": agent_effectiveness,
        "recommendations": generate_recommendations(session_summary, long_term_analysis, agent_effectiveness),
        "timestamp": datetime.now().isoformat()
    }

def generate_recommendations(session_summary: Dict[str, Any], long_term_analysis: Dict[str, Any], agent_effectiveness: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on evaluation data"""
    recommendations = []
    
    # Engagement recommendations
    if session_summary["avg_engagement_score"] < 0.6:
        recommendations.append("Consider increasing interactive elements and emotional expression in agent responses")
    
    if session_summary["inter_agent_interaction_rate"] < 0.3:
        recommendations.append("Encourage more inter-agent interactions to create collaborative dynamics")
    
    # Persuasion recommendations
    if session_summary["persuasion_opportunity_rate"] < 0.4:
        recommendations.append("Increase opportunities for user guidance and role model reinforcement")
    
    # Agent-specific recommendations
    for agent_name, effectiveness in agent_effectiveness.items():
        if effectiveness["avg_persona_adherence"] < 0.7:
            recommendations.append(f"Improve {agent_name}'s persona adherence through prompt refinement")
        
        if effectiveness["consistency_score"] < 0.6:
            recommendations.append(f"Improve {agent_name}'s response consistency")
    
    # Long-term engagement recommendations
    if long_term_analysis.get("engagement_trend") == "declining":
        recommendations.append("Introduce new topics or challenges to maintain long-term engagement")
    
    if len(long_term_analysis.get("preferred_health_domains", [])) < 3:
        recommendations.append("Expand health domain coverage to maintain user interest")
    
    return recommendations 