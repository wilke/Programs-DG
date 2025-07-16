"""
Derep command implementation
"""

import os
import sys
import logging
from pathlib import Path

def run(args):
    """Run derep with CLI arguments"""
    logger = logging.getLogger(__name__)
    
    # The derep.py script already has good CLI handling
    # We just need to call it with the right arguments
    
    if args.dry_run:
        logger.info("DRY RUN - Would process:")
        logger.info(f"  Input: {args.input.name}")
        logger.info(f"  Output: {args.output.name}")
        logger.info(f"  Min count: {args.min_count}")
        if args.memory_limit:
            logger.info(f"  Memory limit: {args.memory_limit}GB")
        return
    
    # Close the file handles opened by argparse
    args.input.close()
    args.output.close()
    
    # Add the parent directory to path for derep.py import
    programs_dir = Path(__file__).parent.parent.parent.parent
    if programs_dir.exists():
        sys.path.insert(0, str(programs_dir))
    
    # Prepare arguments for derep.py
    derep_args = [
        'derep.py',
        args.input.name,
        args.output.name,
        str(args.min_count)
    ]
    
    # Save original sys.argv
    old_argv = sys.argv
    
    try:
        # Set sys.argv for derep.py
        sys.argv = derep_args
        
        # Import and run derep
        import derep
        # The script runs on import/execution
        
        logger.info(f"Deduplication complete: {args.output.name}")
        
    except Exception as e:
        logger.error(f"Error running derep: {e}")
        raise
    finally:
        # Restore sys.argv
        sys.argv = old_argv