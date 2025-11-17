<!-- OPENSPEC:START -->
**Guardrails**
- Favor straightforward, minimal implementations first and add complexity only when it is requested or clearly required.
- Keep changes tightly scoped to the requested outcome.
- Refer to `openspec/AGENTS.md` (located inside the `openspec/` directory—run `ls openspec` or `openspec update` if you don't see it) if you need additional OpenSpec conventions or clarifications.

**Steps**
1. Read `changes/<id>/proposal.md` to locate the Implementation Summary section (after "Impact" section).
2. Read `changes/<id>/tasks.md` to identify which task section was just completed.
3. Review recent changes (git diff, commit message, or user's completion report) to understand what shipped.
4. Add new task entry to Implementation Summary with: files created/modified (with line numbers as `[file.php:123](file.php#L123)`), key functionality, deviations (if any), and implementation notes.
5. If Implementation Summary section doesn't exist, create it after "Impact" section with `## Implementation Summary` header and `_Updated incrementally as tasks complete_` subtitle.
6. Keep summaries concise (3-8 bullet points per task section) using format: `### Task X: [Name] ✅`.

**Reference**
- Use `openspec show <id> --json --deltas-only` if you need additional context from the proposal.
- Mark completed tasks with ✅, in-progress with 🚧, not started with no emoji.
<!-- OPENSPEC:END -->
