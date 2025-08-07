#!/usr/bin/env python3
"""
Advanced Automation Engine for PepeluGPT
Self-healing cybersecurity with intelligent auto-remediation
"""

import json
import logging
import os
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging for automation engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add plugins directory to path for imports
current_dir = Path(__file__).parent
plugins_dir = current_dir.parent
root_dir = plugins_dir.parent
sys.path.insert(0, str(root_dir))

from plugins.base import AuditPlugin, PluginFinding, PluginSeverity, create_finding  # type: ignore


class RemediationAction(Enum):
    """Remediation action types"""

    AUTO_EXECUTE = "auto_execute"  # Execute immediately
    HUMAN_REVIEW = "human_review"  # Flag for manual review
    SCHEDULE_LATER = "schedule_later"  # Schedule for future execution
    SIMULATE_ONLY = "simulate_only"  # Test mode only
    ROLLBACK = "rollback"  # Undo previous action


class RemediationStatus(Enum):
    """Remediation execution status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    HUMAN_REQUIRED = "human_required"


@dataclass
class RemediationPlan:
    """Remediation execution plan"""

    finding_id: str
    action_type: RemediationAction
    script_path: str
    estimated_time: float
    risk_level: str
    prerequisites: List[str]
    rollback_script: Optional[str] = None
    timeout: int = 300
    dry_run: bool = True


@dataclass
class RemediationResult:
    """Remediation execution result"""

    plan: Optional[RemediationPlan]
    status: RemediationStatus
    execution_time: float
    output: str
    error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = field(default_factory=dict)  # type: ignore


class AutoRemediationEngine(AuditPlugin):
    """
    Advanced automation engine for intelligent auto-remediation.

    Capabilities:
    - Intelligent remediation decision making
    - Sandboxed remediation execution
    - Rollback and recovery mechanisms
    - Performance and success metrics
    - Extensible remediation plugin architecture
    """

    # Remediation action mappings
    REMEDIATION_MAPPINGS: Dict[str, Dict[str, Any]] = {
        # Security Configuration Issues
        "unencrypted_backup": {
            "script": "scripts/remediation/encrypt_backup.py",
            "risk_level": "medium",
            "auto_remediate": True,
            "rollback_script": "scripts/remediation/decrypt_backup.py",
            "prerequisites": ["backup_tools", "encryption_keys"],
        },
        "weak_password_policy": {
            "script": "scripts/remediation/strengthen_password_policy.py",
            "risk_level": "high",
            "auto_remediate": False,  # Requires human review
            "rollback_script": "scripts/remediation/restore_password_policy.py",
            "prerequisites": ["policy_admin"],
        },
        "exposed_service": {
            "script": "scripts/remediation/secure_service.py",
            "risk_level": "critical",
            "auto_remediate": True,
            "rollback_script": "scripts/remediation/restore_service.py",
            "prerequisites": ["service_admin", "firewall_access"],
        },
        # Compliance Issues
        "missing_documentation": {
            "script": "scripts/remediation/generate_documentation.py",
            "risk_level": "low",
            "auto_remediate": True,
            "rollback_script": "scripts/remediation/remove_generated_docs.py",
            "prerequisites": ["template_access"],
        },
        "outdated_policy": {
            "script": "scripts/remediation/update_policy.py",
            "risk_level": "medium",
            "auto_remediate": False,
            "rollback_script": "scripts/remediation/restore_policy_version.py",
            "prerequisites": ["policy_admin", "legal_review"],
        },
        # Infrastructure Issues
        "unpatched_system": {
            "script": "scripts/remediation/apply_security_patches.py",
            "risk_level": "high",
            "auto_remediate": False,  # Requires maintenance window
            "rollback_script": "scripts/remediation/rollback_patches.py",
            "prerequisites": ["patch_admin", "maintenance_window"],
        },
        "misconfigured_firewall": {
            "script": "scripts/remediation/fix_firewall_config.py",
            "risk_level": "critical",
            "auto_remediate": True,
            "rollback_script": "scripts/remediation/restore_firewall_config.py",
            "prerequisites": ["firewall_admin", "config_backup"],
        },
        # Development Security
        "hardcoded_secrets": {
            "script": "scripts/remediation/remove_hardcoded_secrets.py",
            "risk_level": "critical",
            "auto_remediate": True,
            "rollback_script": "scripts/remediation/restore_secrets_file.py",
            "prerequisites": ["code_access", "secret_manager"],
        },
        "insecure_dependencies": {
            "script": "scripts/remediation/update_dependencies.py",
            "risk_level": "high",
            "auto_remediate": True,
            "rollback_script": "scripts/remediation/rollback_dependencies.py",
            "prerequisites": ["package_manager", "dependency_scanner"],
        },
    }

    def __init__(self):
        super().__init__()
        self.remediation_history: List[RemediationResult] = []
        self.active_remediations: Dict[str, RemediationResult] = {}
        self.decision_engine = RemediationDecisionEngine()
        self.sandbox = RemediationSandbox()
        self.metrics_collector = AutomationMetrics()

        # Ensure remediation directories exist
        self._setup_remediation_environment()

    def get_metadata(self) -> Dict[str, Any]:
        """Return automation engine metadata"""
        return {
            "name": "Advanced Automation Engine",
            "version": "1.0.0",
            "framework": "AUTO-REMEDIATION",
            "description": "Intelligent auto-remediation engine with sandboxed execution and rollback capabilities",
            "author": "PepeluGPT Automation Team",
            "controls": ["AUTO-001", "AUTO-002", "AUTO-003", "AUTO-004", "AUTO-005"],
            "requirements": ["decision_engine", "sandbox", "rollback_capability"],
            "categories": ["automation", "remediation", "self_healing", "response"],
            "supported_actions": list(self.REMEDIATION_MAPPINGS.keys()),
        }

    @property
    def metadata(self):
        """Property accessor for metadata (for CLI compatibility)"""

        class MetadataObject:
            def __init__(self, data: Dict[str, Any]) -> None:
                for key, value in data.items():
                    setattr(self, key, value)

        return MetadataObject(self.get_metadata())

    def audit(self, config: Dict[str, Any]) -> List[PluginFinding]:
        """Execute automation engine analysis and remediation"""
        findings = []
        workspace_path = config.get("workspace_path", ".")

        # AUTO-001: Remediation Opportunity Analysis
        findings.extend(self._analyze_remediation_opportunities(workspace_path, config))  # type: ignore

        # AUTO-002: Active Remediation Status
        findings.extend(self._report_active_remediations(workspace_path, config))  # type: ignore

        # AUTO-003: Automation Engine Performance
        findings.extend(self._assess_automation_performance(workspace_path, config))  # type: ignore

        # AUTO-004: Self-Healing Capabilities Assessment
        findings.extend(self._evaluate_self_healing_status(workspace_path, config))  # type: ignore

        # AUTO-005: Remediation Recommendations
        findings.extend(  # type: ignore
            self._generate_automation_recommendations(workspace_path, config)
        )

        return findings  # type: ignore

    def execute_remediation(
        self, finding: PluginFinding, mode: str = "auto"
    ) -> RemediationResult:
        """Execute remediation for a specific finding"""
        # Create remediation plan
        plan = self._create_remediation_plan(finding, mode)
        if not plan:
            return RemediationResult(
                plan=None,
                status=RemediationStatus.FAILED,
                execution_time=0.0,
                output="",
                error="No remediation plan available for finding",
            )

        # Decision engine evaluation
        decision = self.decision_engine.evaluate_remediation(finding, plan)
        if decision != RemediationAction.AUTO_EXECUTE:
            return RemediationResult(
                plan=plan,
                status=RemediationStatus.HUMAN_REQUIRED,
                execution_time=0.0,
                output="",
                error=f"Decision engine requires: {decision.value}",
            )

        # Execute in sandbox
        return self.sandbox.execute_remediation(plan)

    def _analyze_remediation_opportunities(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[PluginFinding]:
        """AUTO-001: Analyze available remediation opportunities"""
        findings = []

        # Get findings from other plugins (AI Intelligence, Compliance Predictor)
        external_findings = self._get_external_findings(workspace_path)

        remediable_count = 0
        auto_remediable_count = 0
        critical_remediable_count = 0

        for finding in external_findings:
            finding_type = self._classify_finding_for_remediation(finding)
            if finding_type in self.REMEDIATION_MAPPINGS:
                remediable_count += 1
                mapping = self.REMEDIATION_MAPPINGS[finding_type]

                if mapping.get("auto_remediate", False):
                    auto_remediable_count += 1

                if finding.severity == PluginSeverity.CRITICAL:
                    critical_remediable_count += 1

        if remediable_count > 0:
            findings.append(  # type: ignore
                create_finding(
                    id="AUTO-001.1",
                    title=f"Remediation Opportunities: {remediable_count} Available",
                    description=f"Found {remediable_count} remediable findings ({auto_remediable_count} auto-remediable, {critical_remediable_count} critical)",
                    severity=(
                        PluginSeverity.INFO
                        if critical_remediable_count == 0
                        else PluginSeverity.MEDIUM
                    ),
                    category="remediation_analysis",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-001",
                    remediation="Review remediation opportunities and configure automation preferences",
                    metadata={
                        "total_remediable": remediable_count,
                        "auto_remediable": auto_remediable_count,
                        "critical_remediable": critical_remediable_count,
                        "automation_coverage": (
                            (auto_remediable_count / remediable_count * 100)
                            if remediable_count > 0
                            else 0
                        ),
                    },
                )
            )

        return findings  # type: ignore

    def _report_active_remediations(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[PluginFinding]:
        """AUTO-002: Report status of active remediations"""
        findings = []

        active_count = len(self.active_remediations)
        if active_count > 0:
            findings.append(  # type: ignore
                create_finding(
                    id="AUTO-002.1",
                    title=f"Active Remediations: {active_count} In Progress",
                    description=f"Currently executing {active_count} remediation actions",
                    severity=PluginSeverity.INFO,
                    category="active_remediation",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-002",
                    remediation="Monitor active remediation progress and handle any failures",
                    metadata={
                        "active_count": active_count,
                        "active_remediations": list(self.active_remediations.keys()),
                    },
                )
            )

        # Check for failed remediations
        failed_count = len(
            [
                r
                for r in self.remediation_history
                if r.status == RemediationStatus.FAILED
            ]
        )
        if failed_count > 0:
            findings.append(  # type: ignore
                create_finding(
                    id="AUTO-002.2",
                    title=f"Failed Remediations: {failed_count} Require Attention",
                    description=f"Found {failed_count} failed remediation attempts requiring manual intervention",
                    severity=PluginSeverity.MEDIUM,
                    category="failed_remediation",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-002",
                    remediation="Review failed remediations and implement manual fixes or improve automation",
                    metadata={
                        "failed_count": failed_count,
                        "failure_rate": (
                            (failed_count / len(self.remediation_history) * 100)
                            if self.remediation_history
                            else 0
                        ),
                    },
                )
            )

        return findings  # type: ignore

    def _assess_automation_performance(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[PluginFinding]:
        """AUTO-003: Assess automation engine performance metrics"""
        findings = []

        metrics = self.metrics_collector.get_performance_metrics()

        success_rate = metrics.get("success_rate", 0.0)
        avg_execution_time = metrics.get("avg_execution_time", 0.0)
        total_remediations = metrics.get("total_remediations", 0)

        if total_remediations > 0:
            # Determine severity based on success rate
            if success_rate >= 90:
                severity = PluginSeverity.INFO
                title = "Automation Performance: Excellent"
            elif success_rate >= 75:
                severity = PluginSeverity.LOW
                title = "Automation Performance: Good"
            elif success_rate >= 50:
                severity = PluginSeverity.MEDIUM
                title = "Automation Performance: Needs Improvement"
            else:
                severity = PluginSeverity.HIGH
                title = "Automation Performance: Poor"

            findings.append(  # type: ignore
                create_finding(
                    id="AUTO-003.1",
                    title=title,
                    description=f"Automation engine shows {success_rate:.1f}% success rate over {total_remediations} remediations (avg: {avg_execution_time:.1f}s)",
                    severity=severity,
                    category="automation_performance",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-003",
                    remediation=self._generate_performance_remediation(success_rate),
                    metadata=metrics,
                )
            )

        return findings  # type: ignore

    def _evaluate_self_healing_status(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[PluginFinding]:
        """AUTO-004: Evaluate self-healing capabilities"""
        findings = []

        # Check self-healing configuration
        self_healing_enabled = config.get("auto_remediation_enabled", False)
        risk_tolerance = config.get("auto_remediation_risk_tolerance", "low")

        if not self_healing_enabled:
            findings.append(  # type: ignore
                create_finding(
                    id="AUTO-004.1",
                    title="Self-Healing Disabled",
                    description="Automation engine is in monitoring mode only. Self-healing capabilities are disabled.",
                    severity=PluginSeverity.INFO,
                    category="self_healing_status",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-004",
                    remediation="Enable auto-remediation in configuration to activate self-healing capabilities",
                    metadata={
                        "self_healing_enabled": False,
                        "risk_tolerance": risk_tolerance,
                        "recommendation": "enable_controlled_auto_remediation",
                    },
                )
            )
        else:
            # Evaluate self-healing effectiveness
            healing_metrics = self._calculate_self_healing_metrics()
            findings.append(  # type: ignore
                create_finding(
                    id="AUTO-004.2",
                    title=f"Self-Healing Active: {healing_metrics['healing_rate']:.1f}% Effective",
                    description=f"Self-healing system is operational with {risk_tolerance} risk tolerance",
                    severity=PluginSeverity.INFO,
                    category="self_healing_status",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-004",
                    remediation="Monitor self-healing effectiveness and adjust risk tolerance as needed",
                    metadata=healing_metrics,
                )
            )

        return findings  # type: ignore

    def _generate_automation_recommendations(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[PluginFinding]:
        """AUTO-005: Generate automation improvement recommendations"""
        findings = []

        recommendations = self._compute_automation_recommendations(
            workspace_path, config
        )

        for rec in recommendations:
            findings.append(  # type: ignore
                create_finding(
                    id=f"AUTO-005.{rec['id']}",
                    title=f"Automation Recommendation: {rec['title']}",
                    description=rec["description"],
                    severity=PluginSeverity.INFO,
                    category="automation_recommendations",
                    framework="AUTO-REMEDIATION",
                    control="AUTO-005",
                    remediation=rec["implementation"],
                    metadata={
                        "recommendation_type": rec["type"],
                        "priority": rec["priority"],
                        "effort_estimate": rec["effort"],
                        "expected_impact": rec["impact"],
                        "automation_level": rec.get("automation_level", "manual"),
                    },
                )
            )

        return findings  # type: ignore

    # Helper Methods

    def _setup_remediation_environment(self) -> None:
        """Setup remediation directories and scripts"""
        remediation_dirs = [
            Path("scripts/remediation"),
            Path("logs/remediation"),
            Path("backups/remediation"),
            Path("configs/remediation"),
        ]

        for directory in remediation_dirs:
            directory.mkdir(parents=True, exist_ok=True)

    def _get_external_findings(self, workspace_path: str) -> List[PluginFinding]:
        """Get findings from other plugins for remediation analysis"""
        # Mock implementation - would integrate with plugin registry
        return []

    def _classify_finding_for_remediation(self, finding: PluginFinding) -> str:
        """Classify finding to determine remediation type"""
        description = finding.description.lower()

        # Pattern matching for remediation classification
        if "backup" in description and "encrypt" in description:
            return "unencrypted_backup"
        elif "password" in description and (
            "weak" in description or "policy" in description
        ):
            return "weak_password_policy"
        elif "service" in description and "exposed" in description:
            return "exposed_service"
        elif "documentation" in description and "missing" in description:
            return "missing_documentation"
        elif "secret" in description and (
            "hardcoded" in description or "embedded" in description
        ):
            return "hardcoded_secrets"
        elif "dependencies" in description and (
            "vulnerable" in description or "outdated" in description
        ):
            return "insecure_dependencies"

        return "unknown"

    def _create_remediation_plan(
        self, finding: PluginFinding, mode: str
    ) -> Optional[RemediationPlan]:
        """Create remediation plan for finding"""
        finding_type = self._classify_finding_for_remediation(finding)
        if finding_type not in self.REMEDIATION_MAPPINGS:
            return None

        mapping = self.REMEDIATION_MAPPINGS[finding_type]

        return RemediationPlan(
            finding_id=finding.id,
            action_type=(
                RemediationAction.AUTO_EXECUTE
                if mode == "auto"
                else RemediationAction.HUMAN_REVIEW
            ),
            script_path=mapping["script"],
            estimated_time=30.0,  # Default estimate
            risk_level=mapping["risk_level"],
            prerequisites=mapping["prerequisites"],
            rollback_script=mapping.get("rollback_script"),
            dry_run=(mode != "execute"),
        )

    def _calculate_self_healing_metrics(self) -> Dict[str, Any]:
        """Calculate self-healing effectiveness metrics"""
        if not self.remediation_history:
            return {
                "healing_rate": 0.0,
                "avg_healing_time": 0.0,
                "critical_issues_healed": 0,
                "total_healing_attempts": 0,
            }

        successful_remediations = [
            r for r in self.remediation_history if r.status == RemediationStatus.SUCCESS
        ]
        healing_rate = (
            len(successful_remediations) / len(self.remediation_history)
        ) * 100

        avg_healing_time = (
            sum(r.execution_time for r in successful_remediations)
            / len(successful_remediations)
            if successful_remediations
            else 0.0
        )

        return {
            "healing_rate": healing_rate,
            "avg_healing_time": avg_healing_time,
            "critical_issues_healed": len(
                [
                    r
                    for r in successful_remediations
                    if r.plan and r.plan.risk_level == "critical"
                ]
            ),
            "total_healing_attempts": len(self.remediation_history),
        }

    def _compute_automation_recommendations(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate automation improvement recommendations"""
        return [
            {
                "id": 1,
                "title": "Implement Gradual Automation Rollout",
                "description": "Start with low-risk remediations to build confidence in automation engine",
                "type": "risk_management",
                "priority": "high",
                "effort": "2-3 weeks",
                "impact": "enables_safe_automation",
                "implementation": "Begin with documentation and configuration fixes, gradually expand to infrastructure changes",
            },
            {
                "id": 2,
                "title": "Enhanced Decision Engine",
                "description": "Implement ML-based decision making for more intelligent remediation choices",
                "type": "intelligence_upgrade",
                "priority": "medium",
                "effort": "4-6 weeks",
                "impact": "improved_automation_accuracy",
                "automation_level": "advanced",
                "implementation": "Integrate machine learning models to analyze historical remediation success patterns",
            },
        ]

    def _generate_performance_remediation(self, success_rate: float) -> str:
        """Generate performance-based remediation advice"""
        if success_rate >= 90:
            return "Excellent automation performance. Continue monitoring and consider expanding automation scope."
        elif success_rate >= 75:
            return "Good automation performance. Investigate failed remediations to improve success rate."
        elif success_rate >= 50:
            return "Moderate automation performance. Review remediation scripts and decision engine logic."
        else:
            return "Poor automation performance. Conduct comprehensive review of automation engine and disable high-risk automated actions."

    def pre_audit_setup(self, workspace_path: str, config: Dict[str, Any]) -> bool:
        """Automation engine pre-audit setup."""
        print(
            f"🤖 Automation Engine: Initializing remediation analysis for {workspace_path}"
        )
        return True

    def post_audit_cleanup(self, workspace_path: str, config: Dict[str, Any]) -> None:
        """Automation engine post-audit cleanup."""
        print(
            f"🤖 Automation Engine: Remediation analysis complete for {workspace_path}"
        )

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate automation engine configuration."""
        return True


class RemediationDecisionEngine:
    """Intelligent decision engine for remediation actions"""

    def __init__(self):
        """Initialize decision engine with risk matrices"""
        self.risk_matrix = {
            ("critical", "CRITICAL"): RemediationAction.HUMAN_REVIEW,
            ("critical", "HIGH"): RemediationAction.HUMAN_REVIEW,
            ("high", "CRITICAL"): RemediationAction.HUMAN_REVIEW,
            ("high", "HIGH"): RemediationAction.SCHEDULE_LATER,
            ("medium", "MEDIUM"): RemediationAction.AUTO_EXECUTE,
            ("low", "LOW"): RemediationAction.AUTO_EXECUTE,
            ("low", "INFO"): RemediationAction.AUTO_EXECUTE,
        }

    def evaluate_remediation(
        self, finding: PluginFinding, plan: RemediationPlan
    ) -> RemediationAction:
        """Evaluate whether to auto-remediate, require human review, or schedule"""
        # Dry run override
        if plan.dry_run:
            return RemediationAction.SIMULATE_ONLY

        # Check prerequisites
        if not self._check_prerequisites(plan.prerequisites):
            return RemediationAction.HUMAN_REVIEW

        # Risk-based decision matrix
        risk_key = (plan.risk_level, finding.severity.name)
        decision = self.risk_matrix.get(risk_key, RemediationAction.HUMAN_REVIEW)

        return decision

    def _check_prerequisites(self, prerequisites: List[str]) -> bool:
        """Check if all prerequisites are met"""
        # Simplified prerequisite check - in production, this would
        # verify actual system capabilities and permissions
        required_perms = [
            "backup_tools",
            "encryption_keys",
            "policy_admin",
            "service_admin",
            "firewall_access",
        ]
        return all(req in required_perms for req in prerequisites)


class RemediationSandbox:
    """Sandboxed execution environment for remediations"""

    def __init__(self):
        """Initialize sandbox with security constraints"""
        self.allowed_script_dirs = [
            Path("scripts/remediation").resolve(),
            Path("tools/remediation").resolve(),
        ]

    def _validate_script_path(self, script_path: str) -> bool:
        """Validate script path for security"""
        try:
            path = Path(script_path).resolve()

            # Must be a Python file
            if path.suffix != ".py":
                logger.warning(f"Invalid file extension: {path.suffix}")
                return False

            # Must be in allowed directories
            for allowed_dir in self.allowed_script_dirs:
                try:
                    # Check if path is within allowed directory
                    relative_path = path.relative_to(allowed_dir)
                    # Additional check: ensure no parent directory traversal
                    if ".." in str(relative_path):
                        logger.warning(f"Path traversal detected: {relative_path}")
                        return False
                    logger.info(f"Valid path found in {allowed_dir}: {relative_path}")
                    return True
                except ValueError:
                    # Path is not under this allowed directory, try next
                    continue

            logger.warning(f"Path not in allowed directories: {path}")
            return False

        except Exception as e:
            logger.error(f"Path validation error: {e}")
            return False

    def execute_remediation(self, plan: RemediationPlan) -> RemediationResult:
        """Execute remediation in sandboxed environment with enhanced error handling"""
        start_time = time.time()

        try:
            # Validate script path for security
            if not self._validate_script_path(plan.script_path):
                logger.error(f"Invalid script path: {plan.script_path}")
                raise ValueError(f"Invalid or unsafe script path: {plan.script_path}")

            if plan.dry_run:
                # Simulate execution
                output = f"DRY RUN: Would execute {plan.script_path}"
                status = RemediationStatus.SUCCESS
                error = None
                logger.info(f"Dry run executed for {plan.script_path}")
            else:
                # Create backup before execution
                backup_info = self._create_backup(plan)

                # Secure execution with path validation
                script_path = Path(plan.script_path).resolve()
                if not script_path.exists():
                    logger.error(f"Script not found: {script_path}")
                    raise FileNotFoundError(
                        f"Remediation script not found: {script_path}"
                    )

                logger.info(f"Executing remediation: {script_path}")
                result = subprocess.run(
                    [
                        sys.executable,
                        str(script_path),
                    ],  # Use current Python interpreter
                    capture_output=True,
                    text=True,
                    timeout=plan.timeout,
                    cwd=Path.cwd(),  # Explicit working directory
                    env=os.environ.copy(),  # Controlled environment
                )
                output = result.stdout
                error = result.stderr if result.returncode != 0 else None
                status = (
                    RemediationStatus.SUCCESS
                    if result.returncode == 0
                    else RemediationStatus.FAILED
                )

                if status == RemediationStatus.FAILED:
                    logger.error(f"Remediation failed: {error}")
                    # Attempt rollback on failure
                    if plan.rollback_script:
                        self._execute_rollback(plan, backup_info)
                else:
                    logger.info(f"Remediation completed successfully: {script_path}")

            execution_time = time.time() - start_time

            return RemediationResult(
                plan=plan,
                status=status,
                execution_time=execution_time,
                output=output,
                error=error,
                metrics={
                    "return_code": 0 if not error else 1,
                    "backup_created": not plan.dry_run,
                },
            )

        except subprocess.TimeoutExpired:
            logger.error(f"Remediation timed out: {plan.script_path}")
            return RemediationResult(
                plan=plan,
                status=RemediationStatus.FAILED,
                execution_time=time.time() - start_time,
                output="",
                error="Remediation timed out",
            )
        except Exception as e:
            logger.error(f"Remediation exception: {e}")
            return RemediationResult(
                plan=plan,
                status=RemediationStatus.FAILED,
                execution_time=time.time() - start_time,
                output="",
                error=str(e),
            )

    def _create_backup(self, plan: RemediationPlan) -> Dict[str, Any]:
        """Create backup before remediation execution"""
        backup_dir = Path("backups/remediation") / datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        backup_dir.mkdir(parents=True, exist_ok=True)

        backup_info = {
            "backup_dir": str(backup_dir),
            "timestamp": datetime.now().isoformat(),
            "finding_id": plan.finding_id,
        }

        # Save backup metadata
        with open(backup_dir / "backup_info.json", "w") as f:
            json.dump(backup_info, f, indent=2)

        logger.info(f"Backup created: {backup_dir}")
        return backup_info

    def _execute_rollback(
        self, plan: RemediationPlan, backup_info: Dict[str, Any]
    ) -> bool:
        """Execute rollback script if remediation fails"""
        if not plan.rollback_script:
            return False

        try:
            logger.info(f"Executing rollback: {plan.rollback_script}")
            result = subprocess.run(
                [sys.executable, plan.rollback_script],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout for rollback
                env=os.environ.copy(),
            )

            if result.returncode == 0:
                logger.info("Rollback completed successfully")
                return True
            else:
                logger.error(f"Rollback failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Rollback exception: {e}")
            return False


class AutomationMetrics:
    """Enhanced performance metrics collector for automation engine"""

    def __init__(self):
        self.metrics_history: List[Dict[str, Any]] = []
        self.performance_thresholds = {
            "min_success_rate": 80.0,
            "max_avg_execution_time": 120.0,
            "max_failure_rate": 20.0,
        }

    def record_remediation(self, result: RemediationResult) -> None:
        """Record a remediation result for metrics tracking"""
        metric_entry: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "finding_id": result.plan.finding_id if result.plan else "unknown",
            "success": result.status == RemediationStatus.SUCCESS,
            "execution_time": result.execution_time,
            "risk_level": result.plan.risk_level if result.plan else "unknown",
            "action_type": result.plan.action_type.value if result.plan else "unknown",
            "error": result.error is not None,
        }

        self.metrics_history.append(metric_entry)

        # Keep only last 1000 entries to prevent memory bloat
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        if not self.metrics_history:
            return {
                "success_rate": 0.0,
                "avg_execution_time": 0.0,
                "total_remediations": 0,
                "risk_reduction": 0.0,
                "performance_status": "no_data",
            }

        successful = len([m for m in self.metrics_history if m.get("success", False)])
        total = len(self.metrics_history)
        success_rate = (successful / total) * 100 if total > 0 else 0.0

        avg_time = sum(m.get("execution_time", 0) for m in self.metrics_history) / total

        # Performance assessment
        performance_status = self._assess_performance(success_rate, avg_time)

        # Risk level breakdown
        risk_breakdown = self._analyze_risk_levels()

        return {
            "success_rate": success_rate,
            "avg_execution_time": avg_time,
            "total_remediations": total,
            "risk_reduction": self._calculate_risk_reduction(),
            "performance_status": performance_status,
            "risk_breakdown": risk_breakdown,
            "recent_failures": self._get_recent_failures(),
        }

    def _assess_performance(self, success_rate: float, avg_time: float) -> str:
        """Assess overall performance status"""
        if (
            success_rate >= self.performance_thresholds["min_success_rate"]
            and avg_time <= self.performance_thresholds["max_avg_execution_time"]
        ):
            return "excellent"
        elif success_rate >= 70.0 and avg_time <= 180.0:
            return "good"
        elif success_rate >= 50.0:
            return "needs_improvement"
        else:
            return "poor"

    def _analyze_risk_levels(self) -> Dict[str, int]:
        """Analyze remediation attempts by risk level"""
        risk_counts: Dict[str, int] = defaultdict(int)
        for metric in self.metrics_history:
            risk_level = metric.get("risk_level", "unknown")
            risk_counts[risk_level] += 1
        return dict(risk_counts)

    def _get_recent_failures(self) -> List[Dict[str, Any]]:
        """Get recent failures for analysis"""
        recent_failures = [
            m
            for m in self.metrics_history[-50:]  # Last 50 entries
            if not m.get("success", True)
        ]
        return recent_failures[-5:]  # Last 5 failures

    def _calculate_risk_reduction(self) -> float:
        """Calculate overall risk reduction from remediations"""
        if not self.metrics_history:
            return 0.0

        # Weighted risk reduction based on successful remediations
        risk_weights = {"critical": 10, "high": 7, "medium": 4, "low": 2}
        total_reduction = 0

        for metric in self.metrics_history:
            if metric.get("success", False):
                risk_level = metric.get("risk_level", "low")
                weight = risk_weights.get(risk_level, 1)
                total_reduction += weight

        # Normalize to percentage
        max_possible = len(self.metrics_history) * 10  # Assuming all critical
        return (total_reduction / max_possible * 100) if max_possible > 0 else 0.0


# Make this plugin discoverable
__plugin_class__ = AutoRemediationEngine
