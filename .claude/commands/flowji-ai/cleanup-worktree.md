---
description: Remove worktree after PR merge
argument-hint: [feature-name] [--force] [--delete-branch]
allowed-tools: Bash(scripts/cleanup-worktree.sh:*)
---

# Cleanup Worktree

Remove a git worktree after the PR has been merged.

## Usage

Feature name and optional flags: $ARGUMENTS

## Instructions

1. Execute the centralized script:
   ```bash
   bash scripts/cleanup-worktree.sh $ARGUMENTS
   ```

2. The script will:
   - Ensure it's running from repo root
   - Remove the worktree directory
   - Optionally delete the branch (non-interactive)
   - Prune stale worktree registrations
   - Display remaining worktrees

3. Optional flags:
   - `--force` - Force removal even with uncommitted changes
   - `--delete-branch` - Delete the feature branch (default: keep)

4. Report the result to the user including:
   - What was removed
   - Whether branch was deleted or kept
   - Remaining active worktrees
