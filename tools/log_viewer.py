#!/usr/bin/env python3
"""
Log viewer utility for PepeluGPT.
Provides real-time monitoring and analysis of log files.
"""

import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from typing import Optional, Dict


class LogViewer:
    def __init__(self, logs_dir: str = "logs"):
        self.logs_dir = logs_dir
        self.log_files: Dict[str, Optional[str]] = {
            "main": os.path.join(logs_dir, "pepeluGPT.log"),
            "errors": os.path.join(logs_dir, "errors.log"),
            "audit": os.path.join(logs_dir, "security_audit.log"),
            "current_session": self._get_latest_session_log(),
        }

    def _get_latest_session_log(self) -> Optional[str]:
        """Find the most recent session log file."""
        if not os.path.exists(self.logs_dir):
            return None

        session_files = [
            f for f in os.listdir(self.logs_dir) if f.startswith("session_")
        ]
        if not session_files:
            return None

        # Sort by creation time, get the latest
        session_files.sort(
            key=lambda x: os.path.getctime(os.path.join(self.logs_dir, x)), reverse=True
        )
        return os.path.join(self.logs_dir, session_files[0])

    def tail_log(self, log_type: str = "main", lines: int = 50):
        """Display the last N lines of a log file."""
        log_file = self.log_files.get(log_type)
        if not log_file or not os.path.exists(log_file):
            print(f"❌ Log file not found: {log_file}")
            return

        print(f"📋 Last {lines} lines from {log_type} log:")
        print("=" * 80)

        try:
            if os.name == "nt":  # Windows
                result = subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        f'Get-Content "{log_file}" | Select-Object -Last {lines}',
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                print(result.stdout)
            else:  # Unix-like
                result = subprocess.run(
                    ["tail", "-n", str(lines), log_file], capture_output=True, text=True
                )
                print(result.stdout)
        except Exception:
            # Fallback to Python implementation
            with open(log_file, "r", encoding="utf-8") as f:
                lines_list = f.readlines()
                for line in lines_list[-lines:]:
                    print(line.rstrip())

    def follow_log(self, log_type: str = "main"):
        """Follow a log file in real-time (like tail -f)."""
        log_file = self.log_files.get(log_type)
        if not log_file or not os.path.exists(log_file):
            print(f"❌ Log file not found: {log_file}")
            return

        print(f"👁️  Following {log_type} log in real-time (Ctrl+C to stop):")
        print("=" * 80)

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                # Go to end of file
                f.seek(0, 2)

                while True:
                    line = f.readline()
                    if line:
                        print(line.rstrip())
                    else:
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n⏹️  Stopped following log.")

    def search_logs(self, pattern: str, log_type: str = "main", context: int = 2):
        """Search for a pattern in log files with context."""
        log_file = self.log_files.get(log_type)
        if not log_file or not os.path.exists(log_file):
            print(f"❌ Log file not found: {log_file}")
            return

        print(f"🔍 Searching for '{pattern}' in {log_type} log:")
        print("=" * 80)

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            matches: list[tuple[int, int, int, list[str]]] = []
            for i, line in enumerate(lines):
                if pattern.lower() in line.lower():
                    start = max(0, i - context)
                    end = min(len(lines), i + context + 1)
                    matches.append((i + 1, start, end, lines[start:end]))

            if not matches:
                print(f"No matches found for '{pattern}'")
                return

            for line_num, start, end, context_lines in matches:
                print(f"\n📍 Match at line {line_num}:")
                print("-" * 40)
                for j, context_line in enumerate(context_lines):
                    actual_line_num = start + j + 1
                    marker = ">>>" if actual_line_num == line_num else "   "
                    print(f"{marker} {actual_line_num:4d}: {context_line.rstrip()}")

        except Exception as e:
            print(f"Error searching log: {e}")

    def show_audit_summary(self, hours: int = 24):
        """Show a summary of audit events from the last N hours."""
        audit_file = self.log_files.get("audit")
        if not audit_file or not os.path.exists(audit_file):
            print("❌ Audit log file not found")
            return

        print(f"📊 Audit Summary (last {hours} hours):")
        print("=" * 80)

        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        events: list[dict[str, str]] = []  # type: ignore
        user_queries = 0
        system_events = 0
        errors = 0

        try:
            with open(audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        event_time = datetime.fromisoformat(
                            entry["timestamp"]  # type: ignore
                        ).timestamp()

                        if event_time >= cutoff_time:
                            events.append(entry)  # type: ignore

                            if "user_query" in entry:
                                user_queries += 1
                            elif "system_event" in entry:
                                system_events += 1
                            elif entry.get("level") == "ERROR":  # type: ignore
                                errors += 1

                    except (json.JSONDecodeError, KeyError):
                        continue

            print(f"📈 Statistics:")
            print(f"   • User queries: {user_queries}")
            print(f"   • System events: {system_events}")
            print(f"   • Errors: {errors}")
            print(f"   • Total events: {len(events)}")

            if errors > 0:
                print(f"\n❌ Recent Errors:")
                for event in events:
                    if event.get("level") == "ERROR":  # type: ignore
                        timestamp = datetime.fromisoformat(event["timestamp"]).strftime(  # type: ignore
                            "%H:%M:%S"
                        )
                        print(f"   {timestamp}: {event['message']}")  # type: ignore

            if events:
                print(f"\n⏰ Recent Activity:")
                for event in events[-5:]:  # Last 5 events
                    timestamp = datetime.fromisoformat(event["timestamp"]).strftime(  # type: ignore
                        "%H:%M:%S"
                    )
                    message = event["message"]  # type: ignore
                    if len(message) > 60:  # type: ignore
                        message = message[:60] + "..."  # type: ignore
                    print(f"   {timestamp}: {message}")

        except Exception as e:
            print(f"Error reading audit log: {e}")

    def list_log_files(self):
        """List all available log files."""
        print("📂 Available Log Files:")
        print("=" * 50)

        for log_type, log_path in self.log_files.items():
            if log_path and os.path.exists(log_path):
                size = os.path.getsize(log_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(log_path))
                print(f"✅ {log_type:15} {log_path}")
                print(
                    f"   Size: {size:,} bytes, Modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            else:
                print(f"❌ {log_type:15} {log_path or 'Not found'}")

        # Check for session logs
        if os.path.exists(self.logs_dir):
            session_files = [
                f for f in os.listdir(self.logs_dir) if f.startswith("session_")
            ]
            if session_files:
                print(f"\n📁 Session Logs ({len(session_files)} files):")
                for session_file in sorted(session_files, reverse=True)[
                    :5
                ]:  # Show last 5
                    session_path = os.path.join(self.logs_dir, session_file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(session_path))
                    print(f"   {session_file} - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    parser = argparse.ArgumentParser(description="PepeluGPT Log Viewer")
    parser.add_argument(
        "--logs-dir", default="logs", help="Directory containing log files"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    subparsers.add_parser("list", help="List all log files")

    # Tail command
    tail_parser = subparsers.add_parser("tail", help="Show last N lines of a log")
    tail_parser.add_argument(
        "log_type",
        choices=["main", "errors", "audit", "current_session"],
        help="Type of log to view",
    )
    tail_parser.add_argument(
        "-n", "--lines", type=int, default=50, help="Number of lines to show"
    )

    # Follow command
    follow_parser = subparsers.add_parser("follow", help="Follow a log in real-time")
    follow_parser.add_argument(
        "log_type",
        choices=["main", "errors", "audit", "current_session"],
        help="Type of log to follow",
    )

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for pattern in logs")
    search_parser.add_argument("pattern", help="Pattern to search for")
    search_parser.add_argument(
        "log_type",
        choices=["main", "errors", "audit", "current_session"],
        help="Type of log to search",
    )
    search_parser.add_argument(
        "-c", "--context", type=int, default=2, help="Lines of context around matches"
    )

    # Audit summary command
    audit_parser = subparsers.add_parser("audit", help="Show audit summary")
    audit_parser.add_argument(
        "--hours", type=int, default=24, help="Hours of history to analyze"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    viewer = LogViewer(args.logs_dir)

    if args.command == "list":
        viewer.list_log_files()
    elif args.command == "tail":
        viewer.tail_log(args.log_type, args.lines)
    elif args.command == "follow":
        viewer.follow_log(args.log_type)
    elif args.command == "search":
        viewer.search_logs(args.pattern, args.log_type, args.context)
    elif args.command == "audit":
        viewer.show_audit_summary(args.hours)


if __name__ == "__main__":
    main()
