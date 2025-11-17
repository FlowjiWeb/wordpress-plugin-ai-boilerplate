# Flowji AI Toolkit

**Version:** 0.1.1

Portable AI workflow tools for your repository.

## What is this?

This `.flowji-ai/` directory contains tools that enhance AI-assisted development. Currently installed:

### git-commit-summaries (v0.1.1)
Post-commit summaries in `.flowji-ai/memory/git-summaries/`.

**Features:**
- Markdown summary per commit (metadata + file changes + stats)
- File groupings: created, edited, deleted, renamed
- 180-day retention policy
- Global `/gc` command for detailed commit messages

**Usage:**
- Commit normally → summary auto-generates
- Use `/gc` for AI-generated structured commit messages with nested bullets
- AI agents read summaries to understand repo evolution

**Files:**
- `tools/git-commit-summaries/` - Scripts and documentation
- `memory/git-summaries/*.md` - Generated summaries

## Documentation

- [AGENTS.md](./AGENTS.md) - Instructions for AI agents
- [CHANGELOG.md](./CHANGELOG.md) - Toolkit version history
- Tool-specific docs in `tools/` subdirectories

## License

MIT
