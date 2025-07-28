#!/usr/bin/env python3
"""
Chemical Engineering Thermodynamics Toolkit - Main Entry Point

This is the main entry point for the Chemical Engineering Thermodynamics Toolkit.
It provides both command-line and web interface access to the thermodynamics tools.

Author: Bryan Piguave Llano
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the application."""
    print("🚀 Chemical Engineering Thermodynamics Toolkit")
    print("=" * 50)
    print("📊 Available tools:")
    print("   • Rankine Cycle Analysis")
    print("   • Brayton Cycle Analysis") 
    print("   • Steam Properties Calculator")
    print("   • VLE Calculator")
    print("   • Refrigeration Cycle Analysis")
    print("=" * 50)
    
    try:
        # Import the Flask app
        from src.web.app import app
        
        # Start the Flask application
        print("🌐 Starting web server...")
        print("🔗 Opening browser to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Try installing missing dependencies:")
        print("   conda install matplotlib flask flask-cors iapws")
        return 1
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code if exit_code else 0) 