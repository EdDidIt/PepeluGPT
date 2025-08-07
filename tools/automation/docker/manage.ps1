#!/usr/bin/env pwsh

# PepeluGPT Docker Management Script
# Security: No sensitive paths or credentials exposed

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "start", "stop", "restart", "logs", "shell", "clean", "dev", "prod", "status")]
    [string]$Action = "help",
    
    [switch]$Force,
    [switch]$Follow,
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

# Security: Validate we're in the correct directory
if (-not (Test-Path "docker-compose.yml")) {
    Write-Error "❌ Must run from PepeluGPT root directory (docker-compose.yml not found)"
    exit 1
}

# Security: Validate Docker is available
try {
    docker --version | Out-Null
    docker-compose --version | Out-Null
} catch {
    Write-Error "❌ Docker or Docker Compose not found. Please install Docker Desktop."
    exit 1
}

function Write-SecureLog {
    param([string]$Message, [string]$Color = "White")
    if (-not $Quiet) {
        Write-Host $Message -ForegroundColor $Color
    }
}

function Show-Help {
    Write-Host @"
🐳 PepeluGPT Docker Management

Usage: .\scripts\docker\manage.ps1 <action> [options]

Actions:
  build     - Build the Docker image
  start     - Start PepeluGPT in production mode
  stop      - Stop all containers
  restart   - Restart containers
  logs      - View container logs
  shell     - Open shell in running container
  clean     - Remove containers and images
  dev       - Start in development mode
  prod      - Start in production mode
  status    - Show container status

Options:
  -Force    - Force rebuild/restart
  -Follow   - Follow logs (tail -f)
  -Quiet    - Suppress output messages

Examples:
  .\scripts\docker\manage.ps1 build -Force
  .\scripts\docker\manage.ps1 dev
  .\scripts\docker\manage.ps1 logs -Follow
  .\scripts\docker\manage.ps1 status
"@
}

function Test-DockerSecurity {
    # Security: Check for sensitive files
    $sensitiveFiles = @(".env.docker", ".env", "docker-secrets")
    foreach ($file in $sensitiveFiles) {
        if (Test-Path $file) {
            Write-Warning "⚠️  Sensitive file detected: $file (ensure it's in .gitignore)"
        }
    }
    
    # Security: Verify .gitignore includes environment files
    if (Test-Path ".gitignore") {
        $gitignoreContent = Get-Content ".gitignore" -Raw
        if ($gitignoreContent -notmatch "\.env") {
            Write-Warning "⚠️  .gitignore may not exclude environment files"
        }
    }
}

function Build-Image {
    Write-SecureLog "🔨 Building PepeluGPT Docker image..." "Cyan"
    Test-DockerSecurity
    
    if ($Force) {
        docker-compose build --no-cache
    } else {
        docker-compose build
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-SecureLog "✅ Build completed successfully" "Green"
    } else {
        Write-Error "❌ Build failed"
    }
}

function Start-Production {
    Write-SecureLog "🚀 Starting PepeluGPT in production mode..." "Green"
    Test-DockerSecurity
    docker-compose -f docker-compose.yml up -d --remove-orphans
    Show-ContainerStatus
}

function Start-Development {
    Write-SecureLog "🛠️ Starting PepeluGPT in development mode..." "Yellow"
    Test-DockerSecurity
    docker-compose up -d --remove-orphans
    Show-ContainerStatus
}

function Stop-Containers {
    Write-SecureLog "⏹️ Stopping PepeluGPT containers..." "Red"
    docker-compose down
}

function Restart-Containers {
    Write-SecureLog "🔄 Restarting PepeluGPT..." "Blue"
    Stop-Containers
    Start-Production
}

function Show-Logs {
    Write-SecureLog "📋 Showing container logs..." "Magenta"
    if ($Follow) {
        docker-compose logs -f pepelugpt
    } else {
        docker-compose logs pepelugpt
    }
}

function Open-Shell {
    Write-SecureLog "🐚 Opening shell in PepeluGPT container..." "Magenta"
    
    # Security: Verify container is running
    $running = docker-compose ps -q pepelugpt
    if (-not $running) {
        Write-Error "❌ Container 'pepelugpt' is not running. Start it first."
        exit 1
    }
    
    docker-compose exec pepelugpt /bin/bash
}

function Show-ContainerStatus {
    Write-SecureLog "📊 Container Status:" "Cyan"
    docker-compose ps
}

function Remove-DockerResources {
    Write-SecureLog "🧹 Cleaning up Docker resources..." "DarkRed"
    Write-Host "⚠️  This will remove all containers, images, and volumes. Continue? (y/N): " -NoNewline
    $confirm = Read-Host
    
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        docker-compose down -v --rmi all
        docker system prune -f --volumes
        Write-SecureLog "✅ Cleanup completed" "Green"
    } else {
        Write-SecureLog "❌ Cleanup cancelled" "Yellow"
    }
}

# Main execution logic
switch ($Action) {
    "build" { Build-Image }
    "start" { Start-Production }
    "stop" { Stop-Containers }
    "restart" { Restart-Containers }
    "logs" { Show-Logs }
    "shell" { Open-Shell }
    "clean" { Remove-DockerResources }
    "dev" { Start-Development }
    "prod" { Start-Production }
    "status" { Show-ContainerStatus }
    default { Show-Help }
}
