# Phase 3f–3h Overview (2025-11-14)

## Purpose
Capture the shared understanding from the latest workflow analysis so upcoming OpenSpec changes can be authored with clear scope boundaries. This “mini overview” preserves decisions agreed between Codex and Claude before the next agent formally drafts the specs.

## Current Status
- **Phase 3e (Settlement Currency Validation):** Code landed (auto-detect display, admin notice). Tasks still outstanding before we declare completion:
  1. Unit tests for settlement-currency extractor/validator (Task 6)
  2. Implementation summary update + terminology clarification (Task 8)
  3. Roadmap entry marking Phase 3e complete (Task 9)
- Once those three tasks are done, Phase 3e should be marked complete and future work tracked as new phases.

## Proposed Phasing Strategy
Source backlog: `docs/agent-feedback/product-pricing-ux-enhancement-workflows-consolidated-2025-11-14.md`

### Phase 3f — Data Integrity & Validation (Must-Haves)
**Goal:** Eliminate workflows that corrupt data or block day-to-day operations.

| Workflow | Summary | Notes |
| --- | --- | --- |
| Auto-migrate existing products on activation | Populate base currency rows from MemberPress price for every existing product | Prevents blank checkout prices for established sites |
| New product defaults & zero-price handling | Auto-fill base currency, support intentional `0.00` pricing | Clarify how empty/zero inputs behave |
| Validation preservation for partial entries | Preserve entered values when validation fails | Improves UX without weakening validation |
| Subscription renewal price sync | Ensure renewals respect per-currency tables or locked original price | Keep ledger accurate after price updates |
| Currency enable/disable lifecycle | Soft-delete non-base currencies and restore prior values when re-enabled | Avoids data loss when toggling currencies |

**Implementation focus:** `class-product-pricing.php`, `class-product-pricing-meta-box.php`, and related validation routines.

### Phase 3g — Product Lifecycle Integration (Should-Haves → High Priority)
**Goal:** Ensure multi-currency pricing survives common MemberPress/WordPress product workflows.

| Workflow | Summary | Notes |
| --- | --- | --- |
| Product duplication & template creation | Copy currency rows + gateway IDs verbatim during clone | Hook into duplication logic |
| Bulk edit / Quick Edit compatibility | Detect `_mepr_product_price` edits and resync currency rows | Avoid silent data drift |
| Gateway mapping changes & re-authorization | Provide remediation when Stripe gateway IDs change | Could be admin notice + batch updater |

**Implementation focus:** Hooks around post duplication, Quick Edit/Bulk Edit saves, and gateway map helpers.

### Phase 3h — Advanced Integration & Recovery
**Goal:** Address deeper MemberPress integrations and deployment resilience.

| Workflow | Summary | Notes |
| --- | --- | --- |
| Discounted / time-based pricing (coupons, trials, payment plans) | Define how currency-specific prices interact with MemberPress discounts/trials | Requires investigating MemberPress coupon/trial internals |
| Data migration & environment sync | Ensure gateway IDs + settlement metadata survive imports/exports and stage→prod moves | Document re-detection steps per environment |
| (Deferred) WP-CLI/REST automation support | Provide API contract or CLI command for programmatic product creation | Consider after 3h core work |
| (Deferred) Error recovery & logging guidance | Document retry/resume paths for partial migrations | Pair with automation tooling once defined |

**Implementation focus:** MemberPress coupon/trial pipelines, import/export hooks, and optional CLI interfaces.

## Next Actions
1. Finish remaining Phase 3e tasks (tests, docs, roadmap).
2. Draft **OpenSpec change for Phase 3f** using this document + consolidated backlog as inputs.
3. After 3f spec is approved/implemented, repeat for 3g and 3h, ensuring each phase completes (spec → implementation → testing → documentation) before moving on.

This document should be referenced by any agent writing the Phase 3f spec so the rationale and workflow priorities remain intact even if session context resets.
