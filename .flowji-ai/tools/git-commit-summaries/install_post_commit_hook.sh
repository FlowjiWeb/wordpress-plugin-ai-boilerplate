#!/bin/bash
# Install script for the Git commit summary post-commit hook

set -e  # Exit on any error

TOOL_VERSION=$(cat "$(dirname "${BASH_SOURCE[0]}")/VERSION" 2>/dev/null || echo "unknown")

echo "Installing Git commit summary post-commit hook (v$TOOL_VERSION)..."

# Check if we're in a Git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a Git repository" >&2
    exit 1
fi

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)

# Determine hooks directory (supports custom core.hooksPath)
HOOKS_PATH_CONFIG=$(git config --local core.hooksPath || true)
if [ -n "$HOOKS_PATH_CONFIG" ]; then
    if [[ "$HOOKS_PATH_CONFIG" = /* ]]; then
        HOOKS_DIR="$HOOKS_PATH_CONFIG"
    else
        HOOKS_DIR="$REPO_ROOT/$HOOKS_PATH_CONFIG"
    fi
else
    HOOKS_DIR="$REPO_ROOT/.git/hooks"
fi

mkdir -p "$HOOKS_DIR"

# Get the path to the hook script relative to the repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SOURCE="$SCRIPT_DIR/hooks/post-commit"
HOOK_DEST="$HOOKS_DIR/post-commit"

# Copy the hook to the repository's hooks directory
cp "$HOOK_SOURCE" "$HOOK_DEST"

# Make the hook executable
chmod +x "$HOOK_DEST"

# Install prepare-commit-msg hook for commit template injection
PREPARE_SOURCE="$SCRIPT_DIR/hooks/prepare-commit-msg"
PREPARE_DEST="$HOOKS_DIR/prepare-commit-msg"
if [ -f "$PREPARE_SOURCE" ]; then
    cp "$PREPARE_SOURCE" "$PREPARE_DEST"
    chmod +x "$PREPARE_DEST"
fi

# Ensure the output directory exists
SUMMARY_SUBDIR="${GIT_SUMMARY_DIR:-.flowji-ai/memory/git-summaries}"
SUMMARIES_DIR="$REPO_ROOT/$SUMMARY_SUBDIR"
mkdir -p "$SUMMARIES_DIR"

# Install Flowji AI Git Summaries block in AGENTS.md if it exists and doesn't already have it
AGENTS_MD="$REPO_ROOT/AGENTS.md"
PROTOCOL_TEMPLATE="$SCRIPT_DIR/templates/session-start-protocol.md"

if [ -f "$AGENTS_MD" ] && [ -f "$PROTOCOL_TEMPLATE" ]; then
    if ! grep -q "<!-- FLOWJI-AI-GIT-SUMMARIES:START -->" "$AGENTS_MD"; then
        echo "Adding Flowji AI Git Summaries block to AGENTS.md..."

        # Create backup
        cp "$AGENTS_MD" "$AGENTS_MD.bak"

        # Find insertion point (after frontmatter if exists, otherwise at top)
        if head -1 "$AGENTS_MD" | grep -q "^---"; then
            # Has frontmatter, find closing ---
            insert_line=$(awk '/^---/{c++; if(c==2){print NR; exit}}' "$AGENTS_MD")
        else
            # No frontmatter, insert at top
            insert_line=0
        fi

        # Insert block
        if [ "$insert_line" -eq 0 ]; then
            # Insert at very top
            { cat "$PROTOCOL_TEMPLATE"; echo ""; cat "$AGENTS_MD"; } > "$AGENTS_MD.new"
            mv "$AGENTS_MD.new" "$AGENTS_MD"
        else
            # Insert after frontmatter
            ed -s "$AGENTS_MD" << EOF
${insert_line}a

$(cat "$PROTOCOL_TEMPLATE")
.
w
q
EOF
        fi

        if [ $? -eq 0 ]; then
            echo "✓ Flowji AI Git Summaries block added to AGENTS.md"
            rm "$AGENTS_MD.bak"
        else
            echo "✗ Failed to add Flowji AI Git Summaries block, restoring backup"
            mv "$AGENTS_MD.bak" "$AGENTS_MD"
        fi
    else
        echo "✓ Flowji AI Git Summaries block already exists in AGENTS.md"
    fi
fi

echo "Post-commit hook installed successfully!"
echo "The hook will now generate commit summaries in $SUMMARY_SUBDIR"
echo "Each commit will create a Markdown file with the commit details."
