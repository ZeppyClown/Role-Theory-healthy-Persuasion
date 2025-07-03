#!/usr/bin/env python3
"""
Setup script for the Enhanced Healthy Habits AI Agent System
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("\n🔧 Creating .env file...")
    env_content = """# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize AI Model (default: gpt-4o)
# OPENAI_MODEL=gpt-4o-mini

# Optional: Customize Temperature (default: 0.8)
# OPENAI_TEMPERATURE=0.8

# Optional: Customize Max Tokens (default: 300)
# OPENAI_MAX_TOKENS=300
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created!")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_imports():
    """Test if all imports work correctly"""
    print("\n🧪 Testing imports...")
    try:
        import openai
        import dotenv
        import json
        import random
        from datetime import datetime
        from typing import Dict, List, Any
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_test_simulation():
    """Run the test simulation"""
    print("\n🎮 Running test simulation...")
    try:
        subprocess.check_call([sys.executable, "test_agents.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Test simulation failed: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  test_agents.py not found, skipping simulation test")
        return True

def main():
    """Main setup function"""
    print("🚀 Enhanced Healthy Habits AI Agent System - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Run test simulation
    if not run_test_simulation():
        return False
    
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python agent.py")
    print("3. Enjoy chatting with Momo, Miles, and Lila!")
    print("\n📚 For more information, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 