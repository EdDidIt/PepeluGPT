#!/usr/bin/env python3
"""
Phase 5.1: Project Organization Script
Cleans up workspace structure for enterprise-grade plugin ecosystem
"""

import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGETS = {
    ".md": BASE_DIR / "docs",
    ".json": BASE_DIR / "reports",
    ".yaml": BASE_DIR / "config",
}

EXCLUDE_MD = {"README.md"}


def move_file(file_path: Path, target_dir: Path, dry_run: bool = False) -> None:
    """Move file to target directory with proper logging"""
    target_dir.mkdir(exist_ok=True)
    target = target_dir / file_path.name

    if target.exists():
        print(f"⚠️  Target exists, skipping: {target}")
        return

    if dry_run:
        print(f"🧪 [Dry Run] Would move {file_path} → {target}")
    else:
        print(f"📦 Moving {file_path} → {target}")
        shutil.move(str(file_path), str(target))


def cleanup_empty_dirs(dry_run: bool = False) -> None:
    """Remove empty directories (excluding critical ones)"""
    critical_dirs = {BASE_DIR / "plugins", BASE_DIR / "core", BASE_DIR / "cli"}

    for path in BASE_DIR.rglob("*"):
        if (
            path.is_dir()
            and not any(path.iterdir())
            and path not in critical_dirs
            and not any(critical in path.parents for critical in critical_dirs)
        ):

            if dry_run:
                print(f"🧪 [Dry Run] Would remove empty directory: {path}")
            else:
                print(f"🧹 Removing empty directory: {path}")
                path.rmdir()


def cleanup_ds_store(dry_run: bool = False) -> None:
    """Remove macOS .DS_Store files"""
    for path in BASE_DIR.rglob(".DS_Store"):
        if dry_run:
            print(f"🧪 [Dry Run] Would remove macOS artifact: {path}")
        else:
            print(f"🧹 Removing macOS artifact: {path}")
            path.unlink()


def organize(dry_run: bool = False) -> None:
    """Execute Phase 5.1 organization"""
    print("🚀 Phase 5.1: Structural Refinement")
    print("=" * 50)

    # Move files by extension
    for ext, target_dir in TARGETS.items():
        print(f"\n📁 Processing {ext} files → {target_dir.name}/")

        for path in BASE_DIR.glob(f"*{ext}"):
            if ext == ".md" and path.name in EXCLUDE_MD:
                print(f"⏭️  Skipping excluded file: {path.name}")
                continue
            move_file(path, target_dir, dry_run)

    # Cleanup operations
    print(f"\n🧹 Cleanup Operations")
    cleanup_ds_store(dry_run)
    cleanup_empty_dirs(dry_run)

    print("\n✅ Phase 5.1 Organization complete!")
    if dry_run:
        print("💡 Run without --dry-run to execute changes")


def main() -> None:
    """Main execution with argument parsing"""
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("🧪 DRY RUN MODE - No changes will be made")

    organize(dry_run=dry_run)


if __name__ == "__main__":
    main()
