# /openspec:merge-tasks

Safely merge completed task checkboxes from feature branch into main's tasks.md without losing prior work.

## Purpose

When merging a feature branch that updated `openspec/changes/<id>/tasks.md`, this command helps you:
1. Identify what changed in your branch vs main
2. Preserve all pre-existing completion markers from main
3. Add only your new completion markers and notes
4. Avoid accidentally overwriting the file or losing previous work

## Usage

```
/openspec:merge-tasks <change-id>
```

**Example:**
```
/openspec:merge-tasks phase-3f-product-pricing-ux
```

## What This Command Does

### Step 1: Pre-Merge Verification
- Confirms you're in the middle of a merge (checks for `MERGE_HEAD`)
- Verifies the change-id exists
- Checks for duplicate OpenSpec folders (red flag)

### Step 2: Check for Divergence
```bash
# Find common ancestor (merge base)
git merge-base HEAD MERGE_HEAD

# Check if main has new commits since branch creation
git log --oneline $(git merge-base HEAD MERGE_HEAD)..HEAD -- openspec/changes/<id>/tasks.md

# If output shows commits, main has diverged - rebase recommended
```

### Step 3: Extract Versions
```bash
# Get main's version (current HEAD)
git show HEAD:openspec/changes/<id>/tasks.md > /tmp/main-tasks.md

# Get your branch's version (being merged)
git show MERGE_HEAD:openspec/changes/<id>/tasks.md > /tmp/branch-tasks.md

# Show diff to review changes
diff -u /tmp/main-tasks.md /tmp/branch-tasks.md
```

### Step 4: Guided Merge Decision

**Option A: Auto-merge safe (use branch version)**

ONLY if ALL conditions are met:
- ✅ Branch has same base commit as current HEAD (no divergence)
- ✅ Diff shows ONLY new `[x]` markers and completion notes added
- ✅ Main's task structure unchanged since branch creation
- ✅ No prior `[x]` markers removed in branch
- ✅ Main gained NO new `[x]` markers after branch was cut

**Option B: Rebase or manual merge required**

If ANY of these conditions exist:
- ❌ Main gained new `[x]` markers after branch was created
- ❌ Branch has different base than current HEAD (diverged)
- ❌ Diff shows task rewrites or format changes
- ❌ Prior `[x]` markers removed in branch

**Critical:** Never blindly use branch version if main has been updated with new completion markers. You'll lose concurrent work from other agents.

### Step 5: Apply Merge

**If auto-merge safe:**
```bash
# ONLY use this if ALL conditions above are met
# Your branch version has main's work + your updates
git checkout --theirs openspec/changes/<id>/tasks.md
git add openspec/changes/<id>/tasks.md
```

**If main has diverged (gained new [x] markers):**
```bash
# Option 1: Rebase your branch onto latest main (recommended)
git rebase main

# Option 2: Manual 3-way merge
# 1. Open both versions side-by-side
code /tmp/main-tasks.md /tmp/branch-tasks.md

# 2. Manually edit the conflicted file
code openspec/changes/<id>/tasks.md

# 3. Keep main's structure + main's new [x] markers + your new [x] markers
# 4. Verify all completion markers from both sides preserved
# 5. Stage when satisfied
git add openspec/changes/<id>/tasks.md
```

**If structural changes detected:**
```bash
# Manual merge required - no auto-merge possible
# Command displays side-by-side comparison
# You manually edit tasks.md to combine both versions
# Then stage when ready: git add openspec/changes/<id>/tasks.md
```

### Step 6: Verification

Shows final diff to confirm:
- ✅ All pre-existing `[x]` markers preserved
- ✅ Your new `[x]` markers added
- ✅ Task structure unchanged
- ✅ No sections accidentally removed

## Safety Checks

**Before running:**
- [ ] You're in the middle of a git merge (has `MERGE_HEAD`)
- [ ] Merge conflict exists on `tasks.md`
- [ ] No duplicate OpenSpec folders created

**During merge:**
- [ ] Reviews diff to detect structural changes
- [ ] Warns if prior completion markers being removed
- [ ] Aborts if wholesale task rewrites detected

**After merge:**
- [ ] Shows final diff for confirmation
- [ ] Verifies task count unchanged (unless intentionally modified)
- [ ] Confirms all prior `[x]` markers still present

## When to Use This Command

✅ **Use when:**
- Merging feature branch with `tasks.md` completion updates
- Git shows merge conflict on `openspec/changes/<id>/tasks.md`
- You want to safely preserve all prior work while adding your updates

❌ **Don't use when:**
- Not currently in a merge (no conflict to resolve)
- You intentionally restructured tasks (need manual review)
- Multiple agents worked on same task section (manual merge required)

## Manual Merge Alternative

If command detects unsafe auto-merge or you prefer manual control:

```bash
# 1. Open both versions side-by-side
code /tmp/main-tasks.md /tmp/branch-tasks.md

# 2. Manually edit the conflicted file
code openspec/changes/<id>/tasks.md

# 3. Keep main's structure, add your [x] markers
# 4. Verify all prior [x] markers preserved
# 5. Stage when satisfied
git add openspec/changes/<id>/tasks.md
```

## Example Output

```
🔍 Analyzing merge conflict for phase-3f-product-pricing-ux...

✅ Pre-merge checks passed:
   - Merge in progress (MERGE_HEAD found)
   - Change folder exists
   - No duplicate folders detected

📊 Comparing versions:
   Main (HEAD):     5 tasks, 2 completed sections
   Branch (MERGE):  5 tasks, 4 completed sections

🔎 Changes detected:
   ✅ Added [x] to Task 2 (6 bullets)
   ✅ Added [x] to Task 3 (7 bullets)
   ✅ Added completion note: "> Completed in 0f59d93"
   ⚠️  No structural changes detected

✅ Auto-merge SAFE - your branch preserves all main's work

Applying merge...
✅ Merge complete. Verify with: git diff HEAD openspec/changes/phase-3f-product-pricing-ux/tasks.md
```

## Red Flags (Command Will Abort)

🚨 **Removed completion markers:**
```diff
- [x] Task completed by previous agent
+ [ ] Task completed by previous agent
```

🚨 **Task section rewrites:**
```diff
- ## Zero-Price Support
- - [ ] Adjust validation logic
+ ## Zero-Price Support (1 hour)
+ - [ ] 2.1 Update validation logic in `class-product-pricing.php`
```

🚨 **Lost task sections:**
```diff
- ## Product Auto-Migration
- [x] All tasks completed
+ (section missing entirely)
```

## See Also

- `openspec/AGENTS.md` - Full merge protocol documentation
- `/openspec:apply` - Start implementing a change
- `/gc` - Commit changes with Flowji message format
