# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-18

### Added
- YAML configuration file support for all commands
- Progress indicators for long-running operations
- Comprehensive input validation with helpful error messages
- Unit test suite with pytest framework
- Code coverage reporting (64% coverage)
- GitHub Actions CI workflow
- Coverage badge in README
- Dry-run mode for all commands
- Resume capability for NT screening
- Memory limit option for derep command
- USER_GUIDE.md with detailed usage instructions
- MIGRATION_GUIDE.md for upgrading from v0.1.0
- Example configuration files

### Changed
- Improved error messages throughout the CLI
- Enhanced validation for all file and directory inputs
- Better handling of environment variables
- Standardized logging across all commands

### Fixed
- File path resolution issues in various environments
- Worker count environment variable handling
- Float string parsing in integer validation

### Docker
- Released multi-platform image v1.2.0 with CLI support

## [0.1.0] - 2025-01-17

### Added
- Initial release of cryptic-screen CLI
- Unified command-line interface for all screening tools
- Support for NT screening, PM screening, winnow filtering, and deduplication
- Basic argument parsing and validation
- Environment variable support
- Docker containerization