# Legacy Configuration Files - DEPRECATED

This directory contains deprecated configuration files that have been replaced with the new adaptive/classic mode system.

## Migration Notes

### Deprecated Files

- `learning_dev.yaml` → Use `adaptive.yaml` instead
- `deterministic.yaml` → Use `classic.yaml` instead

### Breaking Changes

- Mode names have changed:
  - `learning` → `adaptive`
  - `deterministic` → `classic`

### Backward Compatibility

- Legacy mode names still work with deprecation warnings
- Legacy config files remain functional but are not actively maintained
- Use `tools/mode_switcher.py` for seamless migration

## Archive Date: August 3, 2025
