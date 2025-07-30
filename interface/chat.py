#!/usr/bin/env python3
"""
PepeluGPT - Professional Chat Interface
Professional cybersecurity intelligence platform.

Cybersecurity analysis and compliance guidance.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Enhanced imports
try:
    from storage.vector_db.retriever import PepeluRetriever
    system_mode = True
except ImportError:
    # Fallback mode - PepeluRetriever not available
    system_mode = False
    PepeluRetriever = None

class ChatInterface:
    """Professional chat interface for cybersecurity intelligence."""
    def __init__(self):
        self.db: Optional[Any] = None
        self.conversation_history: List[Dict[str, Any]] = []
        
    def load_database(self) -> bool:
        """Load the vector database"""
        print("🔵 Loading PepeluGPT knowledge base...")
        
        # Check if database exists - use relative path from project root
        project_root = Path(__file__).parent.parent
        vector_db_path = project_root / "cyber_vector_db"
        
        try:
            if PepeluRetriever is None:
                print("🔴 PepeluRetriever class is not available. Please check your installation.")
                return False
            
            # Use the actual path for the vector database
            self.db = PepeluRetriever(str(vector_db_path))
            
            if self.db.is_ready():
                print("🟢 Knowledge base loaded successfully.")
                return True
            else:
                print("🔴 Knowledge base not ready.")
                print(f"🔵 Expected database at: {vector_db_path}")
                return False
                
        except Exception as e:
            print(f"🔴 Error loading database: {str(e)}")
            print(f"🔵 Database path attempted: {vector_db_path}")
            return False
    
    def search_knowledge(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information"""
        if not self.db:
            return []
        
        try:
            results = self.db.search(query, top_k=num_results, similarity_threshold=0.5)
            return results
        except Exception as e:
            print(f"🔴 Search error: {str(e)}")
            return []
    
    def format_response(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format search results into a professional response"""
        if not results:
            return ("🔴 No relevant information found for your query.\n"
                   "🔵 Try using different keywords or check if your documents are properly indexed.")
        
        response = f"**Query:** {query}\n\n"
        response += f"**Analysis Results:** {len(results)} relevant sources identified\n\n"
        
        for i, result in enumerate(results, 1):
            filename = result['metadata']['filename']
            content = result['chunk_text']
            score = float(result['similarity_score'])
            
            # Clean and truncate content
            content = content.replace('\n', ' ').replace('\t', ' ')
            content = ' '.join(content.split())  # Remove extra whitespace
            
            if len(content) > 250:
                content = content[:250] + "..."
            
            # Determine relevance level
            if score > 0.8:
                relevance = "🟢 High Relevance"
            elif score > 0.6:
                relevance = "🔵 Medium Relevance"
            else:
                relevance = "🔵 Low Relevance"
            
            response += f"{i}. {filename} ({relevance} - {score:.1%})\n"
            response += f"   {content}\n\n"
        
        return response
    
    def chat_loop(self) -> None:
        """Main chat interface loop"""
        # Import version info
        try:
            from version.manager import get_version_info
            version_info = get_version_info()
        except ImportError:
            version_info = {"version": "unknown", "codename": "Professional"}
        
        print("\n" + "="*70)
        print(f"🟢 PepeluGPT v{version_info['version']} \"{version_info['codename']}\"")
        print("   Professional Cybersecurity Intelligence Platform")
        print("="*70)
        print("🔵 System ready for cybersecurity analysis")
        print("🔵 Loaded cybersecurity knowledge from processed documents")
        print("🔵 Ask about RMF, STIG, NIST frameworks, DoD policies, etc.")
        print("🔵 Type 'help' for commands, 'quit' to exit")
        print("="*70)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🔵 Query: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🔵 Thank you for using PepeluGPT Professional Edition.")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                elif user_input.lower() == 'clear':
                    # Cross-platform clear command
                    try:
                        if os.name == 'nt':  # Windows
                            os.system('cls')
                        else:  # Unix/Linux/Mac
                            os.system('clear')
                    except Exception:
                        # Fallback: print newlines if system commands fail
                        print("\n" * 50)
                    continue
                
                elif user_input.lower().startswith('save '):
                    filename = user_input[5:].strip()
                    self.save_conversation(filename)
                    continue
                
                # Process query
                print("🔵 Searching knowledge base...")
                results = self.search_knowledge(user_input)
                
                # Format and display response
                response = self.format_response(user_input, results)
                print(f"\n**PepeluGPT Professional Analysis:**")
                print(response)
                
                # Save to history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "query": user_input,
                    "results_count": len(results),
                    "top_score": float(results[0]['similarity_score']) if results else 0
                })
                
            except KeyboardInterrupt:
                print("\n\n🔵 Session terminated. Thank you for using PepeluGPT Professional Edition.")
                break
            except Exception as e:
                print(f"\n🔴 Error: {str(e)}")
                print("Please try again or type 'help' for assistance.")
    
    def show_help(self) -> None:
        """Show help information"""
        help_text = """
**PepeluGPT Professional Edition - Help Commands**

**Basic Usage:**
- Type your cybersecurity question and press Enter
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

**Technical Notes:**
- Use specific keywords for better results
- Try different phrasings if you don't find what you need
- Combine multiple concepts (e.g., "RMF STIG implementation")
        """
        print(help_text)
    
    def show_history(self) -> None:
        """Show conversation history"""
        if not self.conversation_history:
            print("🔵 No conversation history yet.")
            return
        
        print(f"\n**Conversation History ({len(self.conversation_history)} queries):**")
        for i, item in enumerate(self.conversation_history[-10:], 1):  # Show last 10
            timestamp = datetime.fromisoformat(item['timestamp']).strftime("%H:%M:%S")
            query = item['query'][:50] + "..." if len(item['query']) > 50 else item['query']
            results = item['results_count']
            score = item['top_score']
            print(f"  {i}. [{timestamp}] {query} ({results} results, {score:.1%} relevance)")
    
    def save_conversation(self, filename: str) -> None:
        """Save conversation history to file"""
        if not self.conversation_history:
            print("🔵 No conversation to save.")
            return
        
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            print(f"🟢 Conversation saved to: {filename}")
        except Exception as e:
            print(f"🔴 Error saving file: {str(e)}")

def main() -> None:
    """Main function"""
    # Create ChatInterface instance
    chat_interface = ChatInterface()
    
    # Load the knowledge base
    if not chat_interface.load_database():
        print("\n🔵 To set up PepeluGPT, run these commands:")
        print("   1. python processing/parse_all_documents.py")
        print("   2. python scripts/build_vector_db.py")
        print("   3. python interface/chat.py")
        return
    
    # Start chat interface
    chat_interface.chat_loop()

if __name__ == "__main__":
    main()
