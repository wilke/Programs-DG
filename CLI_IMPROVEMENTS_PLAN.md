# CLI Improvements Plan for cli-options Branch

## Overview

This plan addresses the current hardcoded file dependencies and creates a flexible, production-ready CLI interface for the Cryptic Screening tools.

## Identified Hardcoded File Issues

### Critical Dependencies

1. **Reference Data Files**
   - `LinkedPMs.txt` - Linked point mutations reference
   - `SinglePMs.txt` - Single point mutations reference
   - Hardcoded fallback: `/mnt/f/SRA/SARS2/Wastewater/`
   - **Solution**: Make configurable with smart defaults

2. **Output Files (No User Control)**
   - `NTSeqScreenResults.tsv` - NT screening results
   - `Linked_PM_*_hits.tsv` / `*_misses.tsv` - PM screening results
   - `NTSeqScreen_report.tsv` - Winnow report
   - **Solution**: Add output directory and filename options

3. **Optional Input Files**
   - `NTSeqScreens.txt` - Custom NT sequences
   - `subscreen.txt` - Specific accessions to screen
   - **Solution**: Make these explicit CLI options

4. **Missing Dependencies**
   - `Meta/SRA_meta.tsv` - Referenced but doesn't exist
   - **Solution**: Make metadata file optional with clear error message

## Proposed CLI Interface Design

### 1. Unified Command Structure

```bash
# Main command
cryptic-screen [OPTIONS] COMMAND [ARGS]

# Subcommands
cryptic-screen nt      # Nucleotide screening (was NTSeqScreenMP.py)
cryptic-screen pm      # Point mutation screening (was PMScreenMP.py)
cryptic-screen winnow  # Filter results (was WinnowScreens.py)
cryptic-screen derep   # Deduplicate sequences (was derep.py)
```

### 2. Global Options (All Commands)

```bash
--config FILE              # Load settings from config file
--data-dir PATH            # Directory containing reference files (default: ./)
--output-dir PATH          # Output directory (default: ./)
--log-level LEVEL          # Logging level (default: INFO)
--log-file FILE            # Log to file instead of stderr
--workers N                # Number of parallel workers (default: CPU count)
--quiet                    # Suppress progress output
--dry-run                  # Validate inputs without processing
--version                  # Show version
--help                     # Show help
```

### 3. Command-Specific Options

#### NT Screening (`cryptic-screen nt`)

```bash
# Required
--input PATH               # Input directory with SAM/BAM/CRAM files

# Optional
--output FILE              # Output file (default: {output-dir}/NTSeqScreenResults.tsv)
--sequences FILE           # Custom NT sequences file (default: built-in sequences)
--append-sequences FILE    # Add sequences from file to built-in (was NTSeqScreens.txt)
--resume                   # Resume from existing results file
--file-pattern PATTERN     # File pattern to match (default: "*.{sam,sam.gz,cram}")
--recursive                # Search subdirectories (default: true)

# Example:
cryptic-screen nt \
  --input /data/samples \
  --output-dir /results \
  --data-dir /refs \
  --append-sequences my_sequences.txt \
  --workers 8
```

#### PM Screening (`cryptic-screen pm`)

```bash
# Required
--input PATH               # Input directory with unique_seqs.tsv files

# Optional
--output-dir PATH          # Output directory for results (default: ./)
--single-pm FILE           # Single PM file (default: {data-dir}/SinglePMs.txt)
--linked-pm FILE           # Linked PM file (default: {data-dir}/LinkedPMs.txt)
--subset FILE              # Screen only specific accessions (was subscreen.txt)
--total-cutoff N           # Total count cutoff (default: 10)
--per-file-cutoff N        # Per-file count cutoff (default: 1)
--file-pattern PATTERN     # Pattern for input files (default: "*_unique_seqs.tsv{,.gz}")
--keep-intermediates       # Keep intermediate hit/miss files

# Example:
cryptic-screen pm \
  --input /data/unique_seqs \
  --output-dir /results/pm_screening \
  --data-dir /refs \
  --subset priority_samples.txt \
  --total-cutoff 5
```

#### Winnow (`cryptic-screen winnow`)

```bash
# Required
--nt-results FILE          # NT results file (from nt command)

# Optional
--pm-dir PATH              # Directory with PM results (default: ./)
--output-dir PATH          # Output directory (default: ./)
--metadata FILE            # SRA metadata file (optional)
--nt-cutoff N              # NT count cutoff (default: 10)
--pm-cutoff N              # PM count cutoff (default: 10)
--output-prefix PREFIX     # Prefix for output files (default: "")

# Example:
cryptic-screen winnow \
  --nt-results /results/NTSeqScreenResults.tsv \
  --pm-dir /results/pm_screening \
  --output-dir /results/reports \
  --metadata /data/sra_metadata.tsv \
  --nt-cutoff 15
```

#### Derep (`cryptic-screen derep`)

```bash
# Already has good CLI, just needs integration
--input FILE               # Input FASTA/FASTQ file
--output FILE              # Output file
--min-count N              # Minimum count (default: 2)
--memory-limit GB          # Memory limit (new)
--chunk-size N             # Process in chunks (new)

# Example:
cryptic-screen derep \
  --input sequences.fastq \
  --output unique_seqs.fasta \
  --min-count 3 \
  --memory-limit 16
```

### 4. Configuration File Support

```yaml
# cryptic-screen.yaml
data_dir: /data/references
output_dir: /results
log_level: INFO
workers: 16

# Command-specific settings
nt:
  file_pattern: "*.{sam,bam,cram}"
  sequences_file: /data/custom_sequences.txt
  
pm:
  single_pm: /data/references/SinglePMs_v2.txt
  linked_pm: /data/references/LinkedPMs_v2.txt
  total_cutoff: 5
  per_file_cutoff: 1

winnow:
  metadata: /data/metadata/sra_meta_2024.tsv
  nt_cutoff: 20
  pm_cutoff: 10
```

Usage:
```bash
cryptic-screen --config production.yaml nt --input /data/samples
```

### 5. Default File Resolution Logic

```python
def resolve_file_path(filename, data_dir=None, check_cwd=True):
    """
    Smart file resolution with fallbacks:
    1. If absolute path, use as-is
    2. Check in specified data_dir
    3. Check in current working directory
    4. Check in package data directory
    5. Check in ~/.cryptic-screening/data/
    """
    search_paths = []
    
    if os.path.isabs(filename):
        return filename
    
    if data_dir:
        search_paths.append(os.path.join(data_dir, filename))
    
    if check_cwd:
        search_paths.append(filename)
        
    # Package data
    search_paths.append(pkg_resources.resource_filename('cryptic_screening', f'data/{filename}'))
    
    # User home directory
    search_paths.append(os.path.expanduser(f'~/.cryptic-screening/data/{filename}'))
    
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError(f"Could not find {filename} in any of: {search_paths}")
```

## Implementation Steps

### Phase 1: Basic CLI Structure (Week 1)

1. **Create main CLI entry point**
   ```python
   # src/cli.py
   import click
   
   @click.group()
   @click.option('--config', type=click.Path(exists=True))
   @click.option('--data-dir', type=click.Path(exists=True))
   @click.option('--output-dir', type=click.Path())
   @click.option('--log-level', default='INFO')
   @click.option('--workers', type=int)
   @click.pass_context
   def cli(ctx, config, data_dir, output_dir, log_level, workers):
       """Cryptic Screening Tools - Production-ready CLI"""
       ctx.ensure_object(dict)
       ctx.obj['config'] = load_config(config)
       # ... setup logging, etc.
   ```

2. **Wrap existing functionality**
   - Create wrapper functions that call existing code
   - Map CLI arguments to existing function parameters
   - Handle file resolution and validation

3. **Add validation**
   - Check input files exist
   - Validate reference files are accessible
   - Ensure output directories are writable

### Phase 2: File Management Improvements (Week 1-2)

1. **Replace hardcoded paths**
   - Add parameters for all file inputs/outputs
   - Implement smart default resolution
   - Remove `/mnt/f/` hardcoded paths

2. **Output organization**
   ```
   output_dir/
   ├── nt_screening/
   │   └── NTSeqScreenResults.tsv
   ├── pm_screening/
   │   ├── Linked_PM_*/
   │   └── Single_PM_*/
   └── reports/
       ├── NTSeqScreen_report.tsv
       └── PM_reports/
   ```

3. **Progress tracking**
   - Add progress bars for long operations
   - Save intermediate state for resume capability
   - Log file operations clearly

### Phase 3: Testing and Documentation (Week 2)

1. **CLI Tests**
   ```python
   def test_nt_command_with_custom_output():
       runner = CliRunner()
       result = runner.invoke(cli, [
           'nt',
           '--input', 'test_data',
           '--output', 'custom_results.tsv',
           '--dry-run'
       ])
       assert result.exit_code == 0
   ```

2. **Integration tests**
   - Test file resolution logic
   - Verify backward compatibility
   - Test configuration file loading

3. **Documentation**
   - Command help text
   - Usage examples
   - Migration guide from old scripts

## Backward Compatibility

### Wrapper Scripts

Create wrapper scripts that maintain the old interface:

```python
#!/usr/bin/env python
# NTSeqScreenMP.py (compatibility wrapper)
import sys
import warnings
from cryptic_screening.cli import cli

warnings.warn(
    "NTSeqScreenMP.py is deprecated. Use 'cryptic-screen nt' instead.",
    DeprecationWarning
)

# Map old behavior to new CLI
sys.argv = ['cryptic-screen', 'nt', '--input', '.', '--recursive']
cli()
```

### Migration Messages

When users run old scripts, show helpful migration instructions:

```
DEPRECATION WARNING: NTSeqScreenMP.py is deprecated.

To migrate to the new CLI:
  Old: python NTSeqScreenMP.py
  New: cryptic-screen nt --input .

For more options: cryptic-screen nt --help
```

## Review Checklist

Before implementing, ensure:

- [ ] All hardcoded files have CLI options
- [ ] Default behavior matches current scripts
- [ ] File resolution is intuitive and documented
- [ ] Output organization is logical
- [ ] Progress and logging are improved
- [ ] Backward compatibility is maintained
- [ ] Tests cover all file scenarios
- [ ] Documentation includes migration guide

## Benefits of This Approach

1. **Flexibility**: Users control all file locations
2. **Reproducibility**: Config files document exact parameters
3. **Scalability**: Easy to run on different datasets
4. **Maintainability**: Clear separation of concerns
5. **Usability**: Intuitive command structure with helpful defaults
6. **Compatibility**: Existing workflows continue to work