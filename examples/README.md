# PepeluGPT Examples

This directory contains practical examples demonstrating how to use PepeluGPT effectively.

## 📁 Directory Structure

```text
examples/
├── basic_usage/           # Simple getting started examples
├── plugin_development/    # Plugin creation examples
├── api_integration/       # API usage examples
├── security_scanning/     # Security assessment examples
└── automation_scripts/    # Automation workflow examples
```

## 🚀 Quick Start Examples

### Basic Security Scan

```python
from core.engine import PepeluEngine

# Initialize the engine
engine = PepeluEngine()

# Run a basic security scan
results = engine.scan_directory("./my_project")
print(f"Found {len(results.findings)} security findings")
```

### Plugin Usage

```python
from plugins.security import SecurityPlugin

# Load and configure a security plugin
plugin = SecurityPlugin()
plugin.configure({
    "severity_threshold": "medium",
    "scan_depth": "deep"
})

# Execute the plugin
findings = plugin.execute("./target_directory")
```

## 📋 Example Categories

- **Basic Usage**: Simple command-line and API examples
- **Plugin Development**: How to create custom plugins
- **API Integration**: REST API usage patterns
- **Security Scanning**: Comprehensive security assessment workflows
- **Automation Scripts**: Automated compliance and remediation examples

## 🔗 Related Documentation

- [Plugin Development Guide](../docs/PLUGINS.md)
- [API Reference](../docs/API.md)
- [Security Features](../docs/SECURITY_FEATURES.md)
