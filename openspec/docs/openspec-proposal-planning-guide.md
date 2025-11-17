# OpenSpec Proposal Planning Guide

**Version 1.0 | 2025-11-15**

Practical patterns for determining the right scope and structure for OpenSpec changes.

**Companion to:** `openspec/AGENTS.md` and `.claude/commands/openspec/proposal.md`

---

## The Core Principle

**OpenSpec changes should be atomic:** One change folder should contain one independently deployable and validatable feature that can be described in a single sentence to a stakeholder.

While OpenSpec documentation says "group all related changes for a feature in one folder," real-world implementations consistently show a different pattern: **small, focused changes that build toward larger goals through sequential deployment**.

---

## Task Hygiene = Ground Truth

OpenSpec change folders double as our task tracker. Treat every `tasks.md` file as a living kanban board:

- Check off (`- [x]`) items the moment the code + validation are complete. No waiting for a wrap-up phase.
- Add short inline notes when partially complete (“blocked on Stripe test”), so the next person knows what’s left.
- Never mark the implementation summary as “Complete,” request `/gc`, or close QA while the checklist still shows unchecked boxes for finished work.
- QA/test tasks in `USER-START-HERE.md` must also be reflected back into the relevant OpenSpec checklist—if you run a test for Phase 3f, mark the matching task there.
- When every bullet in a task section is done, add a trailing line noting the completing commit, e.g. `> Completed in 0f10784 (2025-11-15)`. This gives future readers an immediate jump point into git history.

If a box is unchecked, we assume the work has not shipped. Keeping the change folder honest prevents duplicated effort and makes audits painless.

---

## The Sweet Spot: Observable Patterns

Analysis of successful OpenSpec implementations reveals consistent size patterns:

### Task Count Patterns

| Tasks | Change Type | Characteristics |
|-------|-------------|-----------------|
| 8-15 | Simple | Single capability, straightforward implementation, 1-3 days |
| 20-30 | Medium | 1-2 related capabilities, some complexity, 1-2 weeks |
| 30-35 | Complex | Upper limit, single capability with high complexity, 2-3 weeks |
| 36+ | **Too Large** | Strong signal to split into multiple changes |

**Largest documented example:** 28 tasks (Japanese localization with i18n, browser detection, type safety)

### Spec Folder Count Patterns

| Spec Folders | Pattern | Notes |
|--------------|---------|-------|
| 1 | Most Common | Single capability affected |
| 2-3 | Reasonable | Related capabilities that must change together |
| 4-5 | Getting Complex | Review carefully, consider splitting |
| 6+ | **Too Large** | Strong signal to split into multiple changes |

**Key insight:** No documented OpenSpec implementations show 6+ spec folders in a single change.

---

## Decision Framework: When to Split

### Split Into Multiple Changes When:

✅ **Independent stakeholder value**
- Each part delivers value independently
- Stakeholder can describe each part in one sentence
- Example: "Add bulk product editing" and "Add product duplication" are separate features

✅ **Sequential deployment possible**
- Changes can deploy days/weeks apart
- Each deployment can be validated in production
- Later changes can be postponed without blocking earlier ones

✅ **Different implementation owners**
- Different developers could work on different parts
- Parallel development would save time
- Knowledge domains are distinct

✅ **Architectural independence**
- Changes affect different subsystems
- Failure of one wouldn't necessarily break the other
- Database migrations are independent

✅ **Size indicators triggered**
- Approaching 35+ tasks
- More than 5 spec folders affected
- Proposal.md taking 3+ pages to explain

### Keep as Single Change When:

❌ **Tightly coupled implementation**
- Changes must be implemented atomically in same PR
- Deploying partially would break user experience
- Database schema changes are interdependent

❌ **Single user story**
- Describes one coherent workflow from user perspective
- Splitting would create incomplete functionality
- Example: "Add two-factor authentication" (setup + verification flows together)

❌ **Reviewability**
- Splitting would make design decisions harder to understand
- Related technical context needs to be co-located
- Example: Auth changes + security audit logging together

---

## Practical Examples

### Example 1: Simple Change (Ideal Size)

**Change:** Add password reset via email

**Structure:**
```
changes/add-password-reset/
├── proposal.md
├── tasks.md              # 12 tasks
└── specs/
    └── auth/
        └── spec.md       # 1 capability
```

**Tasks breakdown:**
```markdown
## 1. Database Schema
- [ ] 1.1 Add password_reset_tokens table
- [ ] 1.2 Add indexes for token lookup
- [ ] 1.3 Run migration

## 2. Token Generation
- [ ] 2.1 Create token generation service
- [ ] 2.2 Add token expiration logic (24h)
- [ ] 2.3 Add unit tests

## 3. Email Integration
- [ ] 3.1 Create password reset email template
- [ ] 3.2 Add email sending service
- [ ] 3.3 Test email delivery

## 4. Reset Flow
- [ ] 4.1 Add reset password endpoint
- [ ] 4.2 Implement token validation
- [ ] 4.3 Add integration tests
```

**Why this is good:**
- 12 tasks total (within sweet spot)
- Single capability (auth)
- Can describe in one sentence: "Users can reset their password via email"
- 1 week implementation
- Can deploy and validate independently

---

### Example 2: Medium Change (Still Manageable)

**Change:** Add social login (Google + Facebook)

**Structure:**
```
changes/add-social-login/
├── proposal.md
├── tasks.md              # 24 tasks
└── specs/
    ├── auth/
    │   └── spec.md       # OAuth integration
    └── profile/
        └── spec.md       # Social profile data
```

**Tasks breakdown:**
```markdown
## 1. OAuth Infrastructure
- [ ] 1.1 Add OAuth2 client library
- [ ] 1.2 Add OAuth state management
- [ ] 1.3 Create OAuth callback endpoint
- [ ] 1.4 Add CSRF protection

## 2. Google Integration
- [ ] 2.1 Register Google OAuth app
- [ ] 2.2 Implement Google OAuth flow
- [ ] 2.3 Map Google profile data
- [ ] 2.4 Add Google login button
- [ ] 2.5 Test Google auth flow

## 3. Facebook Integration
- [ ] 3.1 Register Facebook OAuth app
- [ ] 3.2 Implement Facebook OAuth flow
- [ ] 3.3 Map Facebook profile data
- [ ] 3.4 Add Facebook login button
- [ ] 3.5 Test Facebook auth flow

## 4. Profile Handling
- [ ] 4.1 Link social accounts to existing users
- [ ] 4.2 Handle new user creation
- [ ] 4.3 Store social profile images
- [ ] 4.4 Update profile display logic

## 5. Testing & Security
- [ ] 5.1 Add OAuth flow tests
- [ ] 5.2 Security audit of token storage
- [ ] 5.3 Add rate limiting
- [ ] 5.4 Document provider setup
```

**Why this is manageable:**
- 24 tasks (within documented range)
- 2 related capabilities that must change together
- OAuth infrastructure is shared dependency
- Still describable in one sentence: "Users can log in with Google or Facebook"
- 2 week implementation
- Could theoretically split (Google-only first), but coupled OAuth infrastructure makes single change reasonable

---

### Example 3: Too Large - Should Split

**Change:** Add complete product pricing system

**❌ Single Change Structure (Too Large):**
```
changes/add-product-pricing-complete/
├── proposal.md           # 5+ pages
├── tasks.md              # 86 tasks (3x documented max)
└── specs/
    ├── product-auto-migration/
    ├── zero-price-support/
    ├── validation-preservation/
    ├── currency-lifecycle/
    ├── renewal-price-sync/
    ├── product-duplication/
    ├── bulk-edit/
    ├── gateway-mapping/
    ├── coupon-trial-integration/
    └── data-migration/   # 10 capabilities (unprecedented)
```

**Why this is too large:**
- 86 tasks (5-10x documented examples)
- 10 capabilities (no documented examples have this many)
- Takes multiple paragraphs to explain
- Can't be reviewed as coherent unit
- Implementation would take months
- Deployment all-or-nothing is risky

**✅ Better: Split Into 3 Related Changes:**

```
changes/add-product-pricing-ux/
├── proposal.md
├── tasks.md              # 28 tasks
└── specs/
    ├── product-auto-migration/
    ├── zero-price-support/
    ├── validation-preservation/
    ├── currency-lifecycle/
    └── renewal-price-sync/

changes/add-product-lifecycle-tools/
├── proposal.md
├── tasks.md              # 26 tasks
└── specs/
    ├── product-duplication/
    ├── bulk-edit/
    └── gateway-mapping/

changes/add-product-advanced-integration/
├── proposal.md
├── tasks.md              # 32 tasks
└── specs/
    ├── coupon-trial-integration/
    └── data-migration/
```

**Why this is better:**
- Each change 26-32 tasks (within sweet spot)
- Each has 2-5 capabilities (manageable)
- Each can be described in one sentence
- Can deploy and validate incrementally
- Can parallelize across team members
- Surgical rollback if one phase has issues
- Each change can be archived independently

---

## Structuring Related Changes

When you split a large feature into multiple changes, maintain clear relationships:

### Naming Convention

Use descriptive, verb-led names that show relationship:

```
changes/add-product-pricing-ux/          # Phase 1: Foundation
changes/add-product-lifecycle-tools/     # Phase 2: Builds on 1
changes/add-product-advanced-integration/ # Phase 3: Builds on 1+2
```

**For phase-based projects**, use phase prefixes:
```
changes/phase-3a-add-pricing-ux/
changes/phase-3b-add-lifecycle-tools/
changes/phase-3c-add-advanced-integration/
```

### Cross-Referencing in Proposals

**In first change (`add-product-pricing-ux/proposal.md`):**

```markdown
# Add Product Pricing UX Enhancements

## Why
Users need automatic product migration and zero-price support for flexible pricing models.

## What Changes
- Automatic product migration during currency changes
- Zero-price product support with validation
- Currency lifecycle management

## Related Changes
- **Depends on:** None (foundational)
- **Enables:** add-product-lifecycle-tools, add-product-advanced-integration
- **Part of initiative:** Multi-Currency Product Pricing System

## Implementation
See tasks.md for 28 implementation steps.
```

**In dependent change (`add-product-lifecycle-tools/proposal.md`):**

```markdown
# Add Product Lifecycle Management Tools

## Why
Administrators need tools to manage products at scale.

## What Changes
- Bulk product editing
- Product duplication with settings
- Gateway payment mapping

## Related Changes
- **Depends on:** add-product-pricing-ux (uses validation system)
- **Enables:** add-product-advanced-integration
- **Part of initiative:** Multi-Currency Product Pricing System

## Implementation
See tasks.md for 26 implementation steps.
```

---

## Red Flags: Your Change Is Too Large

Watch for these warning signs that indicate you should split:

🚩 **Takes 3+ pages to explain the "Why"**
- If proposal.md is getting long, scope is probably too broad
- Each change should have focused, clear motivation

🚩 **Tasks.md has 10+ major sections**
- Indicates too many distinct concerns
- Natural split points usually emerge from section boundaries

🚩 **Multiple developers would naturally own different parts**
- If you think "Bob should do X and Alice should do Y," split them
- Parallel work indicates separable scope

🚩 **Deployment timeline spans 2+ months**
- Long timelines mean many failure points
- Earlier validation opportunities are better

🚩 **You use "and" multiple times describing the feature**
- "Add product migration AND bulk editing AND coupon integration"
- Each "AND" is a potential split point

🚩 **Rollback complexity is high**
- If backing out partially is complicated, you've coupled too much
- Each change should be independently reversible

---

## Green Flags: Your Change Is Right-Sized

✅ **Fits in one sentence**
- "Add password reset via email"
- "Add social login with Google and Facebook"
- Clear, focused description

✅ **Tasks fit on one screen**
- You can review the entire task list without scrolling much
- Generally 8-35 tasks

✅ **Implementation timeline is 1-3 weeks**
- Long enough to be meaningful
- Short enough to maintain focus

✅ **Single developer could own it**
- One person could implement sequentially
- Knowledge domain is cohesive

✅ **Failure doesn't cascade**
- If this change fails, other work isn't blocked
- Can abandon or postpone without major impact

✅ **Design decisions are cohesive**
- All technical choices are related
- Don't need separate design.md files for different parts

---

## Common Sizing Mistakes

### Mistake 1: Grouping by Timeline Instead of Capability

❌ **Wrong thinking:**
"These all need to go out in Q1, so they're one change"

✅ **Right thinking:**
"These are separate capabilities that happen to deploy in same quarter. Each gets its own change."

### Mistake 2: Premature Consolidation

❌ **Wrong thinking:**
"These might be related eventually, so I'll plan them together now"

✅ **Right thinking:**
"I'll create the change I need now. If future work is related, I'll reference this one in its proposal."

### Mistake 3: Over-Splitting

❌ **Wrong thinking:**
"Every task should be its own change for maximum atomicity"

✅ **Right thinking:**
"Changes should deliver stakeholder value. Multiple tasks together often make one coherent feature."

### Mistake 4: Ignoring Natural Boundaries

❌ **Wrong thinking:**
"I have 50 tasks, but they're all 'product improvements' so one change"

✅ **Right thinking:**
"My 50 tasks have 3 natural groupings around user workflows. That's 3 changes."

---

## Practical Workflow for Agents

When asked to create a proposal:

### Step 1: Understand the Full Scope

- Ask clarifying questions about requirements
- Identify all capabilities that will change
- Estimate rough task count (don't need exact)

### Step 2: Apply Size Check

```
Task count estimate: ___
Capability count: ___
Can describe in one sentence: Yes / No
Natural deployment phases: ___
```

### Step 3: Make Split Decision

**If any of these are true, consider splitting:**
- More than 35 tasks estimated
- More than 5 capabilities affected
- Can't describe in one sentence
- Natural deployment phases exist

**If all of these are true, keep as one change:**
- Under 35 tasks
- 1-3 capabilities
- Single sentence description works
- Must deploy atomically

### Step 4: Structure the Change(s)

**Single change:** Create one change folder, proceed with proposal

**Multiple changes:** 
1. Identify logical groupings (by capability, by user workflow, by dependency)
2. Create change folder for first one
3. Reference other planned changes in proposal.md
4. Do NOT create folders for future changes yet (just-in-time principle)

---

## Examples of Good Split Points

### By User Workflow

One feature: "Complete checkout system"

Split into:
1. `add-cart-management` - Add to cart, update quantities
2. `add-checkout-flow` - Payment collection, order creation
3. `add-order-tracking` - Order status, shipping updates

### By Technical Capability

One feature: "Analytics system"

Split into:
1. `add-event-tracking` - Event collection and storage
2. `add-analytics-dashboard` - Visualization and reporting
3. `add-data-export` - CSV/PDF export functionality

### By Dependency Chain

One feature: "Multi-language support"

Split into:
1. `add-i18n-infrastructure` - Translation loading, language detection
2. `add-content-translation` - Translate UI strings
3. `add-dynamic-translation` - User-generated content translation

---

## When to Ask for Guidance

If you're unsure about sizing, ask the human:

**Good questions to ask:**

"I'm planning a change for [description]. My rough estimate is [X] tasks affecting [Y] capabilities. This could be structured as:

**Option A:** Single change (simpler, but [concern about size/timeline/scope])

**Option B:** Split into [N] changes: [list them briefly]

Which approach would you prefer?"

**What NOT to do:**

- Don't silently choose one approach without considering alternatives
- Don't create elaborate multi-phase structures without input
- Don't consolidate everything just because it's "related"

---

## Quick Reference Checklist

Before creating a proposal, verify:

- [ ] Can describe change in one sentence
- [ ] Task count under 35 (rough estimate okay)
- [ ] Affects 1-5 capabilities maximum
- [ ] Implementation timeline 1-3 weeks
- [ ] Can deploy and validate independently
- [ ] Single developer could own it
- [ ] Failure doesn't cascade to other work

**If 6+ checks pass:** Proceed with single change

**If 3- checks pass:** Strong signal to split into multiple changes

**If uncertain:** Ask the human for guidance

---

## Remember

**OpenSpec's strength is atomic changes.** When in doubt, err on the side of smaller, focused changes over large consolidated ones. You can always reference related changes in proposals - you don't need to group them in the filesystem to show they're related.

The goal is changes that are:
- **Reviewable** - Can be understood in 10-15 minutes
- **Implementable** - Can be completed in 1-3 weeks
- **Deployable** - Can go to production independently
- **Validatable** - Success/failure is clear
- **Reversible** - Can be rolled back surgically if needed

When your changes have these properties, you're using OpenSpec well.
