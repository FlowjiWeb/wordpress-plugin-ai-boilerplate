#!/bin/bash
# Update all deployed repositories from deployment-registry.md

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
REGISTRY="$REPO_ROOT/deployment-registry.md"
DEPLOY_SCRIPT="$SCRIPT_DIR/deploy_to_repo.sh"

echo "📦 Updating all deployments from registry..."
echo

if [ ! -f "$REGISTRY" ]; then
    echo "❌ Deployment registry not found: $REGISTRY"
    exit 1
fi

# Extract repo paths from registry (skip header and source toolkit)
REPOS=$(grep -E '^\|.*\|.*\|' "$REGISTRY" | \
        grep -v '|------' | \
        grep -v 'Repository Path' | \
        grep -v 'git-commit-summaries`' | \
        awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $3); print $3}' | \
        sed 's/`//g' | \
        grep -v '^$')

if [ -z "$REPOS" ]; then
    echo "❌ No repositories found in registry"
    exit 1
fi

TOTAL=$(echo "$REPOS" | wc -l | tr -d ' ')
CURRENT=0
UPDATED=0
FAILED=0

echo "Found $TOTAL repositories to update"
echo

while IFS= read -r repo_path; do
    CURRENT=$((CURRENT + 1))
    echo "[$CURRENT/$TOTAL] Updating: $repo_path"

    if [ ! -d "$repo_path" ]; then
        echo "  ⚠️  Directory not found, skipping"
        FAILED=$((FAILED + 1))
        echo
        continue
    fi

    if "$DEPLOY_SCRIPT" "$repo_path" > /tmp/deploy-output.log 2>&1; then
        echo "  ✓ Updated successfully"
        UPDATED=$((UPDATED + 1))
    else
        echo "  ❌ Failed (see /tmp/deploy-output.log)"
        FAILED=$((FAILED + 1))
    fi
    echo
done <<< "$REPOS"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Updated: $UPDATED"
echo "❌ Failed: $FAILED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -gt 0 ]; then
    exit 1
fi
