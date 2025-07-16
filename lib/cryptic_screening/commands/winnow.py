"""
Winnow command implementation
"""

import os
import sys
import logging
from pathlib import Path
import shutil
import tempfile
from ..utils import resolve_file_path

def run(args):
    """Run winnow filtering with CLI arguments"""
    logger = logging.getLogger(__name__)
    
    # Resolve NT results file
    nt_results = Path(args.nt_results)
    if not nt_results.exists():
        logger.error(f"NT results file not found: {args.nt_results}")
        sys.exit(1)
    
    # Set PM directory
    pm_dir = Path(args.pm_dir) if args.pm_dir else Path.cwd()
    
    # Set output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Resolve metadata file if provided
    metadata_file = None
    if args.metadata:
        metadata_path = resolve_file_path(args.metadata, args.data_dir, 'CRYPTIC_SCREEN_METADATA', 
                                        check_exists=False)
        if metadata_path.exists():
            metadata_file = str(metadata_path)
        else:
            logger.warning(f"Metadata file not found: {args.metadata} - proceeding without metadata")
    
    if args.dry_run:
        logger.info("DRY RUN - Would process:")
        logger.info(f"  NT results: {nt_results}")
        logger.info(f"  PM directory: {pm_dir}")
        logger.info(f"  Output directory: {output_dir}")
        logger.info(f"  NT cutoff: {args.nt_cutoff}")
        logger.info(f"  PM cutoff: {args.pm_cutoff}")
        if metadata_file:
            logger.info(f"  Metadata: {metadata_file}")
        return
    
    # Add the Cryptic_Screening directory to path
    cryptic_dir = Path(__file__).parent.parent.parent.parent / 'Cryptic_Screening'
    if cryptic_dir.exists():
        sys.path.insert(0, str(cryptic_dir))
    
    # Set up temporary working directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy NT results file
        temp_nt = temp_path / 'NTSeqScreenResults.tsv'
        shutil.copy(str(nt_results), str(temp_nt))
        
        # Create metadata directory structure if metadata exists
        if metadata_file:
            meta_dir = temp_path / 'Meta'
            meta_dir.mkdir(exist_ok=True)
            temp_meta = meta_dir / 'SRA_meta.tsv'
            shutil.copy(str(metadata_file), str(temp_meta))
        
        # Save current directory and environment
        old_cwd = os.getcwd()
        old_env = dict(os.environ)
        
        try:
            # Change to temporary directory
            os.chdir(str(temp_path))
            
            # Set environment variables
            os.environ['NT_COUNT_CUTOFF'] = str(args.nt_cutoff)
            os.environ['PM_COUNT_CUTOFF'] = str(args.pm_cutoff)
            
            # Copy PM hit files from pm_dir
            for file in pm_dir.glob('*_hits.tsv'):
                dst = temp_path / file.name
                shutil.copy(str(file), str(dst))
            
            # Import and run the original script
            try:
                import WinnowScreens
                # The script runs on import
            except Exception as e:
                logger.error(f"Error running WinnowScreens: {e}")
                raise
            
            # Move output files to desired location
            moved_files = 0
            
            # Move NT report
            nt_report = temp_path / 'NTSeqScreen_report.tsv'
            if nt_report.exists():
                dst = output_dir / nt_report.name
                shutil.move(str(nt_report), str(dst))
                moved_files += 1
            
            # Move PM reports
            for file in temp_path.glob('*_report.tsv'):
                if file.name != 'NTSeqScreen_report.tsv':
                    dst = output_dir / file.name
                    shutil.move(str(file), str(dst))
                    moved_files += 1
            
            logger.info(f"Generated {moved_files} report files in: {output_dir}")
            
        finally:
            # Restore environment
            os.chdir(old_cwd)
            os.environ.clear()
            os.environ.update(old_env)