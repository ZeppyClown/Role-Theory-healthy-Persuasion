"""
Streaming Utilities
Provides real-time text streaming for better user experience
"""

import sys
import time
import threading
from typing import Generator, Optional

def stream_text(text: str, delay: float = 0.03, end_delay: float = 0.5) -> None:
    """
    Stream text character by character to simulate typing
    
    Args:
        text: The text to stream
        delay: Delay between characters in seconds
        end_delay: Delay at the end before newline
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    
    time.sleep(end_delay)
    print()  # New line at the end

def stream_text_with_cursor(text: str, delay: float = 0.03, cursor_char: str = "|") -> None:
    """
    Stream text with a blinking cursor effect
    
    Args:
        text: The text to stream
        delay: Delay between characters in seconds
        cursor_char: Character to use as cursor
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    
    # Blinking cursor effect
    for _ in range(3):
        print(cursor_char, end='', flush=True)
        time.sleep(0.3)
        print('\b \b', end='', flush=True)  # Clear cursor
        time.sleep(0.3)
    
    print()  # Final newline

def stream_response_stream(response_stream: Generator, agent_name: str = "", delay: float = 0.02) -> str:
    """
    Stream a response from OpenAI's streaming API
    
    Args:
        response_stream: The streaming response from OpenAI
        agent_name: Name of the agent for display
        delay: Additional delay between chunks
        
    Returns:
        The complete response text
    """
    full_response = ""
    
    # Print agent name if provided
    if agent_name:
        print(f"\n🤖 {agent_name}: ", end='', flush=True)
    
    try:
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)
                full_response += content
                time.sleep(delay)
        
        print()  # New line at the end
        return full_response
        
    except Exception as e:
        print(f"\n❌ Error during streaming: {e}")
        return full_response

def stream_text_with_typing_sound(text: str, delay: float = 0.05) -> None:
    """
    Stream text with visual typing indicators
    
    Args:
        text: The text to stream
        delay: Delay between characters in seconds
    """
    typing_indicators = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    indicator_index = 0
    
    for char in text:
        # Show typing indicator
        indicator = typing_indicators[indicator_index]
        print(f"\r{indicator} ", end='', flush=True)
        
        # Print the character
        print(char, end='', flush=True)
        
        # Update indicator
        indicator_index = (indicator_index + 1) % len(typing_indicators)
        
        time.sleep(delay)
    
    # Clear typing indicator and add newline
    print("\r" + " " * 2 + "\n", end='', flush=True)

def stream_with_emotion(text: str, emotion: str = "neutral", delay: float = 0.03) -> None:
    """
    Stream text with emotion-based styling
    
    Args:
        text: The text to stream
        emotion: Emotion type (happy, sad, excited, calm, etc.)
        delay: Delay between characters in seconds
    """
    # Emotion-based prefixes
    emotion_prefixes = {
        "happy": "😊 ",
        "excited": "🎉 ",
        "sad": "😔 ",
        "worried": "😟 ",
        "confused": "🤔 ",
        "grateful": "🙏 ",
        "proud": "😌 ",
        "neutral": ""
    }
    
    prefix = emotion_prefixes.get(emotion, "")
    if prefix:
        print(prefix, end='', flush=True)
    
    stream_text(text, delay)

def stream_agent_response(response: str, agent_name: str, agent_emotion: str = "neutral") -> None:
    """
    Stream an agent response with proper formatting
    
    Args:
        response: The agent's response text
        agent_name: Name of the agent
        agent_emotion: Emotion of the agent
    """
    print(f"\n🤖 {agent_name}: ", end='', flush=True)
    stream_with_emotion(response, agent_emotion)

def stream_inter_agent_interaction(agent1: str, agent2: str, response: str) -> None:
    """
    Stream an inter-agent interaction
    
    Args:
        agent1: Name of the responding agent
        agent2: Name of the target agent
        response: The response text
    """
    print(f"\n🔄 {agent1} → {agent2}: ", end='', flush=True)
    stream_text(response)

class StreamingManager:
    """Manages streaming settings and provides utility methods"""
    
    def __init__(self, enabled: bool = True, delay: float = 0.03):
        self.enabled = enabled
        self.delay = delay
        self.typing_sound_enabled = False
    
    def set_streaming(self, enabled: bool):
        """Enable or disable streaming"""
        self.enabled = enabled
    
    def set_delay(self, delay: float):
        """Set the delay between characters"""
        self.delay = delay
    
    def stream(self, text: str, **kwargs) -> None:
        """Stream text with current settings"""
        if not self.enabled:
            print(text)
            return
        
        delay = kwargs.get('delay', self.delay)
        stream_text(text, delay)
    
    def stream_agent(self, response: str, agent_name: str, **kwargs) -> None:
        """Stream an agent response"""
        if not self.enabled:
            print(f"\n🤖 {agent_name}: {response}")
            return
        
        stream_agent_response(response, agent_name, **kwargs)

# Global streaming manager instance
streaming_manager = StreamingManager() 