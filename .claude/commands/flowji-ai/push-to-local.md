---
name: Push to Local
description: Increment version and sync plugin to the Hive local Docker environment for testing
category: Flowji AI
tags: [flowji-ai, local, version]
---

Increment plugin version and sync files to local Docker environment for testing.

**Steps**
1. Read current version from `plugin/memberpress-multi-currency.php` (Version: X.Y.Z comment)
2. Increment patch number (e.g., 1.0.10 → 1.0.11)
3. Update version in main plugin file header comment
4. Update MPMC_VERSION constant if present
5. Sync plugin to `.local-dev-environments/hive-happierbees`: `rsync -av --delete plugin/ ../.local-dev-environments/hive-happierbees/public_html/wp-content/plugins/memberpress-multi-currency/`
6. Report new version and test URL

**Version Strategy**
- Increment patch for each task completion tested locally
- Format: MAJOR.MINOR.PATCH (e.g., 1.0.11, 1.0.12, 1.0.13...)
- When phase complete and deployed: bump MINOR (e.g., 1.1.0)
- Production remains at stable version until deployment

**Test URL**
- WordPress admin: http://localhost:8080/wp-admin/
- Currencies tab: http://localhost:8080/wp-admin/admin.php?page=memberpress-options&tab=currencies

**Notes**
- Only increment version when pushing to local for testing
- Version tracking tied to testing milestones
- Docker containers must be running (`cd ../.local-dev-environments/hive-happierbees && docker-compose up -d`)
