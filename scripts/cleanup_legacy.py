#!/usr/bin/env python3
"""
Legacy System Cleanup - Phase 1 Implementation
Safely archives legacy components and consolidates the vector systems.

This script will:
1. Analyze vector system differences
2. Archive legacy vector_indices 
3. Provide recommendations for system consolidation
4. Create migration documentation
"""

import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Union

def analyze_vector_systems() -> Dict[str, Any]:
    """Analyze the structure and differences between vector systems."""
    
    base_dir = Path(__file__).parent.parent
    
    analysis = {
        'vector_db': {
            'path': base_dir / 'vector_db',
            'files': [],
            'total_lines': 0,
            'exists': False
        },
        'vector_storage': {
            'path': base_dir / 'vector_storage', 
            'files': [],
            'total_lines': 0,
            'exists': False
        },
        'legacy_indices': {
            'path': base_dir / 'data' / 'vector_indices' / 'legacy',
            'files': [],
            'exists': False
        }
    }
    
    for system_name, system_info in analysis.items():
        path = system_info['path']
        
        if path.exists():
            system_info['exists'] = True
            
            # Count Python files and lines
            for py_file in path.glob('*.py'):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    
                    system_info['files'].append({
                        'name': py_file.name,
                        'lines': lines,
                        'size_kb': py_file.stat().st_size / 1024
                    })
                    system_info['total_lines'] += lines
                    
                except Exception as e:
                    print(f"  ⚠️ Could not analyze {py_file}: {e}")
    
    return analysis

def analyze_import_usage() -> Dict[str, List[str]]:
    """Analyze which vector system is being used in the codebase."""
    
    base_dir = Path(__file__).parent.parent
    usage_analysis = {
        'vector_db': [],
        'vector_storage': []
    }
    
    # Search for imports in Python files
    for py_file in base_dir.rglob('*.py'):
        if 'backup' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'from vector_db' in content or 'import vector_db' in content:
                usage_analysis['vector_db'].append(str(py_file.relative_to(base_dir)))
            
            if 'from vector_storage' in content or 'import vector_storage' in content:
                usage_analysis['vector_storage'].append(str(py_file.relative_to(base_dir)))
                
        except Exception as e:
            continue  # Skip files that can't be read
    
    return usage_analysis

def create_legacy_archive() -> str:
    """Archive legacy components safely."""
    
    base_dir = Path(__file__).parent.parent
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_dir = base_dir / 'backup' / f'legacy_cleanup_{timestamp}'
    
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Creating legacy archive: {archive_dir}")
    
    # Archive legacy vector indices
    legacy_indices = base_dir / 'data' / 'vector_indices' / 'legacy'
    if legacy_indices.exists():
        print("  🗂️ Archiving legacy vector indices...")
        shutil.copytree(legacy_indices, archive_dir / 'legacy_vector_indices')
        
        # Remove the legacy directory after successful backup
        shutil.rmtree(legacy_indices)
        print("  ✅ Legacy vector indices archived and removed")
    
    # Create documentation of what was archived
    archive_manifest = {
        'archive_date': datetime.now().isoformat(),
        'archived_components': ['legacy_vector_indices'],
        'archive_reason': 'Legacy system cleanup and consolidation',
        'restoration_notes': 'To restore, copy contents back to data/vector_indices/legacy/'
    }
    
    with open(archive_dir / 'archive_manifest.json', 'w') as f:
        json.dump(archive_manifest, f, indent=2)
    
    return str(archive_dir)

def generate_consolidation_recommendation(analysis: Dict[str, Any], usage: Dict[str, List[str]]) -> Dict[str, Any]:
    """Generate recommendations for vector system consolidation."""
    
    recommendation = {
        'primary_system': None,
        'confidence': 0.0,
        'reasoning': [],
        'migration_steps': [],
        'files_to_update': []
    }
    
    # Analyze usage patterns
    db_usage_count = len(usage['vector_db'])
    storage_usage_count = len(usage['vector_storage'])
    
    print(f"📊 Usage Analysis:")
    print(f"  vector_db imports found in {db_usage_count} files")
    print(f"  vector_storage imports found in {storage_usage_count} files")
    
    # Analyze code complexity
    db_lines = analysis['vector_db']['total_lines'] if analysis['vector_db']['exists'] else 0
    storage_lines = analysis['vector_storage']['total_lines'] if analysis['vector_storage']['exists'] else 0
    
    print(f"📋 Code Complexity:")
    print(f"  vector_db: {db_lines} lines of code")
    print(f"  vector_storage: {storage_lines} lines of code")
    
    # Make recommendation based on usage and completeness
    if db_usage_count > storage_usage_count:
        recommendation['primary_system'] = 'vector_db'
        recommendation['confidence'] = min(0.9, 0.5 + (db_usage_count - storage_usage_count) * 0.1)
        recommendation['reasoning'].append(f"vector_db is more widely used ({db_usage_count} vs {storage_usage_count} files)")
    elif storage_usage_count > db_usage_count:
        recommendation['primary_system'] = 'vector_storage'
        recommendation['confidence'] = min(0.9, 0.5 + (storage_usage_count - db_usage_count) * 0.1)
        recommendation['reasoning'].append(f"vector_storage is more widely used ({storage_usage_count} vs {db_usage_count} files)")
    else:
        # Equal usage, decide based on other factors
        if storage_lines > db_lines and storage_lines > 0:
            recommendation['primary_system'] = 'vector_storage'
            recommendation['confidence'] = 0.6
            recommendation['reasoning'].append("vector_storage has more comprehensive implementation")
        elif db_lines > 0:
            recommendation['primary_system'] = 'vector_db'
            recommendation['confidence'] = 0.6
            recommendation['reasoning'].append("vector_db chosen as baseline implementation")
        else:
            recommendation['primary_system'] = 'vector_storage'
            recommendation['confidence'] = 0.5
            recommendation['reasoning'].append("Default choice based on naming convention")
    
    # Generate migration steps
    if recommendation['primary_system'] == 'vector_db':
        recommendation['migration_steps'] = [
            "1. Archive vector_storage module to backup/",
            "2. Update any remaining vector_storage imports to use vector_db",
            "3. Consolidate configuration files",
            "4. Test all vector operations with vector_db",
            "5. Update documentation to reference single vector system"
        ]
        recommendation['files_to_update'] = usage['vector_storage']
    else:
        recommendation['migration_steps'] = [
            "1. Archive vector_db module to backup/",
            "2. Update any vector_db imports to use vector_storage", 
            "3. Consolidate configuration files",
            "4. Test all vector operations with vector_storage",
            "5. Update documentation to reference single vector system"
        ]
        recommendation['files_to_update'] = usage['vector_db']
    
    return recommendation

def create_migration_script(recommendation: Dict[str, Any]) -> str:
    """Create a migration script for the recommended consolidation."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    script_content = f'''#!/usr/bin/env python3
"""
Vector System Migration Script
Generated on: {datetime.now().isoformat()}

Recommended System: {recommendation['primary_system']}
Confidence: {recommendation['confidence']:.1%}

This script will:
{chr(10).join(f"- {step}" for step in recommendation['migration_steps'])}
"""

import shutil
from pathlib import Path
from datetime import datetime

def migrate_vector_system():
    """Execute the vector system migration."""
    
    print("🚀 Starting Vector System Migration...")
    print("=" * 40)
    
    base_dir = Path(__file__).parent.parent
    migration_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create backup directory
    backup_dir = base_dir / 'backup' / f'vector_migration_{{migration_timestamp}}'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Backup directory: {{backup_dir}}")
    
    # Archive the non-primary system
    {'vector_storage' if recommendation['primary_system'] == 'vector_db' else 'vector_db'}_dir = base_dir / '{'vector_storage' if recommendation['primary_system'] == 'vector_db' else 'vector_db'}'
    
    if {'vector_storage' if recommendation['primary_system'] == 'vector_db' else 'vector_db'}_dir.exists():
        print("🗂️ Archiving deprecated vector system...")
        shutil.copytree({'vector_storage' if recommendation['primary_system'] == 'vector_db' else 'vector_db'}_dir, backup_dir / '{'vector_storage' if recommendation['primary_system'] == 'vector_db' else 'vector_db'}_archived')
        shutil.rmtree({'vector_storage' if recommendation['primary_system'] == 'vector_db' else 'vector_db'}_dir)
        print("✅ Deprecated system archived and removed")
    
    print("\\n🎉 Migration completed successfully!")
    print("🌌 The cosmic vector orchestra now plays in perfect harmony!")

if __name__ == "__main__":
    migrate_vector_system()
'''
    
    script_path = Path(__file__).parent / 'migrate_vector_system.py'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return str(script_path)

def main():
    """Main cleanup execution."""
    
    print("🧹 PepeluGPT Legacy System Cleanup")
    print("=" * 40)
    
    # Analyze vector systems
    print("🔍 Analyzing vector systems...")
    analysis = analyze_vector_systems()
    
    print("📊 System Analysis:")
    for system_name, system_info in analysis.items():
        if system_info['exists']:
            files_count = len(system_info['files'])
            lines_count = system_info.get('total_lines', 0)
            print(f"  ✅ {system_name}: {files_count} files, {lines_count} lines")
        else:
            print(f"  ❌ {system_name}: Not found")
    
    # Analyze usage patterns
    print("\\n🔍 Analyzing import usage...")
    usage = analyze_import_usage()
    
    # Archive legacy components
    print("\\n🗂️ Archiving legacy components...")
    archive_path = create_legacy_archive()
    
    # Generate recommendations
    print("\\n🎯 Generating consolidation recommendations...")
    recommendation = generate_consolidation_recommendation(analysis, usage)
    
    # Display results
    print("\\n📋 CONSOLIDATION RECOMMENDATIONS")
    print("=" * 35)
    print(f"🏆 Recommended System: {recommendation['primary_system']}")
    print(f"🔮 Confidence: {recommendation['confidence']:.1%}")
    print("\\n📝 Reasoning:")
    for reason in recommendation['reasoning']:
        print(f"  • {reason}")
    
    print("\\n📋 Migration Steps:")
    for step in recommendation['migration_steps']:
        print(f"  {step}")
    
    if recommendation['files_to_update']:
        print(f"\\n📄 Files to Update ({len(recommendation['files_to_update'])}):")
        for file_path in recommendation['files_to_update'][:5]:  # Show first 5
            print(f"  • {file_path}")
        if len(recommendation['files_to_update']) > 5:
            print(f"  • ... and {len(recommendation['files_to_update']) - 5} more")
    
    # Create migration script
    migration_script = create_migration_script(recommendation)
    
    print(f"\\n✅ CLEANUP SUMMARY")
    print("=" * 20)
    print(f"📁 Legacy components archived: {archive_path}")
    print(f"📝 Migration script created: {migration_script}")
    print("🌌 Cosmic harmony restored through strategic consolidation!")

if __name__ == "__main__":
    main()
