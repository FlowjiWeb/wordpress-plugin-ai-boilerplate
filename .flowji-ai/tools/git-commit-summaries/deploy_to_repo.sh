#!/bin/bash

# Deploy Flowji Git Commit Summaries toolkit to a target repository
# Usage: ./deploy_to_repo.sh /path/to/target/repo

set -e

if [ -z "$1" ]; then
    echo "Error: Target repository path required"
    echo "Usage: $0 /path/to/target/repo"
    exit 1
fi

TARGET_REPO="$1"

if [ ! -d "$TARGET_REPO" ]; then
    echo "Error: Directory does not exist: $TARGET_REPO"
    exit 1
fi

# Get the toolkit root (3 levels up from this script)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOOLKIT_ROOT="$( cd "$SCRIPT_DIR/../../.." && pwd )"

echo "Deploying Flowji Git Commit Summaries toolkit..."
echo "Source: $TOOLKIT_ROOT/.flowji-ai"
echo "Target: $TARGET_REPO/.flowji-ai"
echo ""

# Use rsync to copy .flowji-ai directory, excluding memory/
rsync -av --exclude='memory/' "$TOOLKIT_ROOT/.flowji-ai/" "$TARGET_REPO/.flowji-ai/"

echo ""
echo "✓ Toolkit files copied (memory/ excluded)"
echo ""

# Check if target is a git repository
if [ ! -d "$TARGET_REPO/.git" ]; then
    echo "⚠ Warning: $TARGET_REPO is not a git repository"
    read -p "Initialize git repository? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$TARGET_REPO"
        git init
        echo "✓ Git repository initialized"
    else
        echo "Skipping git initialization"
        exit 0
    fi
fi

# Run the post-commit hook installer
echo "Installing post-commit hook..."
cd "$TARGET_REPO"
./.flowji-ai/tools/git-commit-summaries/install_post_commit_hook.sh

echo ""
echo "✓ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Make a test commit in $TARGET_REPO"
echo "2. Verify summary appears in .flowji-ai/memory/git-summaries/"
