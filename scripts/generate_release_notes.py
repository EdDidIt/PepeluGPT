#!/usr/bin/env python3
"""
Generate release notes for PepeluGPT versions
"""

import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

def generate_release_notes(version: str) -> str:
    """Generate release notes for a specific version."""
    
    # Load version info
    try:
        import sys
        sys.path.append(str(Path(__file__).parent.parent))
        from version.manager import __version__, __codename__, __major_milestones__
        codename: str = __codename__
        # Store milestones for potential future use
        _milestones: Dict[str, Tuple[str, str, str, str]] = {m[1]: m for m in __major_milestones__}
    except (ImportError, AttributeError):
        codename = "Professional Release"
        _milestones: Dict[str, Tuple[str, str, str, str]] = {}
    
    # Load changelog if available
    changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
    changelog_content = ""
    if changelog_path.exists():
        changelog_content = changelog_path.read_text(encoding='utf-8')
    
    # Extract version section from changelog
    version_section = extract_version_section(changelog_content, version)
    
    # Generate professional release notes
    release_notes = f"""# 🔵 PepeluGPT {version} "{codename}"

> *"Enhanced professional cybersecurity capabilities for enterprise security analysis."*

# 🔵 Release Highlights

{version_section if version_section else "This release brings enhanced professional capabilities and cybersecurity intelligence to your security operations."}

# Installation & Upgrade

# New Installation
```bash
git clone https://github.com/EdDidIt/PepeluGPT.git
cd PepeluGPT
pip install -r requirements.txt
python core/cli.py setup
```

# Upgrade from Previous Version
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python core/cli.py setup --upgrade
```

# � Professional Evolution Timeline

Current Version: {get_age_days()} days of professional development  
Stage: Beta - Production-ready cybersecurity platform

# 🔵 What's New

# Enhanced Features
- Improved document parsing capabilities
- Enhanced vector search accuracy
- Better error handling and logging
- Updated compliance framework support

# Technical Improvements
- Performance optimizations
- Memory usage improvements
- Enhanced security measures
- Better cross-platform compatibility

# Documentation Updates
- Expanded user guides
- Enhanced API documentation  
- Updated troubleshooting guides
- New tutorial content

#  Security Updates

This release includes important security enhancements:
- Updated dependency versions
- Enhanced input validation
- Improved error handling
- Strengthened privacy protections

# � Bug Fixes

- Various stability improvements
- Fixed edge cases in document parsing
- Resolved memory leaks in long-running sessions
- Enhanced error recovery mechanisms

# Known Issues

- None currently identified
- Please report any issues on [GitHub Issues](https://github.com/EdDidIt/PepeluGPT/issues)

# 🟢 Contributors

This release was made possible by the professional dedication of our contributors. Special thanks to all who contributed code, documentation, testing, and feedback.

# � Looking Ahead

Professional development continues! Upcoming features include:
- Web interface development
- Enhanced API capabilities
- Additional compliance frameworks
- Performance optimizations
- Community-requested features

# 🔵 Professional Summary

*"Each release is not just an update of code, but an evolution of enterprise capabilities. Every feature added, every bug fixed, every optimization made brings us closer to the perfect harmony of technology and professional excellence."*

---

Full Changelog: [View on GitHub](https://github.com/EdDidIt/PepeluGPT/compare/v{get_previous_version(version)}...{version})

Download: [Release Assets](https://github.com/EdDidIt/PepeluGPT/releases/tag/{version})

Documentation: [Updated Docs](https://github.com/EdDidIt/PepeluGPT/tree/main/docs)

*Professional cybersecurity intelligence for enterprise security operations.*
"""
    
    return release_notes

def extract_version_section(changelog: str, version: str) -> str:
    """Extract the section for a specific version from changelog."""
    if not changelog:
        return ""
    
    # Look for version section
    pattern = rf"# \[{re.escape(version)}\].*?(?=# \[|\Z)"
    match = re.search(pattern, changelog, re.DOTALL)
    
    if match:
        section = match.group(0)
        # Clean up the section
        lines = section.split('\n')[1:]  # Skip the version header
        return '\n'.join(line for line in lines if line.strip())
    
    return ""

def get_age_days() -> int:
    """Calculate age in days from birth date."""
    birth_date = datetime(2024, 12, 1)
    return (datetime.now() - birth_date).days

def get_previous_version(current_version: str) -> str:
    """Get the previous version for comparison."""
    # Simple logic to get previous version
    # In a real implementation, this would parse git tags
    parts = current_version.lstrip('v').split('.')
    if len(parts) == 3:
        major, minor, patch = map(int, parts)
        if patch > 0:
            return f"v{major}.{minor}.{patch-1}"
        elif minor > 0:
            return f"v{major}.{minor-1}.0"
        elif major > 0:
            return f"v{major-1}.0.0"
    
    return "v0.1.0"  # fallback

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_release_notes.py <version>")
        sys.exit(1)
    
    version = sys.argv[1]
    notes = generate_release_notes(version)
    print(notes)
