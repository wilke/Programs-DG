#!/usr/bin/env python3
"""
Main CLI entry point for cryptic-screen command
"""

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
            config = yaml.safe_load(f) or {}
            logging.info(f"Loaded configuration from {config_file}")
            return config
    except ImportError:
        logging.warning("PyYAML not installed. Install with: pip install pyyaml")
        logging.warning("Config file ignored. Proceeding with command line arguments only.")
        return {}
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration file: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error loading config file: {e}")
        sys.exit(1)

def apply_config_to_args(args, config):
    """Apply configuration values to arguments, with command line taking precedence"""
    if not config:
        return
    
    # Apply global config first
    global_config = config.get('global', {})
    for key, value in global_config.items():
        if hasattr(args, key) and getattr(args, key) is None:
            setattr(args, key, value)
            logging.debug(f"Applied global config: {key}={value}")
    
    # Apply command-specific config
    if args.command and args.command in config:
        for key, value in config.get(args.command, {}).items():
            if hasattr(args, key) and getattr(args, key) is None:
                setattr(args, key, value)
                logging.debug(f"Applied {args.command} config: {key}={value}")

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Setup logging first (so config loading can be logged)
    setup_logging(args)
    
    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info(f"Cryptic Screening Tools v1.0.0")
    logger.info(f"Command: {args.command}")
    
    # Load config file if provided
    config = load_config(args.config)
    
    # Apply config values (command line args override config)
    apply_config_to_args(args, config)
    
    # Log final configuration
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Final configuration:")
        for key, value in vars(args).items():
            if value is not None:
                logger.debug(f"  {key}: {value}")
    
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
        
        logger.info(f"Command '{args.command}' completed successfully")
        
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Error running {args.command}: {e}")
        if args.log_level == 'DEBUG':
            logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == '__main__':
    main()