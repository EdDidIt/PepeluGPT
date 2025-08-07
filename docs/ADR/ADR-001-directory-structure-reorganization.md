# ADR-001: Directory Structure Reorganization

## Status

Accepted

## Context

The PepeluGPT project had grown organically, resulting in:

- Duplicate documentation files
- Scattered utility scripts across multiple directories
- Lack of clear governance and contribution guidelines
- Missing infrastructure and monitoring structure

## Decision

Implement a comprehensive directory structure reorganization based on expert recommendations:

1. **Remove Redundancy**
   - Consolidate individual metrics files into timestamped JSON reports
   - Remove duplicate documentation
   - Archive legacy configurations

2. **Consolidate Structure**
   - Merge `tools/`, `scripts/`, and utilities into a unified `tools/` hierarchy
   - Centralize documentation under `docs/` with only essential files at root
   - Move platform-specific scripts to `tools/windows/`

3. **Add Governance**
   - Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `CODEOWNERS`
   - Create GitHub issue and PR templates
   - Establish Architecture Decision Records (ADR) process

4. **Enhance Infrastructure**
   - Add `infra/` for Infrastructure as Code
   - Add `monitoring/` for observability configurations
   - Add `schemas/` for JSON Schema definitions
   - Add `examples/` for user onboarding

## Consequences

### Positive

- Clear separation of concerns
- Improved developer onboarding experience
- Better maintainability and navigation
- Enterprise-grade governance structure
- Reduced confusion for contributors

### Negative

- One-time migration effort required
- Potential breaking changes for existing automation
- Need to update documentation references
- Learning curve for new structure

## Implementation

- Phase 1: Remove redundant files and consolidate metrics
- Phase 2: Reorganize directory structure
- Phase 3: Add governance and infrastructure files
- Phase 4: Update documentation and references

## Date

2025-08-03
