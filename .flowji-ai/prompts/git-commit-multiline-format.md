# Git Commit Multi-Line Message Format Guide

This guide explains how to properly format multi-line commit messages to avoid escaped newline sequences (`\n`) in your git history.

## The Problem

When commit messages are formatted incorrectly, literal `\n` sequences appear in git instead of actual newlines:

```
## Commit Body\n\n### Added\n- Item 1\n- Item 2
```

This corrupts the markdown formatting and makes summaries unreadable.

## The Solution: Use Heredoc Syntax

The heredoc method (`$(cat <<'EOF'...EOF)`) is the only supported execution path because it preserves actual newlines:

```bash
git commit -m "Subject line" -m "$(cat <<'EOF'
## Commit Body

### Added

- Item 1 description
- Item 2 description

### Updated

- Updated **filename** to do something
  - Specific change 1
  - Specific change 2
EOF
)"
```

**Why this works:**
- Shell heredoc treats the text between `EOF` markers as literal input
- Actual newlines in the heredoc are preserved as newlines, not escape sequences
- The outer `$(...)` passes the multi-line text as a single argument to `-m`

## Why Alternative Methods Fail

### ❌ ANSI-C Quoting (`$'...'`)
```bash
git commit -m "Subject" -m $'## Body\n\n### Added'
# ↑ Results in literal \n sequences in git history
```

### ❌ Direct Paste (Copy/Paste with Line Breaks)
```bash
git commit -m "Subject" -m "## Body

### Added"
# ↑ Shell escapes newlines when pasting; results in \n sequences
```

### ❌ Echo with Escape Sequences
```bash
echo -e "## Body\n\n### Added" | git commit -m "Subject" -F -
# ↑ Even with -e flag, newlines get escaped in transmission
```

## How the Hook Detects Escaped Newlines

The post-commit hook runs `post_commit_summary.py` immediately after every commit. It checks for literal `\n` sequences in the commit message:

```python
def has_escaped_newlines(message):
    """Return True if literal \\n sequences appear outside code blocks."""
    if not message:
        return False

    without_fenced = FENCED_CODE_PATTERN.sub("", message)
    without_inline = INLINE_CODE_PATTERN.sub("", message)
    return "\\n" in without_inline
```

**Key behavior:**
- Code blocks (both fenced and inline) are excluded from the check
- Only actual backslash-n sequences are flagged, not real newlines
- If found, the hook prints an error and skips summary generation

## When the Hook Rejects Your Commit

If validation fails, you'll see:

```
================================================================================
❌ ERROR: Escaped newlines detected in commit message
================================================================================

Your commit contains literal '\n' sequences instead of actual newlines.

To fix:
  git commit --amend
  # Edit message manually

Or reset and recommit:
  git reset HEAD~1
  git add <files>
  git commit -m "Subject" -m "$(cat <<'EOF'
  Body text here
  EOF
  )"

Details: .flowji-ai/tools/git-commit-summaries/AGENTS.md#escaped-newlines
================================================================================
```

## Remediation Steps

### Option 1: Reset and Recommit (Recommended)

1. Reset the commit:
   ```bash
   git reset HEAD~1
   ```

2. Stage your changes again:
   ```bash
   git add <files>
   ```

3. Recommit using heredoc (from `.flowji-ai/tools/git-commit-summaries/templates/gc-command.md`):
   ```bash
   git commit -m "Subject line" -m "$(cat <<'EOF'
   ## Commit Body

   ### Added

   - Item 1 description
   - Item 2 description
   EOF
   )"
   ```

4. The hook will validate automatically and accept the commit

### Option 2: Manual Amend

1. Open the editor:
   ```bash
   git commit --amend
   ```

2. In your editor, ensure:
   - Each section (## Added, ## Updated, etc.) is on its own line
   - There are blank lines between sections
   - No `\n` escape sequences appear anywhere
   - Save and exit

3. The hook will validate and accept the amended commit

## Verifying Successful Format

After committing, verify no escaped newlines were stored:

```bash
git log -1 --format=%B | grep -c '\\n'
```

**Expected output:** `0`

If you see a number greater than 0, follow the remediation steps above.

## For CI/CD and Automation

If you're building scripts that generate commits, always use heredoc or direct newline injection:

```bash
# Good: Heredoc with actual newlines
git commit -m "Subject" -m "$(cat <<'EOF'
Body line 1
Body line 2
EOF
)"

# Bad: Will create escaped newlines
git commit -m "Subject" -m "Body line 1\nBody line 2"
```

## Integration with `/gc` Command

The `/gc` command automates this process:

1. **Generate:** Analyzes changes and creates a structured commit message
2. **Execute:** Uses heredoc syntax to preserve formatting
3. **Validate:** Runs the hook's validation automatically after commit
4. **Report:** Shows success or failure to the user

For details on using `/gc`, see [AGENTS.md](../../AGENTS.md#using-gc-command).

## Common Scenarios

### Scenario 1: Manual Multi-Line Commit

```bash
# Stage changes
git add .

# Commit with proper formatting
git commit -m "Add new feature" -m "$(cat <<'EOF'
## Commit Body

### Added
- New authentication module with JWT support
- Database migration for user tokens
EOF
)"
```

### Scenario 2: Editing Existing Commit

```bash
# If you already committed with escaped newlines:
git commit --amend

# In your editor, write actual multi-line text with blank lines, then save
```

### Scenario 3: Detecting in Git History

```bash
# Find commits with escaped newlines
git log --format=%B | grep -c '\\n'

# Show the problematic commit message
git show HEAD --format=%B
```

## Questions?

- **Troubleshooting:** See [AGENTS.md - Escaped Newlines](../../AGENTS.md#escaped-newlines)
- **Template:** See [gc-command.md](../tools/git-commit-summaries/templates/gc-command.md)
- **Hook Details:** See [post_commit_summary.py](../tools/git-commit-summaries/post_commit_summary.py)
