---
description: Generate Flowji-style commit message from git changes
---

# Generate Commit Message

You are the Flowji commit assistant. Analyze the current git changes to generate a structured commit message following the Flowji template.

## Instructions

1. **Gather context and analyze groupings:**
   - Run `git status` to see staged/unstaged files AND untracked files
   - Run `git diff --cached` if files are staged, otherwise `git diff`
   - Review the actual code changes to understand what changed and why

   **CRITICAL - Multi-Concern Commit Detection:**
   - Analyze if staged changes span multiple UNRELATED concerns that should be separate commits
   - Detection heuristics:
     1. **File type clustering**: Do changes mix documentation (.md) with code (.php/.js/.json)?
     2. **Directory separation**: Do changes span plugin/, docs/, tests/ directories?
     3. **Semantic analysis**: Are changes addressing different features/bugs/concerns?

   - If multiple concerns detected, STOP and suggest splitting:
     "I've detected changes that span multiple unrelated concerns:

     **Concern 1: [Description]**
     - [list files]

     **Concern 2: [Description]**
     - [list files]

     I recommend splitting these into separate atomic commits. Would you like me to:
     1. Commit Concern 1 first, then Concern 2
     2. Let you choose which concern to commit first
     3. Proceed with single commit anyway"

   - Wait for user decision before proceeding
   - If user chooses split: commit first group, then recursively re-run `/gc` for remaining changes

   **CRITICAL - Untracked Files:**
   - If `git status` shows untracked files that are functionally related to the changes being committed, INCLUDE them in the commit
   - Related files include: new test files for new code, new config files for new dependencies, new documentation for new features
   - If unsure whether untracked files belong with current changes, ASK the user before committing
   - Never commit modified files that depend on untracked files without also committing the untracked files

2. **Generate commit message:**
   - **Subject line**: ≤72 characters, summarize WHAT changed
   - **Commit body**: Use template sections below, only include sections with actual content

   **BEFORE generating message - Atomic Commit Check:**
   - Do the staged changes introduce dependencies on unstaged/untracked files?
   - Would the staged changes be incomplete or non-functional without untracked files?
   - If YES to either: STOP and stage related files before proceeding

   Examples of violations:
   - ❌ Staging dependency injection code without staging the tests that use it
   - ❌ Staging composer.json without staging the code that uses the new dependencies
   - ❌ Staging code that references new files without staging those files

3. **Template format:**
```
# Subject line here (≤72 chars)

## Commit Body

### Added
- Describe new files/features with their PURPOSE, not just filenames
- Example: "Added venue-config.json with settings for 2026 Castlemaine course"

### Moved
- Note relocated files/directories with context
- Example: "Moved API handlers from /routes to /api for better organization"

### Updated
- For EACH modified file, use nested bullets with detailed analysis:
  - Main bullet: **bold filename** and high-level change summary
  - Sub-bullets: specific changes (2-4 bullets depending on complexity)
- **IMPORTANT**: Write filenames in bold (`**filename**`) NOT backticks (backticks get stripped by git)
- Analyze diffs to identify: functions modified, sections changed, logic updated
- Example format:
  ```
  - Updated **auth-middleware.js** to add JWT expiration validation
    - Added validateTokenExpiry() helper function
    - Modified authenticateRequest() to call expiry check before proceeding
    - Updated error responses to distinguish expired vs invalid tokens
  ```
- Scale detail to change size: small changes get 1-2 sub-bullets, large changes get 3-5

### Ensured
- Guarantees, validations, or safety mechanisms added
- Example: "Ensured user input is sanitized before database queries"

### Verified
- Tests run, checks performed, validations confirmed
- Example: "Verified all unit tests pass with new dependency versions"

### Removed
- Deletions with rationale if not obvious
- Example: "Removed deprecated OAuth1 support (unused since 2023)"

### Refactored
- Code improvements without behavior changes
- Example: "Refactored date parsing into reusable utility functions"

### Extra Notes
- Additional context, migration notes, breaking changes, etc.
- Example: "Requires npm install due to new dependencies"
```

4. **Guidelines:**
   - Only include sections that have content
   - Omit empty sections entirely (don't use "(none)")
   - Be descriptive: explain WHAT and WHY, not just list filenames
   - Think like a future developer reading git history

5. **Output:**
   - Present the commit message in a fenced markdown code block

   **BEFORE asking to commit:**
   - If untracked files exist that weren't staged, list them and ask:
     "The following untracked files were not included. Should any of these be part of this commit?"
     [list files]

   - Then ask: "Would you like me to commit this automatically?"
   - If yes: Use ONLY the safe file-based commit method below
   - If no/unclear: just present the message for manual use

## Example Output

```markdown
# Add venue configuration for Castlemaine 2026

## Commit Body

### Added
- Added config-castlemaine-2026.json with venue details, course layout, and pricing tiers for new location
- Added venue-loader.js to dynamically load venue configs by year

### Updated
- Updated main-config.js to integrate new venue system
  - Added loadVenueConfig() import from venue-loader
  - Modified initializeApp() to load venue config on startup
  - Updated config validation to check for venue-specific fields
- Updated app.js to handle venue-specific routing
  - Added venue parameter to route handlers
  - Modified error handling for missing venue configs

### Verified
- Tested config loads without errors in dev environment
- Confirmed all venue fields validate correctly
```

Would you like me to commit this automatically?

## Step 4: Execute the Commit (Safe File-Based Method)

**CRITICAL**: Always use the heredoc method below. It is the only supported execution path and guarantees multi-line formatting without literal `\n` sequences.

```bash
git commit -m "Subject line here" -m "$(cat <<'EOF'
## Commit Body

### Added

- Item 1 description
- Item 2 description

### Updated

- Updated **filename** to do something
  - Specific change 1
  - Specific change 2
EOF
)"
```

**Why this works:**
- Heredoc interprets actual newlines correctly
- No escape sequences are created
- Markdown formatting is preserved in git history

## Step 5: Validate Commit (Automatic Hook + Manual Check)

**The hook automatically validates your commit** by checking for literal `\n` sequences. If validation fails, you'll see an error message immediately after commit.

**To manually verify before trusting the hook:**

```bash
git log -1 --format=%B | grep -c '\\n'
```

**Expected output:** `0`

If the output is greater than 0:

**Remediation:**
1. Run: `git reset HEAD~1`
2. Stage files again: `git add <files>`
3. Re-run the commit using the heredoc method in Step 4 above
4. The hook will validate automatically on the second attempt

**Alternative: Manual amend** (if you prefer not to reset):
```bash
git commit --amend
# Edit the message in your editor to use actual newlines, then save
```

## Why This Matters

The hook enforces this automatically because:
- Git history preserves literal `\n` sequences permanently
- Summary generation skips malformed commits (no record created)
- Agents won't see your change reflected in `.flowji-ai/memory/git-summaries/`

See [AGENTS.md](./../../../AGENTS.md#escaped-newlines) for detailed troubleshooting and the escaped newline detection logic.

## Multi-Line Safety Checklist

Before committing, verify:

- [ ] Markdown headers (`##`, `###`) are on separate lines (no literal `\n`)
- [ ] Bullet points have blank lines between sections
- [ ] Heredoc syntax is correct: `$(cat <<'EOF'` ... `EOF\n)"` with actual newlines
- [ ] Test after commit: `git log -1 --format=%B` shows the exact Markdown you expect
