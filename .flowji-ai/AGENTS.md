# Flowji AI Toolkit - Agent Instructions

**Version:** 0.1.0

Instructions for AI agents working in repositories with this toolkit installed.

## Overview

The `.flowji-ai/` directory contains automated workflow tools. When working in this repo:

1. **Check versions**: Read `.flowji-ai/VERSION` and tool-specific VERSION files
2. **Read tool docs**: See `tools/*/AGENTS.md` for tool-specific instructions
3. **Use commit summaries**: Check `.flowji-ai/memory/git-summaries/*.md` for recent commit history

## Installed Tools

### git-commit-summaries (v0.1.0)
Location: `.flowji-ai/tools/git-commit-summaries/`

**Key behaviors:**
- Post-commit hook auto-generates summaries in `.flowji-ai/memory/git-summaries/`
- Use `/gc` command for structured commit messages
- Read summaries to understand recent changes without parsing full git log
- Summaries include file groupings (created/edited/deleted) and stats

**Documentation:** [tools/git-commit-summaries/AGENTS.md](./tools/git-commit-summaries/AGENTS.md)

## Version Management

- Toolkit version: `.flowji-ai/VERSION`
- Tool versions: `.flowji-ai/tools/*/VERSION`
- Report version mismatches if source toolkit is newer than deployed copy
