#!/usr/bin/env python3
"""
Verify and sync /gc command deployments across all AI agents.

This script checks that global /gc commands (Claude Code, Opencode, Codex) are
installed and match the canonical template. It also scans for GitHub Copilot
projects and reports their /gc configuration status.

Usage:
    python3 verify_gc_deployment.py           # Check status
    python3 verify_gc_deployment.py --fix     # Auto-fix global commands
    python3 verify_gc_deployment.py --scan-copilot /path  # Scan path for Copilot configs
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Global command locations
GLOBAL_COMMANDS = {
    "Claude Code": Path.home() / ".claude/commands/gc.md",
    "Opencode": Path.home() / ".config/opencode/command/gc.md",
    "Codex": Path.home() / ".codex/prompts/gc.md",
}


def get_toolkit_root() -> Path:
    """Find the toolkit root directory."""
    script_path = Path(__file__).resolve()
    # Script is in .flowji-ai/tools/git-commit-summaries/
    return script_path.parent


def get_template_path() -> Path:
    """Get path to canonical gc-command.md template."""
    return get_toolkit_root() / "templates/gc-command.md"


def compute_checksum(filepath: Path) -> Optional[str]:
    """Compute MD5 checksum of a file."""
    if not filepath.exists():
        return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def check_global_commands() -> Dict[str, dict]:
    """Check status of global /gc commands."""
    template = get_template_path()
    if not template.exists():
        print(f"❌ Template not found: {template}")
        sys.exit(1)

    template_checksum = compute_checksum(template)
    results = {}

    for agent, path in GLOBAL_COMMANDS.items():
        exists = path.exists()
        checksum = compute_checksum(path) if exists else None
        matches = checksum == template_checksum if exists else False

        results[agent] = {
            "path": path,
            "exists": exists,
            "checksum": checksum,
            "matches_template": matches,
        }

    return results


def find_copilot_configs(search_path: Path) -> List[Tuple[Path, bool]]:
    """
    Find all .vscode/settings.json files and check for /gc command.

    Returns list of tuples: (project_path, has_gc_command)
    """
    configs = []

    for settings_file in search_path.rglob(".vscode/settings.json"):
        project_root = settings_file.parent.parent

        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            commands = data.get("github.copilot.chat.customCommands", [])
            has_gc = any(cmd.get("name") == "gc" for cmd in commands)

            configs.append((project_root, has_gc))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Skip malformed JSON files
            continue

    return configs


def sync_global_command(agent: str, path: Path, template_path: Path) -> bool:
    """Copy template to global command location."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(template_path, "r", encoding="utf-8") as src:
            content = src.read()

        with open(path, "w", encoding="utf-8") as dst:
            dst.write(content)

        return True
    except Exception as e:
        print(f"❌ Failed to sync {agent}: {e}")
        return False


def print_status_table(results: Dict[str, dict], template_checksum: str):
    """Print status table for global commands."""
    print("\n" + "=" * 80)
    print("GLOBAL /gc COMMAND STATUS")
    print("=" * 80)
    print(f"\n{'Agent':<15} {'Installed':<12} {'In Sync':<10} {'Path'}")
    print("-" * 80)

    all_synced = True

    for agent, info in results.items():
        exists_icon = "✓" if info["exists"] else "✗"
        sync_icon = "✓" if info["matches_template"] else "✗"

        if not info["matches_template"]:
            all_synced = False

        print(f"{agent:<15} {exists_icon:<12} {sync_icon:<10} {info['path']}")

    print("-" * 80)
    print(f"Template: {get_template_path()}")
    print(f"Template checksum: {template_checksum[:8]}...")

    if all_synced and all(r["exists"] for r in results.values()):
        print("\n✓ All global commands are installed and in sync")
    else:
        print("\n⚠ Some global commands need updates")
        print("  Run with --fix to auto-update")


def print_copilot_status(configs: List[Tuple[Path, bool]]):
    """Print Copilot project status."""
    print("\n" + "=" * 80)
    print("GITHUB COPILOT /gc COMMAND STATUS")
    print("=" * 80)

    if not configs:
        print("\nNo Copilot projects found in scan path")
        return

    print(f"\n{'Status':<10} {'Project Path'}")
    print("-" * 80)

    for project_path, has_gc in configs:
        status = "✓ /gc" if has_gc else "✗ Missing"
        print(f"{status:<10} {project_path}")

    missing_count = sum(1 for _, has_gc in configs if not has_gc)

    print("-" * 80)
    print(f"\nTotal projects: {len(configs)}")
    print(f"With /gc command: {len(configs) - missing_count}")
    print(f"Missing /gc command: {missing_count}")

    if missing_count > 0:
        print("\n⚠ Some projects need Copilot /gc configuration")
        print(f"  See AGENTS.md for setup instructions")
        print(f"  Template: {get_template_path()}")


def main():
    parser = argparse.ArgumentParser(
        description="Verify and sync /gc command deployments"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-update global commands to match template"
    )
    parser.add_argument(
        "--scan-copilot",
        type=Path,
        metavar="PATH",
        help="Scan path for Copilot .vscode/settings.json files"
    )

    args = parser.parse_args()

    # Check global commands
    template = get_template_path()
    template_checksum = compute_checksum(template)
    results = check_global_commands()

    if args.fix:
        print("Syncing global commands...")
        for agent, info in results.items():
            if not info["matches_template"]:
                print(f"  Updating {agent}...")
                if sync_global_command(agent, info["path"], template):
                    print(f"    ✓ {info['path']}")

        # Re-check after fix
        results = check_global_commands()

    print_status_table(results, template_checksum)

    # Scan for Copilot configs if requested
    if args.scan_copilot:
        if not args.scan_copilot.exists():
            print(f"\n❌ Scan path does not exist: {args.scan_copilot}")
            sys.exit(1)

        print(f"\nScanning for Copilot projects in: {args.scan_copilot}")
        configs = find_copilot_configs(args.scan_copilot)
        print_copilot_status(configs)

    # Exit with error if anything is out of sync
    all_synced = all(r["matches_template"] for r in results.values())
    if not all_synced:
        sys.exit(1)


if __name__ == "__main__":
    main()
