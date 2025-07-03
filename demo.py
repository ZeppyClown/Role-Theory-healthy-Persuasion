"""
Demo: Streaming Functionality
Showcases the real-time text streaming feature
"""

import time
from utils import (
    stream_text, stream_text_with_cursor, stream_text_with_typing_sound,
    stream_with_emotion, stream_agent_response, streaming_manager
)

def demo_basic_streaming():
    """Demo basic text streaming"""
    print("🎬 DEMO: Basic Text Streaming")
    print("="*50)
    
    sample_text = "Hello! I'm an AI agent typing in real-time. This creates a more engaging and natural conversation experience."
    
    print("Original text:")
    print(sample_text)
    print("\nStreaming version:")
    stream_text(sample_text, delay=0.03)
    print()

def demo_cursor_effect():
    """Demo cursor effect"""
    print("🎬 DEMO: Cursor Effect")
    print("="*50)
    
    sample_text = "This text has a blinking cursor at the end to show completion."
    
    print("Streaming with cursor:")
    stream_text_with_cursor(sample_text, delay=0.05)
    print()

def demo_typing_indicators():
    """Demo typing indicators"""
    print("🎬 DEMO: Typing Indicators")
    print("="*50)
    
    sample_text = "This shows visual typing indicators while streaming text."
    
    print("Streaming with typing indicators:")
    stream_text_with_typing_sound(sample_text, delay=0.08)
    print()

def demo_emotional_streaming():
    """Demo emotion-based streaming"""
    print("🎬 DEMO: Emotional Streaming")
    print("="*50)
    
    emotions = [
        ("I'm so excited to share this with you!", "excited"),
        ("Thank you so much for your help!", "grateful"),
        ("I'm a bit confused about this...", "confused"),
        ("I'm really proud of my progress!", "proud")
    ]
    
    for text, emotion in emotions:
        print(f"Emotion: {emotion}")
        stream_with_emotion(text, emotion, delay=0.04)
        print()

def demo_agent_responses():
    """Demo agent response streaming"""
    print("🎬 DEMO: Agent Response Streaming")
    print("="*50)
    
    agent_responses = [
        ("Momo", "Thank you so much for your advice! I really appreciate your guidance.", "grateful"),
        ("Miles", "I'm curious about this nutrition concept. Can you explain it to me?", "confused"),
        ("Lila", "You are absolutely amazing! Your healthy habits inspire me so much!", "excited")
    ]
    
    for agent_name, response, emotion in agent_responses:
        stream_agent_response(response, agent_name, emotion)
        print()

def demo_streaming_controls():
    """Demo streaming control features"""
    print("🎬 DEMO: Streaming Controls")
    print("="*50)
    
    print("Current streaming settings:")
    print(f"  Enabled: {streaming_manager.enabled}")
    print(f"  Delay: {streaming_manager.delay}s")
    
    # Test different delays
    test_text = "This text is streamed at different speeds."
    
    print("\nFast streaming (0.01s delay):")
    streaming_manager.set_delay(0.01)
    streaming_manager.stream(test_text)
    
    print("\nSlow streaming (0.1s delay):")
    streaming_manager.set_delay(0.1)
    streaming_manager.stream(test_text)
    
    # Reset to default
    streaming_manager.set_delay(0.03)
    print()

def demo_streaming_disabled():
    """Demo streaming when disabled"""
    print("🎬 DEMO: Streaming Disabled")
    print("="*50)
    
    test_text = "This text appears instantly when streaming is disabled."
    
    print("With streaming enabled:")
    streaming_manager.set_streaming(True)
    streaming_manager.stream(test_text)
    
    print("\nWith streaming disabled:")
    streaming_manager.set_streaming(False)
    streaming_manager.stream(test_text)
    
    # Re-enable for rest of demo
    streaming_manager.set_streaming(True)
    print()

def main():
    """Run all streaming demos"""
    print("🎬 STREAMING FUNCTIONALITY DEMO")
    print("="*60)
    print("This demo showcases the real-time text streaming features")
    print("that make conversations with AI agents more engaging.")
    print("="*60)
    print()
    
    demos = [
        demo_basic_streaming,
        demo_cursor_effect,
        demo_typing_indicators,
        demo_emotional_streaming,
        demo_agent_responses,
        demo_streaming_controls,
        demo_streaming_disabled
    ]
    
    for i, demo in enumerate(demos, 1):
        demo()
        if i < len(demos):
            print("⏸️  Press Enter to continue to next demo...")
            input()
            print()
    
    print("🎉 DEMO COMPLETE!")
    print("="*60)
    print("You can now run the main application with:")
    print("  python agent_new.py")
    print()
    print("Available streaming commands:")
    print("  'streaming' - View settings")
    print("  'streaming on/off' - Enable/disable")
    print("  'delay [seconds]' - Set typing speed")
    print("  'help' - Show all commands")

if __name__ == "__main__":
    main() 