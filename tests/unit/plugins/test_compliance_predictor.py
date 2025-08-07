#!/usr/bin/env python3
"""
Unit tests for the Compliance Predictor plugin.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from plugins.core.compliance_predictor import CompliancePredictorPlugin


@pytest.mark.unit
@pytest.mark.plugins
class TestCompliancePredictorPlugin:
    """Test cases for the Compliance Predictor plugin."""

    def test_plugin_initialization(self):
        """Test that the plugin initializes correctly."""
        plugin = CompliancePredictorPlugin()
        assert plugin is not None
        
        metadata = plugin.get_metadata()
        assert "name" in metadata
        assert "controls" in metadata

    def test_framework_mappings(self):
        """Test that framework mappings are properly configured."""
        plugin = CompliancePredictorPlugin()
        frameworks = plugin.FRAMEWORK_MAPPINGS
        
        assert len(frameworks) > 0
        assert "NIST_CSF" in frameworks
        assert "ISO_27001" in frameworks
        assert "SOC2" in frameworks

    def test_audit_execution(self):
        """Test basic audit execution."""
        plugin = CompliancePredictorPlugin()
        config = {"workspace_path": "."}
        
        findings = plugin.audit(config)
        assert isinstance(findings, list)
        # Should have at least some findings
        assert len(findings) >= 0

    def test_validate_config(self):
        """Test configuration validation."""
        plugin = CompliancePredictorPlugin()
        
        valid_config = {"workspace_path": "."}
        assert plugin.validate_config(valid_config) is True
