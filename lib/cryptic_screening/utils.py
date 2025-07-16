"""
Utility functions for cryptic screening CLI
"""

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