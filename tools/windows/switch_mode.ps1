# PepeluGPT Mode Switcher - PowerShell Script
# Quick mode switching utility for Windows

param(
    [Parameter(Position=0)]
    [ValidateSet("adaptive", "classic", "status", "interactive", "")]
    [string]$Mode = "",
    
    [switch]$Help
)

# Color functions for better output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    } else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Green { Write-ColorOutput Green $args }
function Write-Red { Write-ColorOutput Red $args }
function Write-Yellow { Write-ColorOutput Yellow $args }
function Write-Cyan { Write-ColorOutput Cyan $args }

# Help function
function Show-Help {
    Write-Cyan @"
🎯 PepeluGPT Mode Switcher

Usage:
  .\switch_mode.ps1 adaptive      # Switch to adaptive mode
  .\switch_mode.ps1 classic       # Switch to classic mode  
  .\switch_mode.ps1 status        # Show current mode
  .\switch_mode.ps1 interactive   # Interactive mode selection
  .\switch_mode.ps1 -Help         # Show this help

Quick Commands:
  python main.py --mode adaptive      # Start in adaptive mode
  python main.py --mode classic       # Start in classic mode
  python tools/mode_switcher.py -i    # Interactive mode switcher

Mode Benefits:
📚 Adaptive Mode:
  • Adaptive responses that improve with feedback
  • Personalized based on your corrections and ratings
  • Advanced learning capabilities with LLM integration

⚡ Deterministic Mode:
  • Fast, consistent, rule-based responses
  • Predictable and auditable output
  • No ML overhead, pure cybersecurity logic
"@
}

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Red "❌ Error: Not in PepeluGPT directory"
    Write-Yellow "💡 Please run this script from the PepeluGPT root directory"
    exit 1
}

# Handle help request
if ($Help -or $Mode -eq "help") {
    Show-Help
    exit 0
}

# If no mode specified, show current status and options
if ($Mode -eq "") {
    Write-Cyan "🎯 PepeluGPT Mode Switcher"
    Write-Output ""
    
    # Try to determine current mode
    try {
        $currentMode = python tools/mode_switcher.py --status 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Output $currentMode
        } else {
            Write-Yellow "⚠️  Could not determine current mode"
        }
    } catch {
        Write-Yellow "⚠️  Mode switcher not available"
    }
    
    Write-Output ""
    Write-Output "Available options:"
    Write-Output "  adaptive      - Switch to adaptive learning mode"
    Write-Output "  classic       - Switch to rule-based mode"
    Write-Output "  status        - Show detailed status"
    Write-Output "  interactive   - Interactive mode selection"
    Write-Output ""
    Write-Output "Use: .\switch_mode.ps1 <mode> or .\switch_mode.ps1 -Help"
    exit 0
}

# Execute mode switch
try {
    Write-Cyan "🔄 Processing mode switch to: $Mode"
    
    switch ($Mode) {
        "status" {
            python tools/mode_switcher.py --status
        }
        "interactive" {
            python tools/mode_switcher.py --interactive
        }
        "adaptive" {
            python tools/mode_switcher.py --mode adaptive
            if ($LASTEXITCODE -eq 0) {
                Write-Green "✅ Switched to adaptive mode"
                Write-Yellow "💡 Restart PepeluGPT or use: python main.py --mode adaptive"
            }
        }
        "classic" {
            python tools/mode_switcher.py --mode classic
            if ($LASTEXITCODE -eq 0) {
                Write-Green "✅ Switched to classic mode"
                Write-Yellow "💡 Restart PepeluGPT or use: python main.py --mode classic"
            }
        }
        default {
            Write-Red "❌ Invalid mode: $Mode"
            Write-Output "Valid modes: adaptive, classic, status, interactive"
            exit 1
        }
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Red "❌ Mode switch failed"
        Write-Yellow "💡 Try: python tools/mode_switcher.py --help"
        exit 1
    }
    
} catch {
    Write-Red "❌ Error: $($_.Exception.Message)"
    Write-Yellow "💡 Make sure Python and required dependencies are installed"
    exit 1
}
