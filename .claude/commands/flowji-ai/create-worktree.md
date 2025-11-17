---
description: Create worktree for parallel multi-agent development
argument-hint: [feature-name] [--base branch]
allowed-tools: Bash(scripts/create-worktree.sh:*)
---

# Create Worktree

Create a new git worktree for parallel development with multiple AI agents.

## Usage

Feature name and optional base branch: $ARGUMENTS

## Instructions

1. Execute the centralized script:
   ```bash
   bash scripts/create-worktree.sh $ARGUMENTS
   ```

2. The script will:
   - Ensure it's running from repo root
   - Fetch the base branch (default: origin/main)
   - Create worktree in ../mpc-<feature-name>
   - Create branch feature/<feature-name> based on the base branch
   - Display next steps

3. Optional flags:
   - `--base <branch>` - Branch from a different base (e.g., `--base origin/release-1.0`)

4. Report the result to the user including:
   - Worktree directory path
   - Branch name
   - Base branch used
   - Next steps (cd to directory, start agent)
