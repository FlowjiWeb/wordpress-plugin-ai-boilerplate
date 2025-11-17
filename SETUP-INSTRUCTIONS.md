# WordPress Plugin AI Boilerplate - Setup Instructions

These instructions are for AI agents setting up a new WordPress plugin from this boilerplate.

## Boilerplate Location

The complete boilerplate is located at:
```
/tmp/wordpress-plugin-ai-boilerplate/
```

## Setup Steps for New Plugin

### 1. Create New Plugin Directory

```bash
# Example for Query Keeper plugin
mkdir -p ~/04-REPOSITORIES/04-REPOSITORIES-flowji/wordpress-plugins/query-keeper
cd ~/04-REPOSITORIES/04-REPOSITORIES-flowji/wordpress-plugins/query-keeper
```

### 2. Copy Boilerplate Files

```bash
# Copy all files from boilerplate
cp -r /tmp/wordpress-plugin-ai-boilerplate/* .
cp -r /tmp/wordpress-plugin-ai-boilerplate/.* . 2>/dev/null || true
```

### 3. Remove This Instruction File

```bash
rm SETUP-INSTRUCTIONS.md
```

### 4. Replace All Placeholders

The boilerplate uses `{{PLACEHOLDER}}` syntax throughout. Replace these with actual values:

#### Required Replacements

| Placeholder | Example Value | Description |
|------------|---------------|-------------|
| `{{PLUGIN_NAME}}` | `Query Keeper` | Human-readable plugin name |
| `{{PLUGIN_SLUG}}` | `query-keeper` | URL-safe slug (lowercase, hyphens) |
| `{{PLUGIN_DESCRIPTION}}` | `Makes UTM and affiliate link data persist between domains` | Brief description |
| `{{PLUGIN_DESCRIPTION_DETAILED}}` | Full paragraph about what the plugin does | Detailed description |
| `{{PLUGIN_URI}}` | `https://github.com/FlowjiWeb/query-keeper` | Plugin homepage URL |
| `{{AUTHOR_NAME}}` | `Flowji` | Author name |
| `{{AUTHOR_URI}}` | `https://flowji.com` | Author website |
| `{{TEXT_DOMAIN}}` | `query-keeper` | Translation domain (same as slug) |
| `{{PACKAGE_NAME}}` | `QueryKeeper` | PHP package name (PascalCase) |
| `{{NAMESPACE}}` | `QueryKeeper` | PHP namespace (PascalCase) |
| `{{CONSTANT_PREFIX}}` | `QK` | Constant prefix (uppercase) |
| `{{FUNCTION_PREFIX}}` | `query_keeper` | Function prefix (snake_case) |

#### SSH/Deployment Placeholders

| Placeholder | Example Value | Description |
|------------|---------------|-------------|
| `{{SSH_KEY_PATH}}` | `$HOME/.ssh/hive_happierbees_ssh_key` | Path to SSH key |
| `{{SSH_PORT}}` | `18765` | SSH port |
| `{{SSH_USER}}` | `u144-gqesyzeld1lk` | SSH username |
| `{{SSH_HOST}}` | `ssh.hive.happierbees.com` | SSH hostname |
| `{{REMOTE_PLUGIN_PATH}}` | `~/www/hive.happierbees.com/public_html/wp-content/plugins/query-keeper` | Remote plugin path |
| `{{WORDPRESS_ADMIN_URL}}` | `https://hive.happierbees.com/wp-admin/plugins.php` | WordPress admin URL |

#### Local Dev Placeholders

| Placeholder | Example Value | Description |
|------------|---------------|-------------|
| `{{LOCAL_DEV_PATH}}` | `../.local-dev-environments/hive-happierbees/` | Path to shared Docker environment |
| `{{DOCKER_CONTAINER_NAME}}` | `hive-happierbees-wordpress` | Docker container name |
| `{{SETTINGS_LOCATION}}` | `Settings > Query Keeper` | Where to find plugin settings |

#### Documentation Placeholders

| Placeholder | Example Value | Description |
|------------|---------------|-------------|
| `{{CREATION_DATE}}` | `2025-11-17` | Date created (YYYY-MM-DD) |
| `{{LAST_UPDATE_DATE}}` | `2025-11-17` | Last updated date |
| `{{RELEASE_DATE}}` | `2025-12-01` | Initial release date |
| `{{NEXT_FEATURE_NAME}}` | `Core Functionality` | Next version feature name |
| `{{MAJOR_FEATURE_NAME}}` | `Advanced Features` | Major version feature name |
| `{{FEATURE_DESCRIPTION}}` | Specific feature description | Feature details |
| `{{ARCHITECTURE_DESCRIPTION}}` | Architecture explanation | System architecture |
| `{{ADD_*}}` | Specific content | Various "add content here" markers |

### 5. Find and Replace Commands

Use these commands to replace placeholders:

```bash
# Basic plugin info
find . -type f -name "*.php" -o -name "*.md" -o -name "*.sh" -o -name "*.json" -o -name "*.xml" | \
  xargs sed -i 's/{{PLUGIN_NAME}}/Query Keeper/g'

find . -type f -name "*.php" -o -name "*.md" -o -name "*.sh" -o -name "*.json" -o -name "*.xml" | \
  xargs sed -i 's/{{PLUGIN_SLUG}}/query-keeper/g'

# Repeat for all other placeholders...
```

**OR** use a script to replace all at once (recommended):

```bash
#!/bin/bash

# Define replacements
declare -A replacements=(
  ["{{PLUGIN_NAME}}"]="Query Keeper"
  ["{{PLUGIN_SLUG}}"]="query-keeper"
  ["{{PLUGIN_DESCRIPTION}}"]="Makes UTM and affiliate link data persist between domains"
  ["{{NAMESPACE}}"]="QueryKeeper"
  ["{{PACKAGE_NAME}}"]="QueryKeeper"
  ["{{CONSTANT_PREFIX}}"]="QK"
  ["{{FUNCTION_PREFIX}}"]="query_keeper"
  ["{{TEXT_DOMAIN}}"]="query-keeper"
  # Add all other replacements...
)

# Replace in all files
for placeholder in "${!replacements[@]}"; do
  replacement="${replacements[$placeholder]}"
  find . -type f \( -name "*.php" -o -name "*.md" -o -name "*.sh" -o -name "*.json" -o -name "*.xml" -o -name "*.toml" \) \
    -exec sed -i "s|${placeholder}|${replacement}|g" {} +
done
```

### 6. Rename Plugin Main File

```bash
# Rename from {{PLUGIN_SLUG}}.php to actual slug
mv plugin/{{PLUGIN_SLUG}}.php plugin/query-keeper.php
```

### 7. Rename Plugin Class Files

```bash
# Rename all class files with {{PLUGIN_SLUG}} in filename
cd plugin/includes
for file in class-{{PLUGIN_SLUG}}*.php; do
  newname=$(echo "$file" | sed 's/{{PLUGIN_SLUG}}/query-keeper/g')
  mv "$file" "$newname"
done
cd ../..
```

### 8. Update OpenSpec project.md

Edit `openspec/project.md` with:
- Product overview
- Business context
- Tech stack specifics
- Important constraints
- Critical terminology

### 9. Initialize Git and Push

```bash
# Already initialized, just add remote and push
git remote add origin https://github.com/FlowjiWeb/query-keeper.git
git branch -M main
git push -u origin main
```

### 10. Install Dependencies

```bash
cd plugin
composer install
```

### 11. Verify Setup

```bash
# Run tests (should pass with sample test)
composer test

# Check coding standards (may need fixes)
composer phpcs

# Verify all placeholders replaced
grep -r "{{" . --exclude-dir=vendor --exclude-dir=node_modules
```

## Post-Setup Tasks

1. **Update openspec/ROADMAP.md** with actual feature roadmap
2. **Create first OpenSpec proposal** for core functionality
3. **Configure local Docker environment** if using shared setup
4. **Update .flowji-ai/config.json** if needed
5. **Test deployment script** (update SSH credentials first)

## Verification Checklist

- [ ] All `{{PLACEHOLDER}}` values replaced
- [ ] Plugin main file renamed correctly
- [ ] Class files renamed correctly
- [ ] Git remote configured and pushed
- [ ] Dependencies installed (`vendor/` directory exists)
- [ ] Tests pass (`composer test`)
- [ ] No placeholder syntax remains (`grep -r "{{" .`)
- [ ] OpenSpec project.md updated with actual product context
- [ ] ROADMAP.md reflects actual planned features

## Common Issues

### Symlinks Not Working

If symlinks don't work in your environment:

```bash
# Remove broken symlinks
find . -type l ! -exec test -e {} \; -delete

# Manually copy symlinked files
# Check .claude/AGENTS.md, .qwen/AGENTS.md, etc.
```

### Git Hooks Not Executing

```bash
# Make hooks executable
chmod +x .git/hooks/*
```

### Composer Install Fails

```bash
# Update composer first
composer self-update

# Try install again
composer install --ignore-platform-reqs
```

## Next Steps

After setup is complete, you're ready to:

1. Create your first OpenSpec proposal: `/openspec:proposal`
2. Start implementing features
3. Use `/flowji-ai:push-to-local` to deploy to local Docker
4. Use `/gc` command for structured commits

Happy coding! 🚀
