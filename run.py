#!/usr/bin/env python3
"""
Simple script to run the Country Financial Agent
"""
import subprocess
import sys
import os

def main():
    print("🌍 Starting Country Financial Agent...")
    print("📍 Make sure you have set up your .env file with API keys")
    print("🔑 Required: GOOGLE_API_KEY")
    print("💡 Optional: EXCHANGE_RATE_API_KEY, GOOGLE_MAPS_API_KEY")
    print("-" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("📝 Please copy .env.template to .env and add your API keys")
        return
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running the application: {e}")
        print("💡 Make sure you have installed all dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()