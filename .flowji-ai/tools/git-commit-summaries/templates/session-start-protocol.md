<!-- FLOWJI-AI-GIT-SUMMARIES:START -->

# Flowji AI Git Summaries

These instructions are for AI assistants working in this project.

## Session Start Protocol

At the start of every chat session:

1. **Silently read** the 5 most recent commit summaries from `.flowji-ai/memory/git-summaries/` (sort by filename descending)
2. **Keep context loaded** for the session - do not present unless relevant
3. **Surface critical information only if:**
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

**Note:** If no summaries exist or fewer than 5 commits, load what's available. Skip protocol if directory doesn't exist.

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

Keep this managed block so toolkit updates can refresh the instructions.

<!-- FLOWJI-AI-GIT-SUMMARIES:END -->
