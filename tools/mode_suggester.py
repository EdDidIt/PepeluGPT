"""
Smart Mode Suggestion Engine for PepeluGPT

Analyzes user queries and suggests optimal mode based on intent classification.
"""

import re
from typing import Any, Dict, List, Optional

from core.utils import get_logger

LOG = get_logger(__name__)


class ModeSuggester:
    """Analyzes queries and suggests optimal mode for better responses."""

    def __init__(self):
        # Query patterns that suggest learning mode
        self.learning_patterns = [
            # Exploratory queries
            r"\b(explain|what is|how does|why|tell me about|help me understand)\b",
            r"\b(explore|research|investigate|analyze|compare)\b",
            r"\b(learn|teach|show me|walk me through)\b",
            # Conceptual questions
            r"\b(concept|theory|approach|methodology|best practice)\b",
            r"\b(trend|evolution|future|emerging)\b",
            # Open-ended queries
            r"\?.*\?",  # Multiple questions
            r"\b(thoughts|opinion|perspective|insights)\b",
            # Creative tasks
            r"\b(brainstorm|ideate|suggest|recommend|creative)\b",
            r"\b(alternative|different|various|multiple)\b",
        ]

        # Query patterns that suggest deterministic mode
        self.deterministic_patterns = [
            # Specific procedures
            r"\b(steps|procedure|process|workflow|checklist)\b",
            r"\b(exact|precise|specific|detailed|step-by-step)\b",
            r"\b(compliance|audit|requirement|standard|regulation)\b",
            # Factual queries
            r"\b(definition|meaning|acronym|stands for)\b",
            r"\b(list|enumerate|show all|complete list)\b",
            r"\b(requirement|specification|criteria)\b",
            # Commands/Actions
            r"\b(configure|install|setup|implement|deploy)\b",
            r"\b(fix|troubleshoot|resolve|solve)\b",
            r"\b(check|verify|validate|test)\b",
            # Documentation queries
            r"\b(documentation|manual|guide|reference)\b",
            r"\b(format|template|example|sample)\b",
        ]

        # Context keywords that influence suggestions
        self.context_weights = {
            "adaptive": {
                "research": 0.8,
                "exploration": 0.7,
                "understanding": 0.6,
                "learning": 0.9,
                "creative": 0.7,
            },
            "classic": {
                "compliance": 0.9,
                "audit": 0.8,
                "production": 0.8,
                "procedure": 0.7,
                "exact": 0.8,
            },
        }

        # Legacy mode mapping for backward compatibility
        self.legacy_mode_mapping = {"learning": "adaptive", "deterministic": "classic"}

    def suggest_mode(
        self, query: str, current_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze query and suggest optimal mode.

        Args:
            query: User's query text
            current_mode: Currently active mode

        Returns:
            Dict with suggestion details
        """
        query_lower = query.lower()

        # Calculate scores for each mode
        adaptive_score = self._calculate_mode_score(query_lower, "adaptive")
        classic_score = self._calculate_mode_score(query_lower, "classic")

        # Determine suggested mode
        if adaptive_score > classic_score:
            suggested_mode = "adaptive"
            confidence = min(adaptive_score / (adaptive_score + classic_score), 0.95)
        elif classic_score > adaptive_score:
            suggested_mode = "classic"
            confidence = min(classic_score / (adaptive_score + classic_score), 0.95)
        else:
            # No clear preference, stick with current mode
            suggested_mode = current_mode or "classic"
            confidence = 0.5

        # Generate explanation
        explanation = self._generate_explanation(
            query_lower, suggested_mode, confidence
        )

        return {
            "suggested_mode": suggested_mode,
            "current_mode": current_mode,
            "confidence": confidence,
            "should_suggest": confidence > 0.7 and suggested_mode != current_mode,
            "explanation": explanation,
            "scores": {"adaptive": adaptive_score, "classic": classic_score},
        }

    def _calculate_mode_score(self, query: str, mode: str) -> float:
        """Calculate how well a query matches a specific mode."""
        score = 0.0

        # Handle legacy mode names
        if mode == "learning":
            mode = "adaptive"
        elif mode == "deterministic":
            mode = "classic"

        # Pattern matching
        patterns = (
            self.learning_patterns
            if mode == "adaptive"
            else self.deterministic_patterns
        )
        for pattern in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                score += 1.0

        # Context keyword weighting
        if mode in self.context_weights:
            for keyword, weight in self.context_weights[mode].items():
                if keyword in query:
                    score += weight

        # Query characteristics
        if mode == "adaptive":
            # Favor longer, more complex queries
            if len(query.split()) > 10:
                score += 0.5
            # Multiple questions suggest exploration
            if query.count("?") > 1:
                score += 0.3
            # Uncertainty markers
            if any(word in query for word in ["might", "could", "perhaps", "maybe"]):
                score += 0.2

        elif mode == "classic":
            # Favor direct, specific queries
            if len(query.split()) < 8:
                score += 0.3
            # Imperative mood
            if re.search(r"^(show|tell|give|list|explain)", query):
                score += 0.4
            # Specific technical terms
            tech_terms = ["rmf", "nist", "stig", "cci", "dod", "compliance", "audit"]
            for term in tech_terms:
                if term in query:
                    score += 0.2

        return score

    def _generate_explanation(
        self, query: str, suggested_mode: str, confidence: float
    ) -> str:
        """Generate human-readable explanation for the suggestion."""
        if confidence < 0.6:
            return f"Query could work well in either mode. Staying with current mode."

        if suggested_mode == "adaptive":
            reasons: List[str] = []
            if any(word in query for word in ["explain", "what", "how", "why"]):
                reasons.append("exploratory question")
            if any(word in query for word in ["concept", "understand", "learn"]):
                reasons.append("conceptual learning")
            if len(query.split()) > 10:
                reasons.append("complex query")

            reason_text = ", ".join(reasons) if reasons else "exploratory nature"
            return f"Adaptive mode suggested due to {reason_text}. Adaptive responses and feedback would be valuable."

        else:  # classic
            reasons: List[str] = []
            if any(word in query for word in ["steps", "procedure", "how to"]):
                reasons.append("procedural request")
            if any(word in query for word in ["exact", "specific", "precise"]):
                reasons.append("need for precision")
            if any(word in query for word in ["compliance", "audit", "standard"]):
                reasons.append("compliance focus")

            reason_text = ", ".join(reasons) if reasons else "need for consistency"
            return f"Classic mode suggested due to {reason_text}. Rule-based responses ensure reliability."

    def get_suggestion_prompt(self, suggestion: Dict[str, Any]) -> Optional[str]:
        """Generate user-friendly suggestion prompt."""
        if not suggestion["should_suggest"]:
            return None

        mode = suggestion["suggested_mode"]
        confidence = suggestion["confidence"]
        explanation = suggestion["explanation"]

        mode_emoji = "🧠" if mode == "learning" else "⚡"
        confidence_text = "strongly" if confidence > 0.8 else "moderately"

        return (
            f"\n💡 Mode Suggestion: I {confidence_text} recommend switching to "
            f"{mode_emoji} {mode.upper()} mode for this type of query.\n"
            f"   Reason: {explanation}\n"
            f"   Use 'mode {mode}' to switch, or continue in current mode.\n"
        )


def suggest_mode_for_query(
    query: str, current_mode: Optional[str] = None
) -> Dict[str, Any]:
    """Convenience function for mode suggestion."""
    suggester = ModeSuggester()
    return suggester.suggest_mode(query, current_mode)
