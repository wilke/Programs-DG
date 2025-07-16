"""
NT screening command implementation
"""

import os
import sys
import logging
from pathlib import Path
import shutil
import tempfile
from ..utils import resolve_file_path

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
    
    # Add the Cryptic_Screening directory to path for imports
    cryptic_dir = Path(__file__).parent.parent.parent.parent / 'Cryptic_Screening'
    if cryptic_dir.exists():
        sys.path.insert(0, str(cryptic_dir))
    
    # Set up temporary working directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy existing results if resuming
        temp_output = temp_path / 'NTSeqScreenResults.tsv'
        if args.resume and output_file.exists():
            shutil.copy(str(output_file), str(temp_output))
            logger.info(f"Resuming from existing results: {output_file}")
        
        # Create append sequences file if needed
        if append_sequences:
            temp_append = temp_path / 'NTSeqScreens.txt'
            shutil.copy(str(append_sequences), str(temp_append))
        
        # Save current directory and environment
        old_cwd = os.getcwd()
        old_env = dict(os.environ)
        
        try:
            # Change to temporary directory
            os.chdir(str(temp_path))
            
            # Set worker count via environment variable
            if args.workers:
                os.environ['SCREENING_WORKERS'] = str(args.workers)
            
            # Create symlinks to input files
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in ['.sam', '.sam.gz', '.cram']):
                        src = Path(root) / file
                        dst = temp_path / file
                        if not dst.exists():
                            dst.symlink_to(src)
            
            # Import and run the original script
            try:
                import NTSeqScreenMP
                # The script runs on import
            except Exception as e:
                logger.error(f"Error running NTSeqScreenMP: {e}")
                raise
            
            # Move output to desired location
            if temp_output.exists():
                shutil.move(str(temp_output), str(output_file))
                logger.info(f"Results written to: {output_file}")
            else:
                logger.warning("No output file generated")
            
        finally:
            # Restore environment
            os.chdir(old_cwd)
            os.environ.clear()
            os.environ.update(old_env)