# PepeluGPT Architecture Documentation

## Architecture Decision Record: Project Structure

**Status**: Accepted ✅  
**Date**: August 1, 2025  
**Decision Makers**: Development Team  

### Decision

**Maintain current modular structure** with `core/` and `processing/` separation, while establishing a clear evolution path for future architectural needs.

### Current Structure (Recommended)

```text
core/                    # Orchestration & coordination
├── orchestrator.py      # Main workflow coordination  
├── engine.py           # Core engine logic
├── data_manager.py     # Conditional parsing system
└── utils.py            # Shared utilities

processing/             # Data processing pipeline
├── parse.py           # Document parsing
├── router.py          # Request routing  
├── validators.py      # Input validation
└── parsers/           # Specialized parsers

cli/                   # Command-line interface
interface/             # User interaction layer
plugins/               # Extensible plugin system
config/                # Configuration management
```

### Design Philosophy

- **Clean separation** between orchestration (core) and data processing (processing)
- **Modular validation** approach with conditional parsing strategies
- **Plugin architecture** for extensible cybersecurity analysis
- **Configuration-driven** behavior for different environments

### Benefits

- Clear conceptual boundaries
- Easy to test individual components  
- Minimal coupling between layers
- Supports current conditional parsing system
- Extensible through plugin architecture

## Configuration Management Strategy

### Overview

PepeluGPT uses a multi-environment configuration system that supports development, testing, and production deployments with appropriate settings for each environment.

### Configuration Files

#### Environment Hierarchy

1. **`default.yaml`** - Base configuration with sensible defaults
2. **`adaptive.yaml`** - AI-driven analysis with learning capabilities
3. **`classic.yaml`** - Traditional rule-based processing
4. **`dev.yaml`** - Development environment overrides  
5. **`prod.yaml`** - Production environment optimizations

#### Configuration Structure

```yaml
# Model configuration
model:
  name: "default-model"
  parameters:
    temperature: 0.7

# Logging configuration  
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/pepelugpt.log"

# Data management configuration
data_management:
  cache_dir: "cyber_vector_db"
  source_dir: "cyber_documents"
  enable_caching: true
  cache_validation: "hash"  # Options: hash, timestamp, none

# Vector database configuration
vector_db:
  index_path: "cyber_vector_db/faiss_index.bin"
  metadata_path: "cyber_vector_db/metadata.pkl"
  chunk_size: 1000
  overlap: 200
```

### Environment-Specific Settings

#### Development Environment (`dev.yaml`)

- **Debug Logging**: Enhanced logging for development
- **Smaller Cache**: Optimized for development machine resources
- **Fast Validation**: Timestamp-based validation for speed
- **Development Paths**: Local development directories

#### Production Environment (`prod.yaml`)

- **Performance Optimized**: Minimal logging overhead
- **Full Cache**: Complete dataset caching for performance
- **Hash Validation**: Complete integrity checking
- **Production Paths**: Optimized directory structure

#### Adaptive Mode (`adaptive.yaml`)

- **AI Learning**: Machine learning capabilities enabled
- **Dynamic Analysis**: Context-aware cybersecurity analysis
- **Feedback Loop**: User interaction learning
- **Advanced Features**: Full AI feature set

#### Classic Mode (`classic.yaml`)

- **Rule-Based**: Traditional cybersecurity analysis
- **Deterministic**: Consistent, predictable results
- **Fast Processing**: Optimized for speed
- **Legacy Compatibility**: Support for existing workflows

## Evolution Roadmap

### Current State (v1.0) ✅

**Philosophy**: Clean separation between orchestration (core) and data processing (processing). Modular validation approach with conditional parsing strategies.

**Benefits**:

- Clear conceptual boundaries
- Easy to test individual components
- Minimal coupling between layers
- Supports current conditional parsing system

### Future Evolution Path (v2.0+)

#### Scenario 1: Deep Integration Required

If parsing logic starts to intertwine deeply with orchestration (dynamic routing, conditional workflows), consider:

```text
application/
├── orchestrator.py     # High-level workflow coordination
├── engine.py          # Core engine logic
├── data_manager.py    # Conditional parsing system
└── pipeline/          # Unified processing pipeline
    ├── parse.py       # Document parsing
    ├── router.py      # Request routing
    ├── validators.py  # Input validation
    └── parsers/       # Specialized parsers
```

#### Scenario 2: Microservice Architecture

For large-scale deployment:

```text
services/
├── orchestration/     # Core coordination service
├── processing/        # Data processing service
├── storage/          # Storage service
├── plugin/           # Plugin management service
└── monitoring/       # Monitoring and metrics service
```

#### Scenario 3: Event-Driven Architecture

For real-time cybersecurity analysis:

```text
events/
├── ingestion/        # Event ingestion service
├── processing/       # Event processing pipeline
├── analysis/         # Real-time analysis engine
└── notification/     # Alert and notification system
```

### Migration Strategy

When architectural changes become necessary:

1. **Incremental Migration**: Move components gradually
2. **Compatibility Layer**: Maintain backward compatibility
3. **Testing Strategy**: Comprehensive testing at each stage
4. **Documentation**: Update architecture documentation
5. **Team Training**: Ensure team understands new structure

### Decision Criteria

Consider architectural changes when:

- **Performance Requirements**: Current structure limits performance
- **Scalability Needs**: System needs to handle significantly more load
- **Integration Complexity**: Deep integration between layers is required
- **Team Growth**: Larger teams need better separation of concerns
- **Technology Evolution**: New technologies offer significant advantages

## Component Design Patterns

### Singleton Pattern (Data Manager)

Used for efficient resource usage with lazy initialization:

```python
class DataManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Plugin Pattern (Extensions)

Extensible architecture for cybersecurity analysis:

```python
class PluginInterface:
    def analyze(self, data):
        raise NotImplementedError
        
    def validate(self):
        raise NotImplementedError
```

### Observer Pattern (Events)

For system monitoring and metrics:

```python
class EventPublisher:
    def __init__(self):
        self._observers = []
    
    def subscribe(self, observer):
        self._observers.append(observer)
```

### Factory Pattern (Parsers)

For creating appropriate parsers based on content type:

```python
class ParserFactory:
    @staticmethod
    def create_parser(content_type):
        if content_type == 'pdf':
            return PDFParser()
        elif content_type == 'xml':
            return XMLParser()
```

This architecture documentation consolidates all architectural decisions, configuration management strategies, and evolution planning into a single comprehensive reference.
