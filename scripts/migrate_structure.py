#!/usr/bin/env python3
"""
PepeluGPT Structure Migration Script
Automated script to implement the recommended folder structure and naming conventions.
"""

import os
import shutil
from pathlib import Path


class PepeluStructureMigrator:
    """Handles the migration to the new PepeluGPT structure."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backup_original_structure"
        
    def create_backup(self):
        """Create backup of current structure before migration."""
        print("🔄 Creating backup of current structure...")
        
        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)
        
        # Backup key files that will be moved
        files_to_backup = [
            "pepelugpt.py",
            "git_integration.py", 
            "version.py",
            "core/response_personalities.py"
        ]
        
        for file_path in files_to_backup:
            source = self.project_root / file_path
            if source.exists():
                dest = self.backup_dir / file_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                print(f"   ✓ Backed up: {file_path}")
    
    def create_new_structure(self):
        """Create the new folder structure."""
        print("\n🏗️  Creating new folder structure...")
        
        new_folders = [
            "personalities",
            "validation", 
            "file_processing",
            "vector_storage",
            "utils",
            "integration",
            "data/documents/cybersecurity",
            "data/documents/reference", 
            "data/vector_indices",
            "data/cache",
            "docs/api",
            "docs/personalities",
            "docs/development",
            "scripts/deployment",
            "scripts/maintenance", 
            "scripts/utilities"
        ]
        
        for folder in new_folders:
            folder_path = self.project_root / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python modules
            if not folder.startswith(('data/', 'docs/', 'scripts/')):
                init_file = folder_path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text('"""Module initialization."""\n', encoding='utf-8')
            
            print(f"   ✓ Created: {folder}")
    
    def migrate_files(self):
        """Migrate files to new locations with new names."""
        print("\n📦 Migrating files to new structure...")
        
        # File migrations following naming conventions
        migrations = [
            # Core files
            ("pepelugpt.py", "core/pepelugpt_engine.py"),
            ("version.py", "manifest/version_manager.py"),
            ("git_integration.py", "integration/git_integration.py"),
            
            # File parser -> file_processing
            ("file_parser/main_parser.py", "file_processing/document_router.py"),
            ("file_parser/parser_utils.py", "file_processing/processing_utils.py"),
            
            # Cyber documents reorganization
            ("cyber_documents/", "data/documents/cybersecurity/"),
            ("cyber_vector_db/", "data/vector_indices/"),
            ("vector_db/", "data/vector_indices/legacy/"),
        ]
        
        for source_path, dest_path in migrations:
            source = self.project_root / source_path
            dest = self.project_root / dest_path
            
            if source.exists():
                # Create destination directory
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                if source.is_file():
                    shutil.copy2(source, dest)
                    print(f"   ✓ Migrated: {source_path} → {dest_path}")
                else:
                    # For directories, move contents
                    if not dest.exists():
                        shutil.copytree(source, dest)
                        print(f"   ✓ Migrated: {source_path} → {dest_path}")
    
    def create_personality_modules(self):
        """Create modular personality files."""
        print("\n🎭 Creating personality modules...")
        
        # Create base personality
        base_personality_content = '''#!/usr/bin/env python3
"""
Base Personality Module - Abstract interface for all personality modes.
Following PepeluGPT naming conventions and modular design.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class PersonalityMode(Enum):
    """Available response personality modes."""
    ORACLE = "oracle"
    COMPLIANCE = "compliance" 
    COSMIC = "cosmic"
    DEFAULT = "default"


class BasePersonality(ABC):
    """Abstract base class for response personality modules."""
    
    def __init__(self, mode: PersonalityMode):
        self.mode = mode
        self.active_since = datetime.now()
    
    @abstractmethod
    def format_response(self, content: str, query: str = "", metadata: Dict = None) -> str:
        """Format response according to personality style."""
        pass
    
    @abstractmethod
    def get_greeting(self) -> str:
        """Get personality-specific greeting."""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get personality-specific system prompt."""
        pass
'''
        
        # Write base personality
        base_file = self.project_root / "personalities" / "base_personality.py"
        base_file.write_text(base_personality_content, encoding='utf-8')
        print("   ✓ Created: personalities/base_personality.py")
        
        # Create personality router
        router_content = '''#!/usr/bin/env python3
"""
Personality Router - Central personality selection and management.
"""

from typing import Dict, Optional
from .base_personality import PersonalityMode, BasePersonality
from .oracle_mode import OracleMode
from .compliance_mode import ComplianceMode
from .cosmic_mode import CosmicMode


class PersonalityRouter:
    """Routes requests to appropriate personality modes."""
    
    def __init__(self):
        self._personalities = {
            PersonalityMode.ORACLE: OracleMode(),
            PersonalityMode.COMPLIANCE: ComplianceMode(),
            PersonalityMode.COSMIC: CosmicMode()
        }
        self._current_mode = PersonalityMode.ORACLE
    
    def get_personality(self, mode: PersonalityMode) -> BasePersonality:
        """Get personality instance by mode."""
        return self._personalities.get(mode, self._personalities[PersonalityMode.ORACLE])
    
    def switch_mode(self, mode: PersonalityMode) -> BasePersonality:
        """Switch to specified personality mode."""
        self._current_mode = mode
        return self.get_personality(mode)
    
    def auto_detect_mode(self, query: str) -> PersonalityMode:
        """Auto-detect personality mode based on query keywords."""
        query_lower = query.lower()
        
        # Compliance keywords
        compliance_keywords = ["audit", "control", "framework", "risk", "policy", "compliance"]
        if any(keyword in query_lower for keyword in compliance_keywords):
            return PersonalityMode.COMPLIANCE
            
        # Cosmic keywords  
        cosmic_keywords = ["quantum", "dimension", "possibility", "consciousness", "cosmic"]
        if any(keyword in query_lower for keyword in cosmic_keywords):
            return PersonalityMode.COSMIC
            
        # Default to Oracle
        return PersonalityMode.ORACLE
'''
        
        router_file = self.project_root / "personalities" / "personality_router.py"
        router_file.write_text(router_content, encoding='utf-8')
        print("   ✓ Created: personalities/personality_router.py")
    
    def create_config_files(self):
        """Create new configuration files following naming conventions."""
        print("\n⚙️  Creating configuration files...")
        
        # Personality profiles config
        personality_config = '''{
  "personalities": {
    "oracle": {
      "name": "Oracle Mode",
      "emoji": "🔮", 
      "tagline": "Deep Wisdom Engaged",
      "description": "Mystical cyber warrior channeling ancient wisdom",
      "tone": "Contemplative, cryptic, layered",
      "use_cases": ["visioning", "deep_analysis", "introspection"]
    },
    "compliance": {
      "name": "Compliance Mode",
      "emoji": "📊",
      "tagline": "Audit Ready", 
      "description": "Methodical auditor with regulatory expertise",
      "tone": "Structured, authoritative, consultative",
      "use_cases": ["risk_assessment", "control_analysis", "documentation"]
    },
    "cosmic": {
      "name": "Cosmic Mode",
      "emoji": "✨",
      "tagline": "Quantum Consciousness",
      "description": "Quantum-mystical technical guide", 
      "tone": "Playful, expansive, multidimensional",
      "use_cases": ["creative_solutions", "paradigm_shifts", "innovation"]
    }
  }
}'''
        
        config_file = self.project_root / "config" / "personality_profiles.json"
        config_file.write_text(personality_config, encoding='utf-8')
        print("   ✓ Created: config/personality_profiles.json")
        
    def create_validation_modules(self):
        """Create validation modules for privacy-first design."""
        print("\n🔐 Creating validation modules...")
        
        privacy_check_content = '''#!/usr/bin/env python3
"""
Privacy Check Module - Core privacy validation for PepeluGPT.
Implements privacy-first design principles.
"""

from typing import Dict, List, Any, Tuple
import re


class PrivacyValidator:
    """Validates and protects privacy in user inputs and outputs."""
    
    def __init__(self):
        self.sensitive_patterns = [
            r'\\b\\d{3}-\\d{2}-\\d{4}\\b',  # SSN
            r'\\b\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}\\b',  # Credit card
            r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',  # Email
        ]
    
    def validate_input(self, user_input: str) -> Tuple[bool, List[str]]:
        """Validate user input for privacy concerns."""
        violations = []
        
        for pattern in self.sensitive_patterns:
            if re.search(pattern, user_input):
                violations.append(f"Potential sensitive data detected: {pattern}")
        
        return len(violations) == 0, violations
    
    def sanitize_response(self, response: str) -> str:
        """Sanitize response to protect privacy."""
        # Implementation for response sanitization
        return response
'''
        
        privacy_file = self.project_root / "validation" / "privacy_check.py"
        privacy_file.write_text(privacy_check_content, encoding='utf-8')
        print("   ✓ Created: validation/privacy_check.py")
    
    def run_migration(self):
        """Execute the complete migration process."""
        print("🚀 Starting PepeluGPT Structure Migration")
        print("=" * 50)
        
        try:
            self.create_backup()
            self.create_new_structure()
            self.migrate_files()
            self.create_personality_modules()
            self.create_config_files()
            self.create_validation_modules()
            
            print("\n" + "=" * 50)
            print("✅ Migration completed successfully!")
            print("\n📋 Next steps:")
            print("1. Review migrated files for import updates")
            print("2. Extract personality classes from original response_personalities.py")
            print("3. Update core module imports")
            print("4. Test personality switching functionality")
            print("5. Update documentation")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("Check backup directory for original files")


if __name__ == "__main__":
    # Run migration for current directory
    migrator = PepeluStructureMigrator("d:/PepeluGPT")
    migrator.run_migration()
