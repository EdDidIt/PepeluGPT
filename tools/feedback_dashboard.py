#!/usr/bin/env python3
"""
PepeluGPT Feedback Dashboard

Enhanced feedback analysis tool with comprehensive statistics, ratings analysis,
corrections tracking, and mode switching history.

Usage:
    python tools/feedback_dashboard.py --summary
    python tools/feedback_dashboard.py --ratings
    python tools/feedback_dashboard.py --corrections
    python tools/feedback_dashboard.py --export report.json
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils import get_logger

LOG = get_logger(__name__)


class FeedbackDashboard:
    """CLI dashboard for viewing and managing learning feedback."""

    def __init__(self, db_path: str = "learning/feedback.db"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensure database exists or show helpful message."""
        if not Path(self.db_path).exists():
            print(f"📊 No feedback database found at {self.db_path}")
            print("Run PepeluGPT with learning enabled to start collecting feedback.")
            return False
        return True

    def show_stats(self):
        """Display overall feedback statistics."""
        if not self._ensure_db_exists():
            return

        with sqlite3.connect(self.db_path) as conn:
            # Overall stats
            cursor = conn.execute(
                "SELECT COUNT(*), AVG(rating), MAX(timestamp) FROM feedback"
            )
            total, avg_rating, last_feedback = cursor.fetchone()

            print("📊 Feedback Statistics")
            print("=" * 40)
            print(f"Total Responses Rated: {total}")
            print(
                f"Average Rating: {avg_rating:.2f}/5.0"
                if avg_rating
                else "No ratings yet"
            )
            print(f"Last Feedback: {last_feedback}")
            print()

            # Rating distribution
            print("📈 Rating Distribution:")
            cursor = conn.execute(
                "SELECT rating, COUNT(*) FROM feedback GROUP BY rating ORDER BY rating"
            )
            for rating, count in cursor.fetchall():
                stars = "⭐" * rating
                bar = "█" * (count * 3)  # Simple bar chart
                print(f"  {rating} {stars:<5} {count:>3} {bar}")
            print()

            # Query types (approximate)
            print("🔍 Popular Query Types:")
            cursor = conn.execute(
                """
                SELECT 
                    CASE 
                        WHEN LOWER(query) LIKE '%ac-%' OR LOWER(query) LIKE '%cm-%' 
                             OR LOWER(query) LIKE '%cp-%' OR LOWER(query) LIKE '%pe-%' 
                        THEN 'NIST Controls'
                        WHEN LOWER(query) LIKE '%what is%' OR LOWER(query) LIKE '%stand for%'
                        THEN 'Acronyms'
                        WHEN LOWER(query) LIKE '%cyber%' OR LOWER(query) LIKE '%security%'
                        THEN 'Cybersecurity'
                        ELSE 'General'
                    END as query_type,
                    COUNT(*) as count,
                    AVG(rating) as avg_rating
                FROM feedback 
                GROUP BY query_type 
                ORDER BY count DESC
            """
            )

            for qtype, count, avg_rating in cursor.fetchall():
                print(f"  {qtype:<15} {count:>3} queries (avg: {avg_rating:.1f}⭐)")

    def show_corrections(self, limit: int = 10):
        """Display recent corrections for priority review."""
        if not self._ensure_db_exists():
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT query, response, correction, rating, timestamp 
                FROM feedback 
                WHERE correction IS NOT NULL 
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (limit,),
            )

            corrections = cursor.fetchall()

            if not corrections:
                print("📝 No corrections found. Users haven't provided any yet.")
                return

            print(f"📝 Recent Corrections (showing {len(corrections)})")
            print("=" * 60)

            for i, (query, response, correction, rating, timestamp) in enumerate(
                corrections, 1
            ):
                print(f"\n{i}. Query: {query}")
                print(
                    f"   Original: {response[:80]}{'...' if len(response) > 80 else ''}"
                )
                print(f"   Correction: {correction}")
                print(f"   Rating: {rating}⭐ | {timestamp}")
                print("-" * 60)

    def show_training_candidates(self, min_rating: int = 4):
        """Show high-quality responses suitable for training."""
        if not self._ensure_db_exists():
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT query, 
                       CASE WHEN correction IS NOT NULL THEN correction ELSE response END as best_response,
                       rating, 
                       timestamp
                FROM feedback 
                WHERE rating >= ? 
                ORDER BY rating DESC, timestamp DESC
            """,
                (min_rating,),
            )

            candidates = cursor.fetchall()

            print(f"🎯 Training Candidates (Rating ≥ {min_rating})")
            print("=" * 50)
            print(f"Found {len(candidates)} high-quality examples")

            if candidates:
                print("\nTop 5 examples:")
                for i, (query, response, rating, timestamp) in enumerate(
                    candidates[:5], 1
                ):
                    print(f"\n{i}. [{rating}⭐] {query}")
                    print(
                        f"   Response: {response[:100]}{'...' if len(response) > 100 else ''}"
                    )
                    print(f"   Date: {timestamp}")

            # Check if we have enough for training
            print(f"\n📊 Training Readiness:")
            print(f"  ✅ High-quality examples: {len(candidates)}")
            print(
                f"  {'✅' if len(candidates) >= 10 else '⚠️ '} Minimum for training: 10 (current: {len(candidates)})"
            )

    def show_poor_responses(self, max_rating: int = 2, limit: int = 10):
        """Show poorly rated responses that need improvement."""
        if not self._ensure_db_exists():
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT query, response, rating, correction, timestamp
                FROM feedback 
                WHERE rating <= ? 
                ORDER BY rating ASC, timestamp DESC
                LIMIT ?
            """,
                (max_rating, limit),
            )

            poor_responses = cursor.fetchall()

            print(f"🔴 Poor Responses (Rating ≤ {max_rating})")
            print("=" * 50)

            if not poor_responses:
                print("🎉 No poor responses found! All responses are well-rated.")
                return

            print(f"Found {len(poor_responses)} responses needing improvement:")

            for i, (query, response, rating, correction, timestamp) in enumerate(
                poor_responses, 1
            ):
                print(f"\n{i}. [{rating}⭐] {query}")
                print(
                    f"   Response: {response[:80]}{'...' if len(response) > 80 else ''}"
                )
                if correction:
                    print(
                        f"   User correction: {correction[:80]}{'...' if len(correction) > 80 else ''}"
                    )
                else:
                    print(f"   ⚠️  No correction provided")
                print(f"   Date: {timestamp}")

    def show_sessions(self, limit: int = 5):
        """Show recent sessions with their feedback patterns."""
        if not self._ensure_db_exists():
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT session_id, COUNT(*) as interactions, AVG(rating) as avg_rating, 
                       MIN(timestamp) as start_time, MAX(timestamp) as end_time
                FROM feedback 
                WHERE session_id IS NOT NULL
                GROUP BY session_id 
                ORDER BY start_time DESC 
                LIMIT ?
            """,
                (limit,),
            )

            sessions = cursor.fetchall()

            print(f"👥 Recent Sessions (showing {len(sessions)})")
            print("=" * 50)

            for session_id, interactions, avg_rating, start_time, end_time in sessions:
                duration = "Unknown"
                if start_time and end_time:
                    start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                    end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                    duration = str(end_dt - start_dt).split(".")[
                        0
                    ]  # Remove microseconds

                print(f"\n📱 {session_id}")
                print(
                    f"   Interactions: {interactions} | Avg Rating: {avg_rating:.1f}⭐"
                )
                print(f"   Duration: {duration}")
                print(f"   Period: {start_time} to {end_time}")


def main():
    """Main CLI interface for feedback dashboard."""
    parser = argparse.ArgumentParser(
        description="PepeluGPT Learning Feedback Dashboard"
    )
    parser.add_argument(
        "--db", default="learning/feedback.db", help="Path to feedback database"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Stats command
    subparsers.add_parser(
        "stats", help="Show overall feedback statistics"
    )

    # Corrections command
    corrections_parser = subparsers.add_parser(
        "corrections", help="Show recent corrections"
    )
    corrections_parser.add_argument(
        "--limit", type=int, default=10, help="Number of corrections to show"
    )

    # Training command
    training_parser = subparsers.add_parser("training", help="Show training candidates")
    training_parser.add_argument(
        "--min-rating",
        type=int,
        default=4,
        help="Minimum rating for training candidates",
    )

    # Poor responses command
    poor_parser = subparsers.add_parser("poor", help="Show poorly rated responses")
    poor_parser.add_argument(
        "--max-rating", type=int, default=2, help="Maximum rating for poor responses"
    )
    poor_parser.add_argument(
        "--limit", type=int, default=10, help="Number of poor responses to show"
    )

    # Sessions command
    sessions_parser = subparsers.add_parser(
        "sessions", help="Show recent user sessions"
    )
    sessions_parser.add_argument(
        "--limit", type=int, default=5, help="Number of sessions to show"
    )

    # All command
    subparsers.add_parser("all", help="Show comprehensive dashboard")

    args = parser.parse_args()

    dashboard = FeedbackDashboard(args.db)

    if args.command == "stats":
        dashboard.show_stats()
    elif args.command == "corrections":
        dashboard.show_corrections(args.limit)
    elif args.command == "training":
        dashboard.show_training_candidates(args.min_rating)
    elif args.command == "poor":
        dashboard.show_poor_responses(args.max_rating, args.limit)
    elif args.command == "sessions":
        dashboard.show_sessions(args.limit)
    elif args.command == "all":
        dashboard.show_stats()
        print()
        dashboard.show_training_candidates()
        print()
        dashboard.show_corrections(5)
        print()
        dashboard.show_poor_responses(2, 5)
    else:
        print("📊 PepeluGPT Learning Dashboard")
        print("Available commands:")
        print("  stats      - Overall feedback statistics")
        print("  corrections- Recent user corrections")
        print("  training   - High-quality training candidates")
        print("  poor       - Poorly rated responses")
        print("  sessions   - Recent user sessions")
        print("  all        - Comprehensive dashboard")
        print("\nExample: python -m tools.feedback_dashboard stats")


if __name__ == "__main__":
    main()
