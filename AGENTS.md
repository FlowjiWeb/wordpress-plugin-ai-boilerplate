---
created: {{CREATION_DATE}}
updated: {{LAST_UPDATE_DATE}}
---

<!-- FLOWJI-AI-GIT-SUMMARIES:START -->

# Flowji AI Git Summaries

These instructions are for AI assistants working in this project.

**Documentation Structure:**
- **ROADMAP.md** - Future planned features and versions
- **CHANGELOG.md** - Complete version history with implementation details
- Completed versions are documented in CHANGELOG only. ROADMAP focuses on what's next.

## Session Start Protocol

At the start of every chat session:

1. **Skim this AGENTS.md** so any standing warnings or rollout notes stay top of mind.
2. **Skip automatic Git summary loading** to conserve context. Only open `.flowji-ai/memory/git-summaries/` when the user explicitly asks about recent changes or when their request clearly depends on the latest commits.
3. **When you do consult summaries, surface information only if:**
   - It directly impacts the user's current request
   - It contradicts what the user is asking for
   - It reveals a breaking change or regression the user should know about
   - It shows recent work on the exact same feature/file the user is asking about

**When to surface:**
- "Note: Recent changes affect this - [brief explanation]"
- "Warning: This contradicts commit abc123 from [date] - [brief explanation]"
- "FYI: This was just modified in commit abc123 - [brief explanation]"

**When NOT to surface:**
- User asks simple question → just answer
- Recent commits unrelated to request → stay silent
- General project updates → keep in context, don't interrupt

**Need a recent history recap?** Browse `.flowji-ai/memory/git-summaries/` manually or run any local tooling you prefer. A dedicated curator workflow is planned, so keep the summaries handy but opt-in only until that ships.

## Git Commit Workflow

This project uses Flowji AI Git Summaries to automatically document all commits.

**How it works:**
- Post-commit hook generates structured markdown summaries in `.flowji-ai/memory/git-summaries/`
- Each commit creates a timestamped file (`YYYY-MM-DD--HHMMSSZ.md`) with metadata, file changes, and stats
- Summaries are retained for 180 days (configurable)

**Agent responsibilities:**
1. **Never commit without user approval** - Always confirm before running git commands
2. **Use `/gc` command for commits** - Generates Flowji-structured messages with detailed nested bullets and bold filenames
3. **Let hooks run automatically** - Post-commit summary generation happens automatically, no intervention needed

**Commit message structure:**
- Subject line (≤72 chars) + structured body with sections: Added, Moved, Updated, Ensured, Verified, Removed, Refactored
- Updated section uses nested bullets: main bullet with **bold filename**, 2-5 sub-bullets with specific changes
- Detail scales with complexity

**Escaped Newlines (Critical):**
- **Problem:** Literal `\n` sequences in commit messages corrupt git history and break summaries
- **Solution:** Always use heredoc syntax: `git commit -m "..." -m "$(cat <<'EOF'\n...\nEOF\n)"`
- **Enforcement:** Post-commit hook automatically validates every commit and rejects if `\n` detected
- **Remediation:** If hook rejects, run `git reset HEAD~1` and recommit using heredoc
- **Details:** See [git-commit-multiline-format.md](.flowji-ai/prompts/git-commit-multiline-format.md) for full guide

Keep this managed block so toolkit updates can refresh the instructions.

<!-- FLOWJI-AI-GIT-SUMMARIES:END -->

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# {{PLUGIN_NAME}} - Agent Guide

## What This Project Is

{{PLUGIN_DESCRIPTION_DETAILED}}

**Current Version:** 1.0.0
**License:** GPL-2.0+

## Development Workflow

Using OpenSpec for all development phases.

See `openspec/ROADMAP.md` for planned features and milestones.

## Local Development Environment

**Shared Docker environment** with other Flowji WordPress plugins.

**Location:** `{{LOCAL_DEV_PATH}}`

**Quick start:**
```bash
# Start shared Docker environment
cd {{LOCAL_DEV_PATH}}
docker-compose up -d

# Deploy this plugin to local
/flowji-ai:push-to-local
```

**Access:**
- WordPress: http://localhost:8080
- Admin: http://localhost:8080/wp-admin
- PHPMyAdmin: http://localhost:8081

**WP CLI:**
```bash
# Full command
docker exec {{DOCKER_CONTAINER_NAME}} wp --allow-root --path=/var/www/html [command]

# Convenience alias (add to ~/.bashrc or ~/.zshrc)
alias wpcli='docker exec {{DOCKER_CONTAINER_NAME}} wp --allow-root --path=/var/www/html'
```

## Tests & Local Development

**PHPUnit/WP_Mock:**
```bash
composer install
composer test
```

**Linting:**
```bash
composer phpcs      # Check coding standards
composer phpcbf     # Auto-fix coding standards
composer phpstan    # Static analysis
composer lint       # Run all checks
```

## Deployment

```bash
./scripts/deploy.sh production
```

See `docs/DEPLOYMENT.md` for detailed deployment instructions.

## Documentation Policy

**README files:**
- **Root README.md:** Minimal, stable content only. User overview, local dev access, links to other docs.
- **plugin/README.md:** Minimal user guide. Installation, usage, troubleshooting, changelog.
- **AGENTS.md (root):** Comprehensive project guide for AI agents and developers.
- **openspec/project.md:** Product context for OpenSpec proposals.
- **plugin/AGENTS.md:** Technical class documentation, database schema, security practices.

**File naming:** Default to kebab-case for new files/folders. Use capitalized names only for canonical docs.

## Technical Documentation

See `plugin/AGENTS.md` for detailed class documentation, database schema, and security practices.
