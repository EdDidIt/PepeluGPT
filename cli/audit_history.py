#!/usr/bin/env python3
"""
Audit history management for PepeluGPT CLI.
Phase 4 preview: Temporal intelligence and audit tracking.
"""

import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict


class AuditMetadata(TypedDict):
    saved_at: str
    audit_type: str
    file_path: str
    pepelugpt_version: str


class AuditSummary(TypedDict):
    critical: int
    high: int
    medium: int
    low: int


class AuditInfo(TypedDict):
    total_findings: int
    timestamp: str


class AuditReport(TypedDict):
    metadata: AuditMetadata
    summary: AuditSummary
    audit_info: AuditInfo


class AuditReportSummary(TypedDict):
    file_path: str
    timestamp: str
    audit_type: str
    total_findings: int
    summary: AuditSummary
    file_size: int


class TrendDataPoint(TypedDict):
    date: str
    value: int


class TrendSummary(TypedDict):
    current: int
    average: float
    trend: str
    change_percent: float


class TrendData(TypedDict):
    metric: str
    days: int
    start_date: str
    end_date: str
    data_points: List[TrendDataPoint]
    summary: TrendSummary


class ComparisonBaseline(TypedDict):
    file: str
    timestamp: str
    total_findings: int
    summary: AuditSummary


class ComparisonCurrent(TypedDict):
    timestamp: str
    total_findings: int
    summary: AuditSummary


class ComparisonChanges(TypedDict):
    total_findings: int
    by_severity: Dict[str, int]
    status: str


class ComparisonResult(TypedDict):
    baseline: ComparisonBaseline
    current: ComparisonCurrent
    changes: ComparisonChanges


class AuditHistoryManager:
    """Manages audit history storage and retrieval."""

    def __init__(self, history_dir: str = "audit_history"):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)

    def save_audit_report(self, report: Dict[str, Any], audit_type: str = "all") -> str:
        """Save an audit report to history."""
        timestamp = datetime.datetime.now()

        # Create year/month directory structure
        year_month_dir = (
            self.history_dir / str(timestamp.year) / f"{timestamp.month:02d}"
        )
        year_month_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"audit_{audit_type}_{timestamp_str}.json"
        file_path = year_month_dir / filename

        # Add metadata to report
        enhanced_report: Dict[str, Any] = {
            **report,
            "metadata": {
                "saved_at": timestamp.isoformat(),
                "audit_type": audit_type,
                "file_path": str(file_path),
                "pepelugpt_version": "1.1.0",
            },
        }

        # Save to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(enhanced_report, f, indent=2)

        return str(file_path)

    def list_audit_reports(
        self, limit: int = 10, audit_type: Optional[str] = None
    ) -> List[AuditReportSummary]:
        """List recent audit reports."""
        reports: List[AuditReportSummary] = []

        # Walk through history directory
        for file_path in self.history_dir.rglob("audit_*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    report = json.load(f)

                # Filter by audit type if specified
                if (
                    audit_type
                    and report.get("metadata", {}).get("audit_type") != audit_type
                ):
                    continue

                # Extract summary info
                report_summary = report.get("summary", {})
                summary: AuditReportSummary = {
                    "file_path": str(file_path),
                    "timestamp": report.get("metadata", {}).get("saved_at", "unknown"),
                    "audit_type": report.get("metadata", {}).get(
                        "audit_type", "unknown"
                    ),
                    "total_findings": report.get("audit_info", {}).get(
                        "total_findings", 0
                    ),
                    "summary": {
                        "critical": report_summary.get("critical", 0),
                        "high": report_summary.get("high", 0),
                        "medium": report_summary.get("medium", 0),
                        "low": report_summary.get("low", 0),
                    },
                    "file_size": file_path.stat().st_size,
                }
                reports.append(summary)

            except (json.JSONDecodeError, FileNotFoundError):
                continue  # Skip corrupted files

        # Sort by timestamp (newest first) and limit
        reports.sort(key=lambda x: x["timestamp"], reverse=True)
        return reports[:limit]

    def get_audit_trend(
        self, days: int = 30, metric: str = "total_findings"
    ) -> TrendData:
        """Analyze audit trends over time."""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        end_date = datetime.datetime.now()

        trends: TrendData = {
            "metric": metric,
            "days": days,
            "start_date": cutoff_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "data_points": [],
            "summary": {
                "current": 0,
                "average": 0.0,
                "trend": "stable",  # "improving", "declining", "stable"
                "change_percent": 0.0,
            },
        }

        reports = self.list_audit_reports(limit=100)  # Get more for trend analysis

        # Filter reports within date range
        relevant_reports: List[AuditReportSummary] = []
        for report in reports:
            try:
                report_date = datetime.datetime.fromisoformat(
                    report["timestamp"].replace("Z", "+00:00")
                )
                if report_date >= cutoff_date:
                    relevant_reports.append(report)
            except (ValueError, TypeError):
                continue

        if not relevant_reports:
            return trends

        # Extract metric values
        values: List[TrendDataPoint] = []
        for report in relevant_reports:
            value: int
            if metric == "total_findings":
                value = report["total_findings"]
            elif metric == "critical_findings":
                value = report["summary"]["critical"]
            elif metric == "high_findings":
                value = report["summary"]["high"]
            else:
                value = report["total_findings"]  # Default

            values.append({
                "date": report["timestamp"][:10],  # YYYY-MM-DD
                "value": value
            })

        trends["data_points"] = sorted(values, key=lambda x: x["date"])

        # Calculate summary statistics
        if values:
            value_list = [v["value"] for v in values]
            trends["summary"]["current"] = value_list[0] if value_list else 0
            trends["summary"]["average"] = sum(value_list) / len(value_list)

            # Simple trend analysis (compare first and last quarters)
            if len(value_list) >= 4:
                first_quarter = sum(value_list[-4:]) / 4  # Most recent
                last_quarter = sum(value_list[:4]) / 4  # Oldest

                if first_quarter < last_quarter * 0.9:
                    trends["summary"]["trend"] = "improving"
                elif first_quarter > last_quarter * 1.1:
                    trends["summary"]["trend"] = "declining"
                else:
                    trends["summary"]["trend"] = "stable"

                # Calculate percentage change
                if last_quarter > 0:
                    change = ((first_quarter - last_quarter) / last_quarter) * 100
                    trends["summary"]["change_percent"] = round(change, 1)

        return trends

    def compare_audits(
        self, baseline_path: str, current_report: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare current audit with a baseline."""
        try:
            with open(baseline_path, "r", encoding="utf-8") as f:
                baseline = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return error as a special case - we'll need to handle this differently
            raise ValueError(f"Could not load baseline from {baseline_path}")

        baseline_summary = baseline.get("summary", {})
        current_summary = current_report.get("summary", {})
        
        comparison: ComparisonResult = {
            "baseline": {
                "file": baseline_path,
                "timestamp": baseline.get("metadata", {}).get("saved_at", "unknown"),
                "total_findings": baseline.get("audit_info", {}).get("total_findings", 0),
                "summary": {
                    "critical": baseline_summary.get("critical", 0),
                    "high": baseline_summary.get("high", 0),
                    "medium": baseline_summary.get("medium", 0),
                    "low": baseline_summary.get("low", 0),
                },
            },
            "current": {
                "timestamp": current_report.get("audit_info", {}).get("timestamp", "unknown"),
                "total_findings": current_report.get("audit_info", {}).get("total_findings", 0),
                "summary": {
                    "critical": current_summary.get("critical", 0),
                    "high": current_summary.get("high", 0),
                    "medium": current_summary.get("medium", 0),
                    "low": current_summary.get("low", 0),
                },
            },
            "changes": {
                "total_findings": 0,
                "by_severity": {},
                "status": "unchanged",  # "improved", "degraded", "unchanged"
            },
        }

        # Calculate changes
        baseline_total = comparison["baseline"]["total_findings"]
        current_total = comparison["current"]["total_findings"]
        comparison["changes"]["total_findings"] = current_total - baseline_total

        # Calculate severity changes
        for severity in ["critical", "high", "medium", "low"]:
            baseline_count = comparison["baseline"]["summary"].get(severity, 0)
            current_count = comparison["current"]["summary"].get(severity, 0)
            comparison["changes"]["by_severity"][severity] = (
                current_count - baseline_count
            )

        # Determine overall status
        critical_change = comparison["changes"]["by_severity"].get("critical", 0)
        high_change = comparison["changes"]["by_severity"].get("high", 0)

        if critical_change > 0 or high_change > 0:
            comparison["changes"]["status"] = "degraded"
        elif critical_change < 0 or high_change < 0:
            comparison["changes"]["status"] = "improved"
        else:
            comparison["changes"]["status"] = "unchanged"

        return comparison


def handle_audit_history_command(args: Any) -> None:
    """Handle audit history subcommands (Phase 4 preview)."""
    history_manager = AuditHistoryManager()

    if hasattr(args, "history_action"):
        if args.history_action == "list":
            reports = history_manager.list_audit_reports(
                limit=args.limit if hasattr(args, "limit") else 10
            )

            if not reports:
                print("📝 No audit history found")
                return

            print(f"📝 Audit History ({len(reports)} reports)")
            print("=" * 50)

            for i, report in enumerate(reports, 1):
                timestamp = report["timestamp"][:19].replace(
                    "T", " "
                )  # Format datetime
                findings = report["total_findings"]
                audit_type = report["audit_type"]

                # Size formatting
                size = report["file_size"]
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f}KB"
                else:
                    size_str = f"{size/(1024*1024):.1f}MB"

                print(
                    f"{i:2d}. {timestamp} | {audit_type:12s} | {findings:2d} findings | {size_str}"
                )

                # Show severity breakdown
                summary = report["summary"]
                severity_parts: List[str] = []
                for sev, emoji in [
                    ("critical", "🔴"),
                    ("high", "🟠"),
                    ("medium", "🟡"),
                    ("low", "🔵"),
                ]:
                    count = summary.get(sev, 0)
                    if count > 0:
                        severity_parts.append(f"{emoji}{count}")

                if severity_parts:
                    print(f"     Severity: {' '.join(severity_parts)}")
                print()

        elif args.history_action == "trend":
            metric = getattr(args, "metric", "total_findings")
            days = getattr(args, "days", 30)

            trend_data = history_manager.get_audit_trend(days=days, metric=metric)

            print(f"📈 Audit Trend Analysis - {metric} (last {days} days)")
            print("=" * 60)

            summary = trend_data["summary"]
            trend_emoji = {"improving": "📈", "declining": "📉", "stable": "➡️"}[
                summary["trend"]
            ]

            print(f"Current Value: {summary['current']}")
            print(f"Average: {summary['average']:.1f}")
            print(f"Trend: {trend_emoji} {summary['trend'].title()}")

            if summary["change_percent"] != 0:
                change_emoji = "📈" if summary["change_percent"] < 0 else "📉"
                print(f"Change: {change_emoji} {summary['change_percent']:+.1f}%")

            print(f"\nData Points: {len(trend_data['data_points'])}")

            # Simple ASCII chart for recent data points
            if trend_data["data_points"]:
                print("\nRecent Trend:")
                recent_points = trend_data["data_points"][-10:]  # Last 10 points
                for point in recent_points:
                    bar_length = min(20, max(1, point["value"]))
                    bar = "█" * bar_length
                    print(f"  {point['date']}: {bar} ({point['value']})")

    else:
        print("📝 Audit History Commands:")
        print("  python main.py audit history list      # List recent audits")
        print("  python main.py audit history trend     # Show trend analysis")
        print("")
        print("Coming in Phase 4:")
        print("  python main.py audit history compare   # Compare with baseline")
        print("  python main.py audit schedule daily    # Schedule automatic audits")
        print("  python main.py audit insights          # AI-powered insights")


def handle_audit_trends_command(args: Any) -> None:
    """Handle audit trends subcommand (Phase 4 preview)."""
    history_manager = AuditHistoryManager()
    
    metric = getattr(args, "metric", "total_findings")
    days = getattr(args, "days", 30)
    audit_type = getattr(args, "type", None)

    trend_data = history_manager.get_audit_trend(days=days, metric=metric)

    print(f"📈 Audit Trend Analysis - {metric} (last {days} days)")
    if audit_type:
        print(f"   Filtered by type: {audit_type}")
    print("=" * 60)

    summary = trend_data["summary"]
    trend_emoji = {"improving": "📈", "declining": "📉", "stable": "➡️"}[
        summary["trend"]
    ]

    print(f"Current Value: {summary['current']}")
    print(f"Average: {summary['average']:.1f}")
    print(f"Trend: {trend_emoji} {summary['trend'].title()}")

    if summary["change_percent"] != 0:
        change_emoji = "📈" if summary["change_percent"] < 0 else "📉"
        print(f"Change: {change_emoji} {summary['change_percent']:+.1f}%")

    print(f"\nData Points: {len(trend_data['data_points'])}")

    # Simple ASCII chart for recent data points
    if trend_data["data_points"]:
        print("\nRecent Trend:")
        recent_points = trend_data["data_points"][-10:]  # Last 10 points
        for point in recent_points:
            bar_length = min(20, max(1, point["value"]))
            bar = "█" * bar_length
            print(f"  {point['date']}: {bar} ({point['value']})")


