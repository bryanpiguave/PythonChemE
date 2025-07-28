#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup script for the Chemical Engineering Thermodynamics Toolkit
@author: Bryan Piguave Llano
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open the web browser to the application"""
    webbrowser.open('http://localhost:5000')

def main():
    """Main function to start the application"""
    print("🚀 Starting Chemical Engineering Thermodynamics Toolkit...")
    print("=" * 60)
    
    # Check if required packages are installed
    try:
        import flask
        import numpy
        import iapws
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install requirements with: pip install -r requirements.txt")
        return
    
    # Start the Flask application
    try:
        from app.app import app
        
        # Open browser after 2 seconds
        Timer(2.0, open_browser).start()
        
        print("🌐 Starting web server...")
        print("📊 Available tools:")
        print("   • Rankine Cycle Analysis")
        print("   • Brayton Cycle Analysis") 
        print("   • Steam Properties Calculator")
        print("   • VLE Calculator")
        print("   • Refrigeration Cycle Analysis")
        print("\n🔗 Opening browser to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask app
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return

if __name__ == "__main__":
    main() 