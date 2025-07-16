# Release Notes - v0.1.0

**Release Date**: 2025-07-16  
**Type**: Initial MVP Release  
**Branch**: cli-options  

## Overview

First functional release of the `cryptic-screen` CLI tool, providing a unified command-line interface for the Cryptic Screening toolkit used in SARS-CoV-2 sequence analysis and viral surveillance.

## Key Features

### 🎯 Unified CLI Interface
- Single `cryptic-screen` command with subcommands (nt, pm, winnow, derep)
- Consistent interface across all tools
- Built with Python's standard argparse library (no additional dependencies)

### 🔧 Configuration Management  
- All hardcoded file paths now configurable
- Environment variable support for automation
- YAML configuration files for reproducible pipelines
- Command-line arguments override all other settings

### 📁 Flexible File Management
- Current working directory as default for all operations
- Smart file resolution with multiple fallback locations
- No more hardcoded paths like `/mnt/f/SRA/`

### 📊 User Experience Enhancements
- Progress indicators for long operations
- Comprehensive input validation with helpful error messages
- Dry-run mode for testing commands
- Clear logging with multiple verbosity levels

### 📚 Documentation
- Comprehensive USER_GUIDE.md with examples
- MIGRATION_GUIDE.md for transitioning from old scripts
- Example configuration files
- Full backward compatibility maintained

## Installation

```bash
# No installation required - use directly
./cryptic-screen --help

# Or add to PATH
export PATH="/path/to/Programs:$PATH"
cryptic-screen --help

# Optional: Install PyYAML for config file support
pip install pyyaml
```

## Quick Start

```bash
# NT screening
cryptic-screen nt --input ./samples

# PM screening  
cryptic-screen pm --input ./unique_seqs

# Generate reports
cryptic-screen winnow --nt-results NTSeqScreenResults.tsv

# With configuration file
cryptic-screen --config config/cryptic-screen.yaml nt --input ./samples
```

## Environment Variables

```bash
export CRYPTIC_SCREEN_DATA_DIR=/data/references
export CRYPTIC_SCREEN_OUTPUT_DIR=/results
export CRYPTIC_SCREEN_WORKERS=32
```

## Migration from Old Scripts

| Old | New |
|-----|-----|
| `python NTSeqScreenMP.py` | `cryptic-screen nt --input .` |
| `python PMScreenMP.py` | `cryptic-screen pm --input .` |

## Known Limitations

This is an MVP release that wraps the original scripts without modifying core logic:
- Original error handling still present in core algorithms
- No unit tests yet
- Large file handling not optimized
- Core scripts still imported rather than refactored

## Next Version (v0.2.0)

Planned improvements:
- Comprehensive test suite
- Refactored core logic with better error handling
- Performance optimizations
- CI/CD pipeline

## Contributing

This is a fork of the original Programs repository. Contributions welcome:
- Fork: github.com/wilke/Programs-DG
- Branch: cli-options
- Original repo will be added as upstream for syncing

## Support

- Check `cryptic-screen --help` for command options
- See docs/USER_GUIDE.md for detailed examples
- Use `--dry-run` to test commands safely
- Run with `--log-level DEBUG` for troubleshooting