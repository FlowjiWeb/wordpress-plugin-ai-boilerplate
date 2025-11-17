# {{PLUGIN_NAME}} - Technical Documentation

This document contains technical implementation details, class documentation, database schema, and security practices.

## Architecture Overview

{{ARCHITECTURE_DESCRIPTION}}

## Class Documentation

### Core Classes

#### Plugin
**File:** `includes/class-{{PLUGIN_SLUG}}.php`
**Namespace:** `{{NAMESPACE}}`

Main plugin class that orchestrates hooks and dependencies.

**Methods:**
- `__construct()` - Initialize plugin
- `run()` - Execute all hooks via loader

#### Loader
**File:** `includes/class-{{PLUGIN_SLUG}}-loader.php`
**Namespace:** `{{NAMESPACE}}`

Manages registration of all WordPress hooks (actions and filters).

**Methods:**
- `add_action()` - Register action hook
- `add_filter()` - Register filter hook
- `run()` - Register all hooks with WordPress

### Admin Classes

{{ADD_ADMIN_CLASS_DOCUMENTATION}}

### Public Classes

{{ADD_PUBLIC_CLASS_DOCUMENTATION}}

## Database Schema

{{ADD_DATABASE_SCHEMA_DOCUMENTATION}}

## Security Practices

### Input Validation
- All user input sanitized using WordPress sanitization functions
- Data validated before processing

### Output Escaping
- All output escaped using appropriate WordPress functions
- `esc_html()`, `esc_attr()`, `esc_url()` used consistently

### Nonce Verification
- All form submissions protected with WordPress nonces
- AJAX requests verified with nonce checks

### Capability Checks
- Admin functions protected with capability checks
- Minimum required: `manage_options`

## WordPress Hooks

### Actions

{{ADD_ACTION_DOCUMENTATION}}

### Filters

{{ADD_FILTER_DOCUMENTATION}}

## Testing

See root `AGENTS.md` for test running instructions.

### Test Coverage

- Unit tests using PHPUnit and WP_Mock
- Code coverage target: 80%+

## Coding Standards

- **Style:** WordPress Coding Standards
- **PHP Version:** 7.4+
- **WordPress Version:** 5.0+
