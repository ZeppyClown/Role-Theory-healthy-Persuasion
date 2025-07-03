#!/usr/bin/env python3
"""
Multi-Agent System Startup Script
Helps users choose the right version to run
"""

import os
import sys
import subprocess

def print_banner():
    """Print the startup banner"""
    print("🤖 Enhanced Healthy Habits AI Agent System")
    print("=" * 50)
    print()

def show_version_info():
    """Show information about available versions"""
    print("📚 Available Versions:")
    print()
    print("🎯 Version 2.0 (Current - Recommended)")
    print("   ✅ Modular architecture with separate agent files")
    print("   ✅ Real-time streaming with typing effect")
    print("   ✅ Enhanced user experience")
    print("   ✅ Easy to maintain and extend")
    print()
    print("📖 Version 1.0 (Legacy)")
    print("   📁 Located in: versions/v1.0/")
    print("   📄 Single file implementation (1,153 lines)")
    print("   ⏳ No streaming - wait for complete responses")
    print("   🔧 Basic functionality only")
    print()

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found")
        print("   Please create a .env file with your OPENAI_API_KEY")
        print("   Example: OPENAI_API_KEY=your_key_here")
        print()
        return False
    
    # Check for required files
    required_files = ['agent.py', 'config.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ Environment looks good!")
    print()
    return True

def run_version_2():
    """Run Version 2.0"""
    print("🚀 Starting Version 2.0...")
    print()
    try:
        subprocess.run([sys.executable, 'agent.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running Version 2.0: {e}")

def run_version_1():
    """Run Version 1.0"""
    print("🚀 Starting Version 1.0...")
    print()
    try:
        os.chdir('versions/v1.0')
        subprocess.run([sys.executable, 'agent.py'], check=True)
        os.chdir('../..')
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        os.chdir('../..')
    except Exception as e:
        print(f"❌ Error running Version 1.0: {e}")
        os.chdir('../..')

def run_demo():
    """Run the streaming demo"""
    print("🎬 Starting Streaming Demo...")
    print()
    try:
        subprocess.run([sys.executable, 'demo.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo ended!")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def show_help():
    """Show help information"""
    print("📋 Available Commands:")
    print()
    print("  2, v2, current    - Run Version 2.0 (recommended)")
    print("  1, v1, legacy     - Run Version 1.0")
    print("  demo              - Run streaming demo")
    print("  help, h           - Show this help")
    print("  quit, exit        - Exit")
    print()

def main():
    """Main startup function"""
    print_banner()
    
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        return
    
    show_version_info()
    
    while True:
        print("🎯 What would you like to do?")
        print("   Enter '2' for Version 2.0 (recommended)")
        print("   Enter '1' for Version 1.0")
        print("   Enter 'demo' for streaming demo")
        print("   Enter 'help' for more options")
        print("   Enter 'quit' to exit")
        print()
        
        choice = input("Your choice: ").strip().lower()
        print()
        
        if choice in ['2', 'v2', 'current', 'new']:
            run_version_2()
            break
        elif choice in ['1', 'v1', 'legacy', 'old']:
            run_version_1()
            break
        elif choice in ['demo', 'd']:
            run_demo()
            break
        elif choice in ['help', 'h', '?']:
            show_help()
        elif choice in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
            print()

if __name__ == "__main__":
    main() 