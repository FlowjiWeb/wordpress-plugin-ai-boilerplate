# Future Enhancement Ideas

*Brainstormed features for potential future development. Not prioritized or committed. These represent ideas captured during development sessions that could become formal OpenSpec proposals if prioritized.*

---

## High-Impact Ideas

### 1. Currency Performance Dashboard
**Value:** Business intelligence for pricing strategy decisions

**Features:**
- Revenue breakdown by currency (charts/graphs)
- Conversion rate tracking (which currencies sell best)
- Top products per currency
- Monthly/quarterly currency trends
- Export reports (CSV, PDF) for accounting

**Use case:** Identify which currencies drive most revenue, optimize pricing strategy

---

### 2. Bulk Product Pricing Tools
**Value:** Massive time-saver for catalog management

**Features:**
- Apply percentage markup across all products (e.g., +10% for EUR)
- Copy pricing from one product to multiple products
- Bulk update prices by currency (e.g., increase all USD prices by $10)
- Pricing templates (save common price sets, apply to new products)

**Use case:** Update 50 products' EUR prices in one operation instead of 50 manual edits

---

### 3. Price Rounding Strategies
**Value:** Professional pricing psychology + saves manual work

**Features:**
- Psychological pricing (end in .95, .99)
- Round to nearest 5/10/50/100
- Country-specific conventions (Japan: round to ¥100)
- Configurable rounding per currency
- Applied automatically with currency conversion suggestions (Phase 7)

**Use case:** AUD $545.67 → Auto-round to $545 or $549 based on strategy

---

## Customer Experience

### 4. Currency Memory & Preferences
**Value:** Better UX for returning customers

**Features:**
- Remember last selected currency per user account
- Store currency preference in user meta (not just cookies)
- Allow logged-in users to change default currency in account settings
- Currency preference inheritance for subscription renewals

**Use case:** US customer's subscription auto-renews in USD without re-selecting

---

### 5. Smart Currency Detection
**Value:** Fewer manual selections, better first impression

**Features:**
- Browser language detection (en-US → USD, en-GB → GBP)
- Combine geolocation + browser language for better accuracy
- Manual override always takes precedence
- "You're viewing prices in USD. Switch to AUD?" notice

**Use case:** UK visitor sees GBP prices automatically without query string

---

### 6. Currency Comparison Tool
**Value:** Transparency for international customers

**Features:**
- "View prices in all currencies" button on product pages
- Side-by-side comparison table
- Helps international customers choose best value
- Includes gateway fees/differences if applicable

**Use case:** Customer compares: USD $390 vs AUD $545 to see real value

---

## Advanced Admin Features

### 7. Advanced Transaction Ledger
**Value:** Complete financial tracking and reconciliation

**Features:**
- Refund tracking with currency-specific amounts
- Partial refunds and adjustments
- Transaction notes/annotations for accounting
- Custom metadata fields (invoice number, tax reference, etc.)
- Reconciliation tools (match Stripe payouts to transactions)

**Use case:** Track $100 USD partial refund on $390 original transaction

---

### 8. Audit Trail
**Value:** Compliance, troubleshooting, accountability

**Features:**
- Log all currency settings changes (who, when, what)
- Product price change history
- Gateway routing decision logs (for dispute resolution)
- Admin action tracking (who deleted/disabled currencies)

**Use case:** Debug why customer was charged wrong currency 3 months ago

---

### 9. Settings Import/Export
**Value:** Environment migration, disaster recovery

**Features:**
- Export all currency configs as JSON
- Import settings from backup/staging
- Validate before import (detect conflicts)
- Selective import (currencies only, or include product prices)

**Use case:** Clone production currency settings to staging environment

---

## Pricing Strategy

### 10. Dynamic Pricing Rules
**Value:** Sophisticated pricing strategies without manual updates

**Features:**
- Time-based pricing (different rates for early bird vs regular)
- Member-tier specific pricing (gold members get 10% off)
- Coupon codes with currency-specific discounts
- Minimum/maximum price enforcement per currency

**Use case:** USD products 20% off during Black Friday, EUR unchanged

---

### 11. Tax & VAT Integration
**Value:** Legal compliance for international sales

**Features:**
- Currency-specific tax rates
- EU VAT handling (MOSS compliance)
- Auto-calculate tax based on customer location + currency
- Tax-inclusive vs tax-exclusive pricing display

**Use case:** UK customer pays VAT on GBP price, US customer doesn't

---

### 12. Promotional Features
**Value:** Marketing flexibility

**Features:**
- Limited-time currency discounts ("20% off USD prices this week")
- Flash sales per currency
- Currency-specific landing pages
- A/B test pricing strategies

**Use case:** Run USD-only promotion without affecting other currencies

---

## Multi-Gateway & Payment

### 13. Payment Method Restrictions by Currency
**Value:** Regional payment method optimization

**Features:**
- Hide certain payment methods for specific currencies
- Example: Only allow credit cards for USD, bank transfer for EUR
- Gateway fee display (Stripe fees vary by region)

**Use case:** Disable PayPal for AUD due to high fees

---

### 14. Multiple Gateways per Currency
**Value:** Reliability and optimization

**Features:**
- Primary + backup gateway (failover)
- Load balancing across gateways
- A/B testing different gateway combinations
- Manual gateway selection for admin-created orders

**Use case:** USD gateway 1 down → Auto-route to USD gateway 2

---

### 15. Subscription Currency Lock
**Value:** Prevent currency arbitrage on subscriptions

**Features:**
- Lock subscription currency on first payment
- Prevent currency switching mid-subscription
- Handle subscription upgrades/downgrades in locked currency
- Renewal reminders show locked currency

**Use case:** Prevent switching from USD to cheaper EUR after subscribing

---

## Integrations

### 16. Accounting Software Sync
**Value:** Eliminate manual entry, reduce errors

**Features:**
- QuickBooks Online integration (multi-currency transactions)
- Xero integration
- FreshBooks integration
- Auto-create invoices in customer's currency

**Use case:** Every Stripe payment auto-creates Xero invoice in correct currency

---

### 17. Affiliate Network Enhancements
**Value:** Fair commission handling across currencies

**Features:**
- Currency-specific commission rates (20% USD, 25% AUD)
- Affiliate dashboard shows earnings in preferred currency
- Currency conversion for cross-border affiliate payouts
- Affiliate link tracking with currency parameter

**Use case:** Australian affiliate earns in AUD, paid in AUD, no conversion

---

### 18. REST API Endpoints
**Value:** External integrations and automation

**Features:**
- Public API for product prices by currency
- Transaction ledger queries
- Currency settings management
- Webhook support for external systems

**Use case:** Mobile app fetches product prices in user's preferred currency

---

## Technical & Developer

### 19. Multisite Support
**Value:** Large networks with different currency needs

**Features:**
- Separate currency configs per subsite
- Network-wide currency settings (optional)
- Consolidated reporting across subsites
- Shared gateway pool or per-site gateways

**Use case:** US subsite uses USD, AU subsite uses AUD, shared network admin

---

### 20. Testing & Debug Tools
**Value:** Faster troubleshooting, confident deployments

**Features:**
- Sandbox mode (test gateway routing without live payments)
- Currency simulation (test checkout flow as if in different country)
- Transaction log replay (debug failed transactions)
- Settings validation checker

**Use case:** Test EUR checkout flow without VPN or test credit card

---

## Compliance & Security

### 21. GDPR Compliance
**Value:** Legal requirement in EU

**Features:**
- Currency preference data retention policies
- Right to erasure (remove currency history)
- Data export (customer transaction history in their currency)
- Cookie consent integration for currency tracking

**Use case:** EU customer requests data deletion including currency preferences

---

### 22. Discontinued Currency Support
**Value:** Handle edge cases gracefully

**Features:**
- Handle products priced in disabled currencies
- Graceful degradation (show base price if currency removed)
- Migration tools (convert old currency to new)
- Historical data preservation

**Use case:** Disable EUR currency but preserve historical EUR transaction data

---

## Polish & UX

### 23. Currency Symbol Customization
**Value:** Regional preferences and clarity

**Features:**
- Override default symbols (use "AUD$" instead of "$")
- Prefix vs suffix positioning per currency
- Custom thousand/decimal separators by locale
- Number formatting per region (1,000.00 vs 1.000,00)

**Use case:** Display "A$545" for AUD to distinguish from "US$390"

---

### 24. Email & Notifications
**Value:** Clear customer communication

**Features:**
- Transaction emails show currency symbol + amount
- Subscription renewal reminders in subscription currency
- Admin notifications for currency mismatches/errors
- Low-balance alerts per Stripe gateway

**Use case:** Renewal reminder: "Your USD $390/year subscription renews in 7 days"

---

## Priority Guidance

**Highest immediate value (post-Phase 6):**
1. Currency Performance Dashboard - Business intelligence
2. Bulk Product Pricing Tools - Time-saver for catalog updates
3. Price Rounding Strategies - Professional pricing
4. Smart Currency Detection - Better UX than query strings
5. Advanced Transaction Ledger - Refund tracking essential

**Long-term value:**
- Tax/VAT Integration - Required for EU expansion
- Accounting Software Sync - Automation for scale
- Subscription Currency Lock - Prevent abuse
- Audit Trail - Compliance and troubleshooting

**Nice-to-have polish:**
- Currency Comparison Tool
- Currency Symbol Customization
- Promotional Features
- Testing/Debug Tools

---

*Last updated: 2025-11-10*
*To propose implementing any of these features, create a new OpenSpec change proposal in `openspec/changes/` following the standard workflow.*
