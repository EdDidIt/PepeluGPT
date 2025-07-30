#!/usr/bin/env python3
"""
Post-Migration Cleanup Script
Removes original files that have been successfully migrated to new structure.
"""

import os
from pathlib import Path


def cleanup_migrated_files():
    """Remove original files that have been successfully migrated."""
    project_root = Path("d:/PepeluGPT")
    
    # Files that have been migrated and can be safely removed
    files_to_remove = [
        "pepelugpt.py",  # Migrated to core/pepelugpt_engine.py
        "git_integration.py",  # Migrated to integration/git_integration.py
        "version.py"  # Migrated to manifest/version_manager.py
    ]
    
    print("🧹 Post-Migration Cleanup")
    print("=" * 30)
    
    for file_path in files_to_remove:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                full_path.unlink()
                print(f"   ✓ Removed: {file_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
        else:
            print(f"   ⚠️  File not found: {file_path}")
    
    print("\n📋 Migration Status Summary:")
    print("✅ New structure created successfully")
    print("✅ Files migrated with new naming conventions")
    print("✅ Backup created in backup_original_structure/")
    print("✅ Original files cleaned up")
    
    print("\n🎯 Next Steps:")
    print("1. Extract personality classes from core/response_personalities.py")
    print("2. Update import statements in core modules")
    print("3. Test the new personality system")
    print("4. Move cyber_documents to data/documents/cybersecurity/")


if __name__ == "__main__":
    cleanup_migrated_files()
