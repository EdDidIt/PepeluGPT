#!/usr/bin/env python3
"""
Plugin Registry for PepeluGPT Audit Framework.
Manages plugin discovery, loading, and metadata.
"""

import datetime
import importlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from .base import (
    AuditPlugin,
    PluginLoadError,
    PluginNotFoundError,
)


class PluginRegistry:
    """
    Manages plugin registration, discovery, and loading.
    """

    def __init__(
        self, plugins_dir: str = "plugins", registry_file: str = "registry.json"
    ):
        self.plugins_dir = Path(plugins_dir)
        self.registry_file = self.plugins_dir / registry_file
        self.registry_data = self._load_registry()
        self.loaded_plugins: Dict[str, AuditPlugin] = {}

        # Ensure plugins directory structure exists
        self._ensure_plugin_directories()

    def _ensure_plugin_directories(self) -> None:
        """Create plugin directory structure if it doesn't exist."""
        directories = [
            self.plugins_dir,
            self.plugins_dir / "core",
            self.plugins_dir / "custom",
            self.plugins_dir / "community",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

            # Create __init__.py files
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Plugin package\n")

    def _load_registry(self) -> Dict[str, Any]:
        """Load plugin registry from file."""
        if not self.registry_file.exists():
            return {
                "registry_version": "1.0",
                "plugins": {},
                "last_updated": datetime.datetime.now().isoformat(),
            }

        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error loading plugin registry: {e}")
            return {
                "registry_version": "1.0",
                "plugins": {},
                "last_updated": datetime.datetime.now().isoformat(),
            }

    def _save_registry(self) -> None:
        """Save plugin registry to file."""
        self.registry_data["last_updated"] = datetime.datetime.now().isoformat()

        try:
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(self.registry_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Error saving plugin registry: {e}")

    def discover_plugins(self) -> List[str]:
        """
        Discover all plugins in the plugins directory.

        Returns:
            List of plugin module names
        """
        discovered: List[str] = []

        # Search for Python files in plugin directories
        plugin_dirs = ["core", "custom", "community"]

        for plugin_dir in plugin_dirs:
            dir_path = self.plugins_dir / plugin_dir
            if not dir_path.exists():
                continue

            for py_file in dir_path.glob("*.py"):
                if py_file.name != "__init__.py":
                    module_name = f"{plugin_dir}.{py_file.stem}"
                    discovered.append(module_name)  # type: ignore

        return discovered

    def register_plugin(self, plugin_path: str, category: str = "custom") -> bool:
        """
        Register a new plugin in the registry.

        Args:
            plugin_path: Path to the plugin file
            category: Plugin category (core, custom, community)

        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Load and validate the plugin
            plugin_class = self._load_plugin_class(plugin_path)
            if not plugin_class:
                return False

            # Get plugin metadata
            plugin_instance = plugin_class()
            metadata_dict = plugin_instance.get_metadata()

            # Register in registry
            plugin_key = metadata_dict["framework"].lower().replace(" ", "-")
            self.registry_data["plugins"][plugin_key] = {
                "name": metadata_dict["name"],
                "version": metadata_dict["version"],
                "framework": metadata_dict["framework"],
                "description": metadata_dict["description"],
                "author": metadata_dict["author"],
                "category": category,
                "file": plugin_path,
                "controls": metadata_dict.get("controls", []),
                "requirements": metadata_dict.get("requirements", []),
                "enabled": True,
                "registered_at": datetime.datetime.now().isoformat(),
            }

            self._save_registry()
            print(f"✅ Plugin '{metadata_dict['name']}' registered successfully")
            return True

        except Exception as e:
            print(f"❌ Error registering plugin: {e}")
            return False

    def _load_plugin_class(self, plugin_path: str) -> Optional[Type[AuditPlugin]]:
        """
        Load a plugin class from a file path.

        Args:
            plugin_path: Path to the plugin file

        Returns:
            Plugin class if found and valid, None otherwise
        """
        try:
            # Convert relative path to absolute
            if not os.path.isabs(plugin_path):
                plugin_path = str(self.plugins_dir / plugin_path)

            # Add plugins directory to path for imports
            import sys

            plugins_path = str(self.plugins_dir.absolute())
            if plugins_path not in sys.path:
                sys.path.insert(0, plugins_path)

            # Load module from file
            spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
            if not spec or not spec.loader:
                raise PluginLoadError(f"Cannot load plugin from {plugin_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find plugin class in module
            plugin_class = None

            # Look for __plugin_class__ attribute first
            if hasattr(module, "__plugin_class__"):
                plugin_class = getattr(module, "__plugin_class__")
                if (
                    isinstance(plugin_class, type)
                    and issubclass(plugin_class, AuditPlugin)
                    and plugin_class != AuditPlugin
                ):
                    return plugin_class

            # Fall back to searching all classes in module
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (
                    isinstance(item, type)
                    and issubclass(item, AuditPlugin)
                    and item != AuditPlugin
                ):
                    print(f"✅ Found plugin class via search: {item}")
                    return item

            raise PluginLoadError(f"No valid plugin class found in {plugin_path}")

        except Exception as e:
            print(f"⚠️ Error loading plugin {plugin_path}: {e}")
            import traceback

            traceback.print_exc()
            return None

    def load_plugin(self, framework: str) -> Optional[AuditPlugin]:
        """
        Load a plugin by framework name.

        Args:
            framework: Framework identifier

        Returns:
            Plugin instance if found and loaded, None otherwise
        """
        plugin_key = framework.lower().replace(" ", "-")

        # Check if already loaded
        if plugin_key in self.loaded_plugins:
            return self.loaded_plugins[plugin_key]

        # Check registry
        plugin_info = self.registry_data["plugins"].get(plugin_key)
        if not plugin_info:
            raise PluginNotFoundError(f"Plugin '{framework}' not found in registry")

        if not plugin_info.get("enabled", True):
            raise PluginLoadError(f"Plugin '{framework}' is disabled")

        # Load plugin class
        plugin_class = self._load_plugin_class(plugin_info["file"])
        if not plugin_class:
            raise PluginLoadError(f"Failed to load plugin class for '{framework}'")

        # Create instance and cache
        plugin_instance = plugin_class()
        self.loaded_plugins[plugin_key] = plugin_instance

        return plugin_instance

    def list_plugins(self, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """
        List all registered plugins.

        Args:
            enabled_only: If True, only return enabled plugins

        Returns:
            List of plugin information dictionaries
        """
        plugins: List[Dict[str, Any]] = []

        for plugin_key, plugin_info in self.registry_data["plugins"].items():
            if enabled_only and not plugin_info.get("enabled", True):
                continue

            plugins.append(  # type: ignore
                {
                    "key": plugin_key,
                    "name": plugin_info["name"],
                    "framework": plugin_info["framework"],
                    "version": plugin_info["version"],
                    "description": plugin_info["description"],
                    "author": plugin_info.get("author", "Unknown"),
                    "category": plugin_info.get("category", "unknown"),
                    "enabled": plugin_info.get("enabled", True),
                    "controls": plugin_info.get("controls", []),
                    "file": plugin_info["file"],
                }
            )

        return plugins

    def enable_plugin(self, framework: str) -> bool:
        """Enable a plugin."""
        plugin_key = framework.lower().replace(" ", "-")

        if plugin_key not in self.registry_data["plugins"]:
            print(f"❌ Plugin '{framework}' not found")
            return False

        self.registry_data["plugins"][plugin_key]["enabled"] = True
        self._save_registry()
        print(f"✅ Plugin '{framework}' enabled")
        return True

    def disable_plugin(self, framework: str) -> bool:
        """Disable a plugin."""
        plugin_key = framework.lower().replace(" ", "-")

        if plugin_key not in self.registry_data["plugins"]:
            print(f"❌ Plugin '{framework}' not found")
            return False

        self.registry_data["plugins"][plugin_key]["enabled"] = False

        # Remove from loaded plugins cache
        if plugin_key in self.loaded_plugins:
            del self.loaded_plugins[plugin_key]

        self._save_registry()
        print(f"🔇 Plugin '{framework}' disabled")
        return True

    def unregister_plugin(self, framework: str) -> bool:
        """Remove a plugin from the registry."""
        plugin_key = framework.lower().replace(" ", "-")

        if plugin_key not in self.registry_data["plugins"]:
            print(f"❌ Plugin '{framework}' not found")
            return False

        # Remove from registry
        del self.registry_data["plugins"][plugin_key]

        # Remove from loaded plugins cache
        if plugin_key in self.loaded_plugins:
            del self.loaded_plugins[plugin_key]

        self._save_registry()
        print(f"🗑️ Plugin '{framework}' unregistered")
        return True

    def get_plugins_by_control(self, control: str) -> List[str]:
        """
        Find plugins that implement a specific control.

        Args:
            control: Control identifier (e.g., "AC-2")

        Returns:
            List of framework names that implement the control
        """
        matching_frameworks: List[str] = []

        for _, plugin_info in self.registry_data["plugins"].items():
            if not plugin_info.get("enabled", True):
                continue

            controls = plugin_info.get("controls", [])
            if control in controls:
                matching_frameworks.append(plugin_info["framework"])  # type: ignore

        return matching_frameworks

    def validate_all_plugins(self) -> Dict[str, bool]:
        """
        Validate all registered plugins.

        Returns:
            Dictionary mapping plugin names to validation status
        """
        results: Dict[str, bool] = {}

        for _, plugin_info in self.registry_data["plugins"].items():
            try:
                plugin_class = self._load_plugin_class(plugin_info["file"])
                results[plugin_info["name"]] = plugin_class is not None
            except Exception:
                results[plugin_info["name"]] = False

        return results
