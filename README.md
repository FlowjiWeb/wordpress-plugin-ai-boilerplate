# {{PLUGIN_NAME}}

{{PLUGIN_DESCRIPTION}}

WordPress plugin developed using AI-assisted workflows with OpenSpec, multi-agent commands, and Flowji AI Git Summaries.

**Version:** 1.0.0  
**License:** GPL-2.0+

## Quick Start

### Installation

1. Upload `plugin/` directory to `/wp-content/plugins/{{PLUGIN_SLUG}}/`
2. Activate through WordPress admin
3. Configure settings at {{SETTINGS_LOCATION}}

### Local Development

```bash
# Start Docker environment
cd {{LOCAL_DEV_PATH}}
docker-compose up -d

# Install dependencies
cd plugin
composer install

# Run tests
composer test
```

Access: http://localhost:8080

## Documentation

- **AGENTS.md** - Complete developer guide and AI agent instructions
- **plugin/AGENTS.md** - Technical implementation details
- **openspec/ROADMAP.md** - Planned features and milestones
- **CHANGELOG.md** - Version history

## Development Tools

- **OpenSpec** - Structured change proposals and specifications
- **Multi-agent CLI** - Claude, Qwen, OpenCode, KiloCode, Gemini support
- **Flowji AI Git** - Automatic commit summaries and documentation
- **PHPUnit/WP_Mock** - Unit testing framework
- **PHPCS/PHPStan** - Code quality and static analysis

## License

GPL-2.0+ - see LICENSE file for details.
