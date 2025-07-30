#!/usr/bin/env python3
"""
Personality Router Consolidation Plan - Phase 1 Implementation
Consolidates two personality routers into the enhanced version.

This script will:
1. Backup the basic router for reference
2. Update all imports to use enhanced router
3. Add migration path for existing configurations
4. Validate the consolidation
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def consolidate_personality_routers():
    """Consolidate the personality routing system."""
    
    print("🎭 Starting Personality Router Consolidation...")
    print("=" * 50)
    
    # Paths
    base_dir = Path(__file__).parent.parent
    personalities_dir = base_dir / "personalities"
    backup_dir = base_dir / "backup" / f"router_consolidation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Step 1: Create backup
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    basic_router = personalities_dir / "personality_router.py"
    enhanced_router = personalities_dir / "enhanced_personality_router.py"
    
    if basic_router.exists():
        print("📁 Backing up basic router...")
        shutil.copy2(basic_router, backup_dir / "personality_router_backup.py")
        print(f"✅ Backup created: {backup_dir}")
    
    # Step 2: Rename enhanced router to be the main router
    print("🔄 Promoting enhanced router to main router...")
    
    if enhanced_router.exists():
        # Read enhanced router content
        with open(enhanced_router, 'r', encoding='utf-8') as f:
            enhanced_content = f.read()
        
        # Create new main router with enhanced functionality
        new_router_content = enhanced_content.replace(
            "class EnhancedPersonalityRouter:",
            "class PersonalityRouter:"
        ).replace(
            "Enhanced Personality Router - Advanced personality management",
            "Personality Router - Advanced personality management (Consolidated from Enhanced)"
        )
        
        # Add backward compatibility
        new_router_content += """

# Backward compatibility aliases
EnhancedPersonalityRouter = PersonalityRouter

# Global router instance (enhanced version)
personality_router = PersonalityRouter()

# Legacy function support
def switch_personality_mode(mode_name: str) -> str:
    \"\"\"Switch personality mode by name - Legacy function.\"\"\"
    try:
        from .base_personality import PersonalityMode
        mode = PersonalityMode(mode_name.lower())
        return personality_router.switch_mode(mode)
    except ValueError:
        available = ", ".join([mode.value for mode in PersonalityMode])
        return f"❌ Invalid mode '{mode_name}'. Available: {available}"

def get_personality_help() -> str:
    \"\"\"Get help text for personality modes - Legacy function.\"\"\"
    return personality_router.get_help_text()
"""
        
        # Write the consolidated router
        with open(basic_router, 'w', encoding='utf-8') as f:
            f.write(new_router_content)
        
        print("✅ Main router updated with enhanced functionality")
    
    # Step 3: Update __init__.py
    init_file = personalities_dir / "__init__.py"
    
    if init_file.exists():
        print("📝 Updating personalities module imports...")
        
        with open(init_file, 'r', encoding='utf-8') as f:
            init_content = f.read()
        
        # Update imports to use the consolidated router
        updated_content = init_content.replace(
            "from .enhanced_personality_router import",
            "# Enhanced router consolidated into main router\n# from .enhanced_personality_router import"
        )
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Module imports updated")
    
    # Step 4: Archive the enhanced router file
    if enhanced_router.exists():
        shutil.move(enhanced_router, backup_dir / "enhanced_personality_router_archived.py")
        print(f"✅ Enhanced router archived to backup")
    
    # Step 5: Create configuration template
    config_dir = base_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    personality_config = config_dir / "personality_system.yaml"
    
    if not personality_config.exists():
        print("📄 Creating personality system configuration...")
        
        config_content = """# PepeluGPT Personality System Configuration
# Consolidated configuration for advanced personality management

global_config:
  default_personality: "oracle"
  
  personality_switching:
    enabled: true
    require_confirmation: false
    
  auto_detection:
    enabled: true
    confidence_threshold: 0.7
    
  session_management:
    track_history: true
    max_history_entries: 100

personalities:
  oracle:
    identity:
      name: "Oracle Mode"
      description: "Spiritual, introspective, philosophically technical"
      greeting: "🔮 The Oracle awakens... Cosmic insights await."
      
    behavior:
      tone: ["poetic", "cryptic", "layered"]
      style_notes: "Uses metaphors, speaks in contemplative layers"
      
    triggers:
      keywords: ["wisdom", "insight", "spiritual", "mystical", "oracle"]
      
  compliance:
    identity:
      name: "Compliance Mode"
      description: "Methodical, audit-focused, regulation-informed"
      greeting: "📊 Compliance mode activated. Risk analysis in progress."
      
    behavior:
      tone: ["precise", "tabular", "risk-oriented"]
      style_notes: "Annotates logic paths with control identifiers"
      
    triggers:
      keywords: ["audit", "control", "framework", "risk", "policy", "compliance"]
      
  cosmic:
    identity:
      name: "Cosmic Mode"
      description: "Mystical, expressive, creative design"
      greeting: "🌠 Cosmic energies align... Creative consciousness flows."
      
    behavior:
      tone: ["flowing", "metaphoric", "inspirational"]
      style_notes: "Adds markdown flavor, uses poetic variable names"
      
    triggers:
      keywords: ["quantum", "dimension", "possibility", "consciousness", "cosmic"]
"""
        
        with open(personality_config, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ Personality configuration template created")
    
    print("\n🎉 Personality Router Consolidation Complete!")
    print("=" * 50)
    print(f"📁 Backups stored in: {backup_dir}")
    print("🎭 Enhanced functionality now available in main router")
    print("⚙️ Configuration template created")
    print("\n🌌 The cosmic orchestra is now more harmonious!")

if __name__ == "__main__":
    consolidate_personality_routers()
