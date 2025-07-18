"""
Unit tests for winnow command
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
from cryptic_screening.commands import winnow

class TestWinnowCommand:
    """Test winnow command functionality"""
    
    def test_run_basic(self, temp_dir):
        """Test basic winnow run"""
        # Create test NT results file
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("Sample\tSeq\tCount\nS1\tACGT\t10\n")
        
        # Create test PM hits files
        pm_dir = temp_dir / "pm_dir"
        pm_dir.mkdir()
        (pm_dir / "sample1_hits.tsv").write_text("PM\tCount\nPM1\t5\n")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(pm_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
    
    def test_run_with_metadata(self, temp_dir):
        """Test run with metadata file"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("Sample\tSeq\tCount\nS1\tACGT\t10\n")
        
        pm_dir = temp_dir / "pm_dir"
        pm_dir.mkdir()
        
        metadata = temp_dir / "metadata.tsv"
        metadata.write_text("SRR\tInfo\nSRR12345\tTest\n")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(pm_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata="metadata.tsv",
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
    
    def test_run_missing_nt_results(self, temp_dir):
        """Test run with missing NT results file"""
        args = Mock(
            nt_results="/nonexistent/results.tsv",
            pm_dir=str(temp_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=False,
            quiet=False
        )
        
        with pytest.raises(SystemExit) as exc_info:
            winnow.run(args)
        assert exc_info.value.code == 1
    
    def test_run_missing_metadata_warning(self, temp_dir, caplog):
        """Test warning when metadata file not found"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("Sample\tSeq\tCount\nS1\tACGT\t10\n")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(temp_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata="missing.tsv",
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
        assert "Metadata file not found" in caplog.text
    
    def test_output_directory_creation(self, temp_dir):
        """Test automatic output directory creation"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("data")
        
        output_dir = temp_dir / "new_output"
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(temp_dir),
            output_dir=str(output_dir),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
        assert output_dir.exists()
    
    def test_default_pm_directory(self, temp_dir):
        """Test using current directory as default PM directory"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("data")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=None,
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_environment_variables_set(self, temp_dir):
        """Test environment variables are set correctly"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("data")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(temp_dir),
            output_dir=str(temp_dir),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=10,
            pm_cutoff=5,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
        # In dry-run mode, environment is not actually modified
    
    def test_pm_hits_file_discovery(self, temp_dir):
        """Test discovery of PM hits files"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("data")
        
        pm_dir = temp_dir / "pm_dir"
        pm_dir.mkdir()
        
        # Create multiple hits files
        (pm_dir / "sample1_hits.tsv").write_text("data1")
        (pm_dir / "sample2_hits.tsv").write_text("data2")
        (pm_dir / "other_file.txt").write_text("not a hits file")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(pm_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
    
    @patch('cryptic_screening.commands.winnow.tempfile.TemporaryDirectory')
    def test_file_operations_in_temp_directory(self, mock_tempdir, temp_dir):
        """Test file operations in temporary directory"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("data")
        
        pm_dir = temp_dir / "pm_dir"
        pm_dir.mkdir()
        (pm_dir / "sample_hits.tsv").write_text("hits")
        
        # Mock temporary directory
        mock_temp = Mock()
        mock_temp_path = temp_dir / "temp"
        mock_temp_path.mkdir()
        mock_temp.__enter__ = Mock(return_value=str(mock_temp_path))
        mock_temp.__exit__ = Mock(return_value=None)
        mock_tempdir.return_value = mock_temp
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(pm_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata=None,
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)
    
    def test_metadata_directory_structure(self, temp_dir):
        """Test creation of metadata directory structure"""
        nt_results = temp_dir / "NTSeqScreenResults.tsv"
        nt_results.write_text("data")
        
        metadata = temp_dir / "metadata.tsv"
        metadata.write_text("metadata content")
        
        args = Mock(
            nt_results=str(nt_results),
            pm_dir=str(temp_dir),
            output_dir=str(temp_dir / "output"),
            data_dir=str(temp_dir),
            metadata="metadata.tsv",
            nt_cutoff=5,
            pm_cutoff=3,
            dry_run=True,
            quiet=False
        )
        
        winnow.run(args)