# OpenSpec Archive Validation Idea

## Purpose

Validate that spec requirements match implementation reality before archiving changes. This prevents archiving fictional or outdated requirements that don't reflect what was actually built.

## The Problem

**OpenSpec archival is mechanical, not intelligent:**
- The `openspec archive` command merges spec deltas into source-of-truth
- It validates syntax (ADDED/MODIFIED/REMOVED headers, scenario formatting)
- It does NOT verify that code actually implements the requirements
- It does NOT check if specs were updated when implementation diverged from plan

**Risk:** You can archive complete fiction, creating permanent documentation that contradicts reality.

## Validation Strategy

### Manual Pre-Archive Checklist

Before running `openspec archive <change-id>`, verify:

**1. Implementation Complete**
- [ ] All tasks in `tasks.md` marked `[x]`
- [ ] All task sections have Implementation Summary in `proposal.md`
- [ ] Test suite passes (`composer test`, `npm test`, etc.)

**2. Spec Alignment**
- [ ] Review each Implementation Summary for deviations
- [ ] Compare deviations against spec requirements
- [ ] Update specs if implementation diverged from original plan
- [ ] Verify SHALL/MUST statements match actual behavior

**3. Code Spot-Check**
- [ ] Read referenced files from Implementation Summaries
- [ ] Check 3-5 key scenarios against actual code
- [ ] Verify edge cases described in specs exist in code

**4. Git History Review**
- [ ] Review commit summaries in `.flowji-ai/memory/git-summaries/`
- [ ] Confirm commits align with spec requirements
- [ ] Check for undocumented functionality added during implementation

**5. OpenSpec Validation**
- [ ] Run `openspec validate <change-id> --strict`
- [ ] Resolve any syntax or formatting errors
- [ ] Verify deltas parse correctly: `openspec show <change-id> --json --deltas-only`

### Automated Validation (AI Agent)

**Concept:** Create an AI agent task that validates specs against implementation.

#### Validation Agent Inputs

1. Spec deltas: `openspec/changes/<change-id>/specs/*/spec.md`
2. Implementation summaries: `openspec/changes/<change-id>/proposal.md`
3. Task checklist: `openspec/changes/<change-id>/tasks.md`
4. Git commit history: `.flowji-ai/memory/git-summaries/*.md`
5. Referenced code files: `plugin/includes/class-*.php`

#### Validation Agent Process

For each requirement in spec deltas:

1. **Extract requirement details:**
   - Requirement name
   - SHALL/MUST statements
   - Scenarios (WHEN/THEN conditions)

2. **Find implementation evidence:**
   - Search `proposal.md` for Implementation Summary matching requirement
   - Extract file references (e.g., `file.php:123`)
   - Find related git commits mentioning requirement

3. **Read referenced code:**
   - Open files mentioned in Implementation Summary
   - Search for functions/methods implementing the requirement
   - Verify behavior matches SHALL/MUST statements

4. **Compare and classify:**
   - **VERIFIED:** Spec matches code, git commits confirm implementation
   - **MISMATCH:** Spec says X, code does Y (requires spec update or code fix)
   - **NOT FOUND:** No implementation evidence (missing feature or missing docs)

5. **Generate validation report**

#### Validation Report Format

```markdown
# Archive Validation Report: <change-id>

## Summary
- Total requirements: 15
- Verified: 13 ✅
- Mismatches: 2 ⚠️
- Not found: 0 ❌
- **Ready to archive:** NO

## Detailed Findings

### ✅ VERIFIED: Currency Configuration Interface
**Spec:** Plugin SHALL provide admin interface for configuring currencies
**Evidence:**
- Code: `plugin/includes/class-currency-settings-admin.php:23-156`
- Commit: `e655326f` "Add currency admin interface"
- Tests: `plugin/tests/test-currency-settings-admin.php:45`
**Status:** Requirement matches implementation

### ⚠️ MISMATCH: Default Settings on Activation
**Spec:** Default settings created with 5 currencies (USD, EUR, GBP, AUD, CAD)
**Implementation Summary:** Default currency seeding with 5 currencies
**Code:** `plugin/includes/class-currency-settings.php:47-53`
```php
$defaults = [
    'USD' => ['enabled' => false, 'gateway_id' => ''],
    'EUR' => ['enabled' => false, 'gateway_id' => ''],
    'GBP' => ['enabled' => false, 'gateway_id' => ''],
    // Only 3 currencies in code!
];
```
**Problem:** Spec says 5 currencies, code only defines 3
**Action Required:** Update code to add AUD and CAD, OR update spec to say 3 currencies
**Status:** MISMATCH - must resolve before archive

### ❌ NOT FOUND: Currency Symbol Auto-Detection
**Spec:** Currency symbol auto-determined from ISO 4217 standard
**Implementation Summary:** No mention of symbol auto-detection
**Code:** No evidence in `class-currency-settings.php` or `class-currency-helper.php`
**Git:** No commits mentioning "symbol" or "ISO 4217"
**Problem:** Requirement appears to be unimplemented
**Action Required:** Either implement feature OR remove requirement from spec
**Status:** NOT FOUND - blocking issue

## Resolution Actions

### Before Archive
1. Resolve MISMATCH: Default Settings on Activation
   - Option A: Update code to include AUD and CAD in defaults
   - Option B: Update spec to reflect 3-currency reality
2. Resolve NOT FOUND: Currency Symbol Auto-Detection
   - Option A: Implement auto-detection feature
   - Option B: Remove requirement from spec (defer to Phase 3b)
3. Re-run validation until all requirements VERIFIED
4. Run `openspec validate --strict`
5. Archive change
```

#### Implementation as Slash Command

**Create:** `.claude/commands/openspec/validate-archive.md`

```markdown
---
name: OpenSpec: Validate Archive
description: Pre-archive validation of spec-implementation alignment
category: OpenSpec
tags: [openspec, validation]
---

**Task:** Validate that spec requirements match implementation reality

**Steps:**
1. Determine change ID to validate (from conversation or prompt user)
2. Read all spec deltas: `openspec/changes/<id>/specs/*/spec.md`
3. Read implementation evidence:
   - `proposal.md` Implementation Summary sections
   - `tasks.md` completed checkboxes
   - Git summaries: `.flowji-ai/memory/git-summaries/*.md`
4. For each requirement:
   - Extract SHALL/MUST statements and scenarios
   - Find Implementation Summary evidence
   - Read referenced code files
   - Compare spec to code behavior
   - Classify as VERIFIED, MISMATCH, or NOT FOUND
5. Generate validation report (format above)
6. If any MISMATCH or NOT FOUND:
   - Block archive
   - Provide resolution actions
7. If all VERIFIED:
   - Confirm ready to archive
   - Suggest next step: `openspec archive <id> --yes`

**Output:** Validation report with actionable findings
```

### Workflow Integration

**Add to `tasks.md` template:**

```markdown
## Final Validation (Before Archive)
- [ ] Run `/openspec:validate-archive <change-id>`
- [ ] Resolve all MISMATCH findings (update spec or fix code)
- [ ] Resolve all NOT FOUND findings (implement or remove requirement)
- [ ] Re-run validation until all requirements VERIFIED
- [ ] Run `openspec validate <change-id> --strict`
- [ ] Confirm test suite passes (`composer test`)
- [ ] Archive: `openspec archive <change-id> --yes`
```

## Common Validation Patterns

### Pattern 1: Implementation Summary Says "Deviations: None"

**Validation:** High confidence spec matches code
**Action:** Spot-check 2-3 key scenarios in code as sanity check

### Pattern 2: Implementation Summary Notes Deviation

**Example:**
```markdown
### Task 1: Settings Storage ✅
- **Deviations:** Changed from 3 to 5 default currencies
```

**Validation:** Check if spec was updated to reflect deviation
**Action:** If spec still says 3 currencies, update to 5

### Pattern 3: Task Marked Complete but No Implementation Summary

**Example:**
```markdown
- [x] 1.3 Add frontend component
```

**Validation:** Low confidence - missing documentation
**Action:** Write Implementation Summary before validating

### Pattern 4: Code Reference Doesn't Exist

**Example:**
```markdown
Files: plugin/includes/class-currency-validator.php:45
```

**Validation:** File doesn't exist in repo
**Action:** Check if file was renamed, moved, or reference is incorrect

## Best Practices

### During Implementation

1. **Update specs when implementation diverges**
   - Don't wait until archive to discover mismatches
   - Treat specs as living documents during development

2. **Write detailed Implementation Summaries**
   - Include file references with line numbers
   - Note deviations explicitly
   - Mention git commits by hash

3. **Keep git summaries accurate**
   - Run `/gc` after each task section
   - Summaries become validation evidence

### Before Archive

1. **Review Implementation Summaries sequentially**
   - Compare each task's summary to spec requirements
   - Update specs for any deviations noted

2. **Spot-check critical scenarios in code**
   - Don't rely solely on Implementation Summaries
   - Verify 3-5 key behaviors in actual code

3. **Run automated validation**
   - Use `/openspec:validate-archive` if implemented
   - Resolve all findings before archiving

4. **Final syntax validation**
   - Always run `openspec validate --strict`
   - Fix any formatting or parsing errors

## Future Enhancements

### Test-Based Validation

**Concept:** Map spec scenarios to test cases

```markdown
#### Scenario: Add new currency
- **WHEN** admin navigates to settings
- **THEN** page displays currency list
- **TEST:** `test_currency_settings_page_displays_list()`
```

**Validation:** Check if referenced test exists and passes

### Automated Spec Updates

**Concept:** AI agent proposes spec updates based on Implementation Summaries

```markdown
Task 1 says: "Changed from 3 to 5 default currencies"
Spec line 127 says: "3 currencies"

Proposed update:
- THEN default settings created with 5 currencies (USD, EUR, GBP, AUD, CAD)
```

### Continuous Validation

**Concept:** Validate on every commit, not just before archive

**Workflow:**
1. Commit includes code changes
2. Git hook triggers validation agent
3. Agent checks if changes affect open spec deltas
4. Reports mismatches in commit message or CI

## Summary

**Manual validation:**
- Review Implementation Summaries for deviations
- Spot-check key scenarios in code
- Update specs during implementation, not after
- Run `openspec validate --strict` before archive

**Automated validation (recommended):**
- Create `/openspec:validate-archive` slash command
- AI agent compares specs to code, git commits, and Implementation Summaries
- Blocks archive if mismatches found
- Provides actionable resolution steps

**Goal:** Ensure `openspec/specs/` source-of-truth accurately documents deployed reality, not original proposals that diverged during implementation.
