#!/usr/bin/env python3
"""
Prometheus Metrics Exporter for PepeluGPT AI Intelligence
Real-time streaming of security metrics and AI insights
"""

import json
import os
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from plugins.registry import PluginRegistry


class PrometheusMetrics:
    """
    Prometheus metrics collector for PepeluGPT AI Intelligence
    """

    def __init__(self, plugins_dir: str = "plugins"):
        self.registry = PluginRegistry(plugins_dir)
        self.metrics_cache: Dict[str, Any] = {}
        self.last_update: datetime | None = None

    def collect_metrics(self, workspace_path: str = ".") -> Dict[str, Any]:
        """Collect all metrics for Prometheus export"""
        metrics: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "workspace": workspace_path,
            "metrics": {},
        }

        try:
            # Load AI Intelligence plugin
            ai_plugin = self.registry.load_plugin("ai_intelligence")
            if not ai_plugin:
                return self._empty_metrics()

            # Run AI audit to get current intelligence
            config = {"workspace_path": workspace_path}
            findings = ai_plugin.audit(config)

            # Extract metrics from AI findings
            metrics["metrics"] = self._extract_prometheus_metrics(
                findings, workspace_path
            )

            # Cache for performance
            self.metrics_cache = metrics
            self.last_update = datetime.now()

        except Exception as e:
            print(f"❌ Error collecting metrics: {e}")
            metrics["metrics"] = self._empty_metrics()["metrics"]
            metrics["error"] = str(e)

        return metrics

    def _extract_prometheus_metrics(
        self, findings: List[Any], workspace_path: str = "."
    ) -> Dict[str, float]:
        """Extract Prometheus-compatible metrics from AI findings"""
        metrics = {
            # Core AI metrics
            "pepelugpt_ai_risk_score": 0.0,
            "pepelugpt_ai_confidence": 0.0,
            "pepelugpt_ai_findings_total": 0.0,
            "pepelugpt_ai_critical_patterns": 0.0,
            "pepelugpt_ai_emerging_threats": 0.0,
            "pepelugpt_ai_anomalies_detected": 0.0,
            "pepelugpt_ai_recommendations_generated": 0.0,
            # Severity breakdown
            "pepelugpt_findings_critical": 0.0,
            "pepelugpt_findings_high": 0.0,
            "pepelugpt_findings_medium": 0.0,
            "pepelugpt_findings_low": 0.0,
            "pepelugpt_findings_info": 0.0,
            # Audit history metrics
            "pepelugpt_audit_history_count": 0.0,
            "pepelugpt_audit_improvement_rate": 0.0,
            # Workspace characteristics
            "pepelugpt_workspace_python_files": 0.0,
            "pepelugpt_workspace_config_files": 0.0,
            "pepelugpt_workspace_docker_present": 0.0,
            # Plugin health
            "pepelugpt_plugin_execution_success": 1.0,
            "pepelugpt_plugin_execution_time": 0.0,
        }

        start_time = time.time()

        try:
            # Process findings by category
            for finding in findings:
                # Convert finding to dict if needed
                if hasattr(finding, "to_dict"):
                    finding_dict = finding.to_dict()  # type: ignore
                else:
                    finding_dict = finding if isinstance(finding, dict) else {}  # type: ignore

                severity = finding_dict.get("severity", "info").lower()  # type: ignore
                category = finding_dict.get("category", "unknown")  # type: ignore
                control = finding_dict.get("control", "")  # type: ignore
                metadata = finding_dict.get("metadata", {})  # type: ignore

                # Count total findings
                metrics["pepelugpt_ai_findings_total"] += 1.0

                # Count by severity
                severity_key = f"pepelugpt_findings_{severity}"
                if severity_key in metrics:
                    metrics[severity_key] += 1.0

                # Extract specific AI metrics
                if control == "AI-003" and "risk_score" in metadata:
                    metrics["pepelugpt_ai_risk_score"] = float(metadata["risk_score"])  # type: ignore
                    metrics["pepelugpt_ai_confidence"] = float(
                        metadata.get("confidence", 0.85)  # type: ignore
                    )

                if category == "pattern_detection":
                    patterns = metadata.get("critical_patterns", [])  # type: ignore
                    metrics["pepelugpt_ai_critical_patterns"] = float(len(patterns))  # type: ignore

                    threats = metadata.get("emerging_threats", [])  # type: ignore
                    metrics["pepelugpt_ai_emerging_threats"] = float(len(threats))  # type: ignore

                if category == "anomaly_detection":
                    metrics["pepelugpt_ai_anomalies_detected"] += 1.0

                if category == "ai_recommendations":
                    metrics["pepelugpt_ai_recommendations_generated"] += 1.0

                if category == "intelligence" and "total_audits" in metadata:
                    metrics["pepelugpt_audit_history_count"] = float(
                        metadata["total_audits"]  # type: ignore
                    )
                    metrics["pepelugpt_audit_improvement_rate"] = float(
                        metadata.get("improvement_rate", 0.0)  # type: ignore
                    )

                # Extract workspace metrics from metadata
                if "file_count" in metadata:
                    metrics["pepelugpt_workspace_python_files"] = float(
                        metadata["file_count"]  # type: ignore
                    )

                if "yaml_count" in metadata and "json_count" in metadata:
                    total_configs = metadata["yaml_count"] + metadata["json_count"]  # type: ignore
                    metrics["pepelugpt_workspace_config_files"] = float(total_configs)  # type: ignore

            # Check for Docker presence (simplified)
            docker_present = any(
                finding_dict.get("metadata", {}).get("type") == "container_exposure"  # type: ignore
                for finding in findings
                for finding_dict in [
                    finding.to_dict() if hasattr(finding, "to_dict") else finding  # type: ignore
                ]
                if isinstance(finding_dict, dict)
            )
            metrics["pepelugpt_workspace_docker_present"] = (
                1.0 if docker_present else 0.0
            )

        except Exception as e:
            print(f"⚠️ Error processing findings: {e}")
            metrics["pepelugpt_plugin_execution_success"] = 0.0

        # Record execution time
        metrics["pepelugpt_plugin_execution_time"] = time.time() - start_time

        # Add compliance metrics
        compliance_metrics = self._collect_compliance_metrics(workspace_path)
        metrics.update(compliance_metrics)

        # Add automation metrics
        automation_metrics = self._collect_automation_metrics(workspace_path)
        metrics.update(automation_metrics)

        return metrics

    def _collect_automation_metrics(
        self, workspace_path: str = "."
    ) -> Dict[str, float]:
        """Collect auto-remediation engine metrics"""
        metrics: Dict[str, float] = {}

        try:
            # Import and run auto-remediation engine
            from plugins.core.auto_remediation import AutoRemediationEngine

            automation_plugin = AutoRemediationEngine()
            config = {"workspace_path": workspace_path}
            findings = automation_plugin.audit(config)

            # Extract automation metrics from findings
            self_healing_enabled = False
            remediation_opportunities = 0
            auto_remediable_count = 0
            performance_score = 0.0

            for finding in findings:
                metadata = finding.metadata if hasattr(finding, "metadata") else {}

                # Self-healing status
                if finding.control == "AUTO-004":
                    if "self_healing_enabled" in metadata:
                        self_healing_enabled = metadata.get(
                            "self_healing_enabled", False
                        )

                # Remediation opportunities
                elif finding.control == "AUTO-001":
                    if "total_remediable" in metadata:
                        remediation_opportunities = metadata.get("total_remediable", 0)
                        auto_remediable_count = metadata.get("auto_remediable", 0)

                # Performance metrics
                elif finding.control == "AUTO-003":
                    if "success_rate" in metadata:
                        performance_score = metadata.get("success_rate", 0.0)

            # Set automation metrics
            metrics["pepelugpt_automation_self_healing_enabled"] = (
                1.0 if self_healing_enabled else 0.0
            )
            metrics["pepelugpt_automation_remediation_opportunities"] = float(
                remediation_opportunities
            )
            metrics["pepelugpt_automation_auto_remediable"] = float(
                auto_remediable_count
            )
            metrics["pepelugpt_automation_performance_score"] = performance_score

            # Calculate automation coverage
            automation_coverage = (
                (auto_remediable_count / remediation_opportunities * 100)
                if remediation_opportunities > 0
                else 0.0
            )
            metrics["pepelugpt_automation_coverage_percentage"] = automation_coverage

            # Automation readiness score
            readiness_factors: List[float] = [
                1.0 if self_healing_enabled else 0.0,
                min(automation_coverage / 100.0, 1.0),
                min(performance_score / 100.0, 1.0),
            ]
            automation_readiness = sum(readiness_factors) / len(readiness_factors) * 100
            metrics["pepelugpt_automation_readiness_score"] = automation_readiness

        except Exception as e:
            print(f"Warning: Could not collect automation metrics: {e}")
            # Set default values on error
            metrics.update(  # type: ignore
                {
                    "pepelugpt_automation_self_healing_enabled": 0.0,
                    "pepelugpt_automation_remediation_opportunities": 0.0,
                    "pepelugpt_automation_auto_remediable": 0.0,
                    "pepelugpt_automation_performance_score": 0.0,
                    "pepelugpt_automation_coverage_percentage": 0.0,
                    "pepelugpt_automation_readiness_score": 0.0,
                }
            )

        return metrics

    def _collect_compliance_metrics(
        self, workspace_path: str = "."
    ) -> Dict[str, float]:
        """Collect compliance prediction metrics"""
        metrics: Dict[str, float] = {}

        try:
            # Import and run compliance predictor
            from plugins.core.compliance_predictor import CompliancePredictorPlugin

            compliance_plugin = CompliancePredictorPlugin()
            config = {"workspace_path": workspace_path}
            findings = compliance_plugin.audit(config)

            # Extract compliance metrics from findings
            framework_scores: Dict[str, float] = {}
            gap_counts = {"critical": 0, "moderate": 0}
            readiness_score = 0.0

            for finding in findings:
                metadata = finding.metadata if hasattr(finding, "metadata") else {}  # type: ignore

                # Framework coverage metrics
                if finding.control == "CP-001":  # type: ignore
                    framework = metadata.get("framework", "unknown").lower()  # type: ignore
                    coverage = metadata.get("coverage_percentage", 0.0)  # type: ignore
                    if framework != "unknown":
                        framework_scores[framework] = coverage  # type: ignore

                # Gap analysis metrics
                elif finding.control == "CP-002":  # type: ignore
                    if finding.id == "CP-002.SUMMARY":  # type: ignore
                        # Extract gap counts from summary metadata
                        summary_metadata = metadata.get("critical_gaps", [])  # type: ignore
                        gap_counts["critical"] = len(summary_metadata)  # type: ignore
                        moderate_gaps = metadata.get("moderate_gaps", [])  # type: ignore
                        gap_counts["moderate"] = len(moderate_gaps)  # type: ignore
                    elif "gap_type" in metadata:
                        gap_type = metadata.get("gap_type")  # type: ignore
                        if gap_type == "critical":
                            gap_counts["critical"] += 1
                        elif gap_type == "moderate":
                            gap_counts["moderate"] += 1

                # Audit readiness metrics
                elif finding.control == "CP-004" and "overall_score" in metadata:  # type: ignore
                    readiness_score = metadata.get("overall_score", 0.0)  # type: ignore

            # Set framework-specific metrics
            for framework, score in framework_scores.items():
                metrics[f"pepelugpt_compliance_{framework.lower()}_coverage"] = score  # type: ignore

                # Predict compliance score (simplified prediction)
                predicted_score = min(score + 10.0, 100.0)  # Simple +10% prediction  # type: ignore
                metrics[f"pepelugpt_compliance_{framework.lower()}_predicted"] = (  # type: ignore
                    predicted_score
                )

            # Set overall compliance metrics
            metrics["pepelugpt_compliance_gaps_critical"] = float(
                gap_counts["critical"]
            )
            metrics["pepelugpt_compliance_gaps_moderate"] = float(
                gap_counts["moderate"]
            )
            metrics["pepelugpt_compliance_audit_readiness"] = readiness_score

            # Overall compliance health score
            avg_coverage = (
                sum(framework_scores.values()) / len(framework_scores)  # type: ignore
                if framework_scores
                else 0.0
            )
            gap_penalty = (gap_counts["critical"] * 10) + (gap_counts["moderate"] * 5)
            health_score = max(0.0, avg_coverage - gap_penalty)
            metrics["pepelugpt_compliance_health_score"] = health_score

        except Exception as e:
            print(f"Warning: Could not collect compliance metrics: {e}")
            # Set default values on error
            metrics.update(  # type: ignore
                {
                    "pepelugpt_compliance_nist_csf_coverage": 0.0,
                    "pepelugpt_compliance_iso_27001_coverage": 0.0,
                    "pepelugpt_compliance_soc2_coverage": 0.0,
                    "pepelugpt_compliance_gaps_critical": 0.0,
                    "pepelugpt_compliance_gaps_moderate": 0.0,
                    "pepelugpt_compliance_audit_readiness": 0.0,
                    "pepelugpt_compliance_health_score": 0.0,
                }
            )

        return metrics

    def _empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics structure"""
        return {
            "timestamp": datetime.now().isoformat(),
            "workspace": ".",
            "metrics": {
                "pepelugpt_ai_risk_score": 0.0,
                "pepelugpt_ai_confidence": 0.0,
                "pepelugpt_ai_findings_total": 0.0,
                "pepelugpt_plugin_execution_success": 0.0,
            },
        }

    def to_prometheus_format(self, metrics_data: Dict[str, Any]) -> str:
        """Convert metrics to Prometheus exposition format"""
        lines: List[str] = []
        timestamp_ms = int(time.time() * 1000)

        # Add header comments
        lines.append(
            "# HELP pepelugpt_ai_risk_score AI-calculated predictive risk score (0-10)"
        )
        lines.append("# TYPE pepelugpt_ai_risk_score gauge")

        lines.append(
            "# HELP pepelugpt_ai_confidence AI confidence score for risk assessment"
        )
        lines.append("# TYPE pepelugpt_ai_confidence gauge")

        lines.append(
            "# HELP pepelugpt_ai_findings_total Total number of AI findings detected"
        )
        lines.append("# TYPE pepelugpt_ai_findings_total counter")

        lines.append("# HELP pepelugpt_findings_critical Number of critical findings")
        lines.append("# TYPE pepelugpt_findings_critical gauge")

        lines.append(
            "# HELP pepelugpt_plugin_execution_success Plugin execution success (1=success, 0=failure)"
        )
        lines.append("# TYPE pepelugpt_plugin_execution_success gauge")

        # Add workspace labels
        workspace_label = f'workspace="{metrics_data.get("workspace", ".")}"'

        # Output metrics with labels and timestamps
        for metric_name, value in metrics_data.get("metrics", {}).items():
            lines.append(f"{metric_name}{{{workspace_label}}} {value} {timestamp_ms}")

        return "\n".join(lines) + "\n"


class PrometheusHandler(BaseHTTPRequestHandler):
    """HTTP handler for Prometheus metrics endpoint"""

    def __init__(self, metrics_collector: 'PrometheusMetrics', *args: Any, **kwargs: Any):
        self.metrics_collector = metrics_collector
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests for metrics"""
        if self.path == "/metrics":
            try:
                # Collect fresh metrics
                metrics_data = self.metrics_collector.collect_metrics()
                prometheus_output = self.metrics_collector.to_prometheus_format(
                    metrics_data
                )

                # Send response
                self.send_response(200)
                self.send_header(
                    "Content-Type", "text/plain; version=0.0.4; charset=utf-8"
                )
                self.end_headers()
                self.wfile.write(prometheus_output.encode("utf-8"))

                print(
                    f"📊 Served metrics: {len(metrics_data.get('metrics', {}))} metrics exported"  # type: ignore
                )

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                error_msg = f"Error collecting metrics: {e}\n"
                self.wfile.write(error_msg.encode("utf-8"))
                print(f"❌ Metrics error: {e}")

        elif self.path == "/health":
            # Health check endpoint
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            health_data: Dict[str, Any] = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "last_metrics_update": (
                    self.metrics_collector.last_update.isoformat()  # type: ignore
                    if self.metrics_collector.last_update  # type: ignore
                    else None
                ),
            }
            self.wfile.write(json.dumps(health_data, indent=2).encode("utf-8"))

        else:
            # 404 for other paths
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found\n")

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default logging"""
        pass


def create_handler(metrics_collector: 'PrometheusMetrics'):
    """Factory function to create handler with metrics collector"""

    def handler(*args: Any, **kwargs: Any) -> PrometheusHandler:
        return PrometheusHandler(metrics_collector, *args, **kwargs)

    return handler


class PrometheusExporter:
    """
    Prometheus metrics exporter for PepeluGPT AI Intelligence
    """

    def __init__(self, port: int = 8000, workspace_path: str = "."):
        self.port = port
        self.workspace_path = workspace_path
        self.metrics_collector = PrometheusMetrics()
        self.server = None
        self.server_thread = None

    def start_server(self, background: bool = True):
        """Start the Prometheus metrics server"""
        handler = create_handler(self.metrics_collector)
        self.server = HTTPServer(("localhost", self.port), handler)

        print(f"🔵 Starting PepeluGPT Prometheus Exporter on port {self.port}")
        print(f"� Metrics endpoint: http://localhost:{self.port}/metrics")
        print(f"🔵 Health endpoint: http://localhost:{self.port}/health")
        print(f"� Monitoring workspace: {self.workspace_path}")

        if background:
            self.server_thread = threading.Thread(
                target=self.server.serve_forever, daemon=True
            )
            self.server_thread.start()
            print("✅ Prometheus exporter running in background")
        else:
            print("🔄 Serving metrics (Ctrl+C to stop)...")
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down Prometheus exporter")
                self.stop_server()

    def stop_server(self):
        """Stop the Prometheus metrics server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("✅ Prometheus exporter stopped")

    def export_snapshot(self, output_file: str | None = None):
        """Export a one-time snapshot of metrics"""
        print("📸 Collecting metrics snapshot...")
        metrics_data = self.metrics_collector.collect_metrics(self.workspace_path)
        prometheus_output = self.metrics_collector.to_prometheus_format(metrics_data)

        if output_file:
            with open(output_file, "w") as f:
                f.write(prometheus_output)
            print(f"💾 Metrics snapshot saved to {output_file}")
        else:
            print("📊 Current Metrics:")
            print("=" * 50)
            print(prometheus_output)

        return metrics_data


def main():
    """Main CLI interface for Prometheus exporter"""
    import argparse

    parser = argparse.ArgumentParser(
        description="PepeluGPT Prometheus Metrics Exporter"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Server port (default: 8000)"
    )
    parser.add_argument("--workspace", default=".", help="Workspace path to monitor")
    parser.add_argument("--snapshot", help="Export one-time snapshot to file")
    parser.add_argument(
        "--background", action="store_true", help="Run server in background"
    )

    args = parser.parse_args()

    exporter = PrometheusExporter(port=args.port, workspace_path=args.workspace)

    if args.snapshot:
        exporter.export_snapshot(args.snapshot)
    else:
        exporter.start_server(background=args.background)

        if args.background:
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                exporter.stop_server()


if __name__ == "__main__":
    main()
