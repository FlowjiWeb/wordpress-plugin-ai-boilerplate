# Multi-Agent Project Documentation

This project uses multiple LLM/AI systems for development. **ALL agent-specific documentation must be synchronized across systems** - this includes commands, workflows, slash commands, skills, and any other LLM-specific configuration.

## Active Agent Systems

- **Claude Code** (`.claude/`)
- **Qwen** (`.qwen/`)
- **OpenCode** (`.opencode/`)
- **KiloCode** (`.kilocode/`)
- **Gemini CLI** (`.gemini/`)
- **Codex CLI** (global only: `~/.codex/prompts/`)

## Synchronization Scope

This synchronization requirement applies to:
- OpenSpec workflow commands (proposal, apply, archive)
- Slash commands and custom workflows
- Agent-specific skill definitions
- Any LLM-specific documentation or configuration

## Synchronized File Locations

### OpenSpec Commands

When updating OpenSpec workflow commands (proposal, apply, archive, summary), update ALL agent-specific versions:

**OpenSpec Command Files:**
- `.claude/commands/openspec/*.md` (Claude Code)
- `.qwen/commands/openspec-*.md` (Qwen)
- `.opencode/command/openspec-*.md` (OpenCode)
- `.kilocode/workflows/openspec-*.md` (KiloCode)

**Critical:** Content between `<!-- OPENSPEC:START -->` and `<!-- OPENSPEC:END -->` markers must be **identical** across all agents.

### Other Command Files

When creating or updating slash commands, workflows, or skills in any agent system, evaluate whether the functionality should be available across all systems. If yes, create equivalent versions in all agent directories.

**Command/Workflow Locations:**
- `.claude/commands/` (Claude Code, Markdown, ✅ subdirs supported)
  - OpenSpec: `.claude/commands/openspec/`
  - Flowji AI: `.claude/commands/flowji-ai/`
- `.qwen/commands/` (Qwen, TOML, ✅ subdirs supported, invocation: `/namespace:command`)
  - Flowji AI: `.qwen/commands/flowji-ai/`
- `.opencode/command/` (OpenCode, Markdown, ✅ subdirs supported)
- `.kilocode/workflows/` (KiloCode, Markdown, ❓ subdirs unclear, CLI support secondary)
- `.gemini/commands/` (Gemini CLI, TOML, ✅ subdirs supported, invocation: `/namespace:command`)
  - Flowji AI: `.gemini/commands/flowji-ai/`
- `~/.codex/prompts/` (Codex CLI, Markdown, ❌ no subdirs, global only, invocation: `/prompts:name`)

### Validation Process

Before committing changes to any OpenSpec command file, verify synchronization:

```bash
# Check all apply.md files are in sync
diff .claude/commands/openspec/apply.md .qwen/commands/openspec-apply.md
diff .claude/commands/openspec/apply.md .opencode/command/openspec-apply.md
diff .claude/commands/openspec/apply.md .kilocode/workflows/openspec-apply.md

# Repeat for proposal.md and archive.md
diff .claude/commands/openspec/proposal.md .qwen/commands/openspec-proposal.md
# ... etc
```

## Multi-Agent Documentation Strategy

This `AGENTS.md` file exists in each agent directory as a symlink to `.claude/AGENTS.md`:

- `.claude/AGENTS.md` (source file)
- `.qwen/AGENTS.md` → symlink
- `.opencode/AGENTS.md` → symlink
- `.kilocode/AGENTS.md` → symlink

**Important:** Only edit the source file at `.claude/AGENTS.md`. Changes automatically propagate to all agent directories via symlinks.

## OpenSpec Process Documentation

For detailed OpenSpec workflow instructions, see:
- `openspec/AGENTS.md` - Comprehensive OpenSpec methodology
- Individual command files in each agent's commands/workflows directory

## Workflow Reminder

When creating or updating OpenSpec commands:

1. Update the source command file (typically in `.claude/commands/openspec/`)
2. Copy changes to all other agent command locations
3. Verify synchronization using diff commands above
4. Test the command in at least one agent system
5. Commit all synchronized files together
