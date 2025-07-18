"""
Unit tests for derep command
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from cryptic_screening.commands import derep

class TestDerepCommand:
    """Test derep command functionality"""
    
    def test_run_basic(self, temp_dir):
        """Test basic derep run"""
        # Create test input file
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        input_file.write_text(">seq1\nACGT\n>seq2\nTGCA\n")
        
        # Mock file objects
        input_mock = Mock()
        input_mock.name = str(input_file)
        input_mock.close = Mock()
        
        output_mock = Mock()
        output_mock.name = str(output_file)
        output_mock.close = Mock()
        
        args = Mock(
            input=input_mock,
            output=output_mock,
            min_count=1,
            memory_limit=None,
            dry_run=True,
            quiet=False
        )
        
        derep.run(args)
        
        # In dry run mode, file handles should not be closed
        input_mock.close.assert_not_called()
        output_mock.close.assert_not_called()
    
    def test_run_with_memory_limit(self, temp_dir):
        """Test run with memory limit"""
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        input_file.write_text(">seq1\nACGT\n")
        
        input_mock = Mock()
        input_mock.name = str(input_file)
        
        output_mock = Mock()
        output_mock.name = str(output_file)
        
        args = Mock(
            input=input_mock,
            output=output_mock,
            min_count=2,
            memory_limit=4,
            dry_run=True,
            quiet=False
        )
        
        derep.run(args)
    
    @patch('cryptic_screening.commands.derep.sys')
    def test_sys_argv_manipulation(self, mock_sys, temp_dir):
        """Test sys.argv is properly manipulated"""
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        input_file.write_text(">seq1\nACGT\n")
        
        # Store original argv
        original_argv = ['test_script.py', 'arg1', 'arg2']
        mock_sys.argv = original_argv.copy()
        
        input_mock = Mock()
        input_mock.name = str(input_file)
        input_mock.close = Mock()
        
        output_mock = Mock()
        output_mock.name = str(output_file)
        output_mock.close = Mock()
        
        args = Mock(
            input=input_mock,
            output=output_mock,
            min_count=3,
            memory_limit=None,
            dry_run=False,
            quiet=False
        )
        
        # Mock the derep module import
        with patch('cryptic_screening.commands.derep.sys.path'):
            with patch.dict('sys.modules', {'derep': Mock()}):
                try:
                    derep.run(args)
                except Exception:
                    pass
        
        # Verify file handles were closed
        input_mock.close.assert_called_once()
        output_mock.close.assert_called_once()
    
    def test_file_handle_closing(self, temp_dir):
        """Test that file handles are properly closed"""
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        input_file.write_text(">seq1\nACGT\n")
        
        input_mock = Mock()
        input_mock.name = str(input_file)
        input_mock.close = Mock()
        
        output_mock = Mock()
        output_mock.name = str(output_file)
        output_mock.close = Mock()
        
        args = Mock(
            input=input_mock,
            output=output_mock,
            min_count=1,
            memory_limit=None,
            dry_run=False,
            quiet=False
        )
        
        # Mock the derep module
        with patch.dict('sys.modules', {'derep': Mock()}):
            derep.run(args)
        
        # Verify file handles were closed
        input_mock.close.assert_called_once()
        output_mock.close.assert_called_once()
    
    def test_error_handling(self, temp_dir):
        """Test error handling during derep execution"""
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        
        input_mock = Mock()
        input_mock.name = str(input_file)
        input_mock.close = Mock()
        
        output_mock = Mock()
        output_mock.name = str(output_file)
        output_mock.close = Mock()
        
        args = Mock(
            input=input_mock,
            output=output_mock,
            min_count=1,
            memory_limit=None,
            dry_run=False,
            quiet=False
        )
        
        # Mock derep module to raise an exception on import
        with patch('cryptic_screening.commands.derep.sys.path', []):
            with patch('builtins.__import__', side_effect=RuntimeError("Test error")):
                with pytest.raises(RuntimeError, match="Test error"):
                    derep.run(args)
        
        # File handles should still be closed
        input_mock.close.assert_called_once()
        output_mock.close.assert_called_once()
    
    def test_sys_argv_restoration(self, temp_dir):
        """Test that sys.argv is restored after execution"""
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        
        input_mock = Mock()
        input_mock.name = str(input_file)
        input_mock.close = Mock()
        
        output_mock = Mock()
        output_mock.name = str(output_file)
        output_mock.close = Mock()
        
        args = Mock(
            input=input_mock,
            output=output_mock,
            min_count=1,
            memory_limit=None,
            dry_run=False,
            quiet=False
        )
        
        # Save original sys.argv
        original_argv = sys.argv.copy()
        
        # Mock derep module
        with patch.dict('sys.modules', {'derep': Mock()}):
            derep.run(args)
        
        # Verify sys.argv was restored
        assert sys.argv == original_argv
    
    def test_different_min_count_values(self, temp_dir):
        """Test different minimum count values"""
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        input_file.write_text(">seq1\nACGT\n")
        
        for min_count in [1, 5, 10, 100]:
            input_mock = Mock()
            input_mock.name = str(input_file)
            
            output_mock = Mock()
            output_mock.name = str(output_file)
            
            args = Mock(
                input=input_mock,
                output=output_mock,
                min_count=min_count,
                memory_limit=None,
                dry_run=True,
                quiet=False
            )
            
            derep.run(args)