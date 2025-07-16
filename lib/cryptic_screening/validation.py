"""
Input validation utilities for cryptic screening tools
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Union

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Raised when validation fails"""
    pass

def validate_input_directory(path: Union[str, Path], 
                           file_types: Optional[List[str]] = None,
                           recursive: bool = True) -> Path:
    """
    Validate that input directory exists and contains expected files
    
    Args:
        path: Directory path to validate
        file_types: List of expected file extensions (e.g., ['.sam', '.bam'])
        recursive: Whether to search subdirectories
        
    Returns:
        Path object for the validated directory
        
    Raises:
        ValidationError: If validation fails
    """
    dir_path = Path(path)
    
    # Check if path exists
    if not dir_path.exists():
        raise ValidationError(f"Input directory does not exist: {path}")
    
    # Check if it's a directory
    if not dir_path.is_dir():
        raise ValidationError(f"Input path is not a directory: {path}")
    
    # Check if directory is readable
    if not os.access(dir_path, os.R_OK):
        raise ValidationError(f"Input directory is not readable: {path}")
    
    # Check for expected file types if specified
    if file_types:
        file_count = 0
        for ext in file_types:
            pattern = f"*{ext}"
            if recursive:
                file_count += len(list(dir_path.rglob(pattern)))
            else:
                file_count += len(list(dir_path.glob(pattern)))
        
        if file_count == 0:
            types_str = ", ".join(file_types)
            raise ValidationError(
                f"No files with extensions [{types_str}] found in {path}"
            )
    
    return dir_path

def validate_output_file(path: Union[str, Path], 
                        create_parent: bool = True) -> Path:
    """
    Validate output file path and optionally create parent directory
    
    Args:
        path: Output file path
        create_parent: Whether to create parent directory if missing
        
    Returns:
        Path object for the output file
        
    Raises:
        ValidationError: If validation fails
    """
    file_path = Path(path)
    parent_dir = file_path.parent
    
    # Check if parent directory exists
    if not parent_dir.exists():
        if create_parent:
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created output directory: {parent_dir}")
            except Exception as e:
                raise ValidationError(
                    f"Failed to create output directory {parent_dir}: {e}"
                )
        else:
            raise ValidationError(
                f"Output directory does not exist: {parent_dir}"
            )
    
    # Check if parent directory is writable
    if not os.access(parent_dir, os.W_OK):
        raise ValidationError(
            f"Output directory is not writable: {parent_dir}"
        )
    
    # Check if file exists and is writable
    if file_path.exists() and not os.access(file_path, os.W_OK):
        raise ValidationError(
            f"Output file exists but is not writable: {path}"
        )
    
    return file_path

def validate_reference_file(path: Union[str, Path], 
                          name: str = "Reference file") -> Path:
    """
    Validate that a reference file exists and is readable
    
    Args:
        path: Reference file path
        name: Descriptive name for error messages
        
    Returns:
        Path object for the reference file
        
    Raises:
        ValidationError: If validation fails
    """
    file_path = Path(path)
    
    if not file_path.exists():
        raise ValidationError(f"{name} not found: {path}")
    
    if not file_path.is_file():
        raise ValidationError(f"{name} is not a file: {path}")
    
    if not os.access(file_path, os.R_OK):
        raise ValidationError(f"{name} is not readable: {path}")
    
    # Check if file is empty
    if file_path.stat().st_size == 0:
        logger.warning(f"{name} is empty: {path}")
    
    return file_path

def validate_positive_integer(value: Union[int, str], 
                            name: str = "Value",
                            min_value: int = 1) -> int:
    """
    Validate that a value is a positive integer
    
    Args:
        value: Value to validate
        name: Parameter name for error messages
        min_value: Minimum allowed value
        
    Returns:
        Validated integer value
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        int_value = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{name} must be an integer, got: {value}")
    
    if int_value < min_value:
        raise ValidationError(
            f"{name} must be at least {min_value}, got: {int_value}"
        )
    
    return int_value

def validate_file_pattern(pattern: str) -> str:
    """
    Validate file pattern for glob operations
    
    Args:
        pattern: File pattern (e.g., "*.sam")
        
    Returns:
        Validated pattern
        
    Raises:
        ValidationError: If pattern is invalid
    """
    if not pattern:
        raise ValidationError("File pattern cannot be empty")
    
    # Check for common issues
    if pattern.startswith('/'):
        raise ValidationError(
            "File pattern should not start with '/'. "
            "Use relative patterns like '*.sam'"
        )
    
    return pattern

def check_dependencies():
    """Check if required external dependencies are available"""
    issues = []
    
    # Check for PyYAML (optional but recommended)
    try:
        import yaml
    except ImportError:
        issues.append(
            "PyYAML not installed. Configuration files will not work. "
            "Install with: pip install pyyaml"
        )
    
    # Check for external tools if needed
    # This is a placeholder for checking tools like samtools, minimap2, etc.
    # if needed by the wrapped scripts
    
    if issues:
        logger.warning("Optional dependencies missing:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    
    return len(issues) == 0