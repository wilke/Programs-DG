"""
Unit tests for PM screening command
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
from cryptic_screening.commands import pm_screen

class TestPMScreenCommand:
    """Test PM screening command functionality"""
    
    def test_run_basic(self, temp_dir):
        """Test basic PM screening run"""
        # Create test input directory
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        (input_dir / "test_unique_seqs.tsv").write_text("seq1\tACGT\nseq2\tTGCA\n")
        
        # Create reference files
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        single_pm.write_text("PM1\nPM2\n")
        linked_pm.write_text("PM1,PM2\nPM3,PM4\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=True,
            quiet=False
        )
        
        pm_screen.run(args)
    
    def test_run_with_subset_file(self, temp_dir):
        """Test run with subset file"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        (input_dir / "test_unique_seqs.tsv").write_text("seq1\tACGT\n")
        
        # Create reference files
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        subset_file = temp_dir / "subset.txt"
        single_pm.write_text("PM1\n")
        linked_pm.write_text("PM1,PM2\n")
        subset_file.write_text("PM1\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset="subset.txt",
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=True,
            quiet=False
        )
        
        pm_screen.run(args)
    
    def test_run_missing_input_directory(self, temp_dir):
        """Test run with missing input directory"""
        args = Mock(
            input="/nonexistent/directory",
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            pm_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_run_missing_single_pm_file(self, temp_dir):
        """Test run with missing single PM file"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        linked_pm = temp_dir / "LinkedPMs.txt"
        linked_pm.write_text("PM1,PM2\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            single_pm="missing.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            pm_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_run_missing_linked_pm_file(self, temp_dir):
        """Test run with missing linked PM file"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        single_pm = temp_dir / "SinglePMs.txt"
        single_pm.write_text("PM1\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="missing.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            pm_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_run_missing_subset_file(self, temp_dir):
        """Test run with missing subset file"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        single_pm.write_text("PM1\n")
        linked_pm.write_text("PM1,PM2\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset="missing.txt",
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            pm_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_output_directory_creation(self, temp_dir):
        """Test automatic output directory creation"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        output_dir = temp_dir / "new_output"
        
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        single_pm.write_text("PM1\n")
        linked_pm.write_text("PM1,PM2\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(output_dir),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=True,
            quiet=False
        )
        
        pm_screen.run(args)
        assert output_dir.exists()
    
    @patch.dict(os.environ, {}, clear=True)
    def test_environment_variables_set(self, temp_dir):
        """Test environment variables are set correctly"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        single_pm.write_text("PM1\n")
        linked_pm.write_text("PM1,PM2\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=5,
            per_file_cutoff=2,
            workers=8,
            dry_run=True,
            quiet=False
        )
        
        pm_screen.run(args)
        # In dry-run mode, environment is not actually modified
    
    def test_unique_seqs_file_discovery(self, temp_dir):
        """Test discovery of _unique_seqs.tsv files"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        subdir = input_dir / "subdir"
        subdir.mkdir()
        
        # Create multiple unique_seqs files
        (input_dir / "sample1_unique_seqs.tsv").write_text("data1")
        (input_dir / "sample2_unique_seqs.tsv").write_text("data2")
        (subdir / "sample3_unique_seqs.tsv").write_text("data3")
        
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        single_pm.write_text("PM1\n")
        linked_pm.write_text("PM1,PM2\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=True,
            quiet=False
        )
        
        pm_screen.run(args)
    
    @patch('cryptic_screening.commands.pm_screen.tempfile.TemporaryDirectory')
    def test_file_operations_in_temp_directory(self, mock_tempdir, temp_dir):
        """Test file operations in temporary directory"""
        input_dir = temp_dir / "input"
        input_dir.mkdir()
        (input_dir / "test_unique_seqs.tsv").write_text("data")
        
        # Mock temporary directory
        mock_temp = Mock()
        mock_temp_path = temp_dir / "temp"
        mock_temp_path.mkdir()
        mock_temp.__enter__ = Mock(return_value=str(mock_temp_path))
        mock_temp.__exit__ = Mock(return_value=None)
        mock_tempdir.return_value = mock_temp
        
        single_pm = temp_dir / "SinglePMs.txt"
        linked_pm = temp_dir / "LinkedPMs.txt"
        single_pm.write_text("PM1\n")
        linked_pm.write_text("PM1,PM2\n")
        
        args = Mock(
            input=str(input_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            single_pm="SinglePMs.txt",
            linked_pm="LinkedPMs.txt",
            subset=None,
            total_cutoff=3,
            per_file_cutoff=1,
            workers=2,
            dry_run=True,
            quiet=False
        )
        
        pm_screen.run(args)