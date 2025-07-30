#!/usr/bin/env python3
"""
PepeluGPT Git Integration for Version Management
Helps create semantic Git tags and manage releases.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

def run_git_command(command: list[str]) -> tuple[bool, str]:
    """Run a git command and return success status and output."""
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True,
            cwd=Path(__file__).parent
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except FileNotFoundError:
        return False, "Git not found. Please install Git."

def check_git_status() -> bool:
    """Check if the repository is clean and ready for tagging."""
    success, output = run_git_command(["git", "status", "--porcelain"])
    if not success:
        print(f"Git status check failed: {output}")
        return False
    
    if output:
        print("Repository has uncommitted changes:")
        print(output)
        response = input("Continue anyway? (y/n): ").lower().strip()
        return response in ['y', 'yes']
    
    print("Repository is clean")
    return True

def get_current_branch() -> Optional[str]:
    """Get the current Git branch."""
    success, output = run_git_command(["git", "branch", "--show-current"])
    if success:
        return output
    return None

def create_version_tag(version: str, message: str) -> bool:
    """Create a Git tag for the version."""
    tag_name = f"v{version}"
    
    # Check if tag already exists
    success, _ = run_git_command(["git", "tag", "-l", tag_name])
    if success:
        success, existing_tags = run_git_command(["git", "tag", "-l"])
        if tag_name in existing_tags:
            print(f"Tag {tag_name} already exists")
            response = input("Overwrite? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                return False
            # Delete existing tag
            run_git_command(["git", "tag", "-d", tag_name])
    
    # Create new tag
    success, output = run_git_command([
        "git", "tag", "-a", tag_name, "-m", message
    ])
    
    if success:
        print(f"Created tag: {tag_name}")
        
        # Ask if user wants to push the tag
        response = input("Push tag to remote? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            success, output = run_git_command(["git", "push", "origin", tag_name])
            if success:
                print(f"Pushed tag {tag_name} to remote")
            else:
                print(f"Failed to push tag: {output}")
        
        return True
    else:
        print(f"Failed to create tag: {output}")
        return False

def list_version_tags():
    """List all version tags."""
    success, output = run_git_command(["git", "tag", "-l", "v*", "--sort=-version:refname"])
    if success and output:
        print("Existing version tags:")
        for tag in output.split('\n')[:10]:  # Show last 10 tags
            success, tag_info = run_git_command([
                "git", "log", "-1", "--pretty=format:%h %s (%cr)", tag
            ])
            if success:
                print(f"  {tag}: {tag_info}")
            else:
                print(f"  {tag}")
    else:
        print("No version tags found")

def generate_release_commit_message(version: str, codename: str) -> str:
    """Generate a conventional commit message for the release."""
    return f"release: bump version to {version} '{codename}'\n\n- Add comprehensive versioning and age tracking\n- Update CLI with version commands\n- Enhance user interface with dynamic version display"

def create_release_workflow():
    """Interactive workflow for creating a release."""
    print("\nPepeluGPT Release Workflow")
    print("=" * 40)
    
    # Check Git status
    if not check_git_status():
        return False
    
    # Get current branch
    branch = get_current_branch()
    if branch:
        print(f"Current branch: {branch}")
        if branch != "main" and branch != "master":
            print("You're not on the main branch")
            response = input("Continue anyway? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                return False
    
    # Get version information
    try:
        from version import get_version_info
        version_info = get_version_info()
        version = version_info['version']
        codename = version_info['codename']
    except ImportError:
        print("Could not load version information")
        return False
    
    print(f"\nCreating release for v{version} '{codename}'")
    
    # List existing tags
    list_version_tags()
    
    # Create commit if there are changes
    success, status = run_git_command(["git", "status", "--porcelain"])
    if success and status:
        print("\nCommitting version changes...")
        commit_message = generate_release_commit_message(version, codename)
        
        # Add version-related files
        version_files = ["version.py", "CHANGELOG.md", "pepelugpt.py", "core/cli.py"]
        for file in version_files:
            if Path(file).exists():
                run_git_command(["git", "add", file])
        
        success, output = run_git_command(["git", "commit", "-m", commit_message])
        if success:
            print("Committed version changes")
        else:
            print(f"Commit failed: {output}")
    
    # Create tag
    tag_message = f"PepeluGPT v{version} '{codename}' - Cybersecurity Intelligence Platform"
    if create_version_tag(version, tag_message):
        print(f"\nRelease v{version} created successfully!")
        print("\nNext steps:")
        print("  1. Create release notes on GitHub")
        print("  2. Update documentation")
        print("  3. Notify users of the new version")
        return True
    
    return False

def main():
    """Main CLI for Git integration."""
    if len(sys.argv) < 2:
        print("""
🔗 PepeluGPT Git Integration

Usage:
  python git_integration.py status      # Check Git status
  python git_integration.py tags        # List version tags  
  python git_integration.py release     # Create release workflow
  python git_integration.py tag <msg>   # Create tag for current version

Examples:
  python git_integration.py status
  python git_integration.py tags
  python git_integration.py release
        """)
        return
    
    command = sys.argv[1]
    
    if command == "status":
        check_git_status()
        branch = get_current_branch()
        if branch:
            print(f"Current branch: {branch}")
    elif command == "tags":
        list_version_tags()
    elif command == "release":
        create_release_workflow()
    elif command == "tag":
        try:
            from version import get_version_info
            version_info = get_version_info()
            message = sys.argv[2] if len(sys.argv) > 2 else f"Release v{version_info['version']}"
            create_version_tag(version_info['version'], message)
        except ImportError:
            print("Could not load version information")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
