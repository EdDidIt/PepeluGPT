# PepeluGPT Plugin Template

This directory provides a template for creating custom PepeluGPT plugins.

## 🚀 Quick Start

1. Copy this template directory to a new location
2. Replace placeholder values in the template files:
   - `{{PLUGIN_NAME}}` - Your plugin class name (e.g., "MySecurityChecker")
   - `{{PLUGIN_NAME_LOWER}}` - Lowercase plugin name (e.g., "my_security_checker")
   - `{{PLUGIN_DESCRIPTION}}` - Brief description of your plugin
   - `{{AUTHOR_NAME}}` - Your name or organization
   - `{{PLUGIN_CATEGORY}}` - Plugin category (security, compliance, analysis, etc.)

3. Implement your plugin logic in the template methods
4. Test your plugin thoroughly
5. Submit a pull request to include it in the main repository

## 📁 Template Files

- `plugin_template.py` - Main plugin implementation template
- `README.md` - This documentation file
- `requirements.txt` - Plugin-specific dependencies
- `tests/` - Unit tests for your plugin
- `docs/` - Plugin documentation

## 🔧 Plugin Structure

A PepeluGPT plugin must:

1. Inherit from `BasePlugin`
2. Implement required methods:
   - `configure()` - Handle configuration
   - `execute()` - Main plugin logic
   - `validate_config()` - Validate configuration

3. Return a `PluginResult` object with findings
4. Follow the plugin naming conventions
5. Include proper error handling and logging

## 📋 Plugin Categories

- **Security** - Security vulnerability detection
- **Compliance** - Regulatory compliance checking
- **Analysis** - Code quality and analysis
- **Automation** - Automated remediation tasks
- **Reporting** - Custom report generation

## 🧪 Testing

Create comprehensive tests for your plugin:

```python
import unittest
from your_plugin import YourPluginClass

class TestYourPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = YourPluginClass()
    
    def test_configuration(self):
        config = {"severity_threshold": "high"}
        self.plugin.configure(config)
        self.assertEqual(self.plugin.severity_threshold, "high")
    
    def test_execution(self):
        result = self.plugin.execute("./test_data")
        self.assertIsNotNone(result)
        self.assertIsInstance(result.findings, list)
```

## 📚 Documentation

Document your plugin thoroughly:

- Purpose and functionality
- Configuration options
- Usage examples
- Known limitations
- Troubleshooting guide

## 🔗 Resources

- [Plugin Development Guide](../docs/PLUGIN_DEVELOPMENT.md)
- [API Reference](../docs/API_REFERENCE.md)
- [Core Models Documentation](../docs/CORE_MODELS.md)
- [Testing Guidelines](../docs/TESTING.md)

## 📞 Support

For plugin development support:

- Check existing plugin examples in `/plugins`
- Review the plugin development documentation
- Ask questions in GitHub discussions
- Contact the maintainers

Happy plugin development! 🎉
