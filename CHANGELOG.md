# Changelog

All notable changes to the Space & Astronomy MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Mars weather data integration
- Hubble Space Telescope image searches
- Exoplanet database queries
- Solar system object positions
- Earth imagery from EPIC camera
- Solar flare and space weather alerts

## [1.0.0] - 2024-11-03

### Added
- Initial release of Space & Astronomy MCP Server
- NASA Astronomy Picture of the Day (APOD) tool
- Mars Rover Photos tool with support for Curiosity, Perseverance, Opportunity, and Spirit
- Near-Earth Object (NEO) asteroid tracking tool
- Real-time International Space Station location tracking tool
- Global space launch tracking tool with Launch Library 2 integration
- Flexible response formats (Markdown and JSON)
- Comprehensive input validation with Pydantic v2
- Full type hints throughout codebase
- Async/await patterns for all I/O operations
- Character limit protection (25,000 chars)
- Pagination support for large datasets
- Comprehensive error handling with actionable messages
- Tool annotations for MCP compliance
- Complete documentation (README, API Reference, Examples)
- 10 evaluation questions for testing
- MIT License

### Technical Details
- Python 3.10+ support
- FastMCP framework integration
- httpx for async HTTP requests
- Pydantic v2 for data validation
- stdio transport for MCP communication

### APIs Integrated
- NASA APOD API
- NASA Mars Rover Photos API
- NASA NeoWs (Near-Earth Object Web Service)
- wheretheiss.at ISS tracking API
- Launch Library 2 API by The Space Devs

### Documentation
- Comprehensive README.md with quick start guide
- Detailed API reference for all 6 tools
- Usage examples for common scenarios
- Configuration guide for Claude Desktop
- Troubleshooting section
- Contributing guidelines
- Code of conduct
- MIT License

### Quality Assurance
- 500+ lines of production-quality code
- Full syntax validation
- Type-safe implementation
- Error handling coverage
- Character limit protection
- Evaluation framework

---

## Version History

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

### Release Types

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security vulnerability fixes

---

## How to Update This Changelog

When making changes to the project:

1. Add your changes under `[Unreleased]` section
2. Use the appropriate category (Added, Changed, Fixed, etc.)
3. Write clear, concise descriptions
4. Include issue/PR numbers when applicable

Example:
```markdown
### Added
- New Mars weather tool (#42)
- Support for multiple API keys (#45)

### Fixed
- ISS tracking timeout issue (#38)
- Mars rover photo pagination bug (#41)
```

When releasing a new version:

1. Move items from `[Unreleased]` to new version section
2. Add release date in YYYY-MM-DD format
3. Update version number in code
4. Create git tag for release

---

## Links

- [Repository](https://github.com/yourusername/space-mcp-server)
- [Issues](https://github.com/yourusername/space-mcp-server/issues)
- [Pull Requests](https://github.com/yourusername/space-mcp-server/pulls)
- [Releases](https://github.com/yourusername/space-mcp-server/releases)

---

*This changelog format is based on [Keep a Changelog](https://keepachangelog.com/).*
