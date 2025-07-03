"""
Utils Package
Contains utility modules for the multi-agent system
"""

from .streaming import (
    stream_text,
    stream_text_with_cursor,
    stream_response_stream,
    stream_text_with_typing_sound,
    stream_with_emotion,
    stream_agent_response,
    stream_inter_agent_interaction,
    StreamingManager,
    streaming_manager
)

from .research import (
    create_structured_response,
    analyze_persona_adherence,
    analyze_persuasion_techniques,
    analyze_health_domains,
    analyze_user_persuader_dynamics,
    analyze_inter_agent_dynamics,
    analyze_engagement_metrics,
    save_research_data,
    analyze_research_data
)

from .conversation import (
    analyze_user_persuasion_opportunities,
    should_trigger_inter_agent_correction,
    generate_inter_agent_interactions,
    create_interaction_prompt,
    run_inter_agent_conversation,
    ConversationManager
)

__all__ = [
    # Streaming utilities
    'stream_text',
    'stream_text_with_cursor', 
    'stream_response_stream',
    'stream_text_with_typing_sound',
    'stream_with_emotion',
    'stream_agent_response',
    'stream_inter_agent_interaction',
    'StreamingManager',
    'streaming_manager',
    
    # Research utilities
    'create_structured_response',
    'analyze_persona_adherence',
    'analyze_persuasion_techniques',
    'analyze_health_domains',
    'analyze_user_persuader_dynamics',
    'analyze_inter_agent_dynamics',
    'analyze_engagement_metrics',
    'save_research_data',
    'analyze_research_data',
    
    # Conversation utilities
    'analyze_user_persuasion_opportunities',
    'should_trigger_inter_agent_correction',
    'generate_inter_agent_interactions',
    'create_interaction_prompt',
    'run_inter_agent_conversation',
    'ConversationManager'
] 