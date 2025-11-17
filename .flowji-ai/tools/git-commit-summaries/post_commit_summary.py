#!/usr/bin/env python3
"""
Git Commit Summary Generator

This script processes the latest Git commit and creates a structured Markdown summary
in the configured summaries directory (default `.flowji-ai/memory/git-summaries/`) with commit metadata, file changes, and stats.
"""
import argparse
import os
import re
import subprocess
import sys
from urllib.parse import quote
from datetime import datetime
from pathlib import Path


def get_git_repo_root():
    """Get the repository root using git rev-parse --show-toplevel."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("[post-commit-summary] Error: Not in a Git repository")
        sys.exit(1)


DEFAULT_SUMMARY_SUBDIR = ".flowji-ai/memory/git-summaries"


def get_summary_subdir():
    """Return the configured summary subdirectory relative to repo root."""
    override = os.environ.get("GIT_SUMMARY_DIR", "").strip()
    if override:
        return override
    return DEFAULT_SUMMARY_SUBDIR


SUMMARY_SUBDIR = get_summary_subdir()
SUMMARY_SUBDIR_NORMALIZED = SUMMARY_SUBDIR.replace("\\", "/").lstrip("./").rstrip("/")

FENCED_CODE_PATTERN = re.compile(r"```[\s\S]*?```", re.MULTILINE)
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")


def has_escaped_newlines(message):
    """Return True if literal \\n sequences appear outside code blocks."""
    if not message:
        return False

    without_fenced = FENCED_CODE_PATTERN.sub("", message)
    without_inline = INLINE_CODE_PATTERN.sub("", without_fenced)
    return "\\n" in without_inline


def get_latest_commit_subject():
    """Return latest commit subject."""
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%s"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def get_latest_commit_message():
    """Return latest commit full body."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout


def is_merge_commit():
    """Determine if HEAD is a merge commit by counting parents."""
    try:
        result = subprocess.run(
            ["git", "rev-list", "--parents", "-1", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        parents_and_sha = result.stdout.strip().split()
        return len(parents_and_sha) > 2
    except subprocess.CalledProcessError:
        return False


def should_skip_validation(current_subject):
    """
    Returns True when validation should be skipped (merge commits or auto summaries).
    """
    if current_subject.startswith("[git-summary]"):
        return True
    return is_merge_commit()


def _print_escaped_newline_error():
    """Emit loud error message with remediation guidance."""
    banner = "=" * 80
    print(banner, file=sys.stderr)
    print("❌ ERROR: Escaped newlines detected in commit message", file=sys.stderr)
    print(banner, file=sys.stderr)
    print(
        "\nYour commit contains literal '\\n' sequences instead of actual newlines.\n",
        file=sys.stderr,
    )
    print("To fix:", file=sys.stderr)
    print("  git commit --amend", file=sys.stderr)
    print("  # Edit message manually", file=sys.stderr)
    print("\nOr reset and recommit:", file=sys.stderr)
    print("  git reset HEAD~1", file=sys.stderr)
    print("  git add <files>", file=sys.stderr)
    print(
        "  git commit -m \"Subject\" -m \"$(cat <<'EOF'\n  Body text here\n  EOF\n  )\"",
        file=sys.stderr,
    )
    print(
        "\nDetails: .flowji-ai/tools/git-commit-summaries/AGENTS.md#escaped-newlines",
        file=sys.stderr,
    )
    print(banner + "\n", file=sys.stderr)


def validate_latest_commit(current_subject, quiet=False):
    """Validate commit message formatting, skipping merges and summaries."""
    if should_skip_validation(current_subject):
        if not quiet and not current_subject.startswith("[git-summary]"):
            print(
                "[post-commit-summary] Skipping escaped newline validation for merge commit"
            )
        return True

    message = get_latest_commit_message()
    if has_escaped_newlines(message):
        _print_escaped_newline_error()
        return False
    return True


def get_commit_info():
    """Get commit metadata (SHA, author, timestamp, message, branch)."""
    try:
        # Get full commit SHA
        sha_full = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        # Get short commit SHA
        sha_short = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        # Get author name and email
        author_name = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%an", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        author_email = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%ae", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        # Get commit timestamp in ISO 8601 format
        timestamp_raw = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%ai", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        # Parse timestamp and convert to ISO format
        dt = datetime.strptime(timestamp_raw, "%Y-%m-%d %H:%M:%S %z")
        iso_timestamp = dt.isoformat()
        
        # Get commit message subject (first line) and full message
        subject = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        full_message = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%b", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        # Get current branch name
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Get parent SHAs (could be empty for initial commit)
        parents_raw = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%P", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        parents = [p for p in parents_raw.split() if p]
        
        return {
            "sha_full": sha_full,
            "sha_short": sha_short,
            "author_name": author_name,
            "author_email": author_email,
            "timestamp": iso_timestamp,
            "subject": subject,
            "full_message": full_message,
            "branch": branch,
            "parents": parents
        }
    except subprocess.CalledProcessError as e:
        print(f"[post-commit-summary] Error getting commit info: {e}")
        sys.exit(1)


def get_file_changes():
    """Parse git show to get file changes grouped by status."""
    try:
        result = subprocess.run(
            ["git", "show", "--name-status", "--pretty=format:", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )

        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        changes = {
            "created": [],
            "edited": [],
            "deleted": [],
            "renamed": [],
            "other": []
        }

        for line in lines:
            parts = line.split('\t')
            if len(parts) >= 2:
                status = parts[0].strip()
                if status.startswith('R') and len(parts) >= 3:
                    old_path = parts[1].strip()
                    new_path = parts[2].strip()
                    if (
                        not should_ignore_file(old_path)
                        and not should_ignore_file(new_path)
                        and not _is_summary_path(old_path)
                        and not _is_summary_path(new_path)
                    ):
                        changes["renamed"].append((old_path, new_path))
                    continue

                filepath = parts[-1].strip()
                if should_ignore_file(filepath) or _is_summary_path(filepath):
                    continue

                status_char = status[0] if status else ""

                if status_char == "A":
                    changes["created"].append(filepath)
                elif status_char == "M":
                    changes["edited"].append(filepath)
                elif status_char == "D":
                    changes["deleted"].append(filepath)
                else:
                    changes["other"].append(f"{status}: {filepath}")

        return changes
    except subprocess.CalledProcessError as e:
        print(f"[post-commit-summary] Error getting file changes: {e}")
        sys.exit(1)


def should_ignore_file(filepath):
    """Check if a file should be ignored based on common ignore patterns."""
    import fnmatch
    
    ignore_patterns = {
        ".DS_Store",
        "Thumbs.db",
        ".DS_Store?",
        ".DS_Store_?",
        "Icon?",
        ".Spotlight-V100",
        ".Trashes",
        "ehthumbs.db",
        "Thumbs.db:encryptable",
        ".fseventsd",
        ".TemporaryItems",
        ".Trashes"
    }
    
    filename = os.path.basename(filepath)
    
    # Check exact matches
    if filename in ignore_patterns:
        return True
    
    # Check for pattern matches
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(filepath, pattern) or fnmatch.fnmatch(filename, pattern):
            return True
    
    # Check for temporary/lock files
    if re.match(r'^\.~.*\.tmp$', filename) or re.match(r'^.*\.tmp$', filename):
        return True

    return False


def _is_summary_path(filepath):
    """Return True if the path points at the generated summaries directory."""
    normalized = filepath.replace("\\", "/").lstrip("./").rstrip("/")
    if not SUMMARY_SUBDIR_NORMALIZED:
        return False
    return normalized.lower().startswith(SUMMARY_SUBDIR_NORMALIZED.lower())


def get_commit_stats():
    """Get commit statistics using git show --stat --oneline."""
    try:
        result = subprocess.run(
            ["git", "show", "--stat", "--oneline", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[post-commit-summary] Error getting commit stats: {e}")
        return ""


def _parse_iso_timestamp(timestamp_str):
    """Return datetime from ISO string, tolerating trailing Z."""
    normalized = timestamp_str.replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        match = re.match(
            r'^(?P<date>\d{4}-\d{2}-\d{2})T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})',
            timestamp_str,
        )
        if not match:
            raise
        naive = (
            f"{match.group('date')}T{match.group('hour')}:"
            f"{match.group('minute')}:{match.group('second')}"
        )
        return datetime.strptime(naive, "%Y-%m-%dT%H:%M:%S")


def _format_utc_offset(dt):
    """Return formatted UTC offset like +11:00."""
    offset = dt.utcoffset()
    if offset is None:
        return "+00:00"
    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    minutes_abs = abs(total_minutes)
    hours, minutes = divmod(minutes_abs, 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def format_header_timestamp(timestamp_str):
    """Format timestamp for Markdown header in local time with TZ."""
    dt = _parse_iso_timestamp(timestamp_str)
    local_dt = dt.astimezone()
    offset = _format_utc_offset(local_dt)
    tz_name = local_dt.tzname() or "local"
    return f"{local_dt.strftime('%Y-%m-%d %H:%M:%S')} {tz_name} (UTC{offset})"


def format_filename_timestamp(timestamp_str):
    """Format timestamp for filenames (YYYY-MM-DD--HHMMSSZ)."""
    dt = _parse_iso_timestamp(timestamp_str)
    return dt.strftime("%Y-%m-%d--%H%M%SZ")



def _link_path(relative_path: str) -> str:
    """Return a markdown link for the given relative path."""
    rel = relative_path.strip()
    if not rel:
        return relative_path
    url = './' + quote(rel)
    return f'[{rel}]({url})'


def _format_change_item(section_name: str, item: str) -> str:
    """Format bullet list item with markdown links where possible."""
    if section_name != 'Other Changes':
        return f'- {_link_path(item)}'

    value = item.strip()
    if value.startswith('renamed: '):
        payload = value[len('renamed: '):]
        if ' -> ' in payload:
            old, new = payload.split(' -> ', 1)
            return f'- renamed: {_link_path(old)} -> {_link_path(new)}'
        return f'- {value}'

    if ': ' in value:
        status, path_part = value.split(': ', 1)
        return f'- {status}: {_link_path(path_part)}'

    return f'- {value}'


def ensure_output_directory(repo_root):
    """Ensure the summaries directory exists."""
    output_dir = Path(repo_root) / SUMMARY_SUBDIR
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_markdown_summary(repo_root, commit_info, file_changes, stats):
    """Write the structured Markdown summary file."""
    output_dir = ensure_output_directory(repo_root)

    timestamp_str = commit_info["timestamp"]
    timestamp_for_filename = format_filename_timestamp(timestamp_str)
    header_timestamp = format_header_timestamp(timestamp_str)

    filename = f"{timestamp_for_filename}.md"
    filepath = output_dir / filename

    # Handle filename collisions by adding numeric suffix
    counter = 1
    while filepath.exists():
        name_part = timestamp_for_filename
        suffix = f"_{counter}.md"
        filepath = output_dir / f"{name_part}{suffix}"
        counter += 1

    subject_full = commit_info["subject"].strip() if commit_info["subject"] else ""
    if not subject_full:
        subject_full = "(no subject)"
    subject = subject_full[:80]
    comment_body = commit_info["full_message"].strip()
    commit_body_display = comment_body if comment_body else "(none)"

    # Keep commit body as-is - human descriptions are better than auto-generated ones

    if commit_body_display != "(none)":
        # Normalize headings to level three and ensure blank lines after headings
        commit_body_display = re.sub(
            r'^####\s*(.*)$',
            lambda match: f"### {match.group(1).strip()}",
            commit_body_display,
            flags=re.MULTILINE,
        )
        commit_body_display = re.sub(
            r'^###\s*(.*)$',
            lambda match: f"### {match.group(1).strip()}",
            commit_body_display,
            flags=re.MULTILINE,
        )
        commit_body_display = re.sub(
            r'^(### [^\n]+)\n(?!\n)',
            r'\1\n\n',
            commit_body_display,
            flags=re.MULTILINE,
        )


    parents_line = ", ".join(commit_info["parents"]) if commit_info["parents"] else "None"
    author_line = f"{commit_info['author_name']} <{commit_info['author_email']}>"

    lines = [
        "---",
        f"Date Created: {timestamp_str}",
        f"Date Updated: {timestamp_str}",
        f"Branch: {commit_info['branch']}",
        f"Author: {author_line}",
        f"SHA: {commit_info['sha_full']}",
        f"Short SHA: {commit_info['sha_short']}",
        f"Parents: {parents_line}",
        f"Subject: {subject_full!r}",
        "---",
        f"# {header_timestamp} — {subject}",
        "",
        "## Commit Subject",
        "",
        subject_full,
        "",
        commit_body_display,
        ""
    ]

    other_entries = [
        f"renamed: {old} -> {new}" for old, new in file_changes.get("renamed", [])
    ]
    other_entries.extend(file_changes.get("other", []))

    sections = [
        ("Files Created", file_changes.get("created", [])),
        ("Files Edited", file_changes.get("edited", [])),
        ("Files Deleted", file_changes.get("deleted", [])),
        ("Other Changes", other_entries),
    ]

    for section_name, items in sections:
        lines.append(f"## {section_name}")
        lines.append("")
        if items:
            for item in items:
                lines.append(_format_change_item(section_name, item))
        else:
            lines.append("(none)")
        lines.append("")

    if stats:
        lines.append("## Stats")
        lines.append("")
        lines.append("```")
        lines.append(stats)
        lines.append("```")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    return filepath


def apply_retention_policy(output_dir, days=180):
    """Remove summary files older than the specified number of days.

    Only removes files matching the git summary naming pattern (YYYY-MM-DD--HHMMSSZ.md)
    to avoid deleting other markdown files or files in subdirectories.
    """
    import time

    current_time = time.time()
    cutoff_time = current_time - (days * 24 * 60 * 60)  # Convert days to seconds

    # Pattern matches: YYYY-MM-DD--HHMMSSZ.md (optionally with _N suffix for duplicates)
    summary_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}--\d{6}Z(_\d+)?\.md$')

    for file_path in output_dir.glob("*.md"):
        # Only process files in the output_dir itself, not subdirectories
        if file_path.parent != output_dir:
            continue

        # Only process files matching git summary naming pattern
        if not summary_pattern.match(file_path.name):
            continue

        file_mod_time = file_path.stat().st_mtime

        # Check if file is older than cutoff
        if file_mod_time < cutoff_time:
            try:
                file_path.unlink()
                print(f"[post-commit-summary] Removed old summary: {file_path.name}")
            except OSError as e:
                print(f"[post-commit-summary] Warning: Could not remove old file {file_path}: {e}")


def main():
    """Main execution function."""
    try:
        # Check if we're in a recursive hook call (committing the summary itself)
        current_subject = get_latest_commit_subject()

        if current_subject.startswith("[git-summary]"):
            print("[post-commit-summary] Skipping summary generation for git-summary commit")
            return

        if not validate_latest_commit(current_subject):
            # Validation failed; exit successfully so commit flow continues.
            return

        # Get repository root
        repo_root = get_git_repo_root()

        # Get commit information
        commit_info = get_commit_info()

        # Get file changes
        file_changes = get_file_changes()

        # Get commit stats
        stats = get_commit_stats()

        # Write markdown summary
        output_path = write_markdown_summary(repo_root, commit_info, file_changes, stats)

        # Apply retention policy to remove old files
        output_dir = ensure_output_directory(repo_root)
        apply_retention_policy(output_dir, days=180)

        # Print confirmation message
        relative_path = output_path.relative_to(Path(repo_root))
        print(f"[post-commit-summary] wrote {relative_path}")

        # Auto-commit the summary file so it's tracked
        # This prevents issues with tools like GitHub Copilot that scan for untracked files
        try:
            subprocess.run(
                ["git", "add", str(output_path)],
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"[git-summary] Add commit summary for {commit_info['sha_short']}"],
                check=True,
                capture_output=True
            )
            print(f"[post-commit-summary] auto-committed {relative_path}")
        except subprocess.CalledProcessError as e:
            # Non-fatal - summary was created, just not auto-committed
            print(f"[post-commit-summary] Warning: Could not auto-commit summary: {e}", file=sys.stderr)

    except Exception as e:
        print(f"[post-commit-summary] Error: {e}", file=sys.stderr)
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Flowji commit summaries and validate commit messages."
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run escaped newline validation for the latest commit and exit.",
    )
    return parser.parse_args()


def run_validation_only():
    """CLI helper for validation-only mode."""
    try:
        current_subject = get_latest_commit_subject()
        if should_skip_validation(current_subject):
            reason = "git-summary commit" if current_subject.startswith("[git-summary]") else "merge commit"
            print(f"✓ Validation skipped ({reason})")
            return 0

        message = get_latest_commit_message()
        if has_escaped_newlines(message):
            _print_escaped_newline_error()
            return 1

        print("✓ No escaped newlines found")
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"[post-commit-summary] Validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    args = parse_args()
    if args.validate_only:
        sys.exit(run_validation_only())
    main()
