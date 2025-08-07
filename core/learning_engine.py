"""
Learning Engine - Phase 1 Implementation
Hybrid approach combining LLM with existing rule-based system.
"""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

# Placeholder imports - would need actual implementations
try:
    import chromadb  # type: ignore
    from sentence_transformers import SentenceTransformer  # type: ignore
    from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore

    has_ml_deps = True
except ImportError:
    has_ml_deps = False

# Make it available as a module constant
HAS_ML_DEPS: bool = has_ml_deps

if TYPE_CHECKING:
    from core.data_manager import DataManager

from core.utils import get_logger

LOG = get_logger(__name__)


@dataclass
class FeedbackEntry:
    """Structure for storing user feedback."""

    query: str
    response: str
    rating: int  # 1-5 stars
    correction: Optional[str] = None
    timestamp: Optional[datetime] = None
    session_id: Optional[str] = None


@dataclass
class ResponseContext:
    """Context for generating and improving responses."""

    query: str
    query_type: str  # 'nist_control', 'acronym', 'general'
    confidence: float
    sources: List[str]
    reasoning: Optional[str] = None


class FeedbackDatabase:
    """Manages storage and retrieval of user feedback."""

    def __init__(self, db_path: str = "feedback.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for feedback storage."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    correction TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS training_examples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    ideal_response TEXT NOT NULL,
                    source TEXT NOT NULL,
                    quality_score REAL DEFAULT 1.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def store_feedback(self, feedback: FeedbackEntry):
        """Store user feedback in database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO feedback (query, response, rating, correction, session_id)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    feedback.query,
                    feedback.response,
                    feedback.rating,
                    feedback.correction,
                    feedback.session_id,
                ),
            )

    def get_training_data(self, min_rating: int = 4) -> List[Dict[str, Any]]:
        """Retrieve high-quality examples for training."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT query, response, correction, rating
                FROM feedback 
                WHERE rating >= ?
                ORDER BY timestamp DESC
            """,
                (min_rating,),
            )

            examples: List[Dict[str, Any]] = []
            for query, response, correction, rating in cursor.fetchall():
                # Use correction if available, otherwise use original response
                ideal_response = correction if correction else response
                examples.append(
                    {
                        "query": query,
                        "response": ideal_response,
                        "quality_score": rating / 5.0,
                    }
                )

            return examples


class LearningEngine:
    """
    Enhanced engine that combines LLM capabilities with rule-based fallbacks.
    Implements learning through user feedback and model fine-tuning.
    """

    def __init__(self, config: Dict[str, Any], data_manager: Optional["DataManager"] = None):
        self.config = config
        self.data_manager = data_manager
        self.feedback_db = FeedbackDatabase()

        # Learning configuration
        self.learning_config = config.get("learning", {})
        self.confidence_threshold = self.learning_config.get(
            "confidence_threshold", 0.8
        )
        self.correction_weight = self.learning_config.get("correction_weight", 2.0)

        # Initialize ML components if available
        self.llm_available = HAS_ML_DEPS
        if self.llm_available:
            self._init_ml_components()
        else:
            LOG.warning(
                "ML dependencies not available, falling back to rule-based system"
            )

        # Import existing engine for fallback
        from core.engine import Engine

        self.fallback_engine = Engine(config, data_manager)

        # Correction overrides - dynamic responses based on user feedback
        self.correction_overrides: Dict[str, str] = self._load_correction_overrides()

        # Session context with enhanced tracking
        self.session_history: List[Dict[str, Any]] = []
        self.session_feedback: List[Dict[str, Any]] = []
        self.session_id = self._generate_session_id()

    def _init_ml_components(self):
        """Initialize ML models and vector store."""
        try:
            # Initialize LLM (start with smaller model for development)
            model_name = self.config.get("llm", {}).get(
                "model", "microsoft/DialoGPT-small"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)  # type: ignore
            self.model = AutoModelForCausalLM.from_pretrained(model_name)  # type: ignore

            # Initialize embeddings
            self.embeddings = SentenceTransformer("all-MiniLM-L6-v2")  # type: ignore

            # Initialize vector store
            self.vector_client = chromadb.Client()  # type: ignore
            self.collection = self.vector_client.get_or_create_collection(  # type: ignore
                name="cybersecurity_knowledge"
            )

            LOG.info("ML components initialized successfully")
        except Exception as e:
            LOG.error(f"Failed to initialize ML components: {e}")
            self.llm_available = False

    def _generate_session_id(self) -> str:
        """Generate unique session identifier."""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def _load_correction_overrides(self) -> Dict[str, str]:
        """Load correction overrides from user feedback with corrections."""
        overrides: Dict[str, str] = {}
        try:
            # Get all entries that have corrections (regardless of rating)
            with sqlite3.connect(self.feedback_db.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT query, correction 
                    FROM feedback 
                    WHERE correction IS NOT NULL AND correction != ''
                    ORDER BY timestamp DESC
                """
                )

                for query, correction in cursor.fetchall():
                    query_normalized = query.lower().strip()
                    # Use the correction as the override response
                    overrides[query_normalized] = correction

            LOG.info(f"Loaded {len(overrides)} correction overrides")
            return overrides

        except Exception as e:
            LOG.warning(f"Could not load correction overrides: {e}")
            return {}

    def _check_correction_override(self, query: str) -> Optional[str]:
        """Check if this query has a user-corrected override response."""
        query_normalized = query.lower().strip()
        return self.correction_overrides.get(query_normalized)

    def _add_to_session(self, query: str, response: str, context: ResponseContext):
        """Add interaction to session history with enhanced tracking."""
        entry: Dict[str, Any] = {
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "query_type": context.query_type,
            "confidence": context.confidence,
            "sources": context.sources,
            "reasoning": context.reasoning,
        }

        self.session_history.append(entry)

    def process_query(self, query: str) -> Tuple[str, ResponseContext]:
        """
        Process query using hybrid approach: LLM + rules + learning + corrections.

        Args:
            query: User input query

        Returns:
            Tuple of (response, context)
        """
        try:
            # First check for user correction overrides
            correction_override = self._check_correction_override(query)
            if correction_override:
                context = ResponseContext(
                    query=query,
                    query_type="correction_override",
                    confidence=1.0,
                    sources=["User Correction"],
                    reasoning="Response from high-quality user correction",
                )

                # Store in session history
                self._add_to_session(query, correction_override, context)
                return correction_override, context

            # Determine query type and confidence
            query_type, confidence = self._classify_query(query)

            # Generate response using appropriate method based on configurable threshold
            if confidence > self.confidence_threshold and self.llm_available:
                response = self._generate_llm_response(query, query_type)
                sources = ["LLM Generation"]
                reasoning = f"High confidence ({confidence:.2f}) LLM response"
            else:
                # Fallback to rule-based system
                response = self.fallback_engine.process_query(query)
                sources = ["Rule-based System"]
                reasoning = f"Confidence below threshold ({confidence:.2f} < {self.confidence_threshold}) or LLM unavailable"

            # Create response context
            context = ResponseContext(
                query=query,
                query_type=query_type,
                confidence=confidence,
                sources=sources,
                reasoning=reasoning,
            )

            # Store in session history with enhanced tracking
            self._add_to_session(query, response, context)

            return response, context

        except Exception as e:
            LOG.error(f"Error processing query: {e}")
            # Always fallback to existing system
            response = self.fallback_engine.process_query(query)
            context = ResponseContext(
                query=query,
                query_type="fallback",
                confidence=0.0,
                sources=["Fallback System"],
                reasoning=f"Error occurred: {str(e)}",
            )
            self._add_to_session(query, response, context)
            return response, context

    def _classify_query(self, query: str) -> Tuple[str, float]:
        """Classify query type and determine confidence."""
        query_lower = query.lower()

        # NIST control patterns
        if any(pattern in query_lower for pattern in ["ac-", "cm-", "cp-", "pe-"]):
            return "nist_control", 0.9

        # Acronym patterns
        if any(word in query_lower for word in ["stand for", "what is", "nist", "cia"]):
            return "acronym", 0.8

        # General cybersecurity
        cyber_terms = ["security", "cyber", "compliance", "risk", "vulnerability"]
        if any(term in query_lower for term in cyber_terms):
            return "cybersecurity", 0.7

        return "general", 0.5

    def _generate_llm_response(self, query: str, query_type: str) -> str:
        """Generate response using LLM with cybersecurity context."""
        if not self.llm_available:
            raise Exception("LLM not available")

        # Retrieve relevant context from vector store
        context = self._get_relevant_context(query)

        # Build prompt with context
        prompt = self._build_prompt(query, context, query_type)

        # Generate response
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")  # type: ignore
        outputs = self.model.generate(  # type: ignore
            inputs,
            max_length=inputs.shape[1] + 200,  # type: ignore
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,  # type: ignore
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)  # type: ignore

        # Extract just the new response part
        response = response[len(prompt) :].strip()  # type: ignore

        return response  # type: ignore

    def _get_relevant_context(self, query: str) -> str:
        """Retrieve relevant context from vector store."""
        if not self.llm_available:
            return ""

        try:
            # Get embeddings for query
            query_embedding = self.embeddings.encode([query])  # type: ignore

            # Search vector store
            results = self.collection.query(  # type: ignore
                query_embeddings=query_embedding.tolist(), n_results=3  # type: ignore
            )

            # Combine relevant documents
            context_parts: List[str] = []
            if results["documents"]:  # type: ignore
                for docs in results["documents"]:  # type: ignore
                    context_parts.extend(docs)  # type: ignore

            return "\n\n".join(context_parts[:500])  # Limit context length

        except Exception as e:
            LOG.error(f"Error retrieving context: {e}")
            return ""

    def _build_prompt(self, query: str, context: str, query_type: str) -> str:
        """Build prompt for LLM with appropriate context."""
        system_prompt = """You are a cybersecurity expert assistant specializing in NIST frameworks, 
        compliance, and security controls. Provide accurate, concise, and helpful responses."""

        if context:
            prompt = f"""{system_prompt}

Context information:
{context}

User question: {query}

Response:"""
        else:
            prompt = f"""{system_prompt}

User question: {query}

Response:"""

        return prompt

    def collect_feedback(
        self, query: str, response: str, rating: int, correction: Optional[str] = None
    ) -> None:
        """Collect user feedback for continuous learning with enhanced weighting."""
        # Weight corrections more heavily than regular ratings
        effective_rating = rating
        if correction:
            # Corrections get weighted higher priority for learning
            effective_rating = min(5, int(rating * self.correction_weight))

        feedback = FeedbackEntry(
            query=query,
            response=response,
            rating=effective_rating,
            correction=correction,
            timestamp=datetime.now(),
            session_id=self.session_id,
        )

        self.feedback_db.store_feedback(feedback)

        # Add to session feedback tracking
        feedback_entry: Dict[str, Any] = {
            "query": query,
            "response": response,
            "rating": rating,
            "effective_rating": effective_rating,
            "correction": correction,
            "timestamp": datetime.now().isoformat(),
        }
        self.session_feedback.append(feedback_entry)

        LOG.info(
            f"Feedback collected: {rating}/5 stars (effective: {effective_rating}/5)"
        )

        # If it's a high-quality correction, add to overrides immediately
        if correction and effective_rating >= 4:
            query_normalized = query.lower().strip()
            self.correction_overrides[query_normalized] = correction
            LOG.info(f"Added correction override for: {query[:50]}...")

        # Trigger learning check
        self._check_learning_trigger()

    def _check_learning_trigger(self):
        """Enhanced learning trigger with correction prioritization."""
        # Get training data with different thresholds
        high_quality_data = self.feedback_db.get_training_data(min_rating=4)
        correction_data = [
            item for item in high_quality_data if "correction" in str(item)
        ]

        total_examples = len(high_quality_data)
        correction_examples = len(correction_data)
        min_threshold = self.learning_config.get("min_training_examples", 10)

        LOG.info(
            f"Learning readiness: {total_examples} total examples, {correction_examples} corrections"
        )

        if total_examples >= min_threshold:
            LOG.info(
                f"✅ Learning trigger: {total_examples} high-quality examples available"
            )
            if correction_examples >= 3:
                LOG.info(f"💡 High-value corrections available: {correction_examples}")
            # TODO: Implement actual learning pipeline in Phase 2
        else:
            remaining = min_threshold - total_examples
            LOG.debug(
                f"Need {remaining} more high-quality examples for learning trigger"
            )

    def get_session_context(self) -> Dict[str, Any]:
        """Get enhanced session conversation history with feedback."""
        return {
            "history": self.session_history.copy(),
            "feedback": self.session_feedback.copy(),
            "session_id": self.session_id,
            "total_interactions": len(self.session_history),
            "feedback_count": len(self.session_feedback),
            "avg_rating": sum(f.get("rating", 0) for f in self.session_feedback)
            / max(1, len(self.session_feedback)),
        }

    def update_knowledge_base(self, documents: List[Dict[str, str]]):
        """Add new documents to the knowledge base."""
        if not self.llm_available:
            LOG.warning("Cannot update knowledge base without ML components")
            return

        try:
            for doc in documents:
                # Generate embeddings
                embedding = self.embeddings.encode([doc["content"]])  # type: ignore

                # Add to vector store
                self.collection.add(  # type: ignore
                    embeddings=embedding.tolist(),  # type: ignore
                    documents=[doc["content"]],
                    metadatas=[
                        {
                            "source": doc.get("source", "unknown"),
                            "timestamp": datetime.now().isoformat(),
                        }
                    ],
                )

            LOG.info(f"Added {len(documents)} documents to knowledge base")

        except Exception as e:
            LOG.error(f"Error updating knowledge base: {e}")
