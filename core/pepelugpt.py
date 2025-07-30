#!/usr/bin/env python3
"""
PepeluGPT - Cosmic Cybersecurity AI Assistant
Consolidated CLI with enhanced features and cosmic intelligence.

Usage:
    python pepelugpt.py setup        # Initial setup and parsing
    python pepelugpt.py chat         # Start interactive chat
    python pepelugpt.py status       # System health check
    python pepelugpt.py update       # Update vector database
    python pepelugpt.py test         # Run comprehensive tests
    python pepelugpt.py config       # Configuration management
    python pepelugpt.py version      # Version information
    python pepelugpt.py age          # Evolution journey
"""

import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Initialize Rich console for beautiful output
console = Console()
app = typer.Typer(
    name="pepelugpt",
    help="🤖 PepeluGPT - Cosmic Cybersecurity AI Assistant",
    add_completion=False,
    rich_markup_mode="rich"
)

class PepeluCore:
    """Enhanced core system manager."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the core system."""
        self.verbose = verbose
        self.core = None
        try:
            # Try to get existing core instance
            from core.orchestrator import get_core, initialize_pepelu_core
            self.core = get_core()
            if not self.core:
                if verbose:
                    console.print("🔧 Initializing PepeluGPT core system...", style="yellow")
                self.core = initialize_pepelu_core()
        except ImportError:
            if verbose:
                console.print("⚠️ Core module not available, using fallback", style="yellow")
        except Exception as e:
            if verbose:
                console.print(f"⚠️ Core initialization issue: {e}", style="yellow")
    
    from typing import Dict, Any

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status with fallback."""
        if self.core:
            return self.core.get_system_status()
        
        # Fallback status check
        return {
            "ready_for_chat": self._check_basic_readiness(),
            "environment_validation": {
                "documents_available": Path("cyber_documents").exists() and len(list(Path("cyber_documents").glob("*.*"))) > 0,
                "vector_db_ready": Path("cyber_vector_db").exists(),
                "dir_data": Path("data").exists() or Path("parsed_cyber_documents.json").exists(),
                "dir_logs": Path("logs").exists()
            }
        }
    
    def _check_basic_readiness(self) -> bool:
        """Basic readiness check."""
        return (Path("cyber_documents").exists() and 
                len(list(Path("cyber_documents").glob("*.*"))) > 0 and
                (Path("cyber_vector_db").exists() or Path("parsed_cyber_documents.json").exists()))

def display_cosmic_banner():
    """Display the enhanced cosmic banner."""
    try:
        from version.manager import get_version_banner
        console.print(get_version_banner())
    except ImportError:
        # Fallback cosmic banner
        banner = """
[bold cyan]🤖 PepeluGPT - Quantum-Secure Cybersecurity Assistant[/bold cyan]
[dim]   Your Cosmic Companion in the Digital Realm[/dim]
[bold]===========================================================[/bold]
        """
        console.print(Panel(banner, border_style="cyan"))


@app.command()
def setup(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    force: bool = typer.Option(False, "--force", "-f", help="Force rebuild even if data exists")
):
    """
    🚀 Initialize PepeluGPT with document parsing and vector database creation.
    
    This command sets up the entire system by:
    1. Validating environment and documents
    2. Parsing cybersecurity documents 
    3. Building the vector database for semantic search
    """
    console.print("\n[bold green]🚀 PepeluGPT Setup & Initialization[/bold green]")
    console.print("-" * 40)
    
    # Removed unused variable assignment to 'core'
    
    if not _validate_environment(verbose):
        raise typer.Exit(1)
    
    try:
        with console.status("[bold green]📄 Parsing cybersecurity documents..."):
            from processing.parse_all_documents import main as parse_main
            parse_main()
        console.print("✅ Document parsing completed", style="green")
        
        with console.status("[bold green]🧠 Building vector database..."):
            from storage.vector_db.builder import main as build_main
            build_main()
        console.print("✅ Vector database built", style="green")
        
        console.print("\n[bold green]🎉 Setup completed successfully![/bold green]")
        console.print("💡 Run: [bold cyan]python pepelugpt.py chat[/bold cyan]")
        
    except Exception as e:
        console.print(f"❌ Setup failed: {e}", style="red")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def chat(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    💬 Start the cosmic chat interface.
    
    Launch the interactive chat interface to communicate with PepeluGPT.
    The system will use either the cosmic interface or fall back to the standard chat.
    """
    try:
        # Try enhanced cosmic interface first
        try:
            from interface.cosmic_chat import main as cosmic_chat_main
            console.print("🚀 Initializing Cosmic Interface...", style="cyan")
            cosmic_chat_main()
        except ImportError:
            # Fallback to regular chat
            from interface.chat import main as chat_main
            console.print("🚀 Starting PepeluGPT Chat Interface...", style="cyan")
            chat_main()
    except Exception as e:
        console.print(f"❌ Chat interface error: {e}", style="red")
        if verbose:
            console.print_exception()
        console.print("💡 Try running: [bold cyan]python pepelugpt.py setup[/bold cyan]")
        raise typer.Exit(1)


@app.command()
def status(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    📊 Display comprehensive system status and health check.
    
    Shows the status of all system components including:
    - Document availability and count
    - Vector database status
    - Directory structure
    - Version information
    """
    console.print("\n[bold blue]📊 PepeluGPT System Status[/bold blue]")
    
    # Show version info if available
    try:
        from version.manager import get_version_info, get_build_age
        version_info = get_version_info()
        age_info = get_build_age()
        console.print(f"🔢 Version: {version_info['version']} \"{version_info['codename']}\" ({version_info['stage']})")
        console.print(f"🕰️ Age: {age_info['total_days']} days | Current Build: {age_info['current_version_days']} days")
    except ImportError:
        console.print("🔢 Version: PepeluGPT Cosmic Edition")
    
    console.print("-" * 50)
    
    # Get system status
    core = PepeluCore(verbose)
    status_data = core.get_system_status()
    validation = status_data.get("environment_validation", {})
    
    # Create status table
    table = Table(title="System Components")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Description", style="green")
    
    components = [
        ("Documents", validation.get("documents_available", False), "Cybersecurity documents"),
        ("Vector DB", validation.get("vector_db_ready", False), "Semantic search database"),
        ("Data Directory", validation.get("dir_data", False), "Parsed documents storage"),
        ("Logs Directory", validation.get("dir_logs", False), "System logs"),
    ]
    
    for component, is_ready, description in components:
        status_icon = "✅ Ready" if is_ready else "❌ Missing"
        status_style = "green" if is_ready else "red"
        table.add_row(component, f"[{status_style}]{status_icon}[/{status_style}]", description)
    
    console.print(table)
    
    # Overall readiness
    ready = status_data.get("ready_for_chat", False)
    if ready:
        console.print("\n[bold green]🟢 Overall Status: Ready for chat[/bold green]")
    else:
        console.print("\n[bold red]🔴 Overall Status: Setup required[/bold red]")
        console.print("💡 Run '[bold cyan]python pepelugpt.py setup[/bold cyan]' to initialize the system")
    
    # Additional verbose information
    if verbose:
        console.print("\n[bold yellow]📁 Directory Structure:[/bold yellow]")
        dirs_to_check = ["cyber_documents", "data", "logs", "cyber_vector_db", "processing", "interface"]
        for dir_name in dirs_to_check:
            dir_path = Path(dir_name)
            if dir_path.exists():
                file_count = len(list(dir_path.glob("*")))
                console.print(f"  ✅ {dir_name}/ ({file_count} items)")
            else:
                console.print(f"  ❌ {dir_name}/ (missing)")


@app.command()
def update(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    🔄 Update the vector database with new documents.
    
    Re-parses all documents and rebuilds the vector database.
    Use this when you've added new documents or want to refresh the system.
    """
    console.print("[bold yellow]🔄 Updating Vector Database...[/bold yellow]")
    
    try:
        with console.status("[bold yellow]📄 Re-parsing documents..."):
            from processing.parse_all_documents import main as parse_main
            parse_main()
        console.print("✅ Document parsing completed", style="green")
        
        with console.status("[bold yellow]🧠 Rebuilding vector database..."):
            from storage.vector_db.builder import main as build_main
            build_main()
        console.print("✅ Vector database rebuilt", style="green")
        
        console.print("\n[bold green]🎉 Update completed successfully![/bold green]")
        
    except Exception as e:
        console.print(f"❌ Update failed: {e}", style="red")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def test(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    🧪 Run comprehensive system tests and validation.
    
    Executes the test suite to validate system functionality and integrity.
    """
    console.print("[bold magenta]🧪 Running PepeluGPT Tests[/bold magenta]")
    console.print("-" * 30)
    
    try:
        # Try comprehensive tests first
        try:
            from tests.test_core import test_pepelugpt
            test_pepelugpt()
        except ImportError:
            # Fallback to basic tests
            from tests.test_system import test_pepelugpt
            test_pepelugpt()
    except Exception as e:
        console.print(f"❌ Tests failed: {e}", style="red")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def config(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    ⚙️ Display current system configuration.
    
    Shows all configuration settings including application, security, and model settings.
    """
    console.print("[bold blue]⚙️ PepeluGPT Configuration[/bold blue]")
    
    core = PepeluCore(verbose)
    
    if not core.core:
        console.print("❌ Core system not initialized", style="red")
        raise typer.Exit(1)
    
    # Create configuration table
    table = Table(title="Configuration Settings")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    # Key configuration items
    config_items = [
        ("Application Name", core.core.get_config("application.name", "PepeluGPT")),
        ("Version", core.core.get_config("application.version", "1.0.0")),
        ("Mode", core.core.get_config("application.mode", "local")),
        ("Embedding Model", core.core.get_config("vector_database.embedding_model", "N/A")),
        ("Chat Model", core.core.get_config("chat.model_name", "N/A")),
        ("Offline Mode", core.core.get_config("security.offline_mode", True)),
        ("Logging Level", core.core.get_config("logging.level", "INFO")),
    ]
    
    for setting, value in config_items:
        table.add_row(setting, str(value))
    
    console.print(table)


@app.command()
def version(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    🔢 Display comprehensive version and evolution information.
    
    Shows version details, build information, and cosmic evolution status.
    """
    try:
        from version.manager import get_version_command_output
        console.print(get_version_command_output())
    except ImportError:
        console.print("[bold cyan]🤖 PepeluGPT Version Information[/bold cyan]")
        console.print("Version: 0.3.1 'Quantum Guardian'")
        console.print("🌌 Cosmic evolution continues...")


@app.command()
def age(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    🕰️ Display PepeluGPT's age and evolution journey.
    
    Shows the cosmic journey and milestones in PepeluGPT's development.
    """
    console.print("\n[bold yellow]🕰️ PepeluGPT Evolution Journey[/bold yellow]")
    console.print("=" * 40)
    
    try:
        from version.manager import get_age_message, get_milestone_history
        age_message = get_age_message()
        console.print(f"\n{age_message}")
        console.print(get_milestone_history())
    except ImportError:
        console.print("\n🌟 PepeluGPT has been evolving since December 2024")
        console.print("📅 Each day brings new cosmic wisdom and stronger defenses")
    
    cosmic_wisdom = """
💫 Cosmic Wisdom:
  Each day brings new knowledge, deeper understanding,
  and stronger defenses against the digital darkness.
  The journey continues... 🌌
    """
    console.print(Panel(cosmic_wisdom, border_style="yellow", title="[bold]Cosmic Wisdom[/bold]"))


def _validate_environment(verbose: bool = False) -> bool:
    """Validate the environment setup."""
    # Check if cyber_documents exists
    if not Path("cyber_documents").exists():
        console.print("❌ cyber_documents/ folder not found!", style="red")
        console.print("   Please create this folder and add your cybersecurity documents.")
        return False
    
    # Check document count
    doc_count = len(list(Path("cyber_documents").glob("*.*")))
    if doc_count == 0:
        console.print("❌ No documents found in cyber_documents/", style="red")
        console.print("   Please add PDF, DOCX, XLSX, TXT, or other supported files.")
        return False
    
    if verbose:
        console.print(f"✅ Found {doc_count} documents to process", style="green")
    
    # Check if file_parser module exists
    if not Path("processing").exists():
        console.print("❌ processing/ module not found!", style="red")
        return False
    
    if verbose:
        console.print("✅ Environment validation passed", style="green")
    
    return True


def main():
    """Main entry point with cosmic enhancements."""
    try:
        # Display banner before processing commands
        if len(sys.argv) > 1 and sys.argv[1] not in ['--help', '-h']:
            display_cosmic_banner()
        
        app()
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]🌟 Cosmic journey interrupted. May your code be elegant and your security eternal![/bold yellow]")
    except Exception as e:
        console.print(f"\n❌ Cosmic disturbance detected: {e}", style="red")
        console.print("🔮 The oracle suggests checking your system configuration.")
        console.print("💡 Try: [bold cyan]python pepelugpt.py status[/bold cyan]")


if __name__ == "__main__":
    main()
