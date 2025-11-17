#!/usr/bin/env bash
# Install global /gc command for Claude Code, Opencode, and Codex
# This creates:
#   - ~/.claude/commands/gc.md (Claude Code)
#   - ~/.config/opencode/command/gc.md (Opencode)
#   - ~/.codex/prompts/gc.md (Codex)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$SCRIPT_DIR/templates/gc-command.md"

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: Template not found at $TEMPLATE_FILE"
    exit 1
fi

# Function to install command for a given path
install_command() {
    local TARGET_DIR="$1"
    local TARGET_FILE="$TARGET_DIR/gc.md"

    # Create directory if needed
    mkdir -p "$TARGET_DIR"

    # Check if already exists
    if [ -f "$TARGET_FILE" ]; then
        echo "✓ /gc command already exists at $TARGET_FILE"
        return 0
    fi

    # Copy template
    cp "$TEMPLATE_FILE" "$TARGET_FILE"
    echo "✓ Installed /gc command to $TARGET_FILE"
}

echo "Installing Flowji /gc command globally..."
echo ""
echo "Note: Different tools use different paths:"
echo "  - Claude Code uses 'commands' (plural)"
echo "  - Opencode uses 'command' (singular)"
echo "  - Codex uses 'prompts'"
echo ""

# Install for Claude Code
install_command "$HOME/.claude/commands"

# Install for Opencode (uses singular "command" not "commands")
install_command "$HOME/.config/opencode/command"

# Install for Codex (uses "prompts")
install_command "$HOME/.codex/prompts"

echo ""
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  - In Claude Code or Opencode, type: /gc"
echo "  - In Codex, type: /prompts:gc"
echo "  - The assistant will analyze your git changes and generate a Flowji-style commit message"
echo "  - You can ask it to commit automatically or copy the message manually"
echo ""
