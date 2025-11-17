# Instructions for AI Agent - WordPress Plugin Boilerplate Setup

This document contains two sets of instructions for AI agents.

---

## PART 1: Push Boilerplate to GitHub (wordpress-plugin-ai-boilerplate repo)

**Task:** Push the boilerplate from `/tmp/wordpress-plugin-ai-boilerplate/` to the GitHub repository.

**Repository:** `https://github.com/FlowjiWeb/wordpress-plugin-ai-boilerplate.git`

### Steps:

```bash
# Navigate to boilerplate directory
cd /tmp/wordpress-plugin-ai-boilerplate

# Verify git is initialized and remote is configured
git status
git remote -v

# Push to GitHub (user will provide credentials when prompted)
git push -u origin main
```

**Expected output:**
- You'll be prompted for GitHub username and password/token
- User will provide credentials
- Push should complete successfully
- Boilerplate will be live at https://github.com/FlowjiWeb/wordpress-plugin-ai-boilerplate

**If push fails:**
- Check that remote is configured: `git remote -v` (should show origin → FlowjiWeb/wordpress-plugin-ai-boilerplate.git)
- Verify branch name: `git branch` (should show `main` or `master`)
- Ask user to provide GitHub Personal Access Token if password doesn't work

---

## PART 2: Set Up New Plugin (Query Keeper) from Boilerplate

**Task:** Create a new WordPress plugin called "Query Keeper" using the boilerplate template.

**Plugin Description:** Makes UTM and affiliate link information persist between chosen domains.

**Target Repository:** Will be created at `https://github.com/FlowjiWeb/query-keeper.git` (or similar)

### Step 1: Create Plugin Directory

```bash
# Create new plugin directory in the Flowji WordPress plugins folder
mkdir -p ~/04-REPOSITORIES/04-REPOSITORIES-flowji/wordpress-plugins/query-keeper
cd ~/04-REPOSITORIES/04-REPOSITORIES-flowji/wordpress-plugins/query-keeper
```

### Step 2: Copy Boilerplate

```bash
# Copy all files from boilerplate (including hidden files)
cp -r /tmp/wordpress-plugin-ai-boilerplate/* .
cp -r /tmp/wordpress-plugin-ai-boilerplate/.[^.]* . 2>/dev/null || true

# Remove the setup instructions file (no longer needed)
rm SETUP-INSTRUCTIONS.md

# Verify copy
ls -la
```

### Step 3: Replace Placeholders with Query Keeper Values

Create and run this replacement script:

```bash
cat > replace-placeholders.sh << 'SCRIPT_END'
#!/bin/bash

echo "Replacing placeholders with Query Keeper values..."

# Define all replacements
declare -A replacements=(
  # Core plugin info
  ["{{PLUGIN_NAME}}"]="Query Keeper"
  ["{{PLUGIN_SLUG}}"]="query-keeper"
  ["{{PLUGIN_DESCRIPTION}}"]="Makes UTM and affiliate link data persist between domains"
  ["{{PLUGIN_DESCRIPTION_DETAILED}}"]="WordPress plugin that captures UTM parameters and affiliate link information, storing them in session/cookies to persist query data as users navigate between chosen domains. Enables accurate tracking of marketing attribution across multi-domain user journeys."
  ["{{PLUGIN_URI}}"]="https://github.com/FlowjiWeb/query-keeper"
  ["{{AUTHOR_NAME}}"]="Flowji"
  ["{{AUTHOR_URI}}"]="https://flowji.com"
  ["{{TEXT_DOMAIN}}"]="query-keeper"
  ["{{PACKAGE_NAME}}"]="QueryKeeper"
  ["{{NAMESPACE}}"]="QueryKeeper"
  ["{{CONSTANT_PREFIX}}"]="QK"
  ["{{FUNCTION_PREFIX}}"]="query_keeper"

  # SSH/Deployment (using hive.happierbees.com as deployment target)
  ["{{SSH_KEY_PATH}}"]="$HOME/.ssh/hive_happierbees_ssh_key"
  ["{{SSH_PORT}}"]="18765"
  ["{{SSH_USER}}"]="u144-gqesyzeld1lk"
  ["{{SSH_HOST}}"]="ssh.hive.happierbees.com"
  ["{{REMOTE_PLUGIN_PATH}}"]="~/www/hive.happierbees.com/public_html/wp-content/plugins/query-keeper"
  ["{{WORDPRESS_ADMIN_URL}}"]="https://hive.happierbees.com/wp-admin/plugins.php"

  # Local dev
  ["{{LOCAL_DEV_PATH}}"]="../.local-dev-environments/hive-happierbees/"
  ["{{DOCKER_CONTAINER_NAME}}"]="hive-happierbees-wordpress"
  ["{{SETTINGS_LOCATION}}"]="Settings > Query Keeper"

  # Documentation
  ["{{CREATION_DATE}}"]="2025-11-17"
  ["{{LAST_UPDATE_DATE}}"]="2025-11-17"
  ["{{RELEASE_DATE}}"]="TBD"
  ["{{NEXT_FEATURE_NAME}}"]="Query Parameter Capture"
  ["{{MAJOR_FEATURE_NAME}}"]="Cross-Domain Persistence"

  # Placeholders to remove (leave blank for user to fill)
  ["{{FEATURE_DESCRIPTION}}"]="[To be defined in roadmap]"
  ["{{ARCHITECTURE_DESCRIPTION}}"]="Query Keeper uses WordPress hooks and filters to capture URL parameters, stores them in PHP sessions and cookies, and makes them available across page loads and domain boundaries."
  ["{{ADD_USAGE_INSTRUCTIONS}}"]="Configure domains in Settings > Query Keeper, then UTM and affiliate parameters will automatically persist."
  ["{{ADD_ADMIN_CLASS_DOCUMENTATION}}"]="[To be documented as classes are created]"
  ["{{ADD_PUBLIC_CLASS_DOCUMENTATION}}"]="[To be documented as classes are created]"
  ["{{ADD_DATABASE_SCHEMA_DOCUMENTATION}}"]="[To be documented if database tables are needed]"
  ["{{ADD_ACTION_DOCUMENTATION}}"]="[To be documented as hooks are implemented]"
  ["{{ADD_FILTER_DOCUMENTATION}}"]="[To be documented as filters are implemented]"
)

# Replace in all relevant files
for placeholder in "${!replacements[@]}"; do
  replacement="${replacements[$placeholder]}"
  echo "Replacing: $placeholder -> $replacement"

  find . -type f \( \
    -name "*.php" -o \
    -name "*.md" -o \
    -name "*.sh" -o \
    -name "*.json" -o \
    -name "*.xml" -o \
    -name "*.neon" -o \
    -name "*.toml" \
  \) -exec sed -i "s|${placeholder}|${replacement}|g" {} +
done

echo "✅ Placeholder replacement complete"
SCRIPT_END

chmod +x replace-placeholders.sh
./replace-placeholders.sh
rm replace-placeholders.sh
```

### Step 4: Rename Plugin Files

```bash
# Rename main plugin file
mv plugin/{{PLUGIN_SLUG}}.php plugin/query-keeper.php

# Rename class files in includes/
cd plugin/includes
for file in class-{{PLUGIN_SLUG}}*.php; do
  if [ -f "$file" ]; then
    newname=$(echo "$file" | sed 's/{{PLUGIN_SLUG}}/query-keeper/g')
    mv "$file" "$newname"
    echo "Renamed: $file -> $newname"
  fi
done
cd ../..

echo "✅ File renaming complete"
```

### Step 5: Verify Placeholder Replacement

```bash
# Check for any remaining {{PLACEHOLDER}} syntax
echo "Checking for remaining placeholders..."
remaining=$(grep -r "{{" . --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null || true)

if [ -z "$remaining" ]; then
  echo "✅ No placeholders remaining - all replaced successfully"
else
  echo "⚠️  Found remaining placeholders:"
  echo "$remaining"
  echo ""
  echo "These may need manual review/replacement"
fi
```

### Step 6: Update OpenSpec project.md

The user has a detailed spec for Query Keeper. Ask them:

"I've set up the Query Keeper boilerplate. You mentioned you have a detailed spec written. Should I:
1. Wait for you to provide the spec, then I'll update `openspec/project.md`?
2. Or should I create a basic project.md now and you'll provide the detailed spec later?"

### Step 7: Initialize Git for Query Keeper

```bash
# Git should already be initialized, but verify
git status

# If needed, initialize
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial Query Keeper setup from boilerplate"
fi

# Configure remote (user will create the repo first)
# NOTE: Don't push yet - user will do this manually
echo ""
echo "✅ Git initialized and ready"
echo ""
echo "Next steps for user:"
echo "1. Create GitHub repo: https://github.com/FlowjiWeb/query-keeper"
echo "2. Then run:"
echo "   git remote add origin https://github.com/FlowjiWeb/query-keeper.git"
echo "   git branch -M main"
echo "   git push -u origin main"
```

### Step 8: Install Dependencies (Optional)

```bash
# Install Composer dependencies
cd plugin
composer install

# Verify installation
if [ -d vendor ]; then
  echo "✅ Composer dependencies installed"

  # Run tests to verify setup
  echo "Running tests..."
  composer test
else
  echo "⚠️  Composer install failed or vendor directory not created"
fi

cd ..
```

### Step 9: Final Verification Checklist

```bash
echo ""
echo "=== Setup Verification Checklist ==="
echo ""

# Check main plugin file exists
[ -f plugin/query-keeper.php ] && echo "✅ Main plugin file: plugin/query-keeper.php" || echo "❌ Main plugin file not found"

# Check class files renamed
[ -f plugin/includes/class-query-keeper.php ] && echo "✅ Core class: class-query-keeper.php" || echo "❌ Core class not renamed"
[ -f plugin/includes/class-query-keeper-loader.php ] && echo "✅ Loader class: class-query-keeper-loader.php" || echo "❌ Loader class not renamed"

# Check for placeholders
placeholder_count=$(grep -r "{{" . --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null | wc -l)
if [ "$placeholder_count" -eq 0 ]; then
  echo "✅ No placeholders remaining"
else
  echo "⚠️  $placeholder_count placeholders still found (may need manual review)"
fi

# Check git status
[ -d .git ] && echo "✅ Git initialized" || echo "❌ Git not initialized"

# Check composer vendor
[ -d plugin/vendor ] && echo "✅ Composer dependencies installed" || echo "⚠️  Composer dependencies not installed"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Query Keeper is ready at:"
echo "  $(pwd)"
echo ""
echo "Next steps:"
echo "1. Review openspec/project.md and add detailed product spec"
echo "2. Update openspec/ROADMAP.md with planned features"
echo "3. Create GitHub repo and push to main (user will handle this)"
echo "4. Start first OpenSpec proposal: /openspec:proposal"
```

---

## Summary for User

After the agent completes both parts:

**Part 1 Result:**
- Boilerplate pushed to https://github.com/FlowjiWeb/wordpress-plugin-ai-boilerplate
- Ready for future projects to clone and use

**Part 2 Result:**
- Query Keeper set up at: `~/04-REPOSITORIES/04-REPOSITORIES-flowji/wordpress-plugins/query-keeper`
- All placeholders replaced with Query Keeper values
- Files renamed correctly
- Git initialized (but NOT pushed - you'll do that manually)

**What you need to do:**
1. Create GitHub repo for Query Keeper: https://github.com/FlowjiWeb/query-keeper
2. Push Query Keeper to GitHub:
   ```bash
   cd ~/04-REPOSITORIES/04-REPOSITORIES-flowji/wordpress-plugins/query-keeper
   git remote add origin https://github.com/FlowjiWeb/query-keeper.git
   git branch -M main
   git push -u origin main
   ```
3. Provide your detailed Query Keeper spec to update `openspec/project.md`

---

## Agent Notes

- User has a detailed spec for Query Keeper - ask for it after setup
- Query Keeper will deploy to hive.happierbees.com initially (same as MemberPress Multi-Currency)
- Uses the same shared Docker local dev environment
- All Flowji AI workflows (OpenSpec, Git Summaries, multi-agent commands) are included

**If anything fails, pause and ask the user before proceeding.**
