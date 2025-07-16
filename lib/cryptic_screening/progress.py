"""
Progress indicator utilities for long-running operations
"""

import sys
import time
import logging
from pathlib import Path
from typing import Optional, Iterator, Any

class ProgressIndicator:
    """Simple progress indicator for command line operations"""
    
    def __init__(self, total: Optional[int] = None, desc: str = "Processing", 
                 quiet: bool = False, logger: Optional[logging.Logger] = None):
        self.total = total
        self.desc = desc
        self.quiet = quiet
        self.logger = logger or logging.getLogger(__name__)
        self.current = 0
        self.start_time = time.time()
        self.last_update = 0
        
    def update(self, n: int = 1) -> None:
        """Update progress by n items"""
        if self.quiet:
            return
            
        self.current += n
        current_time = time.time()
        
        # Update at most once per second
        if current_time - self.last_update < 1.0:
            return
            
        self.last_update = current_time
        elapsed = current_time - self.start_time
        
        if self.total:
            percent = (self.current / self.total) * 100
            rate = self.current / elapsed if elapsed > 0 else 0
            eta = (self.total - self.current) / rate if rate > 0 else 0
            
            msg = f"\r{self.desc}: {self.current}/{self.total} ({percent:.1f}%) - " \
                  f"{rate:.1f} items/s - ETA: {eta:.0f}s"
        else:
            rate = self.current / elapsed if elapsed > 0 else 0
            msg = f"\r{self.desc}: {self.current} items - {rate:.1f} items/s"
        
        # Clear line and write progress
        sys.stderr.write('\r' + ' ' * 80 + '\r')
        sys.stderr.write(msg)
        sys.stderr.flush()
    
    def finish(self) -> None:
        """Complete the progress indicator"""
        if self.quiet:
            return
            
        elapsed = time.time() - self.start_time
        rate = self.current / elapsed if elapsed > 0 else 0
        
        msg = f"\r{self.desc}: Completed {self.current} items in {elapsed:.1f}s " \
              f"({rate:.1f} items/s)\n"
        
        sys.stderr.write('\r' + ' ' * 80 + '\r')
        sys.stderr.write(msg)
        sys.stderr.flush()
        
        self.logger.info(f"{self.desc} completed: {self.current} items in {elapsed:.1f}s")

def track_progress(items: Iterator[Any], total: Optional[int] = None, 
                  desc: str = "Processing", quiet: bool = False) -> Iterator[Any]:
    """
    Wrap an iterator with progress tracking
    
    Example:
        for file in track_progress(files, total=len(files), desc="Screening files"):
            process_file(file)
    """
    progress = ProgressIndicator(total=total, desc=desc, quiet=quiet)
    
    try:
        for item in items:
            yield item
            progress.update()
    finally:
        progress.finish()

def count_files(path: Path, pattern: str = "*") -> int:
    """Count files matching pattern for progress tracking"""
    if path.is_file():
        return 1
    
    count = 0
    for item in path.rglob(pattern):
        if item.is_file():
            count += 1
    
    return count

class FileScanner:
    """Scan for files with progress indication"""
    
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.logger = logging.getLogger(__name__)
    
    def scan_files(self, directory: Path, pattern: str = "*", 
                   recursive: bool = True) -> list[Path]:
        """Scan directory for files matching pattern with progress"""
        if not self.quiet:
            self.logger.info(f"Scanning {directory} for files matching '{pattern}'...")
        
        files = []
        if recursive:
            file_iter = directory.rglob(pattern)
        else:
            file_iter = directory.glob(pattern)
        
        # Convert to list to get count
        all_files = [f for f in file_iter if f.is_file()]
        
        if not self.quiet:
            self.logger.info(f"Found {len(all_files)} files")
        
        return all_files