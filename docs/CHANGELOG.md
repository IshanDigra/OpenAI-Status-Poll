# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-17

### Added

- Initial release of OpenAI Status Monitor
- Core monitoring functionality with ETag-based conditional polling
- Multiple notification channels (Console, Slack, Email)
- Pluggable state management (File, GCS, Gist)
- GitHub Actions automation with Gist-based state
- Comprehensive documentation
- Production-ready error handling and logging
- MIT License

### Features

#### Core Monitoring
- Efficient HTTP conditional GET requests using ETag/Last-Modified
- Achieves 99.9% bandwidth efficiency (304 Not Modified responses)
- Idempotent processing - each incident processed exactly once
- Automatic feed parsing with BeautifulSoup
- State persistence across runs

#### Notifiers
- Console notifier with formatted output
- Slack webhook integration with rich message formatting
- SMTP email support (Gmail-compatible)
- Pluggable architecture for custom notifiers

#### State Management
- File-based storage (local JSON)
- Google Cloud Storage backend
- GitHub Gist storage (for Actions)
- Abstract base class for custom backends

#### Deployment Options
- GitHub Actions workflows (Gist and commit-based)
- Local execution support
- Google Cloud Run compatibility
- Docker support
- Cron/systemd integration

#### Developer Experience
- Environment variable-based configuration
- Comprehensive logging with configurable levels
- `--run-once` flag for scheduled execution
- Well-documented codebase
- Type hints throughout

### Documentation

- README.md with quick start and comprehensive guide
- ARCHITECTURE.md explaining technical design
- CONTRIBUTING.md with development guidelines
- DEPLOYMENT.md with multi-platform instructions
- CHANGELOG.md (this file)
- Artifacts directory for screenshots

### Dependencies

- feedparser >= 6.0.10
- beautifulsoup4 >= 4.12.0
- python-dateutil >= 2.8.2
- requests >= 2.31.0
- google-cloud-storage >= 2.10.0

---

## [Unreleased]

### Planned Features

- Discord notifier
- Microsoft Teams integration
- PagerDuty alerting
- Prometheus metrics export
- Web dashboard for status history
- Multi-feed monitoring in single instance
- Incident analytics and reporting

### Under Consideration

- Redis state backend
- PostgreSQL state backend
- Webhook notification receiver
- Mobile app notifications
- Browser extension

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-11-17 | Initial release with core functionality |

---

## Migration Notes

### From Pre-1.0

No migration needed - this is the first release.

---

## Breaking Changes

None yet.

---

## Security Updates

None yet.

---

For detailed commit history, see: https://github.com/IshanDigra/OpenAI-Status-Poll/commits/main
