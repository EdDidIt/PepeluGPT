# PepeluGPT PowerShell Helper Script
# Windows equivalent of Makefile commands

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "🚀 PepeluGPT Development Commands" -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Basic Commands:" -ForegroundColor Yellow
    Write-Host "  .\make.ps1 run             - Launch PepeluGPT (interactive mode selection)"
    Write-Host "  .\make.ps1 status          - Show system status"
    Write-Host "  .\make.ps1 test            - Run CLI tests"
    Write-Host ""
    Write-Host "Mode Commands:" -ForegroundColor Yellow
    Write-Host "  .\make.ps1 mode-adaptive   - Launch in Adaptive mode"
    Write-Host "  .\make.ps1 mode-classic    - Launch in Classic mode"
    Write-Host ""
    Write-Host "Configuration:" -ForegroundColor Yellow
    Write-Host "  .\make.ps1 config-list     - List available configurations"
    Write-Host "  .\make.ps1 config-validate - Validate current configuration"
    Write-Host ""
    Write-Host "Security & Auditing:" -ForegroundColor Yellow
    Write-Host "  .\make.ps1 audit           - Run complete security audit"
    Write-Host "  .\make.ps1 audit-security  - Run security-only audit"
    Write-Host "  .\make.ps1 audit-config    - Run configuration audit"
    Write-Host "  .\make.ps1 audit-deps      - Run dependency audit"
    Write-Host "  .\make.ps1 audit-report    - Generate markdown audit report"
    Write-Host ""
    Write-Host "Development:" -ForegroundColor Yellow
    Write-Host "  .\make.ps1 debug           - Launch with debug logging"
    Write-Host "  .\make.ps1 clean           - Clean cache files"
    Write-Host "  .\make.ps1 install         - Install/update dependencies"
    Write-Host "  .\make.ps1 health-check    - Complete health check"
    Write-Host ""
}

function Invoke-Run {
    python main.py chat
}

function Invoke-Status {
    python main.py status
}

function Invoke-Test {
    if (Get-Command pytest -ErrorAction SilentlyContinue) {
        python -m pytest cli/test_cli.py -v
    } else {
        python cli/test_cli.py
    }
}

function Invoke-ModeAdaptive {
    python main.py chat --mode adaptive
}

function Invoke-ModeClassic {
    python main.py chat --mode classic
}

function Invoke-ConfigList {
    python main.py config list
}

function Invoke-ConfigValidate {
    python main.py config validate
}

function Invoke-Audit {
    python main.py audit --type all
}

function Invoke-AuditSecurity {
    python main.py audit --type security
}

function Invoke-AuditConfig {
    python main.py audit --type config
}

function Invoke-AuditDeps {
    python main.py audit --type dependencies
}

function Invoke-AuditReport {
    python main.py audit --type all --output markdown --save audit_report.md
    Write-Host "📄 Audit report saved to audit_report.md" -ForegroundColor Green
}

function Invoke-Debug {
    python main.py chat --debug
}

function Invoke-Clean {
    Write-Host "🧹 Cleaning cache files..." -ForegroundColor Yellow
    Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object { Remove-Item -Recurse -Force $_ }
    Get-ChildItem -Path . -Recurse -File -Name "*.pyc" | Remove-Item -Force
    Get-ChildItem -Path . -Recurse -File -Name "*.pyo" | Remove-Item -Force
    Write-Host "✅ Cache cleaned" -ForegroundColor Green
}

function Invoke-Install {
    Write-Host "📦 Installing/updating dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ Dependencies updated" -ForegroundColor Green
}

function Invoke-StatusJson {
    python main.py status --json
}

function Invoke-HealthCheck {
    Write-Host "🔍 PepeluGPT Health Check" -ForegroundColor Cyan
    Write-Host "========================" -ForegroundColor Cyan
    python main.py status
    Write-Host ""
    Write-Host "🧪 Testing CLI imports..." -ForegroundColor Yellow
    python -c "from cli.args import parse_args; print('✅ CLI modules OK')"
    Write-Host ""
    Write-Host "🔐 Running security audit..." -ForegroundColor Yellow
    python main.py audit --type security
    Write-Host ""
    Write-Host "✅ Health check complete!" -ForegroundColor Green
}

# Command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "run" { Invoke-Run }
    "status" { Invoke-Status }
    "test" { Invoke-Test }
    "mode-adaptive" { Invoke-ModeAdaptive }
    "mode-classic" { Invoke-ModeClassic }
    "config-list" { Invoke-ConfigList }
    "config-validate" { Invoke-ConfigValidate }
    "audit" { Invoke-Audit }
    "audit-security" { Invoke-AuditSecurity }
    "audit-config" { Invoke-AuditConfig }
    "audit-deps" { Invoke-AuditDeps }
    "audit-report" { Invoke-AuditReport }
    "debug" { Invoke-Debug }
    "clean" { Invoke-Clean }
    "install" { Invoke-Install }
    "status-json" { Invoke-StatusJson }
    "health-check" { Invoke-HealthCheck }
    default {
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Write-Host "Use '.\make.ps1 help' to see available commands." -ForegroundColor Yellow
        exit 1
    }
}
