"""
Unit tests for progress module
"""

import pytest
import time
from pathlib import Path
from cryptic_screening.progress import (
    ProgressIndicator,
    track_progress,
    count_files,
    FileScanner
)

class TestProgressIndicator:
    """Test ProgressIndicator class"""
    
    def test_progress_indicator_creation(self):
        """Test creating a progress indicator"""
        progress = ProgressIndicator(total=100, desc="Testing")
        assert progress.total == 100
        assert progress.desc == "Testing"
        assert progress.current == 0
    
    def test_progress_update(self):
        """Test updating progress"""
        progress = ProgressIndicator(total=10, quiet=True)
        progress.update(1)
        assert progress.current == 1
        
        progress.update(5)
        assert progress.current == 6
    
    def test_progress_finish(self):
        """Test finishing progress"""
        progress = ProgressIndicator(total=10, quiet=True)
        progress.update(10)
        progress.finish()
        assert progress.current == 10
    
    def test_progress_without_total(self):
        """Test progress indicator without total"""
        progress = ProgressIndicator(desc="Processing", quiet=True)
        progress.update(5)
        assert progress.current == 5
    
    def test_quiet_mode(self, capsys):
        """Test quiet mode suppresses output"""
        progress = ProgressIndicator(total=10, quiet=True)
        progress.update(5)
        progress.finish()
        
        captured = capsys.readouterr()
        assert captured.err == ""  # No output to stderr

class TestTrackProgress:
    """Test track_progress function"""
    
    def test_track_progress_iterator(self):
        """Test tracking progress through iterator"""
        items = list(range(5))
        result = []
        
        for item in track_progress(items, total=len(items), quiet=True):
            result.append(item)
        
        assert result == items
    
    def test_track_progress_generator(self):
        """Test tracking progress with generator"""
        def item_generator():
            for i in range(3):
                yield i
        
        result = list(track_progress(item_generator(), quiet=True))
        assert result == [0, 1, 2]

class TestCountFiles:
    """Test count_files function"""
    
    def test_count_files_in_directory(self, temp_dir):
        """Test counting files in directory"""
        # Create test files
        (temp_dir / "file1.txt").write_text("test")
        (temp_dir / "file2.txt").write_text("test")
        (temp_dir / "file3.log").write_text("test")
        
        assert count_files(temp_dir) == 3
        assert count_files(temp_dir, "*.txt") == 2
    
    def test_count_single_file(self, temp_dir):
        """Test counting when path is a file"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")
        
        assert count_files(test_file) == 1
    
    def test_count_files_recursive(self, temp_dir):
        """Test recursive file counting"""
        # Create nested structure
        (temp_dir / "file1.txt").write_text("test")
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("test")
        
        assert count_files(temp_dir, "*.txt") == 2

class TestFileScanner:
    """Test FileScanner class"""
    
    def test_scan_files_basic(self, temp_dir):
        """Test basic file scanning"""
        # Create test files
        (temp_dir / "file1.txt").write_text("test")
        (temp_dir / "file2.txt").write_text("test")
        (temp_dir / "file3.log").write_text("test")
        
        scanner = FileScanner(quiet=True)
        files = scanner.scan_files(temp_dir, "*.txt")
        
        assert len(files) == 2
        assert all(f.suffix == ".txt" for f in files)
    
    def test_scan_files_recursive(self, temp_dir):
        """Test recursive file scanning"""
        # Create nested structure
        (temp_dir / "file1.txt").write_text("test")
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("test")
        
        scanner = FileScanner(quiet=True)
        files = scanner.scan_files(temp_dir, "*.txt", recursive=True)
        assert len(files) == 2
    
    def test_scan_files_non_recursive(self, temp_dir):
        """Test non-recursive file scanning"""
        # Create nested structure
        (temp_dir / "file1.txt").write_text("test")
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("test")
        
        scanner = FileScanner(quiet=True)
        files = scanner.scan_files(temp_dir, "*.txt", recursive=False)
        assert len(files) == 1