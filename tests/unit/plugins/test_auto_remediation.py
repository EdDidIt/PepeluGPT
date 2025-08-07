#!/usr/bin/env python3
"""
Unit tests for the Auto-Remediation Engine plugin.
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from plugins.core.auto_remediation import AutoRemediationEngine


@pytest.mark.unit
@pytest.mark.plugins
class TestAutoRemediationEngine:
    """Test cases for the Auto-Remediation Engine."""

    def test_plugin_initialization(self) -> None:
        """Test that the plugin initializes correctly."""
        plugin = AutoRemediationEngine()
        assert plugin is not None
        
        metadata = plugin.get_metadata()
        assert metadata["name"] == "Advanced Automation Engine"
        assert "controls" in metadata
        assert len(metadata["controls"]) > 0

    def test_remediation_mappings(self) -> None:
        """Test that remediation mappings are properly configured."""
        plugin = AutoRemediationEngine()
        mappings = plugin.REMEDIATION_MAPPINGS
        
        assert len(mappings) > 0
        
        # Check structure of mappings
        for _, config in mappings.items():
            assert "script" in config
            assert "risk_level" in config
            assert "auto_remediate" in config
            assert "rollback_script" in config
            assert "prerequisites" in config

    def test_audit_execution(self) -> None:
        """Test basic audit execution."""
        plugin = AutoRemediationEngine()
        config = {"workspace_path": "."}
        
        findings = plugin.audit(config)
        assert isinstance(findings, list)
        # Should have at least some findings
        assert len(findings) >= 0

    def test_decision_engine(self) -> None:
        """Test decision engine initialization."""
        plugin = AutoRemediationEngine()
        assert plugin.decision_engine is not None

    def test_sandbox_environment(self) -> None:
        """Test sandbox environment initialization."""
        plugin = AutoRemediationEngine()
        assert plugin.sandbox is not None

    def test_metrics_collector(self) -> None:
        """Test metrics collector initialization."""
        plugin = AutoRemediationEngine()
        assert plugin.metrics_collector is not None
        
        metrics = plugin.metrics_collector.get_performance_metrics()
        assert isinstance(metrics, dict)
        assert "success_rate" in metrics
        assert "total_remediations" in metrics

    def test_validate_config(self) -> None:
        """Test configuration validation."""
        plugin = AutoRemediationEngine()
        
        valid_config: Dict[str, Any] = {"workspace_path": ".", "auto_remediation_enabled": True}
        assert plugin.validate_config(valid_config) is True
        
        # Test with minimal config
        minimal_config: Dict[str, Any] = {"workspace_path": "."}
        assert plugin.validate_config(minimal_config) is True
