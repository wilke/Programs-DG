# CLI Implementation Review Checklist

## Pre-Implementation Review

Before starting implementation on the `cli-options` branch, let's review the key decisions and steps.

## 1. Architecture Decisions

### Should we use Click or argparse?
**Decision**: Use **argparse** ✓
- **Pros**: No additional dependencies, already used in derep.py, standard library
- **Cons**: More verbose, need to implement subcommands manually
- **Implementation**: Use subparsers for command structure

### Directory Structure
```
Programs/
├── cryptic_screening/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── commands/           # CLI command implementations
│   │   ├── __init__.py
│   │   ├── nt.py
│   │   ├── pm.py
│   │   ├── winnow.py
│   │   └── derep.py
│   ├── core/               # Refactored core logic
│   │   ├── __init__.py
│   │   ├── nt_screen.py    # From NTSeqScreenMP.py
│   │   ├── pm_screen.py    # From PMScreenMP.py
│   │   ├── winnow.py       # From WinnowScreens.py
│   │   └── derep.py        # From derep.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_resolver.py # File resolution logic
│   │   └── config.py       # Configuration management
│   └── data/               # Package data files
│       ├── LinkedPMs.txt
│       └── SinglePMs.txt
├── bin/                    # Backward compatibility scripts
│   ├── NTSeqScreenMP.py
│   ├── PMScreenMP.py
│   └── WinnowScreens.py
├── setup.py                # Updated for new structure
└── requirements.txt        # Add click dependency
```

## 2. Implementation Priority

### Phase 1: Minimal Breaking Changes (Week 1)
Focus on making files configurable without changing core logic:

1. **Add CLI wrapper around existing code**
   - Don't refactor the core algorithms yet
   - Just wrap with better interface

2. **File resolution improvements**
   - Replace hardcoded paths with configurable options
   - Add smart defaults that check multiple locations
   - Keep current working directory as default

3. **Maintain exact output format**
   - Same file formats
   - Same column names
   - Same file naming patterns (but configurable location)

### Phase 2: Enhanced Features (Week 2)
After basic CLI works:

1. **Add configuration file support**
2. **Implement dry-run mode**
3. **Add progress indicators**
4. **Improve error messages**

## 3. Critical Implementation Details

### File Resolution Priority
For each reference file (LinkedPMs.txt, SinglePMs.txt, etc.):

1. Command line argument (if provided)
2. Config file setting (if provided)
3. Data directory + filename
4. Current working directory
5. Package data directory
6. ~/.cryptic-screening/data/

### Backward Compatibility Strategy

1. **Keep original scripts functional**
   ```python
   # Cryptic_Screening/NTSeqScreenMP.py stays as-is
   # Create new structure in parallel
   ```

2. **Add deprecation warnings**
   ```python
   import warnings
   warnings.warn(
       "Direct script usage is deprecated. Use 'cryptic-screen nt' command instead.",
       FutureWarning,
       stacklevel=2
   )
   ```

3. **Document migration path**
   - Show old vs new commands
   - Provide conversion script for existing workflows

## 4. Implementation Steps

### Step 1: Set up package structure
```bash
# Create new package structure
mkdir -p cryptic_screening/{commands,core,utils,data}
touch cryptic_screening/__init__.py
touch cryptic_screening/cli.py

# Copy reference files to package
cp Cryptic_Screening/LinkedPMs.txt cryptic_screening/data/
cp Cryptic_Screening/SinglePMs.txt cryptic_screening/data/
```

### Step 2: Create file resolver utility
```python
# cryptic_screening/utils/file_resolver.py
import os
from pathlib import Path
from typing import Optional, List

def resolve_data_file(
    filename: str,
    explicit_path: Optional[str] = None,
    data_dir: Optional[str] = None,
    check_cwd: bool = True
) -> Path:
    """Resolve a data file path with fallback locations"""
    # Implementation here
```

### Step 3: Create CLI wrapper for NT screening
```python
# cryptic_screening/commands/nt.py
import click
from ..utils.file_resolver import resolve_data_file

@click.command()
@click.option('--input', 'input_dir', required=True, help='Input directory')
@click.option('--output', 'output_file', help='Output file path')
@click.option('--sequences', 'seq_file', help='Custom sequences file')
@click.option('--append-sequences', help='Additional sequences file')
@click.option('--workers', type=int, help='Number of workers')
@click.pass_context
def nt_command(ctx, input_dir, output_file, seq_file, append_sequences, workers):
    """Nucleotide sequence screening"""
    # Wrapper implementation
```

### Step 4: Update setup.py
```python
# setup.py modifications
entry_points={
    'console_scripts': [
        'cryptic-screen=cryptic_screening.cli:cli',
    ],
}
```

## 5. Testing Strategy

### Unit Tests for File Resolution
```python
def test_resolve_data_file_explicit_path():
    """Test that explicit paths are used as-is"""
    
def test_resolve_data_file_fallback_order():
    """Test fallback resolution order"""
    
def test_missing_file_error():
    """Test helpful error when file not found"""
```

### Integration Tests
```python
def test_cli_nt_basic():
    """Test basic NT screening via CLI"""
    
def test_cli_maintains_output_format():
    """Ensure output format unchanged"""
    
def test_backward_compatibility():
    """Test old scripts still work"""
```

## 6. Documentation Plan

### User-Facing Docs
1. **Quick Start Guide** - Simple examples
2. **Migration Guide** - Old to new commands
3. **Configuration Guide** - Config file examples
4. **Command Reference** - All options explained

### Developer Docs
1. **Architecture Overview**
2. **Adding New Commands**
3. **File Resolution Logic**
4. **Testing Guidelines**

## 7. Review Questions

Before proceeding:

1. **Is Click the right choice?** ✓ Using argparse (no new dependencies)
2. **Should we refactor core logic now?** Just wrap it for now
3. **Package name**: `cryptic_screening` (Python convention)
4. **Command name**: ✓ `cryptic-screen` 
5. **Config format**: ✓ YAML (if needed)
6. **Should we support environment variables?** ✓ YES (e.g., `CRYPTIC_SCREEN_DATA_DIR`)

## 8. Success Criteria

The CLI implementation is successful when:

- [ ] All hardcoded file paths are configurable
- [ ] Default behavior matches current scripts exactly
- [ ] Users can specify custom input/output locations
- [ ] Reference files can be in multiple locations
- [ ] Existing scripts continue to work
- [ ] New CLI is documented and tested
- [ ] File not found errors are helpful
- [ ] Configuration files work as expected

## Next Steps

1. **Confirm architectural decisions** (Click vs argparse, package structure)
2. **Create minimal working version** (just NT screening)
3. **Test with real data** to ensure compatibility
4. **Get user feedback** before implementing all commands
5. **Iterate based on feedback**

## Notes

- Start simple: just make files configurable
- Don't break existing workflows
- Test with real data early and often
- Document differences clearly
- Consider performance impact of changes