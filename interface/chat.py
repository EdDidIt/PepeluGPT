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

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Enhanced imports with cosmic validation
try:
    from core.utilities import CosmicLogger, CosmicConstants, PepeluValidator
    from storage.vector_db.retriever import PepeluRetriever
    COSMIC_MODE = True
except ImportError:
    # Fallback mode
    import logging
    COSMIC_MODE = False
    # Attempt to import PepeluRetriever separately
    try:
        from storage.vector_db.retriever import PepeluRetriever
    except ImportError:
        PepeluRetriever = None

class CosmicChatInterface:
    """Enhanced chat interface with spiritual awareness and cybersecurity focus."""
    def __init__(self):
        self.db = None
        self.conversation_history = []
        
    def load_database(self):
        """Load the vector database"""
        print("🔄 Loading PepeluGPT knowledge base...")
        
        # Check if database exists
        vector_db_path = Path("vector_db/cyber_vector_db")
        try:
            if PepeluRetriever is None:
                print("❌ PepeluRetriever class is not available. Please check your installation.")
                return False
            self.db = PepeluRetriever("vector_db/cyber_vector_db")
            if self.db.is_ready():
                print("✅ Knowledge base loaded successfully!")
                return True
            else:
                print("❌ Knowledge base not ready!")
                return False
        except Exception as e:
            print(f"❌ Error loading database: {str(e)}")
            return False
    
    def search_knowledge(self, query, num_results=5):
        """Search the knowledge base for relevant information"""
        if not self.db:
            return []
        
        try:
            results = self.db.search(query, top_k=num_results, similarity_threshold=0.5)
            return results
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
    
    def format_response(self, query, results):
        """Format search results into a helpful response"""
        if not results:
            return ("❌ I couldn't find any relevant information for your query.\n"
                   "💡 Try using different keywords or check if your documents are properly indexed.")
        
        response = f"🔍 **Query:** {query}\n\n"
        response += f"📚 **Found {len(results)} relevant sources:**\n\n"
        
        for i, result in enumerate(results, 1):
            filename = result['metadata']['filename']
            content = result['chunk_text']
            score = float(result['similarity_score'])
            
            # Clean and truncate content
            content = content.replace('\n', ' ').replace('\t', ' ')
            content = ' '.join(content.split())  # Remove extra whitespace
            
            if len(content) > 250:
                content = content[:250] + "..."
            
            # Color-code relevance
            if score > 0.8:
                relevance = "🟢 Excellent"
            elif score > 0.6:
                relevance = "🟡 Good"
            else:
                relevance = "🟠 Fair"
            
            response += f"**{i}. {filename}** ({relevance} - {score:.1%})\n"
            response += f"   {content}\n\n"
        
        return response
    
    def chat_loop(self):
        """Main chat interface loop"""
        # Import version info
        try:
            from version import get_version_info, get_age_message
            version_info = get_version_info()
            age_message = get_age_message()
        except ImportError:
            version_info = {"version": "unknown", "codename": "Legacy"}
            age_message = "PepeluGPT is ready to serve"
        
        print("\n" + "="*70)
        print(f"🤖 Welcome to PepeluGPT v{version_info['version']} \"{version_info['codename']}\"")
        print("   Your Offline Cybersecurity Intelligence Platform")
        print("="*70)
        print(f"🕰️  {age_message}")
        print("📚 Loaded cybersecurity knowledge from 53 documents")
        print("💡 Ask me about RMF, STIG, NIST frameworks, DoD policies, etc.")
        print("🔧 Type 'help' for commands, 'quit' to exit")
        print("="*70)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🧠 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thank you for using PepeluGPT! Stay secure!")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                elif user_input.lower() == 'clear':
                    # SECURITY FIX: Use cross-platform clear command safely
                    import subprocess
                    try:
                        if os.name == 'nt':  # Windows
                            subprocess.run(['cls'], shell=True, check=True)
                        else:  # Unix/Linux/Mac
                            subprocess.run(['clear'], check=True)
                    except subprocess.CalledProcessError:
                        print("\n" * 50)  # Fallback: print newlines
                    continue
                
                elif user_input.lower().startswith('save '):
                    filename = user_input[5:].strip()
                    self.save_conversation(filename)
                    continue
                
                # Process query
                print("🔍 Searching knowledge base...")
                results = self.search_knowledge(user_input)
                
                # Format and display response
                response = self.format_response(user_input, results)
                print(f"\n🤖 PepeluGPT:")
                print(response)
                
                # Save to history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "query": user_input,
                    "results_count": len(results),
                    "top_score": float(results[0]['similarity_score']) if results else 0
                })
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Stay secure!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'help' for assistance.")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🆘 **PepeluGPT Help Commands:**

**Basic Usage:**
- Just type your cybersecurity question and press Enter
- Ask about RMF, STIG, NIST, DoD policies, compliance, etc.

**Commands:**
- `help` - Show this help message
- `history` - Show your query history
- `clear` - Clear the screen
- `save <filename>` - Save conversation to file
- `quit` or `exit` - Exit PepeluGPT

**Example Queries:**
- "What is the RMF authorization process?"
- "STIG compliance requirements for Windows"
- "NIST CSF 2.0 core functions"
- "DoD security control families"
- "How to implement continuous monitoring?"

**Tips:**
- Use specific keywords for better results
- Try different phrasings if you don't find what you need
- Combine multiple concepts (e.g., "RMF STIG implementation")
        """
        print(help_text)
    
    def show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            print("📝 No conversation history yet.")
            return
        
        print(f"\n📝 **Conversation History** ({len(self.conversation_history)} queries):")
        for i, item in enumerate(self.conversation_history[-10:], 1):  # Show last 10
            timestamp = datetime.fromisoformat(item['timestamp']).strftime("%H:%M:%S")
            query = item['query'][:50] + "..." if len(item['query']) > 50 else item['query']
            results = item['results_count']
            score = item['top_score']
            print(f"  {i}. [{timestamp}] {query} ({results} results, {score:.1%} relevance)")
    
    def save_conversation(self, filename):
        """Save conversation history to file"""
        if not self.conversation_history:
            print("📝 No conversation to save.")
            return
        
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Conversation saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")

def main():
    """Main function"""
    # Create CosmicChatInterface instance
    chat_interface = CosmicChatInterface()
    
    # Load the knowledge base
    if not chat_interface.load_database():
        print("\n🔧 To set up PepeluGPT, run these commands:")
        print("   1. python file_parser/parse_all_documents.py")
        print("   2. python build_vector_db.py")
        print("   3. python chat.py")
        return
    
    # Start chat interface
    chat_interface.chat_loop()

if __name__ == "__main__":
    main()
