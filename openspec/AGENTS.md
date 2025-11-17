# OpenSpec Instructions

Instructions for AI coding assistants using OpenSpec for spec-driven development.

## TL;DR Quick Checklist

- Search existing work: `openspec spec list --long`, `openspec list` (use `rg` only for full-text search)
- Decide scope: new capability vs modify existing capability
- Pick a unique `change-id`: kebab-case, verb-led (`add-`, `update-`, `remove-`, `refactor-`)
- Scaffold: `proposal.md`, `tasks.md`, `design.md` (only if needed), and delta specs per affected capability
- Write deltas: use `## ADDED|MODIFIED|REMOVED|RENAMED Requirements`; include at least one `#### Scenario:` per requirement
- Validate: `openspec validate [change-id] --strict` and fix issues
- Request approval: Do not start implementation until proposal is approved

## Three-Stage Workflow

### Stage 1: Creating Changes
Create proposal when you need to:
- Add features or functionality
- Make breaking changes (API, schema)
- Change architecture or patterns  
- Optimize performance (changes behavior)
- Update security patterns

Triggers (examples):
- "Help me create a change proposal"
- "Help me plan a change"
- "Help me create a proposal"
- "I want to create a spec proposal"
- "I want to create a spec"

Loose matching guidance:
- Contains one of: `proposal`, `change`, `spec`
- With one of: `create`, `plan`, `make`, `start`, `help`

Skip proposal for:
- Bug fixes (restore intended behavior)
- Typos, formatting, comments
- Dependency updates (non-breaking)
- Configuration changes
- Tests for existing behavior

**Workflow**
1. Review `openspec/project.md`, `openspec list`, and `openspec list --specs` to understand current context.
2. Choose a unique verb-led `change-id` and scaffold `proposal.md`, `tasks.md`, optional `design.md`, and spec deltas under `openspec/changes/<id>/`.
3. Draft spec deltas using `## ADDED|MODIFIED|REMOVED Requirements` with at least one `#### Scenario:` per requirement.
4. Run `openspec validate <id> --strict` and resolve any issues before sharing the proposal.

### Stage 2: Implementing Changes
Track these steps as TODOs and complete them one by one.

**CRITICAL: Before Starting Implementation**
1. **Verify you're working on the CORRECT OpenSpec change folder**
   ```bash
   openspec list  # Confirm change-id exists
   ls openspec/changes/ | grep <change-id>  # Should show ONE folder only
   ```
2. **Create backup of tasks.md BEFORE making changes**
   ```bash
   # Create backup OUTSIDE git tracking for reference during merge
   cp openspec/changes/<change-id>/tasks.md \
      openspec/changes/<change-id>/tasks.pre-branch-backup.md

   # Add to .gitignore so it's never committed
   echo "openspec/changes/*/tasks.pre-branch-backup.md" >> .gitignore

   # IMPORTANT: Remove this backup file before final commit
   # It's only for merge reference, not for version control
   ```
3. **Record existing completion state** - Note which tasks are already `[x]` complete

**Implementation Steps:**
1. **Read proposal.md** - Understand what's being built
2. **Read design.md** (if exists) - Review technical decisions
3. **Read tasks.md** - Get implementation checklist
4. **Implement tasks sequentially** - Complete in order
5. **Two-commit testing workflow** - After each major task group:
   - Commit implementation: Update implementation summary, run `/gc`
   - Deploy to local: Run `/flowji-ai:push-to-local` (increments version, syncs to Docker)
   - Test in browser: Manual verification in local environment
   - Commit fixes: Run `/gc` again (creates commit only if changes made)
6. **Confirm completion** - Ensure every item in `tasks.md` is finished before updating statuses
7. **Update checklist (non-negotiable)** - `openspec/changes/<id>/tasks.md` is the canonical task tracker. After each task + validation step is complete, immediately flip its bullet to `- [x]` (or add a status note if partially done). When an entire task section is complete, add a line like `> Completed in abc1234 (2025-11-15)` referencing the commit that satisfied it. Do not mark implementation summaries or QA gates complete—and do not run `/gc`—while checkboxes misrepresent reality.
8. **Approval gate** - Do not start implementation until the proposal is reviewed and approved

**Updating tasks.md - DO's and DON'Ts**

✅ **Safe Updates (ONLY do these):**
- Add `[x]` to completed task bullets
- Add 1-2 line notes under completed items (test results, bugs found, file references)
- Add `> Completed in abc1234 (YYYY-MM-DD)` at end of completed task sections
- Preserve ALL existing task structure, wording, and prior completion markers

❌ **NEVER Do These:**
- Create new OpenSpec change folders when one already exists
- Expand simple bullets into detailed sub-tasks (structural change)
- Reorganize or rewrite task descriptions
- Overwrite with completely different task format
- Lose prior completed `[x]` checkboxes from previous work
- Remove or modify task sections completed by other agents

**Merge Conflict Resolution:**

When merging feature branch and `tasks.md` conflicts occur:

```bash
# NEVER blindly accept theirs or ours
# Instead, manual 3-way merge:

# 1. Extract both versions
git show HEAD:openspec/changes/<id>/tasks.md > /tmp/main-version.md
git show MERGE_HEAD:openspec/changes/<id>/tasks.md > /tmp/branch-version.md

# 2. Compare versions
diff /tmp/main-version.md /tmp/branch-version.md

# 3. Manually merge YOUR completion updates INTO main's structure
#    - Keep main's task structure
#    - Add your [x] checkboxes
#    - Add your completion notes
#    - Preserve all pre-existing [x] markers from main

# 4. Verify merge preserves all prior work
git diff HEAD openspec/changes/<id>/tasks.md
# Should show ONLY your new [x] markers and notes, NOT wholesale rewrites

# 5. Stage resolved file
git add openspec/changes/<id>/tasks.md
```

**Red Flags During Merge:**
- ❌ Diff shows `-[x]` (removing completed checkboxes) → STOP, you're losing work
- ❌ Diff shows entire task section rewrites → STOP, merge manually
- ❌ Multiple OpenSpec folders with similar names → STOP, you created a duplicate
- ❌ `tasks.md` went from simple bullets to detailed sub-tasks → STOP, structural change

**Merging Other OpenSpec Files:**

When merging conflicts in `proposal.md`, `design.md`, or `specs/**/*.md`:

1. **proposal.md conflicts:**
   - Review both versions carefully
   - Combine implementation summaries from both branches
   - Preserve all technical decisions and rationale
   - Keep both sides' references and documentation links

2. **design.md conflicts:**
   - Preserve all technical decisions from both sides
   - Merge architecture diagrams and flow descriptions
   - Keep both branches' implementation notes
   - Verify no critical constraints were removed

3. **spec delta files (`specs/*/spec.md`) conflicts:**
   - Carefully merge requirements from both versions
   - Don't overwrite - combine both sides' specifications
   - Preserve all acceptance criteria
   - Verify no test scenarios were lost

**General Merge Principle:** When in doubt, keep both sides' content. It's better to have redundant documentation than to lose critical information from either branch.

### Local Testing Workflow (WordPress Plugins)

For WordPress plugins with Docker local-dev environments:

1. **After code changes:** Run `/flowji-ai:push-to-local`
   - Increments patch version (e.g., 1.0.25 → 1.0.26)
   - Syncs `plugin/` → `.local-dev-environments/hive-happierbees/public_html/wp-content/plugins/[plugin-name]/`
   - Makes code testable in browser before completion

2. **Version strategy:**
   - Patch increment: Each task group deployed to local
   - Minor increment: Phase complete and production-ready
   - Major increment: Breaking changes

3. **Test before marking complete:**
   - Browser automation tests
   - Manual UI verification
   - Real checkout flows (if applicable)

### Stage 3: Archiving Changes
After deployment, create separate PR to:
- Move `changes/[name]/` → `changes/archive/YYYY-MM-DD-[name]/`
- Update `specs/` if capabilities changed
- Use `openspec archive <change-id> --skip-specs --yes` for tooling-only changes (always pass the change ID explicitly)
- Run `openspec validate --strict` to confirm the archived change passes checks

## Before Any Task

**Context Checklist:**
- [ ] Read relevant specs in `specs/[capability]/spec.md`
- [ ] Check pending changes in `changes/` for conflicts
- [ ] Read `openspec/project.md` for conventions
- [ ] Run `openspec list` to see active changes
- [ ] Run `openspec list --specs` to see existing capabilities

**Before Creating Specs:**
- Always check if capability already exists
- Prefer modifying existing specs over creating duplicates
- Use `openspec show [spec]` to review current state
- If request is ambiguous, ask 1–2 clarifying questions before scaffolding

### Search Guidance
- Enumerate specs: `openspec spec list --long` (or `--json` for scripts)
- Enumerate changes: `openspec list` (or `openspec change list --json` - deprecated but available)
- Show details:
  - Spec: `openspec show <spec-id> --type spec` (use `--json` for filters)
  - Change: `openspec show <change-id> --json --deltas-only`
- Full-text search (use ripgrep): `rg -n "Requirement:|Scenario:" openspec/specs`

## Quick Start

### CLI Commands

```bash
# Essential commands
openspec list                  # List active changes
openspec list --specs          # List specifications
openspec show [item]           # Display change or spec
openspec validate [item]       # Validate changes or specs
openspec archive <change-id> [--yes|-y]   # Archive after deployment (add --yes for non-interactive runs)

# Project management
openspec init [path]           # Initialize OpenSpec
openspec update [path]         # Update instruction files

# Interactive mode
openspec show                  # Prompts for selection
openspec validate              # Bulk validation mode

# Debugging
openspec show [change] --json --deltas-only
openspec validate [change] --strict
```

### Command Flags

- `--json` - Machine-readable output
- `--type change|spec` - Disambiguate items
- `--strict` - Comprehensive validation
- `--no-interactive` - Disable prompts
- `--skip-specs` - Archive without spec updates
- `--yes`/`-y` - Skip confirmation prompts (non-interactive archive)

## Directory Structure

```
openspec/
├── project.md              # Project conventions
├── specs/                  # Current truth - what IS built
│   └── [capability]/       # Single focused capability
│       ├── spec.md         # Requirements and scenarios
│       └── design.md       # Technical patterns
├── changes/                # Proposals - what SHOULD change
│   ├── [change-name]/
│   │   ├── proposal.md     # Why, what, impact
│   │   ├── tasks.md        # Implementation checklist
│   │   ├── design.md       # Technical decisions (optional; see criteria)
│   │   └── specs/          # Delta changes
│   │       └── [capability]/
│   │           └── spec.md # ADDED/MODIFIED/REMOVED
│   └── archive/            # Completed changes
```

## Creating Change Proposals

### Decision Tree

```
New request?
├─ Bug fix restoring spec behavior? → Fix directly
├─ Typo/format/comment? → Fix directly  
├─ New feature/capability? → Create proposal
├─ Breaking change? → Create proposal
├─ Architecture change? → Create proposal
└─ Unclear? → Create proposal (safer)
```

### Proposal Structure

1. **Create directory:** `changes/[change-id]/` (kebab-case, verb-led, unique)

2. **Write proposal.md:**
```markdown
# Change: [Brief description of change]

## Why
[1-2 sentences on problem/opportunity]

## What Changes
- [Bullet list of changes]
- [Mark breaking changes with **BREAKING**]

## Impact
- Affected specs: [list capabilities]
- Affected code: [key files/systems]

## Implementation Summary

_Updated incrementally as tasks complete_

### Task 1: [Task Name] ✅
- Brief summary of what shipped
- Files: [file.php:123](file.php#L123)
- **Deviations:** None (or list any)
- **Notes:** Implementation decisions
```

3. **Create spec deltas:** `specs/[capability]/spec.md`
```markdown
## ADDED Requirements
### Requirement: New Feature
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result

## MODIFIED Requirements
### Requirement: Existing Feature
[Complete modified requirement]

## REMOVED Requirements
### Requirement: Old Feature
**Reason**: [Why removing]
**Migration**: [How to handle]
```
If multiple capabilities are affected, create multiple delta files under `changes/[change-id]/specs/<capability>/spec.md`—one per capability.

4. **Create tasks.md:**
```markdown
## 1. Implementation
- [ ] 1.1 Create database schema
- [ ] 1.2 Implement API endpoint
- [ ] 1.3 Add frontend component
- [ ] 1.4 Write unit tests for Task 1: Test schema, API validation. Run `composer test` to verify
- [ ] 1.5 Update implementation summary in proposal.md, run `/gc` to commit implementation
- [ ] 1.6 Run `/flowji-ai:push-to-local` to deploy to local-dev for testing
- [ ] 1.7 Manual testing in browser, fix any bugs found
- [ ] 1.8 Run `/gc` to commit any fixes
```

**Note:** Each task section follows the two-commit testing pattern: implement → commit → deploy → test → commit fixes.

**Testing Strategy (Incremental Pattern):**
- Add test checkpoints after major milestones (e.g., Task 1.4, Task 4.7, Task 7.6)
- Run test suite (`composer test`, `npm test`, etc.) at each checkpoint before proceeding
- Catch bugs early rather than discovering them all at the end
- Include a final comprehensive test review task that adds edge cases

5. **Create design.md when needed:**
Create `design.md` if any of the following apply; otherwise omit it:
- Cross-cutting change (multiple services/modules) or a new architectural pattern
- New external dependency or significant data model changes
- Security, performance, or migration complexity
- Ambiguity that benefits from technical decisions before coding

Minimal `design.md` skeleton:
```markdown
## Context
[Background, constraints, stakeholders]

## Goals / Non-Goals
- Goals: [...]
- Non-Goals: [...]

## Decisions
- Decision: [What and why]
- Alternatives considered: [Options + rationale]

## Risks / Trade-offs
- [Risk] → Mitigation

## Migration Plan
[Steps, rollback]

## Open Questions
- [...]
```

## Spec File Format

### Critical: Scenario Formatting

**CORRECT** (use #### headers):
```markdown
#### Scenario: User login success
- **WHEN** valid credentials provided
- **THEN** return JWT token
```

**WRONG** (don't use bullets or bold):
```markdown
- **Scenario: User login**  ❌
**Scenario**: User login     ❌
### Scenario: User login      ❌
```

Every requirement MUST have at least one scenario.

### Requirement Wording
- Use SHALL/MUST for normative requirements (avoid should/may unless intentionally non-normative)

### Delta Operations

- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes

Headers matched with `trim(header)` - whitespace ignored.

#### When to use ADDED vs MODIFIED
- ADDED: Introduces a new capability or sub-capability that can stand alone as a requirement. Prefer ADDED when the change is orthogonal (e.g., adding "Slash Command Configuration") rather than altering the semantics of an existing requirement.
- MODIFIED: Changes the behavior, scope, or acceptance criteria of an existing requirement. Always paste the full, updated requirement content (header + all scenarios). The archiver will replace the entire requirement with what you provide here; partial deltas will drop previous details.
- RENAMED: Use when only the name changes. If you also change behavior, use RENAMED (name) plus MODIFIED (content) referencing the new name.

Common pitfall: Using MODIFIED to add a new concern without including the previous text. This causes loss of detail at archive time. If you aren’t explicitly changing the existing requirement, add a new requirement under ADDED instead.

Authoring a MODIFIED requirement correctly:
1) Locate the existing requirement in `openspec/specs/<capability>/spec.md`.
2) Copy the entire requirement block (from `### Requirement: ...` through its scenarios).
3) Paste it under `## MODIFIED Requirements` and edit to reflect the new behavior.
4) Ensure the header text matches exactly (whitespace-insensitive) and keep at least one `#### Scenario:`.

Example for RENAMED:
```markdown
## RENAMED Requirements
- FROM: `### Requirement: Login`
- TO: `### Requirement: User Authentication`
```

## Troubleshooting

### Common Errors

**"Change must have at least one delta"**
- Check `changes/[name]/specs/` exists with .md files
- Verify files have operation prefixes (## ADDED Requirements)

**"Requirement must have at least one scenario"**
- Check scenarios use `#### Scenario:` format (4 hashtags)
- Don't use bullet points or bold for scenario headers

**Silent scenario parsing failures**
- Exact format required: `#### Scenario: Name`
- Debug with: `openspec show [change] --json --deltas-only`

### Validation Tips

```bash
# Always use strict mode for comprehensive checks
openspec validate [change] --strict

# Debug delta parsing
openspec show [change] --json | jq '.deltas'

# Check specific requirement
openspec show [spec] --json -r 1
```

## Happy Path Script

```bash
# 1) Explore current state
openspec spec list --long
openspec list
# Optional full-text search:
# rg -n "Requirement:|Scenario:" openspec/specs
# rg -n "^#|Requirement:" openspec/changes

# 2) Choose change id and scaffold
CHANGE=add-two-factor-auth
mkdir -p openspec/changes/$CHANGE/{specs/auth}
printf "## Why\n...\n\n## What Changes\n- ...\n\n## Impact\n- ...\n" > openspec/changes/$CHANGE/proposal.md
printf "## 1. Implementation\n- [ ] 1.1 ...\n" > openspec/changes/$CHANGE/tasks.md

# 3) Add deltas (example)
cat > openspec/changes/$CHANGE/specs/auth/spec.md << 'EOF'
## ADDED Requirements
### Requirement: Two-Factor Authentication
Users MUST provide a second factor during login.

#### Scenario: OTP required
- **WHEN** valid credentials are provided
- **THEN** an OTP challenge is required
EOF

# 4) Validate
openspec validate $CHANGE --strict
```

## Multi-Capability Example

```
openspec/changes/add-2fa-notify/
├── proposal.md
├── tasks.md
└── specs/
    ├── auth/
    │   └── spec.md   # ADDED: Two-Factor Authentication
    └── notifications/
        └── spec.md   # ADDED: OTP email notification
```

auth/spec.md
```markdown
## ADDED Requirements
### Requirement: Two-Factor Authentication
...
```

notifications/spec.md
```markdown
## ADDED Requirements
### Requirement: OTP Email Notification
...
```

## Best Practices

### Simplicity First
- Default to <100 lines of new code
- Single-file implementations until proven insufficient
- Avoid frameworks without clear justification
- Choose boring, proven patterns

### Complexity Triggers
Only add complexity with:
- Performance data showing current solution too slow
- Concrete scale requirements (>1000 users, >100MB data)
- Multiple proven use cases requiring abstraction

### Clear References
- Use `file.ts:42` format for code locations
- Reference specs as `specs/auth/spec.md`
- Link related changes and PRs

### Capability Naming
- Use verb-noun: `user-auth`, `payment-capture`
- Single purpose per capability
- 10-minute understandability rule
- Split if description needs "AND"

### Change ID Naming
- Use kebab-case, short and descriptive: `add-two-factor-auth`
- Prefer verb-led prefixes: `add-`, `update-`, `remove-`, `refactor-`
- Ensure uniqueness; if taken, append `-2`, `-3`, etc.

**Phase-based projects:** Prefix with `phase-N-` or `phase-Na-` for clarity:
- `phase-3a-add-currency-settings`
- `phase-4a-affiliate-ledger`
- `phase-4b-commission-calculations`

**Why:** Immediately shows execution sequence without cross-referencing roadmap.

**When to create:** Just-in-time when starting work, not upfront for all future phases.

## Tool Selection Guide

| Task | Tool | Why |
|------|------|-----|
| Find files by pattern | Glob | Fast pattern matching |
| Search code content | Grep | Optimized regex search |
| Read specific files | Read | Direct file access |
| Explore unknown scope | Task | Multi-step investigation |

## Error Recovery

### Change Conflicts
1. Run `openspec list` to see active changes
2. Check for overlapping specs
3. Coordinate with change owners
4. Consider combining proposals

### Validation Failures
1. Run with `--strict` flag
2. Check JSON output for details
3. Verify spec file format
4. Ensure scenarios properly formatted

### Missing Context
1. Read project.md first
2. Check related specs
3. Review recent archives
4. Ask for clarification

## Quick Reference

### Stage Indicators
- `changes/` - Proposed, not yet built
- `specs/` - Built and deployed
- `archive/` - Completed changes

### File Purposes
- `proposal.md` - Why and what
- `tasks.md` - Implementation steps
- `design.md` - Technical decisions
- `spec.md` - Requirements and behavior

### CLI Essentials
```bash
openspec list              # What's in progress?
openspec show [item]       # View details
openspec validate --strict # Is it correct?
openspec archive <change-id> [--yes|-y]  # Mark complete (add --yes for automation)
```

Remember: Specs are truth. Changes are proposals. Keep them in sync.

## Multi-Agent Command Synchronization

When updating OpenSpec workflow commands (proposal, apply, archive), update ALL agent-specific versions:

**Command files to sync:**
- `.claude/commands/openspec/*.md` (Claude Code)
- `.opencode/command/openspec-*.md` (OpenCode)
- `.kilocode/workflows/openspec-*.md` (KiloCode)
- `.qwen/commands/openspec-*.md` (Qwen)

**Critical:** Content between `<!-- OPENSPEC:START -->` and `<!-- OPENSPEC:END -->` markers must be identical across all agents.

**Multi-Agent Documentation:**
Each agent directory contains an `AGENTS.md` file documenting the multi-agent synchronization pattern:
- `.claude/AGENTS.md` (source file)
- `.qwen/AGENTS.md` → symlink
- `.opencode/AGENTS.md` → symlink
- `.kilocode/AGENTS.md` → symlink

See any `AGENTS.md` file for detailed synchronization instructions and validation commands.

**Validation:**
```bash
# Check all apply.md files are in sync (use same pattern for proposal.md, archive.md)
diff .claude/commands/openspec/apply.md .opencode/command/openspec-apply.md
diff .claude/commands/openspec/apply.md .kilocode/workflows/openspec-apply.md
diff .claude/commands/openspec/apply.md .qwen/commands/openspec-apply.md
```
