# Product Roadmap

## Future Phases

### Phase 3e: Settlement Currency Validation 📋 Proposed

Extract and validate Stripe settlement currency matches configured base currency to prevent mixed-currency data corruption.

**Scope:**
- Extract `balance_transaction['currency']` from Stripe API responses
- Validate against configured base currency setting
- Block transaction recording on mismatch with admin notice
- Settings page validation for gateway settlement currencies

**See:** [openspec/changes/phase-3e-settlement-currency-validation/](changes/phase-3e-settlement-currency-validation/)

### Phase 6: Geolocation 📋 Future

IP-based currency detection with cookie caching and fallback to configured base currency.

**Note:** Not critical for hive.happierbees.com initial rollout (Bricks theme handles detection via query strings).

### Phase 7: Polish & Admin Quality of Life 💡 Polish Features

**Cosmetic issues backlog:** See [docs/issues/issues-summaries/cosmetic-polish.md](../docs/issues/issues-summaries/cosmetic-polish.md) for UX refinements deferred to public release.

**Phase 6 Deferred Items:**
- **API Resilience:** Automatic fallback chain (ip-api.com → ipstack.com → MaxMind) + health monitoring dashboard
- **Advanced Testing:** BrowserStack integration for automated multi-geo testing, Docker VPN containers for CI
- **Per-Product Controls:** Optional "Disable geolocation" checkbox for products (only if users request)
- **API Contract Testing:** Record/replay real geolocation API responses for regression testing

#### 7a: Data Cleanup Control

**Scope:** Give admins safe control over plugin data removal.

**Current behavior:**
- Deactivation: Stops functionality, keeps all data (ledger, settings, product prices)
- Uninstall: Same as deactivation - **no data deletion**
- Re-activation: Resumes immediately with all data intact

**Problem:** No way to completely remove plugin data if needed.

**Solution:** Optional cleanup via admin settings:
```
Settings > Multi-Currency > Advanced
☐ Remove all plugin data on uninstall (tables, settings, product prices)
   Warning: This will permanently delete X transactions, Y product prices, and all settings.
```

**Behavior:**
- Default: OFF (data persists - **safe for financial records**)
- When enabled + plugin uninstalled:
  - Drops `mpmc_currency_ledger` table
  - Deletes all `_mpmc_prices` product meta
  - Deletes all plugin options
  - Logs deletion action for audit trail
- Shows confirmation before uninstall: "You are about to permanently delete [X] transactions. This cannot be undone."

**Alternative approach:** "Danger Zone" cleanup tool in admin (manual deletion separate from uninstall)

**Priority:** Low - Current behavior (data persistence) follows WordPress best practices for financial plugins. Optional cleanup is quality-of-life for testing/migration scenarios.

#### 7b: Currency Conversion Suggestions

**Concept:** Suggest equivalent prices when admin enters product pricing in multiple currencies.

**How it works:**
- Admin configures base currency (e.g., AUD for happierbees.com)
- Admin enters base price: $545.00 AUD
- When adding USD/EUR/GBP/CAD prices, system suggests converted amounts
- Example: AUD $545 → Suggests USD $390 (based on live exchange rate)
- Admin can accept suggestion, round up/down, or enter custom price

**Important notes:**
- **Suggestion only** - Not automatic conversion at checkout
- **Still fixed pricing model** - Saved prices don't update with exchange rates
- **Time-saver** - Reduces manual calculator usage during product setup

**Technical requirements:**
- Exchange rate API integration (exchangerate-api.io, fixer.io, or similar)
- Base currency selection in Currency Settings
- Rate caching (24-hour refresh, avoid API limits)
- Rounding options (nearest $1, $5, $10, or custom)
- Visual design: "Suggested: $390 USD (based on current rate)" with accept/edit UX

**Priority:** Low - Quality-of-life enhancement after core multi-currency functionality complete. Not blocking Phase 3-6 features.

### Phase 8: Cryptocurrency Support 💡 Future Consideration

**Concept:** Expand payment options beyond fiat currencies to support cryptocurrency payments.

**Potential cryptocurrencies:**
- Bitcoin (BTC)
- Ethereum (ETH)
- Stablecoins (USDC, USDT, DAI)
- Other major cryptocurrencies

**Technical considerations:**
- Cryptocurrency payment gateway integration (Stripe supports crypto, or dedicated crypto processors like Coinbase Commerce, BTCPay Server)
- Real-time exchange rate handling (crypto volatility vs fixed fiat pricing)
- Transaction confirmation times (blockchain settlement delays)
- Tax/accounting implications (crypto as property vs currency)
- Regulatory compliance per jurisdiction
- Refund handling (exchange rate at refund time vs purchase time)

**Ledger requirements:**
- Record crypto amount + fiat equivalent at time of purchase
- Track exchange rate at transaction time
- Store blockchain transaction ID/hash
- Handle settlement confirmations

**User experience:**
- Crypto price display (live conversion or fixed crypto price?)
- Payment flow (wallet connection, transaction confirmation UX)
- Educational content for crypto-unfamiliar users

**Priority:** Low - capture idea for future exploration. Requires market validation, user demand analysis, and regulatory review before implementation.

### Phase 9: MemberPress Base Currency Sync 💡 Future Enhancement

**Deferred from Phase 2** - See architecture decision in [add-base-currency-configuration proposal](changes/add-base-currency-configuration/proposal.md#architecture-decision-2025-11-12)

**Scope:**
- Detect MemberPress base currency on plugin activation
- Seed plugin base_currency to match MemberPress on fresh installs
- Admin notice when MemberPress base ≠ plugin base
- Optional: Migration tool to convert historical transactions (requires exchange rate API)

**Status:** Not prioritized - Independent base currency prevents data corruption. MemberPress sync adds complexity without clear benefit for current use case.

---

## Completed Phases

- ✅ **Phase 2:** Base Currency Configuration (v1.2.0) - Configurable base currency, database migration, per-transaction audit trail
- ✅ **Phase 2.5:** Unit Testing Setup (v1.2.x) - PHPUnit + WP_Mock, critical path test coverage
- ✅ **Phase 3a:** Currency Settings (v1.3.0) - Currency CRUD, gateway mappings, country detection
- ✅ **Phase 3c:** Currency Detection (v1.4.0) - Query string + cookie persistence, session storage
- ✅ **Phase 3b:** Product Pricing (v1.5.0) - Per-currency pricing meta box, validation, gateway routing
- ✅ **Phase 3d:** Price Display (v1.6.0) - Dynamic price rendering across product tables and registration forms
- ✅ **Phase 3e:** Settlement Currency Validation (v1.1.8) - Transaction-time settlement validation, read-only UI, unit tests
- ✅ **Phase 4:** Easy Affiliates Integration (v1.1.11) - Commission calculations using settlement amounts instead of payment amounts, optional feature toggle, auto-disable on EA plugin deactivation

**See archived OpenSpec changes for implementation details:** `openspec/changes/archive/`

**Active OpenSpec changes:** `openspec/changes/phase-4-easy-affiliates-integration/`
