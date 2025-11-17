# Git Commit Summaries - Changelog

## [0.5.0] - 2025-11-10

### Added
- Escaped newline detection in post-commit hook with loud error messages
- `--validate-only` CLI flag for testing and CI integration
- Step 5 validation requirement in `/gc` workflow
- Test suite for escaped newline detection (`tests/test_escaped_newlines.py`)
- Defense-in-depth validation (both hook and `/gc` prompt)
- Merge commit detection and validation skip logic
- Code block filtering to prevent false positives in detection

### Changed
- `/gc` template simplified to heredoc-only (ANSI-C as advanced fallback)
- Post-commit hook now validates commit messages before generating summaries
- Malformed commits skip summary generation (hook exits 0, non-blocking)
- Updated AGENTS.md with escaped newlines troubleshooting section
- README.md and AGENTS.md consolidated (DRY cleanup, -116 lines net)

### Fixed
- Escaped `\n` sequences now detected and prevented via validation
- Clear fix instructions provided when validation fails

## [0.4.0] - 2025-11-08

### Added
- Multi-concern commit splitting detection in `/gc` command
- File type clustering analysis: documentation (.md) vs code (.php/.js/.json)
- Directory separation detection: plugin/ vs docs/ vs tests/
- Semantic analysis to identify unrelated concerns in single commit
- Interactive prompt to suggest atomic commit splits
- Sequential commit workflow for handling multiple concerns

### Changed
- `/gc` command now analyzes changes before generating commit message
- Agent detects and warns when changes span multiple unrelated concerns
- Updated all 4 locations: Claude Code, Opencode, Codex, GitHub Copilot

## [0.3.1] - 2025-11-08

### Fixed
- `/gc` command now explicitly checks for untracked files and prompts to include them
- Added atomic commit validation to prevent incomplete commits (e.g., dependency injection without tests)
- Enhanced instructions to ask user before excluding functionally-related untracked files

### Changed
- Updated `/gc` template in all 4 locations: Claude Code, Opencode, Codex, GitHub Copilot
- Improved agent guidance based on real-world feedback from memberpress-multi-currency incident

## [0.3.0] - 2025-11-08

### Added
- Auto-commit functionality for git summaries to prevent GitHub Copilot hanging
- Recursive guard to prevent infinite hook loops when committing summaries
- `[git-summary]` commit prefix for auto-generated summary commits

### Changed
- Git summaries now automatically committed and tracked for team collaboration
- Post-commit hook creates two commits: user's commit + auto-commit of summary file

### Fixed
- GitHub Copilot no longer hangs when committing (was confused by untracked summary files)
- Tools that scan for untracked files post-commit now work correctly

## [0.2.0] - 2025-11-08

### Added
- XML-style managed block markers (`<!-- FLOWJI-AI-GIT-SUMMARIES:START/END -->`) for AGENTS.md protocol section
- New "Git Commit Workflow" section in protocol explaining hooks, agent responsibilities, and commit structure
- Blank line after START marker for improved readability
- Frontmatter-aware insertion logic (inserts after closing `---` if present)

### Changed
- Session Start Protocol now positioned at top of AGENTS.md (after frontmatter), before other managed blocks like OpenSpec
- Follows OpenSpec pattern with H1 inside XML markers for self-contained documentation
- Enhanced sync script to handle managed block updates with `--force` flag
- Installer now uses XML markers and smart positioning

### Improved
- Agent instructions now explicitly state: never commit without approval, use `/gc` command, let hooks run automatically
- Clearer documentation of how the toolkit works and what agents should/shouldn't do
- Deployed retention policy fix to all 6 deployed repositories

## [0.1.1] - 2025-11-06

### Fixed
- Fixed variable shadowing where `filepath` loop variable overwrote output file path, causing script to write summary to itself
- Fixed `Path.relative_to()` TypeError by converting string `repo_root` to Path object

### Removed
- Removed experimental auto-generation logic that replaced manual commit descriptions with generic text

## [0.1.0] - 2025-11-05

Initial release.

### Added
- Post-commit hook for automatic summary generation
- Prepare-commit-msg hook for template injection
- Global `/gc` command for Claude Code and Opencode
- 180-day retention policy
- Husky compatibility
- Deployment registry tracking

### Features
- Structured Markdown summaries with frontmatter
- File change tracking (created/edited/deleted/renamed)
- Commit stats integration
- Template-based commit messages
