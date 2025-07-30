#!/usr/bin/env python3
"""
PepeluGPT - Main Entry Point
Professional Cybersecurity Intelligence Platform

This is the primary entry point for PepeluGPT that provides backward compatibility
while directing users to the new enhanced CLI interface.
"""

import sys
import subprocess
from pathlib import Path
from version.manager import get_version_info, get_age_message

def main():
    """Main entry point with modern CLI forwarding."""
    
    # Get version information
    version_info = get_version_info()
    age_message = get_age_message()
    
    # Display the updated branding with dynamic version
    print("PepeluGPT")
    print(f"   Cybersecurity Intelligence Platform v{version_info['version']} \"{version_info['codename']}\"")
    print(f"   {age_message}")
    print("=" * 60)
    
    # Check if arguments were provided for backward compatibility
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        # Map old commands to new CLI
        command_mapping = {
            'setup': 'setup',
            'chat': 'chat', 
            'test': 'test',
            'status': 'status',
            'version': 'version',
            'config': 'config',
            'update': 'update'
        }
        
        if command in command_mapping:
            print(f"Forwarding to enhanced CLI: {command}")
            print("-" * 40)
            
            # Forward to new CLI - SECURITY FIX: Use subprocess instead of os.system
            cli_path = Path(__file__).parent / "core" / "cli.py"
            try:
                subprocess.run([sys.executable, str(cli_path), command_mapping[command]], 
                             check=True, timeout=30)
            except subprocess.TimeoutExpired:
                print("Command timed out")
            except subprocess.CalledProcessError as e:
                print(f"Command failed: {e}")
            except Exception as e:
                print(f"Error executing command: {e}")
            return
        else:
            print(f"Unknown command: {command}")
            print("Try: setup, chat, status, version, age, config, update, or test")
            return
    
    # No arguments provided - show help and new CLI info
    print("""
PepeluGPT has been enhanced with a new modular architecture!

Quick Commands:
   python pepelugpt.py setup     # Initial setup (backward compatible)
   python pepelugpt.py chat      # Start chat (backward compatible)
   python pepelugpt.py status    # System status (backward compatible)
   python pepelugpt.py version   # Version and evolution info
   python pepelugpt.py age       # Age and journey details

Enhanced CLI (Recommended):
   python core/cli.py setup      # Comprehensive setup with progress tracking
   python core/cli.py chat       # Enhanced chat interface
   python core/cli.py status     # Detailed system health dashboard
   python core/cli.py update     # Update vector database
   python core/cli.py version    # Show version and evolution timeline
   python core/cli.py age        # Display age and system status
   python core/cli.py config     # View configuration
   python core/cli.py test       # Run comprehensive tests

New Architecture:
   core/         - Central logic and orchestration
   interface/    - Chat and API interfaces  
   data/         - Parsed documents and outputs
   tests/        - Comprehensive test suite
   vector_db/    - Enhanced semantic search
   file_parser/  - Modular document processing

Coming Soon:
   • Rich terminal interface with colors and progress bars
   • Web-based GUI for document management
   • Advanced compliance workflow automation
   • Multi-language document support
   • Real-time collaboration features

Get Started:
   1. python core/cli.py status     # Check system health
   2. python core/cli.py setup      # Initialize if needed
   3. python core/cli.py chat       # Start your cybersecurity copilot

""")

if __name__ == "__main__":
    main()
