"""
Unit tests for utils module
"""

import pytest
import os
from pathlib import Path
from cryptic_screening.utils import resolve_file_path

class TestResolveFilePath:
    """Test file path resolution"""
    
    def test_absolute_path(self):
        """Test that absolute paths are returned as-is"""
        abs_path = "/absolute/path/to/file.txt"
        result = resolve_file_path(abs_path, check_exists=False)
        assert result == Path(abs_path)
    
    def test_relative_path_with_base_dir(self, temp_dir):
        """Test relative path resolution with base directory"""
        base_dir = temp_dir
        filename = "test.txt"
        expected = base_dir / filename
        
        # Create the file
        expected.write_text("test")
        
        result = resolve_file_path(filename, base_dir=base_dir)
        assert result == expected
    
    def test_env_var_resolution(self, temp_dir, monkeypatch):
        """Test environment variable resolution"""
        test_file = temp_dir / "env_test.txt"
        test_file.write_text("test")
        
        monkeypatch.setenv("TEST_FILE_PATH", str(test_file))
        
        result = resolve_file_path("dummy.txt", env_var="TEST_FILE_PATH")
        assert result == test_file
    
    def test_current_directory_fallback(self, temp_dir):
        """Test fallback to current working directory"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            test_file = temp_dir / "test.txt"
            test_file.write_text("test")
            
            result = resolve_file_path("test.txt")
            assert result.resolve() == test_file.resolve()
        finally:
            os.chdir(original_cwd)
    
    def test_basename_fallback(self, temp_dir):
        """Test fallback to basename in current directory"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            test_file = temp_dir / "file.txt"
            test_file.write_text("test")
            
            # Try to resolve with a different path
            result = resolve_file_path("subdir/file.txt")
            assert result.resolve() == test_file.resolve()
        finally:
            os.chdir(original_cwd)
    
    def test_file_not_found_warning(self, caplog):
        """Test warning when file not found"""
        result = resolve_file_path("nonexistent.txt", check_exists=True)
        assert "File not found" in caplog.text
        assert result == Path("nonexistent.txt")
    
    def test_no_check_exists(self):
        """Test when check_exists is False"""
        result = resolve_file_path("nonexistent.txt", check_exists=False, search_cwd=False)
        assert result == Path("nonexistent.txt")
    
    def test_search_cwd_disabled(self, temp_dir):
        """Test when search_cwd is False"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            test_file = temp_dir / "test.txt"
            test_file.write_text("test")
            
            result = resolve_file_path("test.txt", search_cwd=False, check_exists=False)
            assert result == Path("test.txt")
        finally:
            os.chdir(original_cwd)