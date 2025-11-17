#!/bin/bash
set -euo pipefail

# sync_session_protocol.sh
# Syncs Session Start Protocol section to AGENTS.md files across all deployed repositories
# Usage: ./sync_session_protocol.sh [--check-only] [--force]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$SCRIPT_DIR/templates/session-start-protocol.md"
TOOLKIT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AGENTS_MD="$TOOLKIT_ROOT/AGENTS.md"

# Parse arguments
CHECK_ONLY=false
FORCE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --check-only)
      CHECK_ONLY=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--check-only] [--force]"
      exit 1
      ;;
  esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Read deployment registry from AGENTS.md
echo -e "${BLUE}Reading deployment registry from AGENTS.md...${NC}"

# Extract repository paths from deployment registry table (skip header rows and source toolkit)
# Look for lines with backtick-enclosed paths, skip source toolkit
REPOS=$(grep -A 50 "## Deployment Registry" "$AGENTS_MD" | \
        grep '`/Users/' | \
        grep -v "Source toolkit" | \
        sed 's/.*`\([^`]*\)`.*/\1/')

if [ -z "$REPOS" ]; then
  echo -e "${RED}No repositories found in deployment registry${NC}"
  exit 1
fi

# Count repos
REPO_COUNT=$(echo "$REPOS" | wc -l | tr -d ' ')
echo -e "${GREEN}Found $REPO_COUNT repositories in deployment registry${NC}\n"

# Statistics
MISSING=0
EXISTS=0
UPDATED=0
FAILED=0

# Process each repository
while IFS= read -r repo_path; do
  # Expand tilde to home directory
  repo_path="${repo_path/#\~/$HOME}"

  agents_file="$repo_path/AGENTS.md"

  echo -e "${BLUE}Checking: $repo_path${NC}"

  # Check if AGENTS.md exists
  if [ ! -f "$agents_file" ]; then
    echo -e "  ${RED}✗ AGENTS.md not found${NC}"
    ((FAILED++))
    continue
  fi

  # Check if Flowji AI Git Summaries block already exists
  if grep -q "<!-- FLOWJI-AI-GIT-SUMMARIES:START -->" "$agents_file"; then
    echo -e "  ${GREEN}✓ Flowji AI Git Summaries block exists${NC}"
    ((EXISTS++))

    if [ "$FORCE" = true ] && [ "$CHECK_ONLY" = false ]; then
      echo -e "  ${YELLOW}→ Updating (--force enabled)${NC}"
      # Create backup
      cp "$agents_file" "$agents_file.bak"

      # Remove existing block (from START to END markers inclusive)
      sed -i.tmp '/<!-- FLOWJI-AI-GIT-SUMMARIES:START -->/,/<!-- FLOWJI-AI-GIT-SUMMARIES:END -->/d' "$agents_file"

      # Find insertion point (after frontmatter if exists, otherwise at top)
      if head -1 "$agents_file" | grep -q "^---"; then
        # Has frontmatter, find closing ---
        insert_line=$(awk '/^---/{c++; if(c==2){print NR; exit}}' "$agents_file")
      else
        # No frontmatter, insert at top
        insert_line=0
      fi

      # Insert new block
      if [ "$insert_line" -eq 0 ]; then
        # Insert at very top
        { cat "$TEMPLATE_FILE"; echo ""; cat "$agents_file"; } > "$agents_file.new"
        mv "$agents_file.new" "$agents_file"
      else
        # Insert after frontmatter
        ed -s "$agents_file" << EOF
${insert_line}a

$(cat "$TEMPLATE_FILE")
.
w
q
EOF
      fi

      rm -f "$agents_file.tmp"
      echo -e "  ${GREEN}✓ Updated${NC}"
      ((UPDATED++))
      ((EXISTS--))
    fi
    continue
  fi

  echo -e "  ${YELLOW}✗ Flowji AI Git Summaries block missing${NC}"
  ((MISSING++))

  # Add if not in check-only mode
  if [ "$CHECK_ONLY" = false ]; then
    echo -e "  ${BLUE}→ Adding Flowji AI Git Summaries block...${NC}"

    # Create backup
    cp "$agents_file" "$agents_file.bak"

    # Find insertion point (after frontmatter if exists, otherwise at top)
    if head -1 "$agents_file" | grep -q "^---"; then
      # Has frontmatter, find closing ---
      insert_line=$(awk '/^---/{c++; if(c==2){print NR; exit}}' "$agents_file")
    else
      # No frontmatter, insert at top
      insert_line=0
    fi

    # Insert block
    if [ "$insert_line" -eq 0 ]; then
      # Insert at very top
      { cat "$TEMPLATE_FILE"; echo ""; cat "$agents_file"; } > "$agents_file.new"
      mv "$agents_file.new" "$agents_file"
    else
      # Insert after frontmatter
      ed -s "$agents_file" << EOF
${insert_line}a

$(cat "$TEMPLATE_FILE")
.
w
q
EOF
    fi

    if [ $? -eq 0 ]; then
      echo -e "  ${GREEN}✓ Added successfully${NC}"
      ((UPDATED++))
      ((MISSING--))
      rm "$agents_file.bak"
    else
      echo -e "  ${RED}✗ Failed to add${NC}"
      mv "$agents_file.bak" "$agents_file"
      ((FAILED++))
    fi
  fi

  echo ""
done <<< "$REPOS"

# Summary
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "Total repositories: $REPO_COUNT"
echo -e "${GREEN}Already exists: $EXISTS${NC}"
echo -e "${YELLOW}Missing: $MISSING${NC}"
echo -e "${GREEN}Updated: $UPDATED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ "$CHECK_ONLY" = true ]; then
  echo -e "\n${YELLOW}Check-only mode: No changes made${NC}"
  if [ $MISSING -gt 0 ]; then
    echo -e "${YELLOW}Run without --check-only to add missing protocols${NC}"
  fi
fi

# Exit code based on results
if [ $FAILED -gt 0 ]; then
  exit 1
elif [ "$CHECK_ONLY" = true ] && [ $MISSING -gt 0 ]; then
  exit 2
else
  exit 0
fi
