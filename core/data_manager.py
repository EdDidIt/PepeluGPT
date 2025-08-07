"""
Data Manager - Handles conditional parsing with caching strategies.
Implements hash-based validation, lazy initialization, and persistent storage.
"""

import hashlib
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.utils import get_logger

LOG = get_logger(__name__)


class DataManager:
    """
    Singleton data manager that implements conditional parsing strategies:
    1. Check for parsed output first
    2. Use hash/timestamp validation
    3. Lazy initialization with caching
    """

    _instance = None
    _parsed_data = None
    _data_hash = None
    _last_modified = None

    def __new__(cls, config: Optional[Dict[str, Any]] = None):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if self._initialized:
            return

        self.config = config or {}
        self.cache_dir = Path(self.config.get("cache_dir", "cyber_vector_db"))
        self.cache_dir.mkdir(exist_ok=True)

        # Cache file paths
        self.parsed_data_path = self.cache_dir / "parsed_data.pkl"
        self.metadata_cache_path = self.cache_dir / "cache_metadata.json"
        self.hash_cache_path = self.cache_dir / "data_hashes.json"

        # Source data directory
        self.source_dir = Path(self.config.get("source_dir", "cyber_documents"))

        self._initialized = True
        LOG.debug("🔵 DataManager initialized")

    def get_data(self, force_refresh: bool = False) -> Any:
        """
        Main method to get parsed data with conditional parsing.

        Args:
            force_refresh: Force re-parsing even if cached data exists

        Returns:
            Parsed data object
        """
        if force_refresh:
            LOG.info("🔵 Force refresh requested - clearing cache")
            self._clear_cache()

        # Strategy 1: Check for parsed output first
        if self._parsed_data is not None and not force_refresh:
            LOG.debug("🔵 Returning cached data from memory")
            return self._parsed_data

        # Strategy 2: Check if data has changed using hash validation
        if not force_refresh and self._data_unchanged():
            LOG.info("🔵 Data unchanged - loading from persistent cache")
            self._parsed_data = self._load_parsed_data()
            if self._parsed_data is not None:
                return self._parsed_data

        # Strategy 3: Parse fresh data (lazy initialization)
        LOG.info("🔵 Parsing fresh data")
        raw_data = self._load_raw_data()
        self._parsed_data = self._parse_raw_data(raw_data)
        self._save_parsed_data(self._parsed_data)
        self._update_cache_metadata()

        return self._parsed_data

    def _data_unchanged(self) -> bool:
        """
        Check if source data has changed using hash validation.

        Returns:
            True if data is unchanged, False otherwise
        """
        try:
            current_hashes = self._calculate_data_hashes()
            stored_hashes = self._load_stored_hashes()

            if stored_hashes is None:
                LOG.debug("🔵 No stored hashes found")
                return False

            # Compare hashes
            if current_hashes == stored_hashes:
                LOG.debug("🔵 Data hashes match - no changes detected")
                return True
            else:
                LOG.debug("🔵 Data hashes differ - changes detected")
                self._save_data_hashes(current_hashes)
                return False

        except Exception as e:
            LOG.warning(f"🟡 Error checking data changes: {e}")
            return False

    def _calculate_data_hashes(self) -> Dict[str, str]:
        """
        Calculate hash for all source files.

        Returns:
            Dictionary mapping file paths to their hashes
        """
        hashes: Dict[str, str] = {}

        if not self.source_dir.exists():
            LOG.warning(f"🟡 Source directory not found: {self.source_dir}")
            return hashes

        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file():
                try:
                    # Use file size + modification time as a faster alternative to full file hash
                    stat = file_path.stat()
                    # Create a simple hash from size and mtime (much faster than reading file)
                    file_signature = f"{stat.st_size}:{stat.st_mtime}"
                    file_hash = hashlib.md5(file_signature.encode()).hexdigest()
                    hashes[str(file_path.relative_to(self.source_dir))] = file_hash
                except Exception as e:
                    LOG.warning(f"🟡 Error hashing file {file_path}: {e}")

        LOG.debug(f"🔵 Calculated hashes for {len(hashes)} files")
        return hashes

    def _load_stored_hashes(self) -> Optional[Dict[str, str]]:
        """Load previously stored file hashes."""
        try:
            if self.hash_cache_path.exists():
                with open(self.hash_cache_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            LOG.warning(f"🟡 Error loading stored hashes: {e}")
        return None

    def _save_data_hashes(self, hashes: Dict[str, str]) -> None:
        """Save file hashes to cache."""
        try:
            with open(self.hash_cache_path, "w") as f:
                json.dump(hashes, f, indent=2)
            LOG.debug("🔵 Data hashes saved to cache")
        except Exception as e:
            LOG.error(f"🔴 Error saving data hashes: {e}")

    def _load_raw_data(self) -> List[Path]:
        """
        Load raw data file paths from source directory.

        Returns:
            List of file paths to process
        """
        if not self.source_dir.exists():
            LOG.error(f"🔴 Source directory not found: {self.source_dir}")
            return []

        file_paths: List[Path] = []
        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file():
                file_paths.append(file_path)

        LOG.info(f"🔵 Found {len(file_paths)} files to process")
        return file_paths

    def _parse_raw_data(self, raw_data: List[Path]) -> Dict[str, Any]:
        """
        Parse raw data files. This is where the actual parsing logic goes.

        Args:
            raw_data: List of file paths to parse

        Returns:
            Parsed data structure
        """
        from processing.parse import ParserCoordinator

        parsed_data: Dict[str, Any] = {
            "files": {},
            "metadata": {
                "total_files": len(raw_data),
                "parsed_at": datetime.now().isoformat(),
                "parser_version": "1.0.0",
            },
        }

        # Initialize parser coordinator
        parser_coordinator = ParserCoordinator(self.config)

        for file_path in raw_data:
            try:
                LOG.debug(f"🔵 Parsing file: {file_path}")
                parsed_content = parser_coordinator.parse(str(file_path))

                # Convert list content to string if needed
                if isinstance(parsed_content, list):
                    content_str = "\n\n".join(
                        str(item) for item in parsed_content if item
                    )
                else:
                    content_str = str(parsed_content) if parsed_content else ""

                parsed_data["files"][str(file_path.relative_to(self.source_dir))] = {
                    "content": content_str,
                    "raw_content": parsed_content,  # Keep original for advanced processing
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat(),
                }
            except Exception as e:
                LOG.error(f"🔴 Error parsing {file_path}: {e}")
                parsed_data["files"][str(file_path.relative_to(self.source_dir))] = {
                    "error": str(e),
                    "content": None,
                }

        LOG.info(
            f"🟢 Successfully parsed {len([f for f in parsed_data['files'].values() if f.get('content')])} files"
        )
        return parsed_data

    def _load_parsed_data(self) -> Optional[Any]:
        """Load parsed data from persistent cache."""
        try:
            if self.parsed_data_path.exists():
                with open(self.parsed_data_path, "rb") as f:
                    data = pickle.load(f)
                LOG.debug("🔵 Loaded parsed data from cache")
                return data
        except Exception as e:
            LOG.warning(f"🟡 Error loading parsed data cache: {e}")
        return None

    def _save_parsed_data(self, data: Any) -> None:
        """Save parsed data to persistent cache."""
        try:
            with open(self.parsed_data_path, "wb") as f:
                pickle.dump(data, f)
            LOG.debug("🔵 Saved parsed data to cache")
        except Exception as e:
            LOG.error(f"🔴 Error saving parsed data: {e}")

    def _update_cache_metadata(self) -> None:
        """Update cache metadata with current timestamp and info."""
        metadata: Dict[str, Any] = {
            "last_updated": datetime.now().isoformat(),
            "cache_version": "1.0.0",
            "total_files": (
                len(self._parsed_data.get("files", {})) if self._parsed_data else 0
            ),
        }

        try:
            with open(self.metadata_cache_path, "w") as f:
                json.dump(metadata, f, indent=2)
            LOG.debug("🔵 Updated cache metadata")
        except Exception as e:
            LOG.error(f"🔴 Error updating cache metadata: {e}")

    def _clear_cache(self) -> None:
        """Clear all cached data and force fresh parsing."""
        self._parsed_data = None
        self._data_hash = None

        # Remove cache files
        for cache_file in [
            self.parsed_data_path,
            self.metadata_cache_path,
            self.hash_cache_path,
        ]:
            try:
                if cache_file.exists():
                    cache_file.unlink()
                    LOG.debug(f"🔵 Removed cache file: {cache_file}")
            except Exception as e:
                LOG.warning(f"🟡 Error removing cache file {cache_file}: {e}")

    def is_data_available(self) -> bool:
        """
        Check if data is already loaded in memory or available in cache.

        Returns:
            True if data is readily available, False if it needs to be loaded/parsed
        """
        # Check if data is already in memory
        if self._parsed_data is not None:
            LOG.debug("🔵 Data available in memory")
            return True

        # Check if cached data exists
        if self.parsed_data_path.exists():
            # Try to load stored hashes to check if cache is valid
            stored_hashes = self._load_stored_hashes()
            if stored_hashes is not None:
                # We have hash information, check if data is unchanged
                if self._data_unchanged():
                    LOG.debug("🔵 Valid cached data available (hash verified)")
                    return True
                else:
                    LOG.debug("🔵 Cached data exists but is outdated")
                    return False
            else:
                # No hash info, but cache exists - assume it's usable
                # This happens when cache exists but hash validation hasn't been set up yet
                LOG.debug("🔵 Cached data available (no hash verification)")
                return True

        LOG.debug("🔵 No cached data available - will need to parse from source")
        return False

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the current cache state.

        Returns:
            Dictionary with cache information
        """
        info: Dict[str, Any] = {
            "memory_cache_loaded": self._parsed_data is not None,
            "persistent_cache_exists": self.parsed_data_path.exists(),
            "hash_cache_exists": self.hash_cache_path.exists(),
            "cache_directory": str(self.cache_dir),
        }

        # Add metadata if available
        try:
            if self.metadata_cache_path.exists():
                with open(self.metadata_cache_path, "r") as f:
                    info["cache_metadata"] = json.load(f)
        except Exception as e:
            LOG.warning(f"🟡 Error reading cache metadata: {e}")

        return info

    def invalidate_cache(self) -> None:
        """Public method to invalidate cache and force refresh on next access."""
        LOG.info("🔵 Cache invalidated - will refresh on next access")
        self._clear_cache()

    @classmethod
    def reset_singleton(cls):
        """Reset singleton instance (useful for testing)."""
        cls._instance = None
        cls._parsed_data = None
        cls._data_hash = None
        cls._last_modified = None
