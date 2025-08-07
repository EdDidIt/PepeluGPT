# PepeluGPT PowerShell Utility Script
# Comprehensive development and organization commands for Windows

param(
    [Parameter(Position=0)]
    [ValidateSet("help", "status", "organize", "organize-dry", "plugins", "audit", "health", "create-plugin", "")]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$SubCommand = "",
    
    [Parameter(ValueFromRemainingArguments)]
    [string[]]$RemainingArgs
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
function Write-Blue { Write-ColorOutput Blue $args }

# Help function
function Show-Help {
    Write-Cyan "🚀 PepeluGPT PowerShell Commands"
    Write-Cyan "================================"
    Write-Output ""
    Write-Output "Basic Commands:"
    Write-Output "  .\pepelu.ps1 status          - Show system status"
    Write-Output "  .\pepelu.ps1 health          - Run comprehensive health check"
    Write-Output "  .\pepelu.ps1 audit           - Run security audit"
    Write-Output ""
    Write-Yellow "Phase 5.1 Organization:"
    Write-Output "  .\pepelu.ps1 organize-dry    - Preview workspace organization"  
    Write-Output "  .\pepelu.ps1 organize        - Execute workspace organization"
    Write-Output ""
    Write-Blue "Plugin Management:"
    Write-Output "  .\pepelu.ps1 plugins list    - Show registered plugins"
    Write-Output "  .\pepelu.ps1 plugins audit   - Run plugin-based audits"
    Write-Output ""
    Write-Green "Plugin Development:"
    Write-Output "  .\pepelu.ps1 create-plugin   - Generate new plugin template"
    Write-Output ""
    Write-Output "Examples:"
    Write-Output "  .\pepelu.ps1 organize-dry    # Preview changes"
    Write-Output "  .\pepelu.ps1 plugins list    # Show all plugins"
    Write-Output "  .\pepelu.ps1 audit          # Security scan"
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" {
        Show-Help
    }
    
    "status" {
        Write-Blue "📊 PepeluGPT Status"
        Write-Blue "==================="
        python main.py status
    }
    
    "organize-dry" {
        Write-Yellow "🧪 Phase 5.1: Organization Preview"
        Write-Yellow "=================================="
        python tools/automation/organize_project.py --dry-run
    }
    
    "organize" {
        Write-Green "🚀 Phase 5.1: Workspace Organization"
        Write-Green "===================================="
        python tools/automation/organize_project.py
    }
    
    "plugins" {
        if ($SubCommand -eq "list" -or $SubCommand -eq "") {
            Write-Blue "🔌 Plugin Management"
            Write-Blue "==================="
            python main.py plugins list
        } elseif ($SubCommand -eq "audit") {
            Write-Blue "🔌 Plugin-Based Audits"  
            Write-Blue "======================"
            python main.py plugins audit $RemainingArgs
        } else {
            Write-Green "🔌 Plugin Commands:"
            Write-Output "  plugins list     - Show registered plugins"
            Write-Output "  plugins audit    - Run plugin audits"
        }
    }
    
    "audit" {
        Write-Red "🔐 Security Audit"
        Write-Red "================="
        python main.py audit --type all
    }
    
    "health" {
        Write-Green "🔍 PepeluGPT Health Check"
        Write-Green "========================="
        python main.py status
        Write-Output ""
        Write-Output "🧪 Testing CLI modules..."
        try {
            python -c "from cli.args import parse_args; print('✅ CLI modules OK')"
        } catch {
            Write-Red "❌ CLI module issues detected"
        }
        Write-Output ""
        Write-Output "🔐 Running security audit..."
        python main.py audit --type security
        Write-Output ""
        Write-Green "✅ Health check complete!"
    }
    
    "create-plugin" {
        Write-Green "🔌 Plugin Template Generator"
        Write-Green "============================="
        python scripts/create_plugin_template.py
    }
    
    default {
        Write-Red "❌ Unknown command: $Command"
        Write-Output ""
        Show-Help
    }
}
