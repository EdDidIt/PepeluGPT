# Contributing to PepeluGPT

Welcome! Your desire to contribute to PepeluGPT shows you understand that quality software grows through collaboration and shared expertise.

---

## 🔵 Three Areas of Contribution

## Technical Path - Deep Technical Expertise

Perfect for experienced developers who enjoy architectural challenges:

- Core engine improvements
- Advanced parsing algorithms  
- Performance optimizations
- Security enhancements

## Compliance Path - Structured Excellence

Ideal for those with cybersecurity and regulatory expertise:

- Framework integrations (NIST, RMF, STIG)
- Compliance workflow automation
- Documentation standardization
- Quality assurance processes

## Innovation Path - Creative Solutions

For visionaries and experience designers:

- User interface enhancements
- Documentation and tutorials
- Community building
- Design and branding elements

---

## Quick Start for Contributors

## 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YourUsername/PepeluGPT.git
cd PepeluGPT
```

## 2. Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)  
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy pre-commit
```

## 3. Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run tests to ensure everything works
python -m pytest tests/

# Check code style
black --check .
flake8 .
```

---

## Development Workflow

## Branch Naming Convention

```text
feature/ui-enhancement           # New features
bugfix/vector-db-memory-leak     # Bug fixes  
docs/api-documentation           # Documentation
security/input-sanitization     # Security improvements
refactor/parser-optimization     # Code improvements
```

## Commit Message Format

Follow the standard commit convention:

```text
type(scope): brief description

🟢 feat(parser): add PowerPoint extraction support
� fix(vector): resolve memory leak in batch processing  
� docs(readme): update installation instructions
🔴 security(auth): implement input validation
🔵 refactor(core): optimize query processing pipeline
🔵 test(parser): add edge case coverage for PDF parsing
```

## Pull Request Process

1. Create Feature Branch

   ```bash
   git checkout -b feature/your-enhancement
   ```

2. Develop with Intention
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow existing code style

3. Test Thoroughly

   ```bash
   # Run full test suite
   python -m pytest tests/ -v
   
   # Check code coverage
   python -m pytest --cov=.
   
   # Lint your code
   black .
   flake8 .
   mypy .
   ```

4. Submit Pull Request
   - Use the PR template
   - Link relevant issues
   - Include screenshots for UI changes
   - Request review from maintainers

---

## 🔵 Project Architecture

Understanding PepeluGPT's structure:

```text
PepeluGPT/
├── core/                       # Core intelligence engine
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── core.py                # Main application logic
│   ├── pepelugpt.py          # Core AI functionality
│   ├── response_personalities.py  # Oracle/Compliance/Professional modes
│   ├── security.py           # Security utilities
│   └── utilities.py          # Helper functions
│
├── file_parser/               # Document processing engine
│   ├── main_parser.py        # Core parsing logic
│   ├── parse_all_documents.py # Batch processor
│   ├── schema.py             # Data schemas
│   └── parsers/              # Format-specific parsers
│
├── interface/                 # User interaction layer
├── tests/                     # Comprehensive test suite
├── data/                      # Data processing utilities
├── docs/                      # Documentation
├── config/                    # Configuration files
├── manifest/                  # Version and metadata
└── sprints/                   # Development iterations
```

---

## 🔵 Contribution Areas

## High Priority

- [ ] GitHub Actions CI/CD pipeline
- [ ] Enhanced error handling and logging
- [ ] Performance optimization for large document sets
- [ ] Web interface development
- [ ] API endpoint creation

## Medium Priority

- [ ] Additional document format support
- [ ] Advanced search filters and faceting
- [ ] Batch processing improvements
- [ ] Enhanced CLI features
- [ ] Documentation improvements

## Creative Opportunities

- [ ] Custom personality development
- [ ] UI/UX design enhancements  
- [ ] Tutorial and example creation
- [ ] Community tools and scripts
- [ ] Branding and visual identity

---

## Testing Standards

## Test Categories

```bash
# Unit tests - fast, isolated
python -m pytest tests/unit/

# Integration tests - component interaction
python -m pytest tests/integration/

# End-to-end tests - full workflow
python -m pytest tests/e2e/

# Performance tests - benchmark critical paths
python -m pytest tests/performance/
```

## Coverage Requirements

- Minimum: 80% code coverage
- Target: 90% code coverage  
- Critical paths: 100% coverage (security, data processing)

## Test Naming Convention

```python
def test_should_parse_pdf_when_valid_file_provided():
    # Given: A valid PDF file
    # When: Parser processes the file  
    # Then: Should return structured content
```

---

## Documentation Standards

## Code Documentation

```python
def process_function(input_level: int) -> str:
    """
    Processes input through analysis filters.
    
    Args:
        input_level: The depth of analysis required (1-10)
        
    Returns:
        Processed result as formatted string
        
    Raises:
        ProcessingError: When input level exceeds system capacity
        
    Examples:
        >>> process_function(5)
        "Analysis complete with high confidence..."
    """
```

## README Updates

- Keep examples current and functional
- Update feature lists when adding capabilities
- Maintain accuracy in installation instructions
- Include new configuration options

---

## Code Style Guide

## Python Style

- Follow PEP 8 with Black formatting
- Use type hints for all function signatures
- Prefer descriptive variable names over comments
- Maximum line length: 88 characters (Black default)

## Professional Naming Conventions

```python
# Classes: PascalCase with clear naming
class DocumentParser:
class VectorDatabase:

# Functions: snake_case with clarity
def parse_document():
def build_vector_index():

# Constants: UPPER_SNAKE_CASE
CHUNK_SIZE = 512
RESPONSE_LIMIT = 2000
```

---

## 🟢 Recognition & Growth

## Contributor Levels

- Contributor: First contribution accepted
- Active Developer: 5+ meaningful contributions
- Maintainer: Trusted with review responsibilities
- Core Team: Team member with special access

## Recognition Methods

- GitHub contributor highlighting
- Changelog acknowledgments
- Special contributor badges and titles
- Invitation to private contributor channels

---

## 🔵 Community Guidelines

## Core Principles

1. Respect: Honor all perspectives and experience levels
2. Collaboration: Share knowledge freely and constructively  
3. Excellence: Strive for quality in all contributions
4. Innovation: Embrace creative solutions and professional thinking
5. Security: Protect the digital realm and user privacy

## Communication Channels

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Pull Requests: Code review and technical discussion
- Email: Private security or sensitive matters

---

## � Getting Help

## Stuck on Something?

1. Check existing [GitHub Issues](https://github.com/EdDidIt/PepeluGPT/issues)
2. Search [GitHub Discussions](https://github.com/EdDidIt/PepeluGPT/discussions)
3. Review documentation in `docs/` folder
4. Create a new issue with detailed description

## Mentorship Available

New contributors can request mentorship for:

- First-time setup and orientation
- Code review guidance
- Architecture understanding
- Best practices coaching

---

## Professional Excellence for Contributors

"Code is poetry written in the language of logic. Every function you craft, every bug you fix, every test you write adds to the comprehensive suite of digital tools."

"Remember: You're not just building software—you're forging tools that protect the digital realm and empower defenders of cybersecurity."

---

Ready to begin your contribution journey?

Create your first issue, fork the repository, and let your expertise join the PepeluGPT development team!

---

Last Updated: July 30, 2025  
Version: 1.1.0
