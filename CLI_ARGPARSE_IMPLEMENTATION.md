# CLI Implementation with argparse

## Overview

This document provides the concrete implementation plan using argparse, environment variables, and current working directory defaults.

## Core Design Principles

1. **Use argparse** - No new dependencies
2. **Environment variables** - All file paths can be set via env vars
3. **Current working directory** - Default for all file operations
4. **Preserve output patterns** - Keep existing file naming patterns
5. **YAML config** - Optional configuration file support

## Environment Variables

All file paths can be configured via environment variables:

```bash
# Data directories
export CRYPTIC_SCREEN_DATA_DIR="./data"          # Reference files location
export CRYPTIC_SCREEN_OUTPUT_DIR="./"            # Output files location
export CRYPTIC_SCREEN_WORK_DIR="./"              # Working directory

# Reference files
export CRYPTIC_SCREEN_LINKED_PM="LinkedPMs.txt"  # Linked PM file
export CRYPTIC_SCREEN_SINGLE_PM="SinglePMs.txt"  # Single PM file
export CRYPTIC_SCREEN_METADATA="metadata.tsv"    # Metadata file

# Runtime options
export CRYPTIC_SCREEN_WORKERS="8"                # Number of workers
export CRYPTIC_SCREEN_LOG_LEVEL="INFO"           # Logging level
```

## Implementation Structure

### 1. Main CLI Entry Point

```python
#!/usr/bin/env python3
# cryptic_screen_cli.py

import argparse
import os
import sys
import logging
from pathlib import Path

def get_env_or_default(env_var, default=None, type_func=str):
    """Get environment variable with type conversion"""
    value = os.environ.get(env_var, default)
    if value is not None and type_func != str:
        try:
            return type_func(value)
        except ValueError:
            logging.warning(f"Invalid value for {env_var}: {value}, using default: {default}")
            return type_func(default) if default else None
    return value

def resolve_file_path(filename, base_dir=None, env_var=None, check_exists=True):
    """
    Resolve file path with the following priority:
    1. If absolute path, use as-is
    2. If env_var set, use that
    3. If base_dir set, join with filename
    4. Use current working directory
    """
    # Check environment variable first
    if env_var:
        env_value = os.environ.get(env_var)
        if env_value:
            filename = env_value
    
    # If absolute path, return as-is
    if os.path.isabs(filename):
        path = Path(filename)
    else:
        # Use base_dir or current working directory
        base = Path(base_dir) if base_dir else Path.cwd()
        path = base / filename
    
    # Check existence if required
    if check_exists and not path.exists():
        logging.warning(f"File not found: {path}")
        # Try current working directory as fallback
        cwd_path = Path.cwd() / Path(filename).name
        if cwd_path.exists():
            logging.info(f"Found in current directory: {cwd_path}")
            return cwd_path
    
    return path

def setup_logging(args):
    """Configure logging based on arguments and environment"""
    log_level = args.log_level or get_env_or_default('CRYPTIC_SCREEN_LOG_LEVEL', 'INFO')
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logging.getLogger().addHandler(file_handler)

def add_common_arguments(parser):
    """Add arguments common to all subcommands"""
    parser.add_argument('--data-dir', 
                       default=get_env_or_default('CRYPTIC_SCREEN_DATA_DIR', './'),
                       help='Directory containing reference files (default: current directory)')
    parser.add_argument('--output-dir', 
                       default=get_env_or_default('CRYPTIC_SCREEN_OUTPUT_DIR', './'),
                       help='Output directory (default: current directory)')
    parser.add_argument('--workers', type=int,
                       default=get_env_or_default('CRYPTIC_SCREEN_WORKERS', os.cpu_count(), int),
                       help='Number of parallel workers')
    parser.add_argument('--log-level', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    parser.add_argument('--log-file', help='Log to file instead of stderr')
    parser.add_argument('--config', help='Configuration file (YAML)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Validate inputs without processing')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress output')

def create_parser():
    """Create the main argument parser with subcommands"""
    parser = argparse.ArgumentParser(
        prog='cryptic-screen',
        description='Cryptic Screening Tools - Production-ready CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  CRYPTIC_SCREEN_DATA_DIR     Default data directory for reference files
  CRYPTIC_SCREEN_OUTPUT_DIR   Default output directory
  CRYPTIC_SCREEN_WORKERS      Default number of workers
  CRYPTIC_SCREEN_LOG_LEVEL    Default logging level
  CRYPTIC_SCREEN_LINKED_PM    Default linked PM file name
  CRYPTIC_SCREEN_SINGLE_PM    Default single PM file name
  CRYPTIC_SCREEN_METADATA     Default metadata file name

Examples:
  %(prog)s nt --input ./samples --output results.tsv
  %(prog)s pm --input ./unique_seqs --output-dir ./results
  %(prog)s winnow --nt-results results.tsv --output-dir ./reports
        """
    )
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # NT screening subcommand
    nt_parser = subparsers.add_parser('nt', help='Nucleotide sequence screening')
    add_common_arguments(nt_parser)
    nt_parser.add_argument('--input', required=True,
                          help='Input directory with SAM/BAM/CRAM files')
    nt_parser.add_argument('--output',
                          help='Output file (default: OUTPUT_DIR/NTSeqScreenResults.tsv)')
    nt_parser.add_argument('--sequences',
                          help='Custom NT sequences file (replaces built-in)')
    nt_parser.add_argument('--append-sequences',
                          help='Additional sequences file (adds to built-in)')
    nt_parser.add_argument('--resume', action='store_true',
                          help='Resume from existing results file')
    nt_parser.add_argument('--file-pattern', default='*.{sam,sam.gz,cram}',
                          help='File pattern to match')
    nt_parser.add_argument('--recursive', action='store_true', default=True,
                          help='Search subdirectories (default: True)')
    
    # PM screening subcommand
    pm_parser = subparsers.add_parser('pm', help='Point mutation screening')
    add_common_arguments(pm_parser)
    pm_parser.add_argument('--input', required=True,
                          help='Input directory with unique_seqs.tsv files')
    pm_parser.add_argument('--single-pm',
                          default=get_env_or_default('CRYPTIC_SCREEN_SINGLE_PM', 'SinglePMs.txt'),
                          help='Single PM file (default: DATA_DIR/SinglePMs.txt)')
    pm_parser.add_argument('--linked-pm',
                          default=get_env_or_default('CRYPTIC_SCREEN_LINKED_PM', 'LinkedPMs.txt'),
                          help='Linked PM file (default: DATA_DIR/LinkedPMs.txt)')
    pm_parser.add_argument('--subset',
                          help='Screen only specific accessions (file path)')
    pm_parser.add_argument('--total-cutoff', type=int, default=10,
                          help='Total count cutoff (default: 10)')
    pm_parser.add_argument('--per-file-cutoff', type=int, default=1,
                          help='Per-file count cutoff (default: 1)')
    pm_parser.add_argument('--file-pattern', default='*_unique_seqs.tsv{,.gz}',
                          help='Pattern for input files')
    
    # Winnow subcommand
    winnow_parser = subparsers.add_parser('winnow', help='Filter and report results')
    add_common_arguments(winnow_parser)
    winnow_parser.add_argument('--nt-results', required=True,
                              help='NT results file (from nt command)')
    winnow_parser.add_argument('--pm-dir',
                              help='Directory with PM results (default: current directory)')
    winnow_parser.add_argument('--metadata',
                              default=get_env_or_default('CRYPTIC_SCREEN_METADATA'),
                              help='SRA metadata file (optional)')
    winnow_parser.add_argument('--nt-cutoff', type=int, default=10,
                              help='NT count cutoff (default: 10)')
    winnow_parser.add_argument('--pm-cutoff', type=int, default=10,
                              help='PM count cutoff (default: 10)')
    
    # Derep subcommand
    derep_parser = subparsers.add_parser('derep', help='Deduplicate sequences')
    add_common_arguments(derep_parser)
    derep_parser.add_argument('input', type=argparse.FileType('r'),
                             help='Input FASTA/FASTQ file')
    derep_parser.add_argument('output', type=argparse.FileType('w'),
                             help='Output file')
    derep_parser.add_argument('--min-count', type=int, default=2,
                             help='Minimum count (default: 2)')
    derep_parser.add_argument('--memory-limit', type=int,
                             help='Memory limit in GB')
    
    return parser

def load_config(config_file):
    """Load configuration from YAML file"""
    if not config_file:
        return {}
    
    try:
        import yaml
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except ImportError:
        logging.warning("PyYAML not installed, config file ignored")
        return {}
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return {}

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Setup logging
    setup_logging(args)
    
    # Load config file if provided
    config = load_config(args.config)
    
    # Apply config values (command line args override config)
    for key, value in config.get(args.command, {}).items():
        if hasattr(args, key) and getattr(args, key) is None:
            setattr(args, key, value)
    
    # Log configuration
    logging.info(f"Running command: {args.command}")
    logging.debug(f"Arguments: {args}")
    
    # Import and run the appropriate command
    try:
        if args.command == 'nt':
            from .commands import nt_screen
            nt_screen.run(args)
        elif args.command == 'pm':
            from .commands import pm_screen
            pm_screen.run(args)
        elif args.command == 'winnow':
            from .commands import winnow
            winnow.run(args)
        elif args.command == 'derep':
            from .commands import derep
            derep.run(args)
    except Exception as e:
        logging.error(f"Error running {args.command}: {e}")
        if args.log_level == 'DEBUG':
            raise
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### 2. NT Command Wrapper

```python
# cryptic_screening/commands/nt_screen.py

import os
import sys
import logging
from pathlib import Path
from ..utils import resolve_file_path

# Add the Cryptic_Screening directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'Cryptic_Screening'))

def run(args):
    """Run NT screening with CLI arguments"""
    logger = logging.getLogger(__name__)
    
    # Resolve file paths
    output_file = args.output
    if not output_file:
        output_file = Path(args.output_dir) / 'NTSeqScreenResults.tsv'
    else:
        output_file = Path(output_file)
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Handle sequence files
    custom_sequences = None
    append_sequences = None
    
    if args.sequences:
        seq_path = resolve_file_path(args.sequences, args.data_dir)
        if seq_path.exists():
            custom_sequences = str(seq_path)
        else:
            logger.error(f"Sequences file not found: {args.sequences}")
            sys.exit(1)
    
    if args.append_sequences:
        append_path = resolve_file_path(args.append_sequences, args.data_dir)
        if append_path.exists():
            append_sequences = str(append_path)
        else:
            logger.error(f"Append sequences file not found: {args.append_sequences}")
            sys.exit(1)
    
    # Validate input directory
    input_dir = Path(args.input)
    if not input_dir.exists():
        logger.error(f"Input directory not found: {args.input}")
        sys.exit(1)
    
    if args.dry_run:
        logger.info("DRY RUN - Would process:")
        logger.info(f"  Input: {input_dir}")
        logger.info(f"  Output: {output_file}")
        logger.info(f"  Workers: {args.workers}")
        if custom_sequences:
            logger.info(f"  Custom sequences: {custom_sequences}")
        if append_sequences:
            logger.info(f"  Append sequences: {append_sequences}")
        return
    
    # Temporarily modify behavior of NTSeqScreenMP
    # This is a wrapper approach - later we'll refactor the core code
    
    # Set up temporary environment for the script
    old_cwd = os.getcwd()
    temp_env = {}
    
    try:
        # Change to input directory (NTSeqScreenMP expects this)
        os.chdir(str(input_dir))
        
        # Create temporary output file in current directory
        temp_output = Path('NTSeqScreenResults.tsv')
        
        # If resuming, copy existing results
        if args.resume and output_file.exists():
            import shutil
            shutil.copy(str(output_file), str(temp_output))
        
        # Handle append sequences by creating temporary NTSeqScreens.txt
        if append_sequences:
            with open('NTSeqScreens.txt', 'w') as f:
                with open(append_sequences, 'r') as src:
                    f.write(src.read())
        
        # Set worker count via environment variable
        temp_env['SCREENING_WORKERS'] = str(args.workers)
        os.environ.update(temp_env)
        
        # Import and run the original script
        import NTSeqScreenMP
        # The script runs on import
        
        # Move output to desired location
        if temp_output.exists():
            import shutil
            shutil.move(str(temp_output), str(output_file))
            logger.info(f"Results written to: {output_file}")
        
    finally:
        # Restore environment
        os.chdir(old_cwd)
        for key in temp_env:
            os.environ.pop(key, None)
        
        # Clean up temporary files
        if append_sequences and Path('NTSeqScreens.txt').exists():
            Path('NTSeqScreens.txt').unlink()
```

### 3. File Resolution Utility

```python
# cryptic_screening/utils.py

import os
import logging
from pathlib import Path
from typing import Optional, Union

def resolve_file_path(
    filename: Union[str, Path],
    base_dir: Optional[Union[str, Path]] = None,
    env_var: Optional[str] = None,
    check_exists: bool = True,
    search_cwd: bool = True
) -> Path:
    """
    Resolve a file path with the following priority:
    1. If absolute path, use as-is
    2. Environment variable (if env_var specified)
    3. base_dir / filename
    4. Current working directory / filename
    5. Current working directory / basename(filename)
    
    Args:
        filename: File name or path
        base_dir: Base directory to search in
        env_var: Environment variable to check
        check_exists: Whether to verify file exists
        search_cwd: Whether to search current working directory
    
    Returns:
        Path object (may not exist if check_exists=False)
    """
    logger = logging.getLogger(__name__)
    
    # Check environment variable first
    if env_var and env_var in os.environ:
        filename = os.environ[env_var]
        logger.debug(f"Using {env_var}={filename}")
    
    path = Path(filename)
    
    # If absolute path, return as-is
    if path.is_absolute():
        if check_exists and not path.exists():
            logger.warning(f"File not found: {path}")
        return path
    
    # Try with base_dir
    if base_dir:
        candidate = Path(base_dir) / path
        if not check_exists or candidate.exists():
            return candidate
    
    # Try current working directory
    if search_cwd:
        # First try full path in cwd
        candidate = Path.cwd() / path
        if not check_exists or candidate.exists():
            return candidate
        
        # Then try just filename in cwd
        candidate = Path.cwd() / path.name
        if not check_exists or candidate.exists():
            return candidate
    
    # Return original path if nothing found
    if check_exists:
        logger.warning(f"File not found in any location: {filename}")
    
    return path
```

### 4. Configuration File Format

```yaml
# cryptic-screen.yaml
# Global settings
data_dir: /data/references
output_dir: /results
workers: 16
log_level: INFO

# Command-specific settings
nt:
  file_pattern: "*.{sam,bam,cram}"
  append_sequences: /data/custom_sequences.txt
  recursive: true

pm:
  single_pm: SinglePMs_v2.txt
  linked_pm: LinkedPMs_v2.txt
  total_cutoff: 5
  per_file_cutoff: 1
  file_pattern: "*_unique_seqs.tsv{,.gz}"

winnow:
  metadata: /data/metadata/sra_meta_2024.tsv
  nt_cutoff: 20
  pm_cutoff: 10
  
derep:
  min_count: 3
  memory_limit: 16
```

### 5. Setup.py Entry Point

```python
# setup.py additions
setup(
    name='cryptic-screening',
    # ... other settings ...
    entry_points={
        'console_scripts': [
            'cryptic-screen=cryptic_screening.cli:main',
        ],
    },
    package_data={
        'cryptic_screening': [
            'data/LinkedPMs.txt',
            'data/SinglePMs.txt',
        ],
    },
)
```

### 6. Backward Compatibility Wrapper

```python
#!/usr/bin/env python3
# bin/NTSeqScreenMP.py - Compatibility wrapper

import sys
import warnings
import subprocess
from pathlib import Path

warnings.warn(
    "NTSeqScreenMP.py is deprecated. Use 'cryptic-screen nt' instead.\n"
    "Example: cryptic-screen nt --input . --output NTSeqScreenResults.tsv",
    DeprecationWarning,
    stacklevel=2
)

# Run the original script
original_script = Path(__file__).parent.parent / 'Cryptic_Screening' / 'NTSeqScreenMP.py'
subprocess.run([sys.executable, str(original_script)] + sys.argv[1:])
```

## Testing the Implementation

### Basic Usage Examples

```bash
# NT screening with defaults (current directory)
cryptic-screen nt --input .

# NT screening with custom output
cryptic-screen nt --input /data/samples --output /results/nt_results.tsv

# PM screening with environment variables
export CRYPTIC_SCREEN_DATA_DIR=/refs
export CRYPTIC_SCREEN_OUTPUT_DIR=/results
cryptic-screen pm --input /data/unique_seqs

# Winnow with config file
cryptic-screen --config production.yaml winnow --nt-results results.tsv

# Dry run to validate
cryptic-screen nt --input /data/samples --dry-run

# Increased verbosity
cryptic-screen --log-level DEBUG nt --input .
```

### Environment Variable Usage

```bash
# Set all defaults via environment
export CRYPTIC_SCREEN_DATA_DIR=/data/references
export CRYPTIC_SCREEN_OUTPUT_DIR=/results
export CRYPTIC_SCREEN_WORKERS=32
export CRYPTIC_SCREEN_LOG_LEVEL=DEBUG
export CRYPTIC_SCREEN_LINKED_PM=LinkedPMs_v2.txt
export CRYPTIC_SCREEN_SINGLE_PM=SinglePMs_v2.txt

# Now commands use these defaults
cryptic-screen pm --input /data/unique_seqs
```

## Next Steps

1. **Implement the CLI wrapper** without modifying original scripts
2. **Test with real data** to ensure compatibility
3. **Add validation and error handling**
4. **Create documentation and examples**
5. **Gradually refactor core logic** in future phases