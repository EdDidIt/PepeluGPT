#!/usr/bin/env python3
"""
PepeluGPT Version and Build Tracking System
Tracks the deployment and operational status of the cybersecurity intelligence platform.
"""

from datetime import datetime, date
from typing import Dict, Any

# Core Version Information
__version__ = "0.3.1"
__release_date__ = "2025-07-29"
__codename__ = "Quantum Guardian"
__stage__ = "Beta"

# Project Birth and Evolution Tracking
__birth_date__ = "2024-12-01"  # When PepeluGPT first came into existence
__major_milestones__ = [
    ("2024-12-01", "0.1.0", "Genesis", "Initial concept and foundation"),
    ("2025-01-15", "0.2.0", "Awakening", "Core AI capabilities established"),
    ("2025-03-10", "0.2.5", "Enhancement", "Document parsing and vector DB"),
    ("2025-07-29", "0.3.1", "Quantum Guardian", "Modular architecture and versioning")
]

def get_version_info() -> Dict[str, Any]:
    """Get comprehensive version information."""
    return {
        "version": __version__,
        "codename": __codename__,
        "stage": __stage__,
        "release_date": __release_date__,
        "birth_date": __birth_date__
    }

def get_build_age() -> Dict[str, Any]:
    """Calculate how long PepeluGPT has been operational."""
    birth = datetime.strptime(__birth_date__, "%Y-%m-%d").date()
    release = datetime.strptime(__release_date__, "%Y-%m-%d").date()
    today = date.today()
    
    total_age = (today - birth).days
    current_version_age = (today - release).days
    
    return {
        "total_days": total_age,
        "current_version_days": current_version_age,
        "birth_date": __birth_date__,
        "release_date": __release_date__,
        "today": today.strftime("%Y-%m-%d")
    }

def get_age_message() -> str:
    """Get a professional status message for PepeluGPT."""
    age_info = get_build_age()
    total_days = age_info["total_days"]
    
    # Calculate years, months, and days for total age
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    
    from typing import List
    age_parts: List[str] = []
    if years > 0:
        age_parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        age_parts.append(f"{months} month{'s' if months != 1 else ''}")
    if days > 0 or not age_parts:
        age_parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    age_str = ", ".join(age_parts)
    
    # Professional status messages based on age
    if total_days < 30:
        status = "Recently deployed and operational 🟢"
    elif total_days < 90:
        status = "System maturing with continued usage 🟢"
    elif total_days < 365:
        status = "Established platform with proven reliability 🟢"
    else:
        status = "Mature cybersecurity intelligence platform 🟢"
    
    return f"PepeluGPT has been operational for {age_str}. {status}"

def get_version_banner() -> str:
    """Get a formatted version banner for display."""
    info = get_version_info()
    age_info = get_build_age()
    
    return f"""
╔═══════════════════════════════════════════════════════════════╗
║                    PEPELU GPT {info['version']}                           ║
║                  "{info['codename']}"                    ║
║                                                               ║
║     �  Cybersecurity Intelligence Platform          ║
║                                                               ║
║  Age: {age_info['total_days']} days | Current Build: {age_info['current_version_days']} days old     ║
║              Professional Cybersecurity Intelligence               ║
╚═══════════════════════════════════════════════════════════════╝
"""

def get_milestone_history() -> str:
    """Get formatted milestone history."""
    history = "\n🔵 Version Timeline:\n"
    for milestone_date, version, codename, description in __major_milestones__:
        history += f"  {milestone_date} - v{version} \"{codename}\" - {description}\n"
    return history


def get_version_command_output() -> str:
    """Get comprehensive version output for CLI commands."""
    info = get_version_info()
    age_info = get_build_age()
    age_msg = get_age_message()
    milestones = get_milestone_history()
    
    return f"""
╔════════════════════════════════════════════════════════════════╗
║                      VERSION INFORMATION                       ║
╚════════════════════════════════════════════════════════════════╝

� Current Build:
  Version: {info['version']}
  Codename: "{info['codename']}"
  Stage: {info['stage']}
  Released: {info['release_date']}

🔵 System Metrics:
  Total Age: {age_info['total_days']} days
  Current Build Age: {age_info['current_version_days']} days
  Deployed: {info['birth_date']}

🟢 Status:
  {age_msg}

{milestones}

def get_roadmap():
    return f"""
    Development Roadmap:
    - Enhanced analysis capabilities
    - Advanced compliance workflows
    - Real-time collaboration features
    - Multi-language document support
    """


def validate():
    """Validate version consistency across the project."""
    print("🔵 Validating version consistency...")

    # Check if version info is accessible
    try:
        info = get_version_info()
        print(f"🟢 Version info valid: {info['version']} \"{info['codename']}\"")
    except Exception as e:
        print(f"🔴 Version info validation failed: {e}")
        return False

    # Check if age calculation works
    try:
        age = get_build_age()
        print(f"🟢 Age calculation valid: {age['total_days']} days total")
    except Exception as e:
        print(f"🔴 Age calculation failed: {e}")
        return False

    print("🟢 All version validations passed!")
    return True


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        success = validate()
        sys.exit(0 if success else 1)
    else:
        # Test the version system
        print(get_version_banner())
        print(get_version_command_output())
