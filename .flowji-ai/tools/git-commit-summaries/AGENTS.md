# Git Commit Summaries - Agent Guidelines

**Version:** 0.5.0

Complete technical reference for AI agents and users working with Git Commit Summaries.

## Overview

This toolkit provides two components:
1. **Post-commit hook** - Generates structured Markdown summaries automatically
2. **`/gc` command** - AI-powered commit message formatter

## Installation

### Multi-Agent `/gc` Command Setup

| Agent | Type | Location | Installation |
|-------|------|----------|--------------|
| Claude Code | Global | `~/.claude/commands/gc.md` | Run installer once |
| Opencode | Global | `~/.config/opencode/command/gc.md` | Run installer once |
| Codex | Global | `~/.codex/prompts/gc.md` | Run installer once |
| GitHub Copilot | Per-project | `.vscode/settings.json` | Manual JSON config |

**Global install (Claude/Opencode/Codex):**
```bash
./.flowji-ai/tools/git-commit-summaries/install_gc_command.sh
```

**Verify:**
```bash
python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py

# Or check manually
md5sum ~/.claude/commands/gc.md ~/.config/opencode/command/gc.md ~/.codex/prompts/gc.md
```

**Copilot setup:**

Add to `.vscode/settings.json`:
```json
{
    "github.copilot.chat.customCommands": [
        {
            "name": "gc",
            "description": "Generate Flowji-style commit subject and body.",
            "prompt": "<COPY FROM templates/gc-command.md>"
        }
    ]
}
```

### Toolkit Installation (Per-Repository)

**Deploy to target repo:**
```bash
./.flowji-ai/tools/git-commit-summaries/deploy_to_repo.sh /path/to/target/repo
```

**Or install in current repo:**
```bash
./.flowji-ai/tools/git-commit-summaries/install_post_commit_hook.sh
```

**Multi-repo bootstrap:**
```bash
./.flowji-ai/tools/git-commit-summaries/bootstrap_git_summaries.sh
```

Installs:
- Post-commit and prepare-commit-msg hooks
- Python summary generator
- Templates and configuration
- Auto-detects custom `core.hooksPath` (e.g., Husky)

## Using `/gc` Command

Type `/gc` in your AI assistant to:

1. Analyze staged changes and detect multi-concern commits
2. Generate Flowji-structured commit message
3. Execute commit with safe heredoc syntax
4. Trigger post-commit summary generation

### Commit Message Structure

Template sections (use only relevant ones):

- **Added** - New files/features with PURPOSE
- **Updated** - Modified files with nested bullets (**bold filename** + specific changes)
- **Moved** - Relocated files with context
- **Removed** - Deletions with rationale
- **Refactored** - Code improvements without behavior changes
- **Ensured** - Validations/guarantees
- **Verified** - Tests/checks performed
- **Extra Notes** - Migration notes, breaking changes

**Example:**
```markdown
### Updated
- Updated **auth-middleware.js** to add JWT expiration validation
  - Added validateTokenExpiry() helper function
  - Modified authenticateRequest() to call expiry check
  - Updated error responses to distinguish expired vs invalid tokens
```

### Safe Commit Execution

**Always use heredoc syntax to prevent escaped `\n` in git history:**

```bash
git commit -m "Subject line" -m "$(cat <<'EOF'
## Commit Body

### Added
- Description here

### Updated
- Updated **filename.js** with changes
  - Specific change 1
  - Specific change 2
EOF
)"
```

#### Advanced: ANSI-C Quoting (Use Sparingly)

Only use ANSI-C quoting if you explicitly need shell variable substitution. It is easier to make mistakes with this method, so prefer heredoc whenever possible.

```bash
git commit -m "Subject line" -m $'## Commit Body\n\n### Added\n\n- Item 1 description'
```

After using any method, always follow Step 5 of the `/gc` workflow (escaped-newline validation) before you finish the task.

## Reading Commit Summaries

### Location and Naming

- **Directory:** `.flowji-ai/memory/git-summaries/`
- **Format:** `YYYY-MM-DD--HHMMSSZ.md`
- **Example:** `2025-10-15--120338Z.md`

### File Structure

```markdown
---
Date Created: 2025-10-15T12:03:38+00:00
Branch: main
Author: Name <email>
SHA: abc123...
Short SHA: abc123d
Parents: def456...
Subject: 'Add feature X'
---
# 2025-10-15 12:03:38 EST (UTC-05:00) — Add feature X

## Commit Subject
Add feature X

## Commit Body (from template sections)
### Added
- Added config-file.json with settings for feature X

## Files Created
- [config-file.json](./config-file.json)

## Files Edited
- [main.js](./main.js)

## Files Deleted
(none)

## Stats
```
diff --git ...
```
```

### For AI Agents

**Best practices:**
1. Read last 5 summaries at session start for project context
2. Use frontmatter metadata for precise commit details
3. Agent sections (Added/Updated) = intent/context
4. Auto-generated sections (Files Created/Edited) = audit trail

**Limitations:**
- No actual diff content (only file lists and stats)
- Files matching ignore patterns excluded
- Commits with `--no-verify` won't have summaries (run script manually)

## Configuration

### Summary Directory

Override default location:
```bash
export GIT_SUMMARY_DIR="docs/summaries"
./.flowji-ai/tools/git-commit-summaries/install_post_commit_hook.sh
```

### Retention Policy

Edit `post_commit_summary.py`:
```python
apply_retention_policy(output_dir, days=180)  # Change days value
```

### Commit Template

Edit template sections:
```
.flowji-ai/tools/git-commit-summaries/templates/commit-template.md
```

## Troubleshooting

### Summaries Not Generating

1. **Check hook exists and is executable:**
   ```bash
   ls -la .git/hooks/post-commit
   chmod +x .git/hooks/post-commit
   ```

2. **Test manually:**
   ```bash
   python3 ./.flowji-ai/tools/git-commit-summaries/post_commit_summary.py
   ```

3. **Check for `--no-verify`:**
   - Hooks skipped if you used `git commit --no-verify`
   - Run Python script manually after commit

### `/gc` Command Not Working

1. **Verify installation:**
   ```bash
   python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py
   ```

2. **Check file locations:**
   - Claude Code: `~/.claude/commands/gc.md`
   - Opencode: `~/.config/opencode/command/gc.md`
   - Codex: `~/.codex/prompts/gc.md`
   - Copilot: `.vscode/settings.json` (per-project)

3. **Auto-fix global commands:**
   ```bash
   python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py --fix
   ```

4. **Scan for Copilot projects:**
   ```bash
   python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py --scan-copilot /path/to/search
   ```

### Escaped Newlines in Commits

**Problem:** Literal `\n` appears instead of actual line breaks, usually when heredoc syntax was not used.

**Detection (preferred):**
```bash
python3 ./.flowji-ai/tools/git-commit-summaries/post_commit_summary.py --validate-only
```
- Prints `✓ Validation skipped` for merge commits or `[git-summary]` auto-commits
- Exits with an error and step-by-step instructions if escaped newlines are found

**Detection (quick check / Step 5):**
```bash
git log -1 --format=%B | grep -c '\\n'
```
Expected output is `0`. Anything greater than zero means the commit message must be fixed.

**Prevention:** Always follow the heredoc workflow in [Safe Commit Execution](#safe-commit-execution) and the Step 5 validation in the `/gc` prompt.

**Fix:**
```bash
# Option 1: Amend the commit message in place
git commit --amend
# Edit the message manually and save

# Option 2: Reset and recommit with heredoc syntax
git reset HEAD~1
git add <files>
git commit -m "Subject" -m "$(cat <<'EOF'
Body text here
EOF
)"
```

**Hook behavior:** When escaped newlines are detected, the post-commit hook prints a loud error, skips summary generation, and exits 0 so the developer can amend or reset without being blocked. Validation automatically skips merge commits and `[git-summary]` auto-commits.

## Deployment Verification

Use the verification script to check all deployments:

```bash
# Check global commands
python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py

# Auto-fix out-of-sync commands
python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py --fix

# Find all Copilot projects
python3 ./.flowji-ai/tools/git-commit-summaries/verify_gc_deployment.py --scan-copilot ~/projects
```

Output shows:
- ✓/✗ installation status for each agent
- Checksum verification
- Copilot project status
- Action items for fixes

## File Structure Reference

```
repo-root/
├── .flowji-ai/
│   ├── memory/
│   │   └── git-summaries/
│   │       └── YYYY-MM-DD--HHMMSSZ.md
│   └── tools/
│       └── git-commit-summaries/
│           ├── post_commit_summary.py
│           ├── verify_gc_deployment.py
│           ├── install_gc_command.sh
│           ├── install_post_commit_hook.sh
│           ├── deploy_to_repo.sh
│           ├── bootstrap_git_summaries.sh
│           ├── hooks/
│           │   ├── post-commit
│           │   └── prepare-commit-msg
│           └── templates/
│               ├── commit-template.md
│               ├── gc-command.md
│               └── session-start-protocol.md
└── .git/
    └── hooks/
        ├── post-commit
        └── prepare-commit-msg
```

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

Current: v0.4.0 - Multi-concern commit detection
