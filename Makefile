# PepeluGPT Makefile - Simplified Development Workflows
.PHONY: help run test test-unit test-integration test-core test-plugins test-demo test-coverage status config-list mode-adaptive mode-classic debug clean install install-learning organize organize-dry

# Default target
help:
	@echo "🚀 PepeluGPT Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install         - Install basic dependencies"
	@echo "  make install-learning - Install with ML learning features"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run all tests"
	@echo "  make test-unit       - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-core       - Run core functionality tests"
	@echo "  make test-plugins    - Run plugin tests"
	@echo "  make test-demo       - Run demo/showcase tests"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "Basic Commands:"
	@echo "  make run             - Launch PepeluGPT (interactive mode selection)"
	@echo "  make status          - Show system status"
	@echo ""
	@echo "Organization:"
	@echo "  make organize-dry    - Preview Phase 5.1 organization changes"
	@echo "  make organize        - Execute Phase 5.1 workspace organization"
	@echo ""
	@echo "Mode Commands:"
	@echo "  make mode-adaptive   - Launch in Adaptive mode"
	@echo "  make mode-classic    - Launch in Classic mode"
	@echo ""
	@echo "Configuration:"
	@echo "  make config-list     - List available configurations"
	@echo "  make config-validate - Validate current configuration"
	@echo ""
	@echo "Security & Auditing:"
	@echo "  make audit           - Run complete security audit"
	@echo "  make audit-security  - Run security-only audit"
	@echo "  make audit-config    - Run configuration audit"
	@echo "  make audit-deps      - Run dependency audit"
	@echo ""
	@echo "Development:"
	@echo "  make debug           - Launch with debug logging"
	@echo "  make clean           - Clean cache files"
	@echo "  make install         - Install/update dependencies"
	@echo ""

# Installation commands
install:
	@echo "📦 Installing PepeluGPT dependencies..."
	poetry install
	@echo "✅ Installation complete!"

install-learning:
	@echo "🧠 Installing with ML learning features..."
	poetry install --extras learning
	@echo "✅ Installation with learning features complete!"

# Basic launcher
run:
	@echo "🚀 Launching PepeluGPT..."
	poetry run python main.py chat

# Show system status
status:
	@echo "📊 System Status:"
	poetry run python main.py status

# Run tests
test:
	@echo "🧪 Running all tests..."
	poetry run python tests/run_tests.py --all

test-unit:
	@echo "🧪 Running unit tests..."
	poetry run python tests/run_tests.py --unit

test-integration:
	@echo "🧪 Running integration tests..."
	poetry run python tests/run_tests.py --integration

test-core:
	@echo "🧪 Running core functionality tests..."
	poetry run pytest tests/unit/core/ -v

test-plugins:
	@echo "🧪 Running plugin tests..."
	poetry run pytest tests/unit/plugins/ -v

test-demo:
	@echo "🧪 Running demo/showcase tests..."
	poetry run python tests/run_tests.py --demo

test-coverage:
	@echo "🧪 Running tests with coverage report..."
	poetry run pytest --cov=. --cov-report=html --cov-report=term tests/

# Mode-specific launchers
mode-adaptive:
	@echo "🎯 Launching in Adaptive mode..."
	poetry run python main.py chat --mode adaptive

mode-classic:
	@echo "🎯 Launching in Classic mode..."
	poetry run python main.py chat --mode classic

# Configuration commands
config-list:
	python main.py config list

config-validate:
	python main.py config validate

# Security audit commands
audit:
	python main.py audit --type all

audit-security:
	python main.py audit --type security

audit-config:
	python main.py audit --type config

audit-deps:
	python main.py audit --type dependencies

audit-report:
	python main.py audit --type all --output markdown --save audit_report.md
	@echo "📄 Audit report saved to audit_report.md"

# Development commands
debug:
	python main.py chat --debug

# Maintenance
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Cache cleaned"

# JSON status output (useful for scripts)
status-json:
	python main.py status --json

# Quick health check
health-check:
	@echo "🔍 PepeluGPT Health Check"
	@echo "========================"
	@python main.py status
	@echo ""
	@echo "🧪 Testing CLI imports..."
	@python -c "from cli.args import parse_args; print('✅ CLI modules OK')"
	@echo ""
	@echo "🔐 Running security audit..."
	@python main.py audit --type security
	@echo ""
	@echo "✅ Health check complete!"

# Phase 5.1: Project Organization
organize-dry:
	@echo "🧪 Phase 5.1: Dry Run Preview"
	@echo "============================="
	@python scripts/organize_project.py --dry-run

organize:
	@echo "🚀 Phase 5.1: Workspace Organization"
	@echo "==================================="
	@python scripts/organize_project.py
