"""
PM screening command implementation
"""

import os
import sys
import logging
from pathlib import Path
import shutil
import tempfile
from ..utils import resolve_file_path

def run(args):
    """Run PM screening with CLI arguments"""
    logger = logging.getLogger(__name__)
    
    # Validate input directory
    input_dir = Path(args.input)
    if not input_dir.exists():
        logger.error(f"Input directory not found: {args.input}")
        sys.exit(1)
    
    # Resolve reference files
    single_pm = resolve_file_path(args.single_pm, args.data_dir, 'CRYPTIC_SCREEN_SINGLE_PM')
    linked_pm = resolve_file_path(args.linked_pm, args.data_dir, 'CRYPTIC_SCREEN_LINKED_PM')
    
    if not single_pm.exists():
        logger.error(f"Single PM file not found: {single_pm}")
        sys.exit(1)
    
    if not linked_pm.exists():
        logger.error(f"Linked PM file not found: {linked_pm}")
        sys.exit(1)
    
    # Handle subset file
    subset_file = None
    if args.subset:
        subset_path = resolve_file_path(args.subset, args.data_dir)
        if subset_path.exists():
            subset_file = str(subset_path)
        else:
            logger.error(f"Subset file not found: {args.subset}")
            sys.exit(1)
    
    # Set output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.dry_run:
        logger.info("DRY RUN - Would process:")
        logger.info(f"  Input: {input_dir}")
        logger.info(f"  Output directory: {output_dir}")
        logger.info(f"  Single PM: {single_pm}")
        logger.info(f"  Linked PM: {linked_pm}")
        logger.info(f"  Total cutoff: {args.total_cutoff}")
        logger.info(f"  Per-file cutoff: {args.per_file_cutoff}")
        logger.info(f"  Workers: {args.workers}")
        if subset_file:
            logger.info(f"  Subset file: {subset_file}")
        return
    
    # Add the Cryptic_Screening directory to path
    cryptic_dir = Path(__file__).parent.parent.parent.parent / 'Cryptic_Screening'
    if cryptic_dir.exists():
        sys.path.insert(0, str(cryptic_dir))
    
    # Set up temporary working directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy reference files to temp directory
        temp_single = temp_path / 'SinglePMs.txt'
        temp_linked = temp_path / 'LinkedPMs.txt'
        shutil.copy(str(single_pm), str(temp_single))
        shutil.copy(str(linked_pm), str(temp_linked))
        
        # Copy subset file if provided
        if subset_file:
            temp_subset = temp_path / 'subscreen.txt'
            shutil.copy(str(subset_file), str(temp_subset))
        
        # Save current directory and environment
        old_cwd = os.getcwd()
        old_env = dict(os.environ)
        
        try:
            # Change to temporary directory
            os.chdir(str(temp_path))
            
            # Set environment variables
            if args.workers:
                os.environ['SCREENING_WORKERS'] = str(args.workers)
            os.environ['PM_TOTAL_CUTOFF'] = str(args.total_cutoff)
            os.environ['PM_PER_FILE_CUTOFF'] = str(args.per_file_cutoff)
            
            # Create symlinks to input files
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    if '_unique_seqs.tsv' in file:
                        src = Path(root) / file
                        dst = temp_path / file
                        if not dst.exists():
                            dst.symlink_to(src)
            
            # Import and run the original script
            try:
                import PMScreenMP
                # The script runs on import
            except Exception as e:
                logger.error(f"Error running PMScreenMP: {e}")
                raise
            
            # Move output files to desired location
            moved_files = 0
            for file in temp_path.iterdir():
                if file.name.endswith('_hits.tsv') or file.name.endswith('_misses.tsv'):
                    dst = output_dir / file.name
                    shutil.move(str(file), str(dst))
                    moved_files += 1
            
            logger.info(f"Moved {moved_files} output files to: {output_dir}")
            
        finally:
            # Restore environment
            os.chdir(old_cwd)
            os.environ.clear()
            os.environ.update(old_env)