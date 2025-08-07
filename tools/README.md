# PepeluGPT Tools

This directory contains all tools and utilities for PepeluGPT system management, development, and demonstration.

## 📁 Directory Structure

```text
tools/
├── admin/          # System administration tools
├── demo/           # Demonstration and showcase tools  
├── dev/            # Development utilities (future)
└── README.md       # This file
```

## 🔧 Admin Tools (`tools/admin/`)

### `data_cli.py` - **Main Administrative CLI**

Full-featured command-line interface for data management operations.

**Usage:**

```bash
# Run from project root directory
python tools/admin/data_cli.py [command] [options]
```

**Commands:**

- `status` - Show cache status and information
- `parse` - Parse data with caching options
- `clear` - Clear all cached data
- `benchmark` - Run performance benchmarks
- `export` - Export parsed data to JSON

**Examples:**

```bash
# Check cache status
python tools/admin/data_cli.py status

# Parse with verbose output
python tools/admin/data_cli.py parse --verbose

# Force refresh cache
python tools/admin/data_cli.py parse --force

# Clear cache
python tools/admin/data_cli.py clear

# Run performance benchmark
python tools/admin/data_cli.py benchmark

# Export data
python tools/admin/data_cli.py export --output my_data.json
```

## 🎯 Demo Tools (`tools/demo/`)

### `conditional_parsing_demo.py` - **Interactive Demonstration**

Live demonstration of PepeluGPT's conditional parsing and caching capabilities.

**Usage:**

```bash
python tools/demo/conditional_parsing_demo.py
```

**Features:**

- Demonstrates all three conditional parsing strategies
- Shows real-time performance improvements
- Interactive examples with live metrics
- Educational content for stakeholders

## 🚀 Quick Start

Most common operations:

```bash
# Check system status
python tools/admin/data_cli.py status

# Run performance benchmark
python tools/admin/data_cli.py benchmark

# Clear cache if needed
python tools/admin/data_cli.py clear

# See capabilities demo
python tools/demo/conditional_parsing_demo.py
```

## 📊 Expected Output Examples

**Status Command:**

```text
🔵 Data Manager Status
==================================================
memory_cache_loaded: True
persistent_cache_exists: True
hash_cache_exists: True
cache_directory: cyber_vector_db
cache_metadata:
  last_updated: 2025-08-01T10:30:00
  total_files: 53
```

**Benchmark Results:**

```text
📊 Benchmark Results:
  First run (no cache):  0.465s
  Second run (cached):   0.000s
  Forced refresh:        0.178s
  Cache speedup:         149870.0x
```

**Demo Output:**

```text
🤖 PepeluGPT Conditional Parsing Demonstration
============================================

🔵 Strategy 1: Check for Parsed Output First
📄 First call (no cache): ⏱️ 0.465s

```text
📄 Second call (cached): ⏱️ 0.000s 🚀 149870x faster

✅ All demonstrations completed successfully!
```

## 🛠️ Development Notes

### Path Resolution

All tools automatically handle path resolution when run from the project root directory. The tools use relative paths to find:

- Configuration: `config/default.yaml`
- Core modules: `core/`
- Cache directory: `cyber_vector_db/`

### Import Handling

Tools automatically add the project root to Python path for importing core modules.

### Error Handling

All tools include comprehensive error handling and user-friendly error messages.

## 🔍 Troubleshooting

### Import Errors

Make sure you're running from the project root directory:

```bash
# ✅ Correct - from project root
python tools/admin/data_cli.py status

# ❌ Wrong - from tools directory  
cd tools && python admin/data_cli.py status
```

### Cache Issues

1. Check status: `python tools/admin/data_cli.py status`
2. Clear cache: `python tools/admin/data_cli.py clear`
3. Force refresh: `python tools/admin/data_cli.py parse --force`

### Performance Issues

1. Run benchmark: `python tools/admin/data_cli.py benchmark`
2. Check cache is working (should show massive speedup)
3. If no speedup, check file permissions on cache directory

## 🎯 Integration with Core System

These tools integrate with:

- **`core/data_manager.py`** - Conditional parsing and caching system
- **`core/orchestrator.py`** - Main application orchestration
- **`config/default.yaml`** - System configuration
- **`processing/`** - Document parsing pipeline

The tools provide administrative access to the same data management system used by the main PepeluGPT application.
