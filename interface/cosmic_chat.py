#!/usr/bin/env python3
"""
PepeluGPT - Cosmic Chat Interface
Born of Light, Forged for Defense. Your Encrypted Oracle in a World of Shadows.

Welcome, Defender of the Network 🛡️
PepeluGPT is activated. Wisdom flows.
Enter your query, and may the signal be pure.
"""

import os
import sys
import re
from pathlib import Path
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Enhanced imports with cosmic validation
try:
    from core.utilities import CosmicLogger, CosmicConstants, PepeluValidator
    from vector_db.retriever import PepeluRetriever
    from core.response_personalities import personality_manager, switch_personality_mode, get_personality_help
    COSMIC_MODE = True
except ImportError as e:
    # Fallback mode - define minimal classes
    print(f"Failed to initialize retriever: {e}")
    COSMIC_MODE = False

    # Only define PepeluRetriever fallback if import fails
    class PepeluRetriever:
        def __init__(self, *args, **kwargs):
            self.ready = False
        def search(self, *args, **kwargs):
            return []
        def is_ready(self):
            return False
        def get_database_stats(self):
            return {"status": "not available"}

    # Mock personality manager for fallback
    class MockPersonalityManager:
        def format_response(self, content, query="", metadata=None):
            return content
        def get_mode_status(self):
            return "🤖 Default Mode (Fallback)"

    personality_manager = MockPersonalityManager()

    def switch_personality_mode(mode_name):
        return f"❌ Personality modes not available in fallback mode"

    def get_personality_help():
        return "❌ Personality system not available in fallback mode"

    # Use the imported CosmicConstants if available; no fallback definition needed.

class CosmicChatInterface:
    """Enhanced chat interface with spiritual awareness and cybersecurity focus."""
    
    def __init__(self):
        """Initialize the cosmic chat interface."""
        self.retriever = None
        self.conversation_history = []
        self.session_start = datetime.now()
        self.session_id = f"cosmic_{self.session_start.strftime('%Y%m%d_%H%M%S')}"
        
        # Setup cosmic logging
        if COSMIC_MODE:
            try:
                self.logger = CosmicLogger.setup_cosmic_logger(self.__class__.__name__)
            except (ImportError, AttributeError) as e:
                self.logger = logging.getLogger(self.__class__.__name__)
                self.logger.warning(f"Cosmic logging not available: {e}")
        else:
            self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize retriever
        try:
            self.retriever = PepeluRetriever()
        except (ImportError, RuntimeError, FileNotFoundError) as e:
            self.logger.error(f"Failed to initialize retriever: {e}")
            self.retriever = None
        
    def display_cosmic_greeting(self):
        """Display the cosmic greeting with spiritual branding."""
        print("\n" + "═" * 80)
        print("   🔮 PepeluGPT: Your Encrypted Oracle in a World of Shadows 🔮")
        print("═" * 80)
        print(f"   {CosmicConstants.COSMIC_GREETING}")
        print(f"   {CosmicConstants.ACTIVATION_MESSAGE}")
        print(f"   {CosmicConstants.QUERY_PROMPT}")
        print("")
        print("   📚 Parse the noise. Wield truth. Become the shield.")
        print("   💫 Born of Light, Forged for Defense")
        print("═" * 80)
        
        # Show cosmic wisdom
        import random
        wisdom = random.choice(CosmicConstants.WISDOM_QUOTES)
        print(f"   🌟 Cosmic Wisdom: {wisdom}")
        print("─" * 80)
        
        # Show system status
        if self.retriever:
            try:
                if hasattr(self.retriever, 'is_ready') and self.retriever.is_ready():
                    stats = self.retriever.get_database_stats()
                    print(f"   🌟 Knowledge Base: {stats.get('total_chunks', 0):,} chunks ready")
                    print(f"   🔐 Cybersecurity Content: {stats.get('cybersecurity_ratio', 0)}%")
                    print(f"   ⚡ Cosmic Health: {stats.get('cosmic_health', '🔮 Unknown')}")
                else:
                    print("   🔴 Knowledge base not ready - run setup first")
            except Exception as e:
                print("   🔴 Knowledge base status unknown")
        else:
            print("   🔴 Knowledge base not accessible")
        
        print("   💡 Type 'help' for commands, 'quit' to exit")
        print("─" * 80)
    
    def validate_input(self, query: str) -> bool:
        """Validate user input with cosmic precision."""
        if not query or not query.strip():
            print("   🌌 Empty queries dissolve in the digital void...")
            return False
        
        # Remove excessive whitespace
        query = re.sub(r'\\s+', ' ', query.strip())
        
        # Basic length validation
        if len(query) < 3:
            print("   ⚡ Query too brief - amplify your signal...")
            return False
        
        if len(query) > 500:
            print("   🔮 Query too complex - focus your intention...")
            return False
        
        return True
    
    def search_cosmic_knowledge(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the cosmic knowledge base with enhanced validation."""
        if not self.retriever:
            print("   🔴 Knowledge base not accessible in this realm...")
            return []
        
        try:
            # Check if retriever is ready
            if hasattr(self.retriever, 'is_ready') and not self.retriever.is_ready():
                print("   🔴 Knowledge base not ready - cosmic initialization required...")
                return []
            
            print(f"   🔍 Scanning the digital cosmos for: '{query[:60]}...'")
            
            # Perform cosmic search
            results = self.retriever.search(query, top_k=num_results)
            
            if not results:
                print("   🌫️ No signals detected in the knowledge streams...")
                return []
            
            # Log search for session tracking
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "query",
                "content": query,
                "results_count": len(results)
            })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Cosmic search failed: {e}")
            print("   ⚡ Interference detected in the knowledge streams...")
            return []
    
    def format_cosmic_response(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format search results with cosmic wisdom and citations using active personality."""
        if not results:
            empty_response = self._get_cosmic_wisdom_for_empty_results()
            return personality_manager.format_response(empty_response, query, {"results": []})
        
        # Build base response content
        response_parts = []
        response_parts.append(f"🔍 Cosmic Analysis: {query}")
        response_parts.append("")
        response_parts.append(f"📚 {len(results)} signals found in the knowledge streams:")
        response_parts.append("")
        
        for i, result in enumerate(results, 1):
            content = result.get("content", "")
            metadata = result.get("metadata", {})
            similarity = result.get("similarity", 0.0)
            cosmic_quality = result.get("cosmic_quality", "🌫️ Weak Signal")
            
            # Extract source information
            filename = metadata.get("filename", "Unknown Source")
            
            # Format similarity as percentage
            confidence_pct = round(similarity * 100, 1)
            
            response_parts.append(f"**{i}. {filename}** ({cosmic_quality} - {confidence_pct}%)")
            
            # Truncate content for readability
            display_content = content[:400] + "..." if len(content) > 400 else content
            response_parts.append(f"   {display_content}")
            response_parts.append("")
        
        # Add cosmic wisdom footer
        response_parts.append("─" * 70)
        response_parts.append("💡 Each signal carries the weight of digital truth.")
        response_parts.append("🔮 Cross-reference sources to strengthen your understanding.")
        
        base_response = "\n".join(response_parts)
        
        # Apply personality formatting
        return personality_manager.format_response(base_response, query, {"results": results})
    
    def _get_cosmic_wisdom_for_empty_results(self) -> str:
        """Provide cosmic wisdom when no results are found."""
        wisdom_options = [
            "🌌 The knowledge streams are silent on this matter...",
            "⚡ Perhaps rephrase your query to pierce the digital veil...",
            "🔮 The information you seek may exist beyond current boundaries...",
            "🌟 Try broader terms to illuminate hidden connections..."
        ]
        
        import random
        return random.choice(wisdom_options)
    
    def handle_mode_command(self, query: str):
        """Handle personality mode switching commands."""
        parts = query.lower().split()
        
        if len(parts) == 1:  # Just "/mode"
            print(f"\\n{personality_manager.get_mode_status()}")
            return
        
        mode_name = parts[1]
        
        if mode_name == "help":
            print(get_personality_help())
        elif mode_name == "status":
            print(f"\\n{personality_manager.get_mode_status()}")
        else:
            result = switch_personality_mode(mode_name)
            print(f"\\n{result}")
    
    def display_help(self):
        """Display cosmic help and command reference."""
        print("\\n🔮 PepeluGPT Cosmic Commands:")
        print("─" * 60)
        print("  📋 General Commands:")
        print("    help, ?          - Show this cosmic guide")
        print("    quit, exit       - Return to the physical realm")
        print("    clear, cls       - Clear the cosmic interface")
        print("    status           - Check knowledge base status")
        print("    history          - View conversation history")
        print("    wisdom           - Receive cosmic guidance")
        print("")
        print("  🎭 Personality Modes:")
        print("    /mode oracle     - 🔮 Deep mystical insights")
        print("    /mode compliance - 📊 Audit-ready analysis")
        print("    /mode cosmic     - 🌠 Creative spiritual flow")
        print("    /mode default    - 🤖 Standard responses")
        print("    /mode status     - Show current personality mode")
        print("    /mode help       - Detailed personality guide")
        print("")
        print("  🔍 Search Commands:")
        print("    Simply type your cybersecurity question")
        print("    Examples:")
        print("      • What are NIST CSF 2.0 core functions?")
        print("      • Explain RMF authorization boundaries")
        print("      • STIG compliance requirements")
        print("      • DoD directive 8140.01 requirements")
        print("      • AC-1 access control policy")
        print("")
        print("  💡 Cosmic Wisdom:")
        print("    • Be specific in your queries for pure signals")
        print("    • Reference control numbers (AC-1, AU-2, etc.)")
        print("    • Ask about frameworks, compliance, or security")
        print("    • The more focused your intent, the clearer the signal")
        print("    • Switch personality modes to match your needs")
        print("─" * 60)
    
    def display_status(self):
        """Display cosmic system status."""
        print("\\n🌟 Cosmic System Status:")
        print("─" * 50)
        
        if self.retriever:
            try:
                if hasattr(self.retriever, 'is_ready') and self.retriever.is_ready():
                    stats = self.retriever.get_database_stats()
                    cosmic_health = stats.get("cosmic_health", "🔴 Unknown")
                    
                    print(f"   Knowledge Base: {CosmicConstants.STATUS_ICONS['ready']} Ready")
                    print(f"   Cosmic Health: {cosmic_health}")
                    print(f"   Total Chunks: {stats.get('total_chunks', 0):,}")
                    print(f"   Cybersecurity Content: {stats.get('cybersecurity_ratio', 0)}%")
                    print(f"   Average Chunk Size: {stats.get('average_chunk_size', 0)} chars")
                    print(f"   Embedding Model: {stats.get('model_name', 'Unknown')}")
                else:
                    print(f"   Knowledge Base: {CosmicConstants.STATUS_ICONS['error']} Not Ready")
                    print("   🔴 Run 'python core/cli.py setup' to initialize")
            except Exception as e:
                print(f"   Knowledge Base: {CosmicConstants.STATUS_ICONS['error']} Error")
                print(f"   🔴 Status check failed: {str(e)}")
        else:
            print(f"   Knowledge Base: {CosmicConstants.STATUS_ICONS['error']} Not Accessible")
        
        print(f"   Session Duration: {self._get_session_duration()}")
        print(f"   Queries Processed: {self._count_session_queries()}")
        print("─" * 50)
    
    def display_wisdom(self):
        """Display cosmic wisdom."""
        print("\\n🔮 Cosmic Wisdom from the Digital Realm:")
        print("─" * 60)
        
        wisdom_collection = [
            "🌟 In cybersecurity, preparation is the bridge between knowledge and action.",
            "⚡ Every control implemented is a barrier against the forces of chaos.",
            "🛡️ Documentation is the light that illuminates the path to compliance.",
            "🔮 Understanding the framework is the first step to mastering the domain.",
            "💫 Risk without awareness is chaos; risk with knowledge is opportunity.",
            "🌌 The strongest defenses are built on foundations of continuous learning.",
            "⚡ In the realm of security, questioning everything leads to protecting everything."
        ]
        
        import random
        selected_wisdom = random.sample(wisdom_collection, 3)
        
        for i, wisdom in enumerate(selected_wisdom, 1):
            print(f"   {i}. {wisdom}")
        
        print("─" * 60)
        print("   💡 Let these words guide your cybersecurity journey.")
    
    def display_history(self):
        """Display conversation history with cosmic formatting."""
        if not self.conversation_history:
            print("   🌌 No cosmic interactions in this session...")
            return
        
        print(f"\\n🔮 Cosmic Session History ({self.session_id}):")
        print("─" * 70)
        
        for i, entry in enumerate(self.conversation_history[-10:], 1):  # Show last 10
            timestamp = entry.get("timestamp", "")
            query = entry.get("content", "")
            results_count = entry.get("results_count", 0)
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except (ValueError, TypeError) as e:
                time_str = "Unknown"
            
            print(f"  {i}. [{time_str}] {query[:50]}{'...' if len(query) > 50 else ''}")
            print(f"      └─ {results_count} signals found")
        
        print("─" * 70)
    
    def _get_session_duration(self) -> str:
        """Get formatted session duration."""
        duration = datetime.now() - self.session_start
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    
    def _count_session_queries(self) -> int:
        """Count queries in current session."""
        return len([h for h in self.conversation_history if h.get("type") == "query"])
    
    def run_cosmic_chat(self):
        """Main cosmic chat loop."""
        self.display_cosmic_greeting()
        
        # Check system readiness
        if not self.retriever:
            print("\\n🔴 Cosmic Knowledge Base Not Accessible")
            print("   The digital realm remains beyond reach...")
            print("   Please run: python core/cli.py setup")
            return
        
        while True:
            try:
                # Get user input with cosmic prompt
                query = input("\\n🔮 cosmic> ").strip()
                
                if not query:
                    continue
                
                # Handle special commands
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\\n🌟 Returning to the physical realm...")
                    print("   May your cybersecurity journey be illuminated.")
                    print("   Until the digital streams call you back... 🔮")
                    break
                
                elif query.lower() in ['help', '?']:
                    self.display_help()
                    continue
                
                elif query.lower() in ['clear', 'cls']:
                    # SECURITY FIX: Use cross-platform clear command safely
                    import subprocess
                    try:
                        if os.name == 'nt':  # Windows
                            subprocess.run(['cls'], shell=True, check=True)
                        else:  # Unix/Linux/Mac
                            subprocess.run(['clear'], check=True)
                    except subprocess.CalledProcessError:
                        print("\n" * 50)  # Fallback: print newlines
                    self.display_cosmic_greeting()
                    continue
                
                elif query.lower() == 'status':
                    self.display_status()
                    continue
                
                elif query.lower() == 'history':
                    self.display_history()
                    continue
                
                elif query.lower() == 'wisdom':
                    self.display_wisdom()
                    continue
                
                # Handle personality mode commands
                elif query.lower().startswith('/mode'):
                    self.handle_mode_command(query)
                    continue
                
                # Validate input
                if not self.validate_input(query):
                    continue
                
                # Perform cosmic search
                print(f"   {CosmicConstants.STATUS_ICONS['processing']} Processing cosmic query...")
                results = self.search_cosmic_knowledge(query)
                
                # Display formatted results
                response = self.format_cosmic_response(query, results)
                print(f"\\n{response}")
                
            except KeyboardInterrupt:
                print("\\n\\n🌟 Cosmic session interrupted by user.")
                print("   May the digital force be with you. 🔮")
                break
            except Exception as e:
                self.logger.error(f"Cosmic error: {e}")
                print(f"\\n⚡ Cosmic interference detected: {str(e)}")
                print("   The digital realm shifts unexpectedly...")

def main():
    """Main entry point for cosmic chat interface."""
    try:
        cosmic_chat = CosmicChatInterface()
        cosmic_chat.run_cosmic_chat()
    except Exception as e:
        print(f"🔴 Failed to initialize cosmic interface: {e}")
        print("   The digital realm remains inaccessible...")
        print("   Try running: python core/cli.py setup")

if __name__ == "__main__":
    main()
