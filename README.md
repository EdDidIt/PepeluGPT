# PepeluGPT

## Professional Cybersecurity Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![Version](https://img.shields.io/badge/Version-v0.3.1-blue.svg)  
![Status](https://img.shields.io/badge/Status-Beta-brightgreen.svg)  
[![Tests](https://github.com/EdDidIt/PepeluGPT/actions/workflows/tests.yml/badge.svg)](https://github.com/EdDidIt/PepeluGPT/actions)  
[![Security](https://github.com/EdDidIt/PepeluGPT/actions/workflows/security.yml/badge.svg)](https://github.com/EdDidIt/PepeluGPT/actions)

## Executive Summary

- Privacy-first, offline cybersecurity AI platform
- Integrated RMF, STIG, NIST CSF & DoD compliance frameworks
- Multi-format document parser: PDF, DOCX, XLSX, HTML, XML, TXT, PPTX
- Command-line interface: `setup`, `chat`, `status`, `test`, `update`, `config`, `version`
- Semantic search with automated control mapping capabilities  

## Quick Start

1. **Clone and install**

   ```bash
   git clone https://github.com/EdDidIt/PepeluGPT.git
   cd PepeluGPT
   pip install -r requirements.txt
   ```

2. **Add your documents under `data/documents/`**

   ```text
   data/documents/
   ├── cybersecurity/
   │   ├── nist_sp_800_53.pdf
   │   ├── dod_stig_guidelines.pdf
   │   └── your_docs.*
   ```

3. **Initialize and run**

   ```bash
   python core/pepelugpt.py setup
   python core/pepelugpt.py chat
   python core/pepelugpt.py status
   ```

## Key Features

- Offline, zero-cloud footprint  
- Rapid semantic search (85–95% accuracy)  
- Automated compliance reports & evidence  
- Support for NIST, RMF, STIG, DoD standards  
- Plugin-style parsers and vector DB  

## Architecture

```text
PepeluGPT/
├── core/                   # Main engine & CLI
│   ├── pepelugpt.py       # Primary CLI interface
│   ├── orchestrator.py    # Core orchestration
│   └── pepelugpt_engine.py # AI engine
├── processing/             # Document parsers & schema
├── personalities/          # AI personality system
├── interface/              # Chat interfaces
├── storage/                # Vector database
├── data/                   # User documents & cache
├── cyber_vector_db/        # Generated vector database
└── tests/                  # Test suite
```

## Supported Formats

| Format       | Extension     | Parser        |
|--------------|---------------|---------------|
| PDF          | `.pdf`        | PyMuPDF       |
| Word         | `.docx`       | python-docx   |
| Excel        | `.xls`,`.xlsx`| openpyxl, xlrd|
| HTML / XML   | `.html`,`.xml`| BeautifulSoup |
| Text         | `.txt`        | Built-in      |
| PowerPoint   | `.pptx`       | python-pptx   |

## Configuration

Set environment variables as needed:

```bash
export PEPELU_MODEL="all-MiniLM-L6-v2"
export PEPELU_CHUNK_SIZE=512
```

Configuration files are located in `config/` directory and `storage/vector_db/config.py`.

## Troubleshooting

| Issue                      | Solution                                  |
|----------------------------|-------------------------------------------|
| `langdetect` fails         | Ensure text length ≥ 20 characters        |
| PDF parsing errors         | Confirm PyMuPDF is installed correctly    |
| Empty search results       | Verify files in `data/documents/`         |
| Vector DB loading failure  | Rerun `python core/pepelugpt.py setup`       |

## Contributing

1. Fork the repo  
2. Create a feature branch  
3. Run tests and linting  
4. Submit a pull request  
5. Follow semantic versioning and update `CHANGELOG.md`

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Roadmap

- Phase 1: Document parsing & vector DB (Complete)  
- Phase 2: CLI & search (Complete)  
- Phase 3: Summarization & report generation  
- Phase 4: Web interface & API  
- Phase 5: External tool integrations  

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
