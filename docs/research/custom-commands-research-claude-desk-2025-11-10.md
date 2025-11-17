# Multi-Agent CLI Custom Commands Research

**Version:** 1.0  
**Date:** 2025-11-10  
**Purpose:** Compare custom command/slash command capabilities across AI CLI tools to organize worktree commands

---

## Comparison Table

| Agent | Custom Commands Support | Directory Structure | Subdirectory Support | File Format | Invocation Syntax | Subdirectory Invocation |
|-------|------------------------|-------------------|---------------------|-------------|------------------|------------------------|
| **Qwen CLI** | ✅ Yes | `~/.qwen/commands/` (global)<br>`<project>/.qwen/commands/` (local) | ✅ Yes | TOML (.toml) | `/command-name` | `/namespace:command`<br>Example: `/git:commit` |
| **Gemini CLI** | ✅ Yes | `~/.gemini/commands/` (global)<br>`<project>/.gemini/commands/` (local) | ✅ Yes | TOML (.toml) | `/command-name` | `/namespace:command`<br>Example: `/git:commit` |
| **OpenCode CLI** | ✅ Yes | `~/.config/opencode/command/` (global)<br>`.opencode/command/` (local) | ⚠️ Requested but not fully implemented | Markdown (.md) | `/command-name` | Feature requested in Issue #299<br>Proposed: `/namespace:command` |
| **KiloCode CLI** | ✅ Yes (via workflows) | `~/.kilocode/workflows/` (global)<br>`.kilocode/workflows/` (local) | ❓ Unclear | Markdown (.md) | `/workflow-name.md` | Not documented |
| **GitHub Copilot** | ✅ Yes (prompt files) | `.github/prompts/` (workspace)<br>User profile location (global) | ❓ Not documented | Markdown (.prompt.md) | `#prompt:name` or `/name` | Not documented |

---

## Detailed Findings

### 1. Qwen CLI

**Custom Commands Support:** Full support with robust implementation

**Directory Structure:**

- Global: `~/.qwen/commands/`
- Project: `<project-root>/.qwen/commands/`

**Subdirectory Support:** ✅ Fully supported

- Subdirectories create namespaced commands
- Path separator (`/` or `\`) converts to colon (`:`)
- Example structure:
  ```
  ~/.qwen/commands/
  ├── test.toml → /test
  └── git/
      └── commit.toml → /git:commit
  ```

**File Format:** TOML (.toml)

**Command Structure:**

```toml
prompt = "Your prompt text here"
description = "Brief description for /help menu"
```

**Argument Support:**

- `{{args}}` - All arguments as single string
- `$1`, `$2`, etc. - Positional arguments
- Named arguments: `$NAME` format (uppercase letters, numbers, underscores)

**Invocation:**

- Simple: `/test`
- Namespaced: `/git:commit`
- With args: `/test argument-here`

**Additional Notes:**

- Project commands override global commands with same name
- Supports shell command execution with `!{...}`
- Supports file content injection with `@{...}`
- Based on Gemini CLI architecture with enhancements for Qwen models

---

### 2. Gemini CLI

**Custom Commands Support:** Full support (original implementation that inspired Qwen)

**Directory Structure:**

- Global: `~/.gemini/commands/`
- Project: `<project-root>/.gemini/commands/`

**Subdirectory Support:** ✅ Fully supported

- Subdirectories create namespaced commands
- Path separator (`/` or `\`) converts to colon (`:`)
- Example structure:
  ```
  ~/.gemini/commands/
  ├── test.toml → /test
  └── refactor/
      └── pure.toml → /refactor:pure
  ```

**File Format:** TOML (.toml)

**Command Structure:**

```toml
description = "Brief description"
prompt = """
Your multi-line prompt here
"""
```

**Argument Support:**

- `{{args}}` - All arguments
- Shell command execution: `!{command}`
- File content injection: `@{path/to/file}`
- Directory listing: `@{path/to/dir}` (recursive)

**Invocation:**

- Simple: `/test`
- Namespaced: `/refactor:pure`
- With args: `/test "argument here"`

**Additional Notes:**

- Project commands override global commands
- Shell commands require confirmation for security
- Supports MCP prompts as slash commands
- Respects `.gitignore` and `.geminiignore`

---

### 3. OpenCode CLI

**Custom Commands Support:** Yes, but evolving

**Directory Structure:**

- Global: `~/.config/opencode/command/` (note: singular "command")
- Project: `.opencode/command/`

**Subdirectory Support:** ⚠️ Requested feature (Issue #299)

- Currently NOT fully supported
- Feature request open since June 2025
- Proposed implementation would follow Claude Code/Gemini CLI pattern
- Proposed namespace pattern: `/project:frontend:component`

**File Format:** Markdown (.md)

**Command Structure:**

```markdown
---
description: "What this command does"
---

Your prompt content here.
Use $ARGUMENTS for all arguments.
Use $1, $2 for positional arguments.
```

**Can also be defined in config:**

```json
{
  "commands": {
    "test": {
      "template": "Run the full test suite...",
      "description": "Test command"
    }
  }
}
```

**Argument Support:**

- `$ARGUMENTS` - All arguments
- `$1`, `$2` - Positional arguments
- Named placeholders: `$NAME` format

**Invocation:**

- `/command-name`
- Namespaced (when implemented): `/namespace:command`

**Additional Notes:**

- File name becomes command name
- Can override built-in commands
- Feature inspired by Claude Code's slash command system
- Community actively requesting namespace/subdirectory support

---

### 4. KiloCode CLI

**Custom Commands Support:** Yes, via "workflows" feature

**Directory Structure:**

- Global: `~/.kilocode/workflows/`
- Project: `.kilocode/workflows/`

**Subdirectory Support:** ❓ Unclear from documentation

- Documentation shows flat structure examples
- No explicit mention of subdirectory/namespace support
- Symlinks are NOT supported (Issue #1826)

**File Format:** Markdown (.md)

**Workflow Structure:**

```markdown
# Submit PR Workflow

You are helping submit a pull request. Follow these steps:

1. First, use `search_files` to check for any TODO comments
2. Run tests using `execute_command` with `npm test`
3. If tests pass, stage and commit changes
4. Push the branch and create PR using `gh pr create`
```

**Invocation:**

- `/workflow-name.md` (includes .md extension)
- Example: `/submit-pr.md`

**Additional Notes:**

- Workflows are step-by-step instructions for the AI
- More like structured prompts than traditional commands
- Custom modes system separate from workflows (`.kilocodemodes` files)
- CLI currently doesn't support custom modes from `custom_modes.yaml` (Issue #3304)
- Focus on VS Code extension, CLI support is secondary

---

### 5. GitHub Copilot (VS Code/IDEs)

**Custom Commands Support:** Yes, via prompt files

**Directory Structure:**

- Workspace: `.github/prompts/` (repository-specific, shared with team)
- User: Stored in current profile folder (synced via Settings Sync)
- Additional: Configurable via `chat.promptFilesLocations` setting

**Subdirectory Support:** ❓ Not explicitly documented

- No clear documentation on subdirectory organization
- Commands stored as individual `.prompt.md` files in prompts directory

**File Format:** Markdown (.prompt.md)

**Command Structure:**

```markdown
---
mode: 'agent'
model: GPT-4o
tools: ['githubRepo', 'search/codebase']
description: 'Brief description of what this prompt does'
---

Your prompt content here.
Use Markdown formatting.
Reference files as: [filename](../path/to/file.md)
Reference other prompts: [prompt](./other-prompt.prompt.md)
```

**Frontmatter Fields:**
- `mode` - 'agent' or 'ask' (how Copilot executes the command)
- `model` - AI model to use (e.g., 'GPT-4o', 'Claude Sonnet')
- `tools` - Array of tools command can use (e.g., ['githubRepo', 'search/codebase'])
- `description` - Brief explanation shown in command suggestions

**Invocation:**

- In chat: `#prompt:name` (references prompt file by name)
- As slash command: `/name` (if prompt file is named `name.prompt.md`)
- Via context menu: ➕ icon to add as context

**Built-in Variables:**
- `${selection}` - Currently selected code
- Input variables can be defined for flexible prompts

**Additional Notes:**

- Prompt files are public preview (VS Code and JetBrains only)
- Files can reference other prompt files for hierarchical organization
- Workspace prompts are committed to repository for team sharing
- User prompts sync across devices via Settings Sync
- Can be configured to auto-apply via `github.copilot.chat.codeGeneration.instructions`
- Also supports custom instructions (`.github/copilot-instructions.md`)
- Also supports custom chat modes (`.github/chatmodes/*.chatmode.md`)
- **Note:** GitHub Copilot CLI has different slash commands (built-in only like `/model`, `/delegate`)

---

## Key Differences Summary

### Invocation Style

- **Qwen/Gemini:** `/command` or `/namespace:command`
- **OpenCode:** `/command` (namespace support pending)
- **KiloCode:** `/workflow.md` (requires .md extension)
- **GitHub Copilot:** `#prompt:name` or `/name` (prompt files in IDE chat)

### File Format

- **Qwen/Gemini:** TOML (.toml) - structured configuration format
- **OpenCode/KiloCode:** Markdown (.md) - more readable, prose-style
- **GitHub Copilot:** Markdown (.prompt.md) - with YAML frontmatter

### Namespace/Organization

- **Qwen/Gemini:** ✅ Full subdirectory support with colon-separated namespaces
- **OpenCode:** ⚠️ Requested but not yet implemented
- **KiloCode:** ❓ Not documented, unclear if supported
- **GitHub Copilot:** ❓ Not explicitly documented

### Maturity

- **Qwen/Gemini:** Most mature, well-documented
- **OpenCode:** Growing, community-driven improvements
- **KiloCode:** Focus on workflows rather than traditional commands
- **GitHub Copilot:** Public preview, IDE-focused (VS Code/JetBrains)

---

## Sources

1. [Qwen CLI Commands Documentation](https://github.com/QwenLM/qwen-code/blob/main/docs/cli/commands.md)
2. [Gemini CLI Custom Commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)
3. [OpenCode Commands Documentation](https://opencode.ai/docs/commands/)
4. [OpenCode Issue #299: Custom Slash Commands](https://github.com/sst/opencode/issues/299)
5. [KiloCode Workflows Documentation](https://kilocode.ai/docs/features/slash-commands/workflows)
6. [Gemini CLI Tutorial - Custom Commands](https://medium.com/google-cloud/gemini-cli-tutorial-series-part-7-custom-slash-commands-64c06195294b)
7. [GitHub Copilot Prompt Files Documentation](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
8. [GitHub Copilot Custom Instructions Guide](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-chat-context)
