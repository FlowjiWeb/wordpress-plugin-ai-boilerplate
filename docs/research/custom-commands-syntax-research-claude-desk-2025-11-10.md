# Multi-Agent CLI Command Syntax & Format Reference

**Version:** 1.0  
**Date:** 2025-11-10  
**Purpose:** Reference guide for front matter, argument handling, and command formatting across AI CLI tools

---

## Quick Reference Table

| CLI Tool | File Format | Front Matter | Arguments | Shell Execution | File Injection |
|----------|-------------|--------------|-----------|-----------------|----------------|
| **Qwen** | TOML | `prompt`, `description` | `{{args}}`, `$1-$9`, `$NAME` | `!{command}` | `@{path}` |
| **Gemini** | TOML | `description`, `prompt` | `{{args}}`, `$1-$9` | `!{command}` | `@{path}` |
| **Claude Code** | Markdown | YAML frontmatter | `$ARGUMENTS`, `$1-$9` | Bash blocks | `@path` notation |
| **Codex (OpenAI)** | Markdown | YAML frontmatter | `$ARGUMENTS`, `$1-$9` | Inline in prompt | Not documented |
| **OpenCode** | Markdown | YAML frontmatter | `$ARGUMENTS`, `$1`, `$2`, `$NAME` | Not built-in | Not built-in |
| **KiloCode** | Markdown | Prose-based | Context-dependent | Via execute_command tool | Via file tools |
| **GitHub Copilot** | Markdown (.prompt.md) | YAML frontmatter | `${selection}`, variables | Not supported | Markdown links |

---

## 1. Qwen CLI

### File Format
TOML (.toml)

### Basic Command Structure

```toml
prompt = "Your prompt text here"
description = "Brief description for /help menu"
```

### Complete Example

```toml
# File: ~/.qwen/commands/git/commit.toml
# Invocation: /git:commit

description = "Generate a conventional commit message"

prompt = """
Generate a conventional commit message for the staged changes.

Use the format: <type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore

Analyze the git diff and create an appropriate message.
"""
```

### Argument Handling

#### Simple Arguments (All Args as String)

```toml
prompt = "Analyze the following code: {{args}}"
```

Usage: `/command some code here` → `{{args}}` = "some code here"

#### Positional Arguments

```toml
prompt = """
Create a $1 component named $2 with the following features:
$3
"""
```

Usage: `/command React Button "onClick handler"`
- `$1` = "React"
- `$2` = "Button"
- `$3` = "onClick handler"

#### Named Arguments

```toml
prompt = """
Fetch issue $ISSUE_NUMBER from repository $REPO_NAME and analyze it.
"""
```

Usage: Qwen will prompt for each `$NAME` placeholder

**Named Argument Rules:**
- Format: `$NAME` (uppercase letters, numbers, underscores)
- Must start with a letter
- Qwen prompts for each unique placeholder
- Provides clear identification of required values

### Shell Command Execution

```toml
prompt = """
Current git status:
!{git status --short}

Recent commits:
!{git log --oneline -5}

Please analyze and suggest next steps.
"""
```

**Execution Flow:**
1. Shell commands execute first
2. Output is injected into prompt
3. `{{args}}` substitution happens last
4. Final prompt sent to model

**Security:**
- Commands require user confirmation
- Context-aware argument escaping when `{{args}}` inside `!{...}`

### File Content Injection

#### Single File

```toml
prompt = """
Review the following file:

@{src/utils/helper.ts}

Suggest improvements.
"""
```

#### Directory Listing

```toml
prompt = """
Analyze all configuration files:

@{config/}

Check for inconsistencies.
"""
```

**Features:**
- Directory traversal is recursive
- Respects `.gitignore` and `.qwenignore`
- Workspace-aware (searches current and workspace directories)
- Absolute paths allowed if within workspace

### Multi-line Prompts

```toml
prompt = """
Step 1: Analyze the codebase structure
Step 2: Identify performance bottlenecks
Step 3: Suggest optimizations with code examples

Focus on {{args}} specifically.
"""
```

---

## 2. Gemini CLI

### File Format
TOML (.toml)

### Basic Command Structure

```toml
description = "Brief description"
prompt = """
Your prompt here
"""
```

### Complete Example

```toml
# File: ~/.gemini/commands/refactor/pure.toml
# Invocation: /refactor:pure

description = "Refactor code into a pure function"

prompt = """
Please analyze the code I've provided in the current context.
Refactor it into a pure function.

Your response should include:
1. The refactored, pure function code block
2. A brief explanation of the key changes
3. Why these changes contribute to purity

Consider: {{args}}
"""
```

### Argument Handling

#### Simple Arguments

```toml
prompt = "Explain the concept of {{args}} in simple terms"
```

#### With Context

```toml
prompt = """
Review the following context using best practices:

Context: {{args}}

Best practices reference:
@{docs/best-practices.md}
"""
```

### Shell Command Execution

```toml
description = "Generate commit message from staged changes"

prompt = """
Analyze the staged changes:

```diff
!{git diff --staged}
```

Create a conventional commit message following these rules:
- Use present tense
- Start with type (feat/fix/docs/etc)
- Keep subject under 50 characters
"""
```

**Security Features:**
- Confirmation required before execution
- Security check on final resolved command
- Arguments automatically shell-escaped when inside `!{...}`

### File Content Injection

#### Single File

```toml
prompt = """
Review {{args}} against this style guide:

@{.style-guide.md}
"""
```

#### Multiple Files

```toml
prompt = """
Compare the following files:

API Definition:
@{api/schema.yaml}

Implementation:
@{src/api/handlers.ts}

Identify any discrepancies.
"""
```

### Advanced Features

#### Balanced Braces Requirement

Both `!{...}` and `@{...}` require balanced braces inside:

```toml
# ✅ Valid - balanced braces
prompt = "Run: !{jq '.key.subkey' data.json}"

# ❌ Invalid - unbalanced braces
prompt = "Run: !{echo {incomplete}"
```

**Workaround:** Use external script for complex commands

```toml
prompt = "Result: !{./scripts/complex-command.sh}"
```

---

## 3. Claude Code CLI

### File Format
Markdown (.md)

### Basic Command Structure

```markdown
---
description: Brief description of the command
---

# Command Instructions

Your detailed prompt here.
```

### Complete Example

```markdown
<!-- File: ~/.claude/commands/security-review.md -->
<!-- Invocation: /security-review -->

---
description: Review code for security vulnerabilities
---

# Security Review

Perform a comprehensive security review of the provided code.

Focus areas:
1. Input validation
2. Authentication/authorization
3. Data sanitization
4. Injection vulnerabilities
5. Sensitive data exposure

Analyze: $ARGUMENTS
```

### Frontmatter Options

#### Basic Frontmatter

```markdown
---
description: What this command does
---
```

#### Advanced Frontmatter (Proposed/Feature Request)

```markdown
---
description: Fix a GitHub issue by number
argument-hint: "<issue-number>"
allowed-tools: ["Read", "Edit", "Bash(npm run test:*)"]
disable-model-invocation: false
---
```

**Frontmatter Fields:**
- `description` - Shown in `/help` menu (required for SlashCommand tool)
- `argument-hint` - Shows expected parameters in autocomplete
- `allowed-tools` - Tools command can use without prompting
- `disable-model-invocation` - Prevents Claude from auto-invoking (true/false)

### Argument Handling

#### All Arguments

```markdown
---
description: Create a new component
---

# Create Component

Create a new React component: $ARGUMENTS

Include:
- TypeScript types
- PropTypes validation
- Unit tests
```

Usage: `/create-component Button` → `$ARGUMENTS` = "Button"

#### Positional Arguments

```markdown
---
description: Create module structure
---

Create a $1 module in $2 directory with $3 pattern.

Example structure:
- index.ts
- types.ts
- utils.ts
```

Usage: `/command feature src/ barrel-export`
- `$1` = "feature"
- `$2` = "src/"
- `$3` = "barrel-export"

### File References

```markdown
---
description: Review specific file
---

# File Review

Review the file: @README.md

Check for:
- Clarity
- Completeness
- Accuracy
```

**Note:** Uses `@` notation similar to chat interface

### Bash Execution in Prompts

```markdown
---
description: Run tests and analyze
---

# Test Analysis

Execute the test suite and analyze results.

Run:
```bash
npm test
```

If tests fail, identify the issue and suggest fixes.
```

### Namespacing

```markdown
<!-- File: .claude/commands/project/create.md -->
<!-- Invocation: /project:create -->

---
description: Create new project structure
---

Create a project named $ARGUMENTS with standard structure.
```

### SlashCommand Tool Integration

**How It Works:**
- Claude can auto-invoke custom commands when mentioned in instructions
- Requires `description` field in frontmatter
- Command metadata included in context up to character budget

**Character Budget:**
- Default: 10,000 characters
- Custom: Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable
- Includes: command name, args hint, and description

**Preventing Auto-Invocation:**

```markdown
---
description: Destructive operation
disable-model-invocation: true
---
```

---

## 4. Codex (OpenAI) CLI

### File Format
Markdown (.md)

### Basic Command Structure

```markdown
---
description: Brief description
argument-hint: [OPTIONAL_ARGS]
---

Your prompt content here.
```

### Complete Example

```markdown
<!-- File: ~/.codex/prompts/insights.md -->
<!-- Invocation: /prompts:insights -->

---
description: Run Laravel Insights and fix issues
argument-hint: "context note"
---

# Run Laravel Insights and fix every issue (mandatory)

Context:
- Always use Sail. Never run host binaries.
- After major changes, you MUST run Insights and fix ALL issues.
- If user provided context, consider it: $ARGUMENTS

Commands to run:
1) sail artisan insights --no-interaction --format=json --flush-cache

Do:
- Parse the JSON; group findings by Category → File → Line
- Propose minimal diffs to fix each issue
- After proposed edits, ask approval before writing
- Re-run Insights until **clean**; paste final summary
```

### Frontmatter Fields

```markdown
---
description: What the command does
argument-hint: [PARAM1=<value>] [PARAM2="<value>"]
---
```

**Fields:**
- `description` - Shown in command list
- `argument-hint` - Documents expected parameters (optional)

### Argument Handling

#### Basic Arguments

```markdown
---
description: Generate commit message
---

Analyze recent changes and create commit for: $ARGUMENTS
```

#### Positional Arguments

```markdown
---
description: Create feature branch
argument-hint: <feature-name>
---

Create branch: dev/$1
Commit staged changes for: $1
Open draft PR with title: $2
```

Usage: `/prompts:create-feature user-dashboard "Add dashboard UI"`

### Invocation Format

**New Format (v0.46.0+):**
- Commands invoked with `/prompts:` prefix
- Example: `/prompts:insights` not `/insights`

**Change:**
- Earlier versions used `/command-name`
- Current versions require `/prompts:command-name` namespace

### Integration with AGENTS.md

```markdown
<!-- In ~/.codex/AGENTS.md -->

When user mentions "run insights", execute /prompts:insights automatically.

Before any PR:
1. Run /prompts:insights
2. Fix all issues
3. Run /prompts:test-suite
4. Only then create PR
```

**Note:** This is a workaround; SlashCommand tool auto-invocation is requested feature

### Limitations

**Current:**
- Slash commands only work in interactive mode
- `codex exec` does not parse slash commands
- No auto-invocation by model (requested in Issue #4311)

**Requested Features:**
- SlashCommand tool support (like Claude Code)
- Slash commands in `codex exec` mode
- Model-initiated command invocation

---

## 5. OpenCode CLI

### File Format
Markdown (.md)

### Basic Command Structure

```markdown
---
description: "What this command does"
---

Your prompt content here.
Use $ARGUMENTS for all arguments.
Use $1, $2 for positional arguments.
```

### Complete Example

```markdown
<!-- File: .opencode/command/test.md -->
<!-- Invocation: /test -->

---
description: "Run test suite with coverage"
---

Run the full test suite with coverage report and show any failures.

Focus on the failing tests and suggest fixes.

Additional context: $ARGUMENTS
```

### Frontmatter

```markdown
---
description: "Brief command description"
---
```

**Field:**
- `description` - Shown in command list (optional)

### Argument Handling

#### All Arguments

```markdown
---
description: "Create React component"
---

Create a new React component named $ARGUMENTS with TypeScript support.
Include proper typing and basic structure.
```

#### Positional Arguments

```markdown
---
description: "Create module"
---

Create a $1 in the $2 directory.
```

Usage: `/command service features`

#### Named Placeholders

```markdown
---
description: "Process data"
---

Process the $TYPE data from $SOURCE.
```

**Note:** Named arguments like `$TYPE` work similar to positional but with descriptive names

### Config-based Commands

**Alternative to Markdown files:**

```json
{
  "commands": {
    "test": {
      "template": "Run the full test suite with coverage report.\nFocus on failing tests.",
      "description": "Test command"
    },
    "format": {
      "template": "Format all files in $ARGUMENTS using prettier.",
      "description": "Code formatting"
    }
  }
}
```

**Location:** `~/.config/opencode/opencode.json` or `.opencode/opencode.json`

### Current Limitations

**Subdirectory/Namespace Support:**
- Not yet implemented
- Requested in Issue #299
- Currently must use flat structure

**Workaround:**

```
.opencode/command/
├── git-commit.md
├── git-push.md
├── test-unit.md
└── test-integration.md
```

Instead of:

```
.opencode/command/
├── git/
│   ├── commit.md
│   └── push.md
└── test/
    ├── unit.md
    └── integration.md
```

### Proposed Future Format (Issue #299)

```markdown
---
description: "Analyze code for performance"
allowed-tools: ["bash", "read", "edit"]
---

Analyze this code for performance issues: $ARGUMENTS
```

---

## 6. KiloCode CLI

### File Format
Markdown (.md)

### Workflow Structure

```markdown
# Workflow Title

You are helping with [task description]. Follow these steps:

1. First step with specific instructions
   - Sub-detail
   - Use `tool_name` for specific operations

2. Second step
   - More details
   - Conditional logic if needed

3. Final step
   - Completion criteria
```

### Complete Example

```markdown
<!-- File: .kilocode/workflows/submit-pr.md -->
<!-- Invocation: /submit-pr.md -->

# Submit PR Workflow

You are helping submit a pull request. Follow these steps:

1. First, use `search_files` to check for any TODO comments or console.log statements that shouldn't be committed

2. Run tests using `execute_command` with `npm test` or the appropriate test command

3. If tests pass, stage and commit changes with a descriptive commit message

4. Push the branch and create a pull request using `gh pr create`

5. Use `ask_followup_question` to get the PR title and description from the user

Parameters needed (ask if not provided):
- Branch name
- Reviewers to assign
```

### Structure Characteristics

**No Formal Frontmatter:**
- Title is markdown H1
- Instructions are prose-based
- Tool references use backticks

**Step-by-Step Format:**
- Numbered lists for sequential operations
- Bulleted lists for options or details
- Tool names in code formatting: `tool_name`

### Tool References

```markdown
1. Use `search_files` to find pattern: "TODO"
2. Use `execute_command` to run: "npm run lint"
3. Use `read_file` to check: "package.json"
4. Use `write_file` to update configuration
```

**Common Tools:**
- `search_files` - Find files matching pattern
- `execute_command` - Run shell commands
- `read_file` - Read file contents
- `write_file` - Write/update files
- `ask_followup_question` - Prompt user for input

### Parameters/Arguments

```markdown
Parameters needed (ask if not provided):
- $PARAM1
- $PARAM2
- $PARAM3
```

**Note:** Parameters are descriptive, not programmatic placeholders

### Invocation

**Includes File Extension:**
- `/workflow-name.md` (note the `.md`)
- Example: `/submit-pr.md`

**Different from other CLIs:**
- Most CLIs: `/command`
- KiloCode: `/command.md`

### Custom Modes vs Workflows

**Workflows:**
- Location: `.kilocode/workflows/`
- Format: Markdown prose
- Purpose: Multi-step processes

**Custom Modes:**
- Location: `.kilocodemodes` file or `custom_modes.yaml`
- Format: YAML or JSON
- Purpose: AI agent personality/behavior

**Example Mode (YAML):**

```yaml
customModes:
  - slug: test-engineer
    name: 🧪 Test Engineer
    roleDefinition: You are an expert test engineer
    whenToUse: When creating or reviewing tests
    customInstructions: |
      Always write comprehensive test coverage
      Use AAA pattern (Arrange, Act, Assert)
    groups:
      - read
      - edit
```

---

## 7. GitHub Copilot (VS Code/IDEs)

### Custom Commands Status

**Current State:**
- ✅ Supports custom commands via prompt files (.prompt.md)
- Available in VS Code and JetBrains IDEs (public preview)
- Stored in `.github/prompts/` directory
- Can be invoked via `#prompt:name` or `/name` syntax
- GitHub Copilot CLI has separate built-in commands only

### File Format
Markdown (.prompt.md)

### Basic Structure

```markdown
---
mode: 'agent'
model: GPT-4o
tools: ['githubRepo', 'search/codebase']
description: 'Brief description shown in command suggestions'
---

# Prompt Title

Your detailed prompt instructions here.

Use Markdown formatting for clarity.
```

### Complete Example

```markdown
<!-- File: .github/prompts/explain-code.prompt.md -->
<!-- Invocation: #prompt:explain-code or /explain-code -->

---
mode: 'agent'
description: 'Generate a clear code explanation with examples'
---

# Explain Code

Explain the following code in a clear, beginner-friendly way:

**Code to explain:** ${selection}

**Audience:** Beginners

## Requirements

1. Break down the code step-by-step
2. Explain any technical terms
3. Provide a simple analogy if helpful
4. Include a usage example
```

### Frontmatter Fields

```markdown
---
mode: 'agent'                    # 'agent' or 'ask' mode
model: 'GPT-4o'                  # AI model (GPT-4o, Claude Sonnet, etc.)
tools: ['githubRepo', 'search']  # Array of available tools
description: 'Command description'  # Shown in suggestions
---
```

**Field Descriptions:**
- `mode` - How Copilot executes:
  - `'agent'` - Autonomous mode, can use tools and make changes
  - `'ask'` - Advisory mode, provides guidance without actions
- `model` - Specific AI model to use
- `tools` - Array of tools command can access
- `description` - Brief explanation shown when browsing commands

### Built-in Variables

```markdown
Use the currently selected code: ${selection}

Reference workspace files: [filename](../path/to/file.ts)

Reference other prompts: [other-prompt](./other-prompt.prompt.md)
```

**Available Variables:**
- `${selection}` - Currently selected code in editor
- Custom input variables can be defined

### File References

#### Reference Workspace Files

```markdown
---
description: 'Review code against style guide'
---

# Code Review

Compare the selected code against our style guide:

Style Guide: [style-guide.md](../docs/style-guide.md)

Selected Code: ${selection}

Identify any deviations and suggest corrections.
```

#### Reference Other Prompts

```markdown
---
description: 'Create component with tests'
---

# Create Component with Tests

First, create the component using our component template:
[create-component](./create-component.prompt.md)

Then, generate tests using:
[generate-tests](./generate-tests.prompt.md)
```

### Advanced Example

```markdown
<!-- File: .github/prompts/create-assignment.prompt.md -->

---
mode: agent
description: Create a new programming homework assignment
---

# Create New Programming Assignment

## Step 1: Gather Assignment Information
Ask for the assignment topic if not provided.

## Step 2: Create Assignment Structure
- Create a new directory in `assignments/` for the assignment
- Add a `README.md` file using the template at [template](../templates/assignment-template.md)
- Fill out the assignment details and add starter code if needed

## Step 3: Update Website Configuration
- Update `config.json` to include the new assignment
- Set the due date to the current date plus 7 days, unless specified otherwise

## Requirements
- Use consistent formatting across all files
- Include clear learning objectives
- Provide starter code with helpful comments
```

### Invocation Methods

#### Via Chat Context Menu

```
1. Click ➕ icon in chat input
2. Select "Add Prompt File"
3. Choose from available prompts
```

#### Via #prompt: Syntax

```
#prompt:explain-code
```

#### Via Slash Command

```
/explain-code
```

**Note:** Slash command works if prompt file named `explain-code.prompt.md`

### Auto-Apply Configuration

**Automatically include prompts in requests:**

```json
// In .vscode/settings.json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": ".github/prompts/code-style.prompt.md"
    }
  ]
}
```

**Multiple prompts:**

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": ".github/prompts/code-style.prompt.md" },
    { "file": ".github/prompts/naming-conventions.prompt.md" }
  ]
}
```

### Directory Locations

**Workspace Prompts (Shared with Team):**
```
.github/prompts/
├── explain-code.prompt.md
├── generate-tests.prompt.md
└── code-review.prompt.md
```

**User Prompts (Personal, Synced):**
- Stored in user profile folder
- Location varies by platform
- Synced via Settings Sync

**Custom Locations:**
```json
// Configure additional prompt locations
{
  "chat.promptFilesLocations": [
    ".github/prompts",
    "docs/copilot-prompts"
  ]
}
```

### Related Features

#### Custom Instructions (.github/copilot-instructions.md)

**Different from prompt files:**
- Instructions are always applied
- Provide project-wide context
- Define coding standards and preferences

```markdown
<!-- File: .github/copilot-instructions.md -->

# Project Description
This project is an educational website for homework assignments.

## Project Structure
- `assignments/`: Homework subfolders
- `templates/`: Reusable templates
- `assets/`: CSS, JS, images

## Coding Standards
- Use 2 spaces for indentation
- Single quotes for strings
- Document all functions with JSDoc
```

#### Custom Chat Modes (.github/chatmodes/)

**Define specialized Copilot personalities:**

```markdown
<!-- File: .github/chatmodes/security-review.chatmode.md -->

---
description: 💡 Security review specialist
tools: ["codebase", "search"]
---

# 💡 Security Review Assistant

## My Response Style
- Focus on security vulnerabilities
- Reference OWASP Top 10
- Provide remediation guidance

## Rules
- Always check for input validation
- Flag hardcoded secrets
- Suggest security best practices
```

### GitHub Copilot CLI vs IDE

**Important Distinction:**

**GitHub Copilot CLI:**
- Built-in commands only (`/model`, `/delegate`, `/login`, `/feedback`)
- Does NOT support custom prompt files
- Uses `CLAUDE.md` for custom instructions (repository-based)
- Different tool with separate capabilities

**GitHub Copilot in IDE (VS Code/JetBrains):**
- ✅ Supports custom prompt files
- ✅ Supports custom instructions
- ✅ Supports custom chat modes
- Public preview feature

### Comparison with Other Tools

**Similarities to Claude Code:**
- Both use Markdown format
- Both support hierarchical prompt organization
- Both can reference other files

**Differences from CLI Tools:**
- IDE-integrated, not standalone CLI
- Uses `#prompt:` and `/` syntax, not pure `/command`
- Tighter integration with editor context (selections, files)
- Focused on code generation and explanation tasks

### Best Practices

**1. Clear Descriptions:**
```markdown
---
description: 'Generate React component with TypeScript and tests'
---
```

**2. Reference Templates:**
```markdown
Use our component template: [template](../templates/component-template.tsx)
```

**3. Provide Examples:**
```markdown
## Example Output

\`\`\`typescript
export const Button: React.FC<ButtonProps> = ({ children, onClick }) => {
  return <button onClick={onClick}>{children}</button>;
};
\`\`\`
```

**4. Layer with Instructions:**
- Prompts: Specific, repeatable tasks
- Instructions: Project-wide standards
- Chat Modes: Specialized workflows

**5. Team Sharing:**
- Commit prompt files to repository
- Document available prompts in README
- Use consistent naming conventions

---

## Comparison Summary

### File Format Philosophy

**TOML (Qwen/Gemini):**
- ✅ Structured, machine-readable
- ✅ Clear separation of metadata and prompt
- ✅ Easy to parse programmatically
- ❌ Less readable for complex multi-line prompts
- ❌ Requires escaping for certain characters

**Markdown (Claude Code/Codex/OpenCode/KiloCode):**
- ✅ Highly readable
- ✅ Natural for long-form prompts
- ✅ Supports rich formatting (lists, code blocks, headers)
- ✅ Familiar to developers
- ❌ Frontmatter can be overlooked
- ❌ Less structured for programmatic parsing

### Argument Placeholders

| CLI | All Args | Positional | Named | Special Features |
|-----|----------|------------|-------|------------------|
| **Qwen** | `{{args}}` | `$1`-`$9` | `$NAME` | Auto-prompts for named args |
| **Gemini** | `{{args}}` | `$1`-`$9` | ❌ | Context-aware escaping |
| **Claude Code** | `$ARGUMENTS` | `$1`-`$9` | ❌ | SlashCommand tool auto-invoke |
| **Codex** | `$ARGUMENTS` | `$1`-`$9` | ❌ | Integration with AGENTS.md |
| **OpenCode** | `$ARGUMENTS` | `$1`, `$2` | `$NAME` | Config-based alternative |
| **KiloCode** | Context-based | N/A | Descriptive | Prose-based workflows |
| **GitHub Copilot** | N/A | N/A | Variables | `${selection}`, custom vars |

### Special Features

**Shell Execution:**
- **Qwen/Gemini:** `!{command}` with security confirmation
- **Claude Code:** Bash code blocks in markdown
- **Codex:** Inline in prompt (no special syntax)
- **OpenCode/KiloCode:** Via tool system, not inline
- **GitHub Copilot:** Not supported in prompt files

**File Injection:**
- **Qwen/Gemini:** `@{path}` notation with gitignore support
- **Claude Code:** `@path` notation
- **GitHub Copilot:** Markdown links to workspace files
- **Others:** Use tool system (read_file, etc.)

**Auto-Invocation:**
- **Claude Code:** SlashCommand tool enables model to invoke commands
- **Codex:** Requested feature (Issue #4311)
- **GitHub Copilot:** Agent mode can use tools autonomously
- **Others:** Manual invocation only

### Best Practices Across All CLIs

**1. Description Field:**
- Always include clear, concise description
- Users see this in `/help` menu
- Required for auto-invocation features

**2. Argument Documentation:**
- Document expected arguments in description or hint field
- Provide examples in command body
- Use descriptive placeholder names when possible

**3. Error Handling:**
- Include instructions for common failure scenarios
- Guide model on when to ask for clarification
- Specify required vs optional arguments

**4. Security:**
- Whitelist specific commands when using shell execution
- Avoid destructive operations without explicit confirmation
- Use restricted tool access when available

**5. Composability:**
- Keep commands focused on single task
- Allow commands to reference each other
- Build complex workflows from simple commands

**6. Documentation:**
- Add README in command directories
- Include usage examples
- Document any special requirements

---

## Sources

1. [Qwen CLI Commands Documentation](https://github.com/QwenLM/qwen-code/blob/main/docs/cli/commands.md)
2. [Gemini CLI Custom Commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)
3. [Claude Code Slash Commands](https://docs.claude.com/en/docs/claude-code/slash-commands)
4. [Codex CLI Slash Commands Guide](https://developers.openai.com/codex/guides/slash-commands)
5. [OpenCode Commands Documentation](https://opencode.ai/docs/commands/)
6. [KiloCode Workflows Documentation](https://kilocode.ai/docs/features/slash-commands/workflows)
7. [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
8. [Supercharge Your Codex Workflow](https://jpcaparas.medium.com/supercharge-your-codex-workflow-with-slash-commands-a53c59edde38)
9. [Build Global Custom Slash Commands](https://asepalazhari.com/blog/build-global-custom-slash-commands-claude-gemini)
