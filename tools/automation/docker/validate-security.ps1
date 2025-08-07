#!/usr/bin/env pwsh

# PepeluGPT Docker Security Validation Script

Write-Host "🔒 PepeluGPT Docker Security Validation" -ForegroundColor Cyan
Write-Host "=" * 50

$securityIssues = @()

# Check 1: Verify .gitignore excludes environment files
Write-Host "`n📋 Checking .gitignore configuration..." -ForegroundColor Yellow

if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    
    $requiredExclusions = @(".env", ".env.docker", "*.env")
    foreach ($exclusion in $requiredExclusions) {
        if ($gitignoreContent -notmatch [regex]::Escape($exclusion)) {
            $securityIssues += "❌ .gitignore missing exclusion: $exclusion"
        } else {
            Write-Host "✅ .gitignore excludes: $exclusion" -ForegroundColor Green
        }
    }
} else {
    $securityIssues += "❌ .gitignore file not found"
}

# Check 2: Verify sensitive files are not tracked by Git
Write-Host "`n📋 Checking for tracked sensitive files..." -ForegroundColor Yellow

$sensitiveFiles = @(".env", ".env.docker", ".env.local", ".env.production")
foreach ($file in $sensitiveFiles) {
    if (Test-Path $file) {
        $gitStatus = git ls-files $file 2>$null
        if ($gitStatus) {
            $securityIssues += "❌ Sensitive file tracked by Git: $file"
        } else {
            Write-Host "✅ Sensitive file properly excluded: $file" -ForegroundColor Green
        }
    }
}

# Check 3: Verify template file exists
Write-Host "`n📋 Checking for template files..." -ForegroundColor Yellow

if (Test-Path ".env.docker.template") {
    Write-Host "✅ Environment template file exists" -ForegroundColor Green
    
    # Check template doesn't contain real secrets
    $templateContent = Get-Content ".env.docker.template" -Raw
    if ($templateContent -match "password|secret|key|token" -and $templateContent -notmatch "TEMPLATE|EXAMPLE") {
        $securityIssues += "⚠️  Template file may contain real secrets"
    }
} else {
    $securityIssues += "⚠️  .env.docker.template file not found"
}

# Check 4: Verify Docker files don't contain secrets
Write-Host "`n📋 Checking Docker files for hardcoded secrets..." -ForegroundColor Yellow

$dockerFiles = @("Dockerfile", "docker-compose.yml", "docker-compose.override.yml")
foreach ($file in $dockerFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match "password|secret|apikey|token" -and $content -notmatch "ENV|ARG|\$") {
            $securityIssues += "❌ Potential hardcoded secret in: $file"
        } else {
            Write-Host "✅ No hardcoded secrets in: $file" -ForegroundColor Green
        }
    }
}

# Check 5: Verify management script permissions
Write-Host "`n📋 Checking management script security..." -ForegroundColor Yellow

if (Test-Path "scripts/docker/manage.ps1") {
    $scriptContent = Get-Content "scripts/docker/manage.ps1" -Raw
    
    # Check for security features
    if ($scriptContent -match "Test-DockerSecurity") {
        Write-Host "✅ Management script includes security checks" -ForegroundColor Green
    } else {
        $securityIssues += "⚠️  Management script missing security checks"
    }
    
    # Check for confirmation prompts on destructive operations
    if ($scriptContent -match "Continue\?\s*\(y/N\)") {
        Write-Host "✅ Management script has confirmation prompts" -ForegroundColor Green
    } else {
        $securityIssues += "⚠️  Management script missing confirmation prompts"
    }
} else {
    $securityIssues += "❌ Management script not found"
}

# Summary
Write-Host "`n" + "=" * 50
if ($securityIssues.Count -eq 0) {
    Write-Host "🎉 All security checks passed!" -ForegroundColor Green
    Write-Host "Your PepeluGPT Docker setup is secure." -ForegroundColor Green
} else {
    Write-Host "⚠️  Security issues found:" -ForegroundColor Red
    foreach ($issue in $securityIssues) {
        Write-Host "  $issue" -ForegroundColor Red
    }
    Write-Host "`nPlease address these issues before deployment." -ForegroundColor Yellow
}

Write-Host "`n📚 For more information, see docs/SECURITY.md" -ForegroundColor Cyan
