#!/usr/bin/env python3
"""
Enhanced Classic Mode Demonstration
Shows how classic mode now has access to learned corrections from adaptive mode training.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine import Engine

def demo_enhanced_classic_mode():
    """Demonstrate the enhanced classic mode with learned corrections."""
    
    print("=" * 80)
    print("🎯 ENHANCED CLASSIC MODE DEMONSTRATION")
    print("=" * 80)
    
    print("\n🔵 What Changed:")
    print("  ✅ Classic mode now loads learned corrections from adaptive mode")
    print("  ✅ Maintains classic mode's stability and predictability")  
    print("  ✅ No active learning - just uses pre-trained corrections")
    print("  ✅ Perfect for production/user-facing deployments")
    
    # Test configuration (classic mode)
    config = {
        "learning": {"enabled": False},  # Classic mode - no active learning
        "model": {"name": "classic-model"},
        "logging": {"level": "INFO"}
    }
    
    try:
        # Initialize enhanced classic mode engine
        engine = Engine(config, None)  # No data manager needed for this demo
        
        print(f"\n📊 Status:")
        print(f"  • Mode: CLASSIC (learning disabled)")  
        print(f"  • Learned corrections loaded: {len(engine.correction_overrides)}")
        print(f"  • Source: Adaptive mode training database")
        
        if engine.correction_overrides:
            print(f"\n📚 Available Learned Knowledge:")
            for i, (query, correction) in enumerate(list(engine.correction_overrides.items())[:3], 1):
                print(f"  {i}. \"{query.title()}\"")
                print(f"     → {correction[:80]}...")
                print()
                
            if len(engine.correction_overrides) > 3:
                print(f"     ... and {len(engine.correction_overrides) - 3} more corrections")
        
        print(f"\n🧪 Testing Query Processing:")
        test_queries = [
            "PT-2",
            "pt-2 control", 
            "explain confidentiality",  # This one won't have a correction yet
            "authority to process pii"
        ]
        
        for query in test_queries:
            print(f"\n❓ Query: \"{query}\"")
            
            # Check for learned correction
            correction = engine._check_correction_override(query)
            if correction:
                print(f"  ✅ Found learned response:")
                print(f"     {correction[:100]}...")
                print(f"  🎯 Source: Adaptive mode training")
            else:
                print(f"  🔍 No learned response - would use knowledge base search")
                print(f"  💡 Train this query in adaptive mode to improve classic mode")
        
        print(f"\n🎉 SUMMARY:")
        print(f"  • Classic mode enhanced successfully!")
        print(f"  • Can access {len(engine.correction_overrides)} learned corrections")
        print(f"  • Perfect workflow: Train in adaptive → Deploy in classic")
        print(f"  • Users get stable, learned responses without active learning")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")
        return False

if __name__ == "__main__":
    demo_enhanced_classic_mode()
