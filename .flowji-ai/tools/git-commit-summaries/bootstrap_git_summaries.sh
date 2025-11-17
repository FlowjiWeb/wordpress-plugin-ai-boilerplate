#!/bin/bash
# Bootstrap script to install Git commit summary hooks in multiple repositories

set -e  # Exit on any error

# Check if global /gc command is installed
check_gc_command() {
    local missing=()

    [ ! -f "$HOME/.claude/commands/gc.md" ] && missing+=("Claude Code (~/.claude/commands/gc.md)")
    [ ! -f "$HOME/.config/opencode/command/gc.md" ] && missing+=("Opencode (~/.config/opencode/command/gc.md)")

    if [ ${#missing[@]} -gt 0 ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⚠️  Global /gc command not found for:"
        for item in "${missing[@]}"; do
            echo "   - $item"
        done
        echo ""
        echo "The /gc command helps generate Flowji-structured commit messages."
        echo ""
        read -p "Would you like to install it now? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
            "$SCRIPT_DIR/install_gc_command.sh"
        else
            echo "Skipping /gc installation. You can install it later with:"
            echo "  ./.flowji-ai/tools/git-commit-summaries/install_gc_command.sh"
        fi
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
    fi
}

# Default search paths - adjust these as needed for your system
SEARCH_PATHS=(
    "$HOME/Projects"
    "$HOME/Development"
    "$HOME/Git"
    "$HOME/Code"
    # Add additional paths here if needed
)

# Allow custom search paths via environment variable
if [ -n "$GIT_SUMMARIES_SEARCH_PATHS" ]; then
    IFS=':' read -ra SEARCH_PATHS <<< "$GIT_SUMMARIES_SEARCH_PATHS"
fi

# Function to check if directory is a git repository
is_git_repo() {
    local dir="$1"
    [ -d "$dir/.git" ] && [ -f "$dir/.git/config" ]
}

# Function to install hook in a repository
install_hook_in_repo() {
    local repo_path="$1"
    echo "Installing hook in: $repo_path"
    
    # Change to the repository directory and install the hook
    (
        cd "$repo_path"
        # Use the install script to install the hook
        # First, find the relative path to the install script from the repo
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        INSTALL_SCRIPT="$SCRIPT_DIR/install_post_commit_hook.sh"
        
        if [ -f "$INSTALL_SCRIPT" ]; then
            "$INSTALL_SCRIPT" || echo "Failed to install in $repo_path"
        else
            echo "Install script not found: $INSTALL_SCRIPT"
        fi
    )
}

# Main function to scan and install
scan_and_install() {
    # Check for /gc command first
    check_gc_command

    local count=0
    echo "Scanning for Git repositories in the following paths:"
    for path in "${SEARCH_PATHS[@]}"; do
        echo "  - $path"
    done
    echo
    
    for search_path in "${SEARCH_PATHS[@]}"; do
        if [ ! -d "$search_path" ]; then
            echo "Warning: Search path does not exist: $search_path"
            continue
        fi
        
        # Find all git repositories under the search path
        while IFS= read -r -d '' repo_dir; do
            repo_dir=$(dirname "$repo_dir")  # Get the directory containing .git
            if [ "$repo_dir" != "." ]; then  # Skip current directory
                install_hook_in_repo "$repo_dir"
                ((count++))
            fi
        done < <(find "$search_path" -name ".git" -type d -print0)
    done
    
    echo
    echo "Installation completed. Processed $count repositories."
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--path)
            SEARCH_PATHS=("$2")
            shift 2
            ;;
        -c|--config)
            if [ -f "$2" ]; then
                source "$2"
            else
                echo "Configuration file not found: $2"
                exit 1
            fi
            shift 2
            ;;
        -h|--help)
            echo "Bootstrap Git commit summary hook installation in multiple repositories"
            echo
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -p, --path PATH    Install hooks in repositories under PATH only"
            echo "  -c, --config FILE  Load configuration from FILE"
            echo "  -h, --help         Show this help message"
            echo
            echo "By default, searches in: ${SEARCH_PATHS[*]}"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Execute the scan and install
scan_and_install