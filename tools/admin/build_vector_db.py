#!/usr/bin/env python3
"""
Vector Database Builder - Create FAISS index from parsed documents.
"""

import argparse
import pickle
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import yaml

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.data_manager import DataManager
from core.utils import get_logger
from storage.vector_db.chunking import chunk_text

LOG = get_logger(__name__)


def load_config(config_path: str = "../../config/active_config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        # Handle both relative and absolute paths
        if not Path(config_path).is_absolute():
            # If running from admin directory, adjust path
            config_path = str(Path(__file__).parent / config_path)

        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        LOG.error(f"🔴 Error loading config: {e}")
        return {}


def create_simple_embeddings(text_chunks: List[str]) -> np.ndarray:
    """
    Create simple embeddings for demonstration.
    In a real implementation, you'd use sentence-transformers or similar.
    """
    print("🔵 Creating simple TF-IDF style embeddings...")

    # Simple character-based features for demonstration
    embeddings: List[List[float]] = []
    for chunk in text_chunks:
        # Create a simple feature vector based on text characteristics
        features: List[float] = [
            float(len(chunk)),  # text length
            float(chunk.count(" ")),  # word count approximation
            float(chunk.count(".")),  # sentence count approximation
            float(chunk.count("cyber")),  # cybersecurity keyword count
            float(chunk.count("security")),
            float(chunk.count("control")),
            float(chunk.count("NIST")),
            float(chunk.count("compliance")),
            float(chunk.count("risk")),
            float(chunk.count("policy")),
        ]

        # Pad to consistent dimension
        while len(features) < 128:
            features.append(0.0)

        embeddings.append(features[:128])  # Ensure consistent dimension

    return np.array(embeddings, dtype=np.float32)


def build_vector_database(args: argparse.Namespace):
    """Build the vector database from parsed documents."""
    config = load_config(args.config)

    print("🔵 Building Vector Database")
    print("=" * 50)

    # Initialize data manager
    data_manager = DataManager(config.get("data_management", {}))

    # Get parsed data
    print("🔵 Loading parsed data...")
    data = data_manager.get_data()

    if not data or not data.get("files"):
        print("🔴 No parsed data found. Run data parsing first.")
        return False

    # Extract text content and create chunks
    print("🔵 Creating text chunks...")
    chunk_size = config.get("vector_db", {}).get("chunk_size", 1000)
    overlap = config.get("vector_db", {}).get("overlap", 200)

    chunks: List[str] = []
    chunk_metadata: List[Dict[str, Any]] = []

    for filename, file_data in data["files"].items():
        content = file_data.get("content")
        if content and isinstance(content, str):
            # Create chunks from this file
            file_chunks = chunk_text(content, chunk_size, overlap)

            for i, chunk in enumerate(file_chunks):
                if len(chunk.strip()) > 50:  # Skip very small chunks
                    chunks.append(chunk)
                    chunk_metadata.append(
                        {
                            "source_file": filename,
                            "chunk_index": i,
                            "chunk_size": len(chunk),
                            "file_size": file_data.get("size", 0),
                        }
                    )

    print(f"🔵 Created {len(chunks)} chunks from {len(data['files'])} files")

    if not chunks:
        print("🔴 No text chunks created. Check document parsing.")
        return False

    # Create embeddings
    print("🔵 Generating embeddings...")
    try:
        embeddings = create_simple_embeddings(chunks)
        print(f"🔵 Generated embeddings shape: {embeddings.shape}")
    except Exception as e:
        LOG.error(f"🔴 Error creating embeddings: {e}")
        return False

    # Save vector database
    vector_config = config.get("vector_db", {})
    index_path = vector_config.get("index_path", "cyber_vector_db/faiss_index.bin")
    metadata_path = vector_config.get("metadata_path", "cyber_vector_db/metadata.pkl")

    # Ensure directories exist
    Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    Path(metadata_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        # Try to use FAISS if available
        import faiss  # type: ignore[import-untyped]

        print("🔵 Building FAISS index...")

        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)  # type: ignore[attr-defined]
        index.add(embeddings)  # type: ignore[attr-defined]

        # Save FAISS index
        faiss.write_index(index, index_path)  # type: ignore[attr-defined]
        print(f"🟢 FAISS index saved to: {index_path}")

    except ImportError:
        print("🟡 FAISS not available, saving embeddings as numpy array...")
        np.save(index_path.replace(".bin", ".npy"), embeddings)

    # Save metadata
    metadata: Dict[str, Any] = {
        "chunks": chunks,
        "chunk_metadata": chunk_metadata,
        "embeddings_shape": embeddings.shape,
        "total_chunks": len(chunks),
        "total_files": len(data["files"]),
        "created_at": data.get("metadata", {}).get("parsed_at"),
        "vector_config": vector_config,
    }

    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)

    print(f"🟢 Metadata saved to: {metadata_path}")
    print(f"🟢 Vector database built successfully!")
    print(f"🔵 Total chunks: {len(chunks)}")
    print(f"🔵 Embedding dimension: {embeddings.shape[1]}")

    return True


def check_vector_database(args: argparse.Namespace):
    """Check the status of the vector database."""
    config = load_config(args.config)
    vector_config = config.get("vector_db", {})

    index_path = vector_config.get("index_path", "cyber_vector_db/faiss_index.bin")
    metadata_path = vector_config.get("metadata_path", "cyber_vector_db/metadata.pkl")

    print("🔵 Vector Database Status")
    print("=" * 50)

    # Check index
    index_exists = Path(index_path).exists()
    npy_path = index_path.replace(".bin", ".npy")
    npy_exists = Path(npy_path).exists()

    print(f"FAISS Index ({index_path}): {'✅' if index_exists else '❌'}")
    print(f"NumPy Array ({npy_path}): {'✅' if npy_exists else '❌'}")

    # Check metadata
    metadata_exists = Path(metadata_path).exists()
    print(f"Metadata ({metadata_path}): {'✅' if metadata_exists else '❌'}")

    if metadata_exists:
        try:
            with open(metadata_path, "rb") as f:
                metadata = pickle.load(f)

            print(f"\n🔵 Vector Database Info:")
            print(f"  Total chunks: {metadata.get('total_chunks', 'Unknown')}")
            print(f"  Total files: {metadata.get('total_files', 'Unknown')}")
            print(f"  Embeddings shape: {metadata.get('embeddings_shape', 'Unknown')}")
            print(f"  Created at: {metadata.get('created_at', 'Unknown')}")

        except Exception as e:
            print(f"🔴 Error reading metadata: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="PepeluGPT Vector Database Builder")
    parser.add_argument(
        "--config",
        "-c",
        default="../../config/active_config.yaml",
        help="Configuration file path",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    subparsers.add_parser("build", help="Build vector database")

    # Status command
    subparsers.add_parser("status", help="Check vector database status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Setup logging
    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Execute command
    try:
        if args.command == "build":
            success = build_vector_database(args)
            sys.exit(0 if success else 1)
        elif args.command == "status":
            check_vector_database(args)
    except Exception as e:
        print(f"🔴 Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
