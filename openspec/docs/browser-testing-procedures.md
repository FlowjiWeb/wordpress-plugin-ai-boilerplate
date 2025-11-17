---
created: 2025-11-06
updated: 2025-11-12
plugin-version: 1.0.10
---

# Browser Testing Procedures

**Automation-First Approach:** Most UI/browser-based tests can be automated using the `browser-automation` agent with Chrome DevTools MCP. Only defer to manual testing when automation is blocked by technical limitations (Stripe live mode, external services, etc.) or when human judgment is required.

**Prerequisites for Automated Testing:**
- Docker running with WordPress + MemberPress + Plugin active
- Stripe **test mode** enabled in MemberPress gateway with test API keys
- Test product configured (http://localhost:8080/register/test-product-multi-currency-poc/)
- Browser automation agent has WordPress credentials (see `plugin/AGENTS.md`)
- Admin URLs (local dev):
  - Currency Settings: `http://localhost:8080/wp-admin/admin.php?page=memberpress-options#mepr-currencies`
  - Currency Transactions: `http://localhost:8080/wp-admin/admin.php?page=memberpress-currency-transactions`
  - Requires account with `manage_options` capability (full WordPress admin)

**Stripe Test Cards:**
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Requires auth: `4000 0025 0000 3155`

## Transaction Recording Test Procedures

### Automated Transaction Recording Test

**Automation Status:** ✅ **Can be automated** with browser-automation agent

**Test Flow:**
1. **Enable Debug Logging** (bash/SQL - manual or automated via bash tools)
   ```bash
   docker exec -it hive-happierbees-mysql mysql -uwordpress -pwordpress -e \
     "USE wordpress; UPDATE cgc_options SET option_value = '1' WHERE option_name = 'SCRIPT_DEBUG';"
   ```

2. **Create Test Transaction** (browser automation)
   - Navigate to test product page: `http://localhost:8080/register/test-product-multi-currency-poc/`
   - Fill checkout form with Stripe test card: `4242 4242 4242 4242`
   - Expiry: any future date (e.g., `12/25`), CVC: `123`
   - Fill billing information (test data)
   - Submit form
   - Monitor network requests for Stripe API calls
   - Verify success page/redirect via DOM inspection

3. **Verify Recording Occurred** (bash - manual or automated)
   ```bash
   # Check WordPress error log
   docker exec hive-happierbees-mysql tail -n 20 /var/www/html/wp-content/debug.log | grep "Currency Transaction"
   ```

4. **Verify Database Entry** (bash - manual or automated)
   ```bash
   docker exec -it hive-happierbees-mysql mysql -uwordpress -pwordpress -e \
     "USE wordpress; SELECT id, mepr_transaction_id, original_currency, original_amount, base_amount FROM {$wpdb->prefix}mp_currency_ledger ORDER BY created_at DESC LIMIT 5;"
   ```

5. **Verify Admin Display** (browser automation)
   - Log in to WordPress admin: `http://localhost:8080/wp-admin`
   - Navigate to MemberPress > Currency Transactions
   - Take screenshot to verify transaction appears
   - Click transaction to verify detail view
   - Capture console errors if any

### Automated Test Checklist

- [ ] Transaction recorded with correct MemberPress ID
- [ ] Currency correctly extracted from Stripe
- [ ] Original amount matches payment
- [ ] AUD amount calculated correctly
- [ ] Stripe Payment Intent ID captured
- [ ] Transaction appears in admin log
- [ ] Filters (currency, status) work correctly
- [ ] No errors in debug.log

---

## Multi-Currency Checkout Test Checklist

**Automation Status:** ✅ **Can be automated** with browser-automation agent

> Use the `?currency=` parameter in new tests (legacy links using `?cur=` continue to function and should be spot-checked periodically).

### Pre-Test Setup

- [ ] Multiple currencies configured in database
- [ ] Multiple Stripe accounts connected via MemberPress gateways (test mode)
- [ ] Test products with pricing in multiple currencies (Phase 3 feature)
- [ ] Error logs cleared

### Checkout Flow Tests (Browser Automation)

#### Single Currency Transaction
**Automated:** browser-automation agent navigates, fills forms, submits, monitors network requests

- [ ] Navigate to product page with `?cur=AUD` parameter
- [ ] Fill Stripe test card form (`4242 4242 4242 4242`)
- [ ] Submit checkout
- [ ] Verify network request to Stripe API (monitor via DevTools)
- [ ] Verify transaction recorded with AUD currency (check admin table)
- [ ] Verify amount matches expected purchase price

#### Multiple Currency Support (Phase 3+)
**Automated:** Same as single currency, test with different `?cur=` parameters

- [ ] Navigate with `?cur=USD`
- [ ] Verify currency selector shows USD selected (inspect DOM)
- [ ] Complete checkout with test card
- [ ] Verify Stripe uses USD account (check network request headers/body)
- [ ] Verify transaction recorded with USD (admin table check)
- [ ] Verify amount conversion if applicable

#### Error Scenarios
**Automation:** Use Stripe test cards for decline/error conditions

- [ ] Use decline card (`4000 0000 0000 0002`) → verify error message shown
- [ ] Test with invalid currency code `?cur=ZZZ` → verify fallback to AUD
- [ ] Monitor console for JavaScript errors during checkout
- [ ] Verify failed transactions not recorded in ledger (database check)

### Admin Functionality Tests (Browser Automation)

**Automated:** browser-automation agent navigates admin, interacts with UI, captures screenshots

- [ ] Navigate to MemberPress > Currency Transactions
- [ ] Test pagination (click next/prev, verify URL params, count displayed rows)
- [ ] Test currency filter dropdown (select USD, verify filtered results)
- [ ] Test status filter (select "complete", verify only complete transactions shown)
- [ ] Test sorting (click column headers, verify order changes in DOM)
- [ ] Click transaction row, verify detail view displays correctly
- [ ] Take screenshots of each state for documentation

---

## Phase 3d — Dynamic Price Display QA

**Automation Status:** ☑️ Partially automatable. DOM inspection + screenshots can be scripted; cookie/log validation still requires manual log review or bash helpers.

### Pre-Test Checklist

- [ ] Legacy Fluent Snippet #17 disabled (default) so plugin filters own the display
- [ ] Product 2304 “Test Product – Multi-Currency POC” seeded with USD/EUR/AUD prices
- [ ] WordPress debug logging enabled (`WP_DEBUG_LOG` true)
- [ ] Docker containers running (`hive-happierbees-wordpress` + db)

### Test Matrix

1. **USD override**
   - Visit `http://localhost:8080/register/test-product-multi-currency-poc/?currency=USD`
   - Inspect `.mepr_price_cell` and registration invoice rows – expect `$1.00`
   - Capture screenshot → `docs/screenshots/phase-3d-price-display-usd.png`
   - Check `debug.log` for `[MPMC] Price display: Detected currency USD... RETURNING: $1.00`
   - `curl -I ...?currency=USD` → confirm `Set-Cookie: mpmc_currency=USD; domain=.happierbees.com`

2. **EUR override**
   - Hit same URL with `?currency=EUR`
   - Expect `€2.00` in both product + invoice tables; capture screenshot `...-eur.png`
   - Verify log lines with EUR detection + override

3. **AUD/base fallback**
   - Remove query string (`?currency=AUD` or no param)
   - Expect `$1.50` (AUD fallback) and `[MPMC] Currency AUD ... fallback to base price` log entries
   - Screenshot saved to `...-aud.png`

4. **`?cur=` alias compatibility**
   - Repeat USD/EUR scenarios using `?cur=` to confirm legacy links still work
   - Ensure log lines show “from query string: cur”

5. **No multi-currency price**
   - Temporarily remove a currency price (or use fresh product) and refresh page without query string
   - Expect MemberPress base price + log entry `fallback to base price`

6. **Free/zero products (optional)**
   - Set product price to `Free` or `0.00` and confirm plugin logs “Free/empty price passthrough”

### Troubleshooting Tips

- Missing overrides usually means the detector never saw the query parameter — verify cookie + session via `document.cookie` and `tail -f debug.log | grep MPMC`
- If snippets override values, confirm `mpmc_enable_legacy_poc_snippet` filter remains `false`
- For ReadyLaunch templates that bypass `mepr_price_display`, the `mepr_price_string` hook still fires; inspect log lines to confirm
- Keep the screenshots folder updated; they are gitignored but referenced from OpenSpec docs/tasks

---

## Expected Error Log Messages

### Success Messages

```
Currency Transaction Recorder: Successfully recorded transaction 12345
```
**When:** Transaction recorded successfully to database
**Action:** None required

---

### Warning Messages

```
Currency Transaction Recorder: Failed to extract Stripe data for transaction 12345
```
**When:** Stripe API call failed or returned invalid data
**Action:** Check Stripe API connectivity, review MemberPress gateway configuration

**Possible causes:**
- Stripe API unreachable
- MemberPress Stripe connection not configured
- Payment intent not found in Stripe
- Invalid Stripe API response

---

### Info Messages

```
Currency Transaction Sync: Starting sync process
Currency Transaction Sync: Found 5 missing transactions
Currency Transaction Sync: Synced 5 transactions successfully
```
**When:** Auto-sync runs on admin page load
**Action:** Normal operation, no action required

---

### Error Messages

```
Currency Transaction Recorder: Exception for transaction 12345 - [Exception message]
```
**When:** Unexpected exception during recording
**Possible causes:**
- Database connectivity issue
- Invalid transaction data
- PHP error in plugin code

---

## Phase 3b · Product Pricing QA Checklist

**Automation Status:** ✅ **Can be automated** with browser-automation agent

> Run these steps on the local MemberPress dev stack (`http://localhost:8080`) after enabling Phase 3b code. Use the `ai-agent-dev` credentials from `plugin/AGENTS.md`.

### Meta Box Rendering (Task 9.1)
**Automated:** browser-automation agent navigates, takes screenshots, inspects DOM

1. Navigate to **MemberPress → Products → Edit** for any product
2. Take screenshot of page
3. Use DOM inspection to verify **Multi-Currency Prices** meta box exists
4. Count table rows and verify match with enabled currencies
5. Verify each row contains: currency code, symbol, gateway label, price input

**Expected:** Table renders one row per enabled currency with formatted symbols and gateway IDs. Agent reports missing meta box if not found.

### Saving Prices (Task 9.2)
**Automated:** browser-automation agent fills forms, submits, reloads, verifies persistence

1. Fill price inputs with test values (e.g., `390.00`, `350.00`, `310.00`)
2. Click **Update** button
3. Wait for save completion (monitor network request)
4. Reload page (force refresh)
5. Verify input values match saved data

**Expected:** Agent reports success/failure of persistence. Check browser console logs for `[MPMC]` messages.

### Validation Errors (Task 9.3)
**Automated:** browser-automation agent tests error conditions

1. Clear one currency input field and submit
2. Verify admin notice appears with error message
3. Take screenshot of error state
4. Enter invalid decimal (e.g., `12.345`) and submit
5. Verify validation error displayed

**Expected:** Agent captures screenshots of error notices and reports validation behavior.

### Currency Delete Protection (Task 9.4)
**Automated:** browser-automation agent tests delete workflow

1. Navigate to **MemberPress → Settings → Currencies**
2. Attempt to delete a currency used in product prices
3. Verify blocking notice appears
4. Take screenshot showing affected products list
5. Verify product links are present and clickable

**Expected:** Agent reports deletion blocked with product references.

### Base Price Fallback (Task 9.5)
**Semi-Automated:** Requires checkout flow + log inspection

1. **Setup (manual/bash):** Create product without multi-currency prices
2. **Browser automation:** Navigate to product, attempt checkout
3. **Verification (bash):** Check PHP error log for `[MPMC] Base price fallback` message

**Expected:** Agent can complete checkout flow; fallback verification requires log analysis.

### Meta Box With No Enabled Currencies (Task 9.6)
**Automated:** browser-automation agent verifies warning state

1. Navigate to **MemberPress → Settings → Currencies** and disable all
2. Navigate to product edit screen
3. Verify meta box shows yellow warning notice
4. Verify no price inputs are rendered
5. Take screenshot of warning state

**Expected:** Agent captures warning message and empty meta box state.

> **Heads-up:** Legacy Fluent Snippet #17 now returns early unless the `mpmc_enable_legacy_poc_snippet` filter is forced to `true`. Leave it disabled for routine QA so the plugin’s price display logic is authoritative; only re-enable when you explicitly need to regression-test the old POC behavior.

**Action:** Check PHP error logs, verify database connectivity

---

## Debugging Guide

### Check Transaction Recording Status

```bash
# Recent successful recordings
docker exec -it hive-happierbees-mysql mysql -uwordpress -pwordpress -e \
  "USE wordpress; SELECT id, mepr_transaction_id, original_currency, created_at FROM cgc_mp_currency_ledger ORDER BY created_at DESC LIMIT 10;"
```

### Check Error Logs

```bash
# View WordPress debug log
docker exec hive-happierbees-mysql tail -f /var/www/html/wp-content/debug.log | grep "Currency Transaction"

# Search for specific transaction
docker exec hive-happierbees-mysql grep "transaction 12345" /var/www/html/wp-content/debug.log
```

### Verify Stripe Connection

```php
// In WordPress admin (or via WP CLI):
// Check if MemberPress Stripe gateway is configured
$gateways = MeprGateway::all();
foreach ($gateways as $gateway) {
    if (get_class($gateway) === 'MeprStripeGateway') {
        echo "Stripe Gateway: " . $gateway->name . " (ID: " . $gateway->id . ")\n";
        echo "Connected: " . ($gateway->test_mode ? "Test Mode" : "Live Mode") . "\n";
    }
}
```

### Test Stripe API Directly

```php
// From plugin code or WP admin:
$gateway = MeprStripeGateway::get_instance('your-gateway-id');
$charge = $gateway->send_stripe_request(
    'charges/ch_test12345',
    ['expand' => ['balance_transaction']],
    'get'
);
if (is_wp_error($charge)) {
    echo "Error: " . $charge->get_error_message();
} else {
    echo "Charge found: " . $charge->amount . " " . $charge->currency;
}
```

---

## Database Verification Queries

### Check Table Structure

```sql
-- Verify cgc_mp_currency_ledger table exists
DESCRIBE cgc_mp_currency_ledger;

-- Expected columns:
-- id, mepr_transaction_id, mepr_user_id, user_email, mepr_product_id,
-- original_currency, original_amount, stripe_account_used, base_amount,
-- stripe_payment_intent_id, transaction_status, created_at
```

### Check Data Integrity

```sql
-- Verify UNIQUE constraint on mepr_transaction_id (no duplicates)
SELECT mepr_transaction_id, COUNT(*) as count
FROM cgc_mp_currency_ledger
GROUP BY mepr_transaction_id
HAVING count > 1;

-- Should return empty result
```

### Data Summary

```sql
-- Summary by currency
SELECT original_currency, COUNT(*) as count, SUM(original_amount) as total
FROM cgc_mp_currency_ledger
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY original_currency;

-- Summary by status
SELECT transaction_status, COUNT(*) as count
FROM cgc_mp_currency_ledger
GROUP BY transaction_status;

-- 7-day transaction count
SELECT DATE(created_at) as date, COUNT(*) as count
FROM cgc_mp_currency_ledger
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at);
```

---

## Performance Testing

### Transaction Recording Speed

**Expected Performance:**
- Stripe API call: 200-500ms
- Database insert: 10-50ms
- Total overhead per transaction: 200-550ms

**Measurement Method:**
```php
// In transaction bridge, wrap operations
$start = microtime(true);
// ... transaction recording code ...
$duration = (microtime(true) - $start) * 1000; // Convert to ms
error_log("Currency Transaction Recorder: Recorded in {$duration}ms");
```

### Database Performance

**Transaction Ledger Query Performance:**
```sql
-- Test index effectiveness
EXPLAIN SELECT * FROM cgc_mp_currency_ledger
WHERE original_currency = 'USD'
AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY created_at DESC;

-- Should use indexes: currency_idx, date_idx
```

---

## Load Testing Considerations

**Not yet implemented** - Manual testing only at this phase.

For Phase 3+ when admin interface is complete:
- Test with 1000+ transactions
- Verify pagination performance
- Check filter query optimization
- Monitor admin page load times

---

## Common Issues & Solutions

### Issue: Transaction Not Recorded
**Symptoms:** Transaction completes but doesn't appear in admin log

**Diagnostic Steps:**
1. Check error log for `Currency Transaction Recorder` messages
2. Verify MemberPress transaction created successfully
3. Verify Stripe account configuration
4. Check if manual payment gateway used (Stripe data won't be available)

**Solution:**
- Enable debug logging
- Check Stripe API connectivity
- Verify MemberPress gateway is Stripe (not manual)

### Issue: Duplicate Transaction Errors
**Symptoms:** Error log shows duplicate transaction warnings

**Diagnostic Steps:**
1. Check database for duplicate mepr_transaction_id entries
2. Review transaction sync logs
3. Verify UNIQUE constraint is active

**Solution:**
- Run deduplication query:
  ```sql
  -- Manual cleanup (if duplicates exist)
  DELETE FROM cgc_mp_currency_ledger
  WHERE id NOT IN (
      SELECT MIN(id) FROM cgc_mp_currency_ledger
      GROUP BY mepr_transaction_id
  );
  ```

### Issue: Currency Shows as AUD But Should Be Different
**Symptoms:** All transactions show 'AUD' currency

**Diagnostic Steps:**
1. Check Stripe API response in logs
2. Verify MemberPress Stripe gateway configuration
3. Test Stripe connection directly

**Solution:**
- Verify Stripe account is properly connected
- Check payment was actually processed on Stripe
- Review transaction bridge extraction logic

---

## Cross-Domain Currency Detection & Cookie Tests

**Automation Status:** ✅ **Can be automated** with browser-automation agent

### Pre-Test Checklist

- Enable at least two currencies (AUD + USD recommended) in the Phase 3a admin UI with gateway IDs assigned
- Disable Fluent Snippets #16/#17 in the target environment so the plugin owns session + cookie state
- Clear the `mpmc_currency` cookie before each scenario (via DevTools or automated)
- Browser automation can inspect cookies directly via Chrome DevTools Protocol

### Test Cases (Browser Automation)

**1. URL Detection / Cookie Write**
**Automated:** Navigate with parameter, inspect cookies via DevTools API

- Navigate to `http://localhost:8080/.../?cur=USD`
- Monitor console for `[MPMC]` messages: `Currency detected: USD (from query string)`
- Use DevTools cookie inspection to verify:
  - Cookie name: `mpmc_currency`
  - Value: `USD`
  - Domain: `.happierbees.com` (or localhost for local testing)
  - Secure flag: enabled (HTTPS only)
  - HttpOnly flag: enabled
  - SameSite: `Lax`
  - Expires: ~90 days from now
- Take screenshot of DevTools Application → Cookies panel

**2. Cookie Persistence**
**Automated:** Navigate without param, verify cookie is read

- Navigate to `http://localhost:8080/...` (no `?cur=` param)
- Monitor console for: `Currency detected: USD (from cookie)`
- Verify session storage via script evaluation (if accessible)

**3. URL Override**
**Automated:** Change currency via URL, verify cookie updates

- Navigate with `?cur=EUR`
- Verify console shows query detection + cookie write
- Refresh page without params
- Verify EUR persists in cookie

**4. Invalid Currency**
**Automated:** Test error handling

- Navigate with `?cur=ZZZ`
- Verify console shows: `Invalid currency format: ZZZ, using base currency`
- Verify console shows: `Currency fallback: AUD (base currency)`
- Verify cookie remains unchanged (read existing cookie value before/after)

**5. Disabled Currency**
**Automated:** Test disabled currency rejection

- Disable USD in admin UI (via browser automation in separate flow)
- Navigate with `?cur=USD`
- Verify console shows: `Currency USD is not enabled, using base currency`
- Verify cookie not updated

**6. Session Storage**
**Semi-Automated:** Session inspection requires script evaluation or PHP verification

- After valid detection, use `evaluate_script` to check `$_SESSION` if exposed to JavaScript
- OR verify via bash: `docker exec` into container and inspect session files
- Close browser tab and reopen to test cookie rehydration

### Troubleshooting (Automated Detection)

**Agent can detect:**
- Console errors about "headers already sent" → report with screenshot
- Missing cookies → verify via DevTools inspection, report failure
- JavaScript errors → capture from console logs

**Manual verification still needed:**
- PHP session configuration (`session.save_path` permissions)
- Server-side session state inspection

Document actual results (pass/fail + screenshots/console logs) in test reports. Browser automation agent captures evidence automatically.

---

## Phase 3 Testing Additions

When Phase 3 Admin Interface is implemented, add tests for:
- [ ] Currency configuration management
- [ ] Per-product pricing in multiple currencies
- [ ] Geolocation-based currency detection
- [ ] Currency preference persistence (cookies/sessions)
- [ ] Currency override UI
- [ ] Checkout form multi-currency display
- [ ] Payment routing to correct Stripe account

---

## References

- **Error Messages Source:** `plugin/includes/class-transaction-bridge.php` (lines 40, 64, 67, 69, 74)
- **Transaction Sync Source:** `plugin/includes/class-transaction-sync.php`
- **Database Schema:** `plugin/includes/class-database.php`
- **Audit Report:** `FLUENT-SNIPPET-AUDIT-2025-11-06.md`

---

**Last Updated:** 2025-11-06
**Plugin Version:** 1.0.10
**Status:** Phase 2 Complete, Phase 3 Pending
