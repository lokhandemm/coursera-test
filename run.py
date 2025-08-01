#!/usr/bin/env python3
"""
Small Business Chatbot - Startup Script
This script helps you run both the Flask backend and React frontend
"""

import subprocess
import sys
import os
import time
from threading import Thread

def run_backend():
    """Run the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    try:
        subprocess.run(["python3", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error running backend: {e}")

def run_frontend():
    """Run the React frontend development server"""
    print("🚀 Starting React frontend server...")
    try:
        # Wait a bit for backend to start
        time.sleep(3)
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error running frontend: {e}")

def main():
    print("🤖 Small Business Chatbot - Starting Up...")
    print("=" * 50)
    
    # Check if npm is installed
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm is not installed. Please install Node.js and npm first.")
        sys.exit(1)
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install Node.js dependencies")
        sys.exit(1)
    
    print("✅ All dependencies installed successfully!")
    print("\n🌟 Starting servers...")
    print("Backend will run on: http://localhost:5000")
    print("Frontend will run on: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers\n")
    
    try:
        # Start backend in a separate thread
        backend_thread = Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Start frontend in main thread
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("👋 Thanks for using Small Business Chatbot!")

if __name__ == "__main__":
    main()