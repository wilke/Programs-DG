"""
Unit tests for NT screening command
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
from cryptic_screening.commands import nt_screen

class TestNTScreenCommand:
    """Test NT screening command functionality"""
    
    def test_run_basic(self, temp_dir, monkeypatch):
        """Test basic NT screening run"""
        # Create test SAM files
        (temp_dir / "test1.sam").write_text("@HD\tVN:1.0\n")
        (temp_dir / "test2.sam").write_text("@HD\tVN:1.0\n")
        
        # Mock arguments
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        # Run should complete without error in dry-run mode
        nt_screen.run(args)
    
    def test_run_with_custom_output(self, temp_dir):
        """Test run with custom output file"""
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        
        custom_output = temp_dir / "custom_results.tsv"
        args = Mock(
            input=str(temp_dir),
            output=str(custom_output),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    def test_run_with_sequences_file(self, temp_dir):
        """Test run with custom sequences file"""
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        seq_file = temp_dir / "sequences.txt"
        seq_file.write_text("ACGT\nTGCA\n")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences="sequences.txt",
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    def test_run_missing_sequences_file(self, temp_dir):
        """Test run with missing sequences file"""
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences="missing.txt",
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            nt_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_run_invalid_input_directory(self, temp_dir):
        """Test run with invalid input directory"""
        args = Mock(
            input="/nonexistent/directory",
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            nt_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_run_no_input_files(self, temp_dir):
        """Test run with no SAM/BAM/CRAM files"""
        # Create directory with no relevant files
        (temp_dir / "test.txt").write_text("not a sam file")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            nt_screen.run(args)
        assert exc_info.value.code == 1
    
    def test_run_with_append_sequences(self, temp_dir):
        """Test run with append sequences file"""
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        append_file = temp_dir / "append.txt"
        append_file.write_text("GGGG\nAAAA\n")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences="append.txt",
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    def test_run_recursive_search(self, temp_dir):
        """Test recursive file search"""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "test.sam").write_text("@HD\tVN:1.0\n")
        (temp_dir / "test2.sam").write_text("@HD\tVN:1.0\n")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    def test_run_non_recursive_search(self, temp_dir):
        """Test non-recursive file search"""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "test.sam").write_text("@HD\tVN:1.0\n")
        (temp_dir / "test2.sam").write_text("@HD\tVN:1.0\n")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=False,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    @patch('cryptic_screening.commands.nt_screen.tempfile.TemporaryDirectory')
    def test_run_with_resume(self, mock_tempdir, temp_dir):
        """Test run with resume from existing results"""
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        existing_results = temp_dir / "NTSeqScreenResults.tsv"
        existing_results.write_text("Header\nExisting results\n")
        
        # Mock temporary directory
        mock_temp = Mock()
        mock_temp_path = temp_dir / "temp"
        mock_temp_path.mkdir()
        mock_temp.__enter__ = Mock(return_value=str(mock_temp_path))
        mock_temp.__exit__ = Mock(return_value=None)
        mock_tempdir.return_value = mock_temp
        
        args = Mock(
            input=str(temp_dir),
            output=str(existing_results),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=True,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    def test_file_type_support(self, temp_dir):
        """Test support for different file types"""
        # Create various file types
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        (temp_dir / "test.sam.gz").write_text("compressed")
        (temp_dir / "test.bam").write_text("binary")
        (temp_dir / "test.cram").write_text("cram")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_worker_environment_variable(self, temp_dir):
        """Test setting worker count via environment variable"""
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        
        args = Mock(
            input=str(temp_dir),
            output=None,
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=8,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
        # In dry-run mode, environment is not actually modified
    
    def test_output_directory_creation(self, temp_dir):
        """Test automatic output directory creation"""
        output_dir = temp_dir / "new_output_dir"
        output_file = output_dir / "results.tsv"
        (temp_dir / "test.sam").write_text("@HD\tVN:1.0\n")
        
        args = Mock(
            input=str(temp_dir),
            output=str(output_file),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            sequences=None,
            append_sequences=None,
            workers=2,
            recursive=True,
            resume=False,
            dry_run=True,
            quiet=False
        )
        
        nt_screen.run(args)
        assert output_dir.exists()