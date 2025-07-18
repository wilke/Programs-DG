"""
Unit tests for validation module
"""

import pytest
from pathlib import Path
from cryptic_screening.validation import (
    ValidationError,
    validate_input_directory,
    validate_output_file,
    validate_reference_file,
    validate_positive_integer,
    validate_file_pattern,
)

class TestValidateInputDirectory:
    """Test input directory validation"""
    
    def test_valid_directory(self, temp_dir):
        """Test validation of a valid directory"""
        # Create test files
        (temp_dir / "test.sam").write_text("test")
        
        result = validate_input_directory(temp_dir, file_types=[".sam"])
        assert result == temp_dir
    
    def test_nonexistent_directory(self):
        """Test validation of non-existent directory"""
        with pytest.raises(ValidationError, match="does not exist"):
            validate_input_directory("/path/that/does/not/exist")
    
    def test_file_instead_of_directory(self, temp_dir):
        """Test validation when path is a file"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")
        
        with pytest.raises(ValidationError, match="not a directory"):
            validate_input_directory(test_file)
    
    def test_empty_directory_with_required_files(self, temp_dir):
        """Test validation of empty directory when files are required"""
        with pytest.raises(ValidationError, match="No files with extensions"):
            validate_input_directory(temp_dir, file_types=[".sam", ".bam"])
    
    def test_recursive_search(self, temp_dir):
        """Test recursive file search"""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "test.sam").write_text("test")
        
        result = validate_input_directory(temp_dir, file_types=[".sam"], recursive=True)
        assert result == temp_dir

class TestValidateOutputFile:
    """Test output file validation"""
    
    def test_valid_output_file(self, temp_dir):
        """Test validation of valid output file path"""
        output_file = temp_dir / "output.txt"
        result = validate_output_file(output_file)
        assert result == output_file
    
    def test_create_parent_directory(self, temp_dir):
        """Test parent directory creation"""
        output_file = temp_dir / "new_dir" / "output.txt"
        result = validate_output_file(output_file, create_parent=True)
        assert result == output_file
        assert output_file.parent.exists()
    
    def test_no_create_parent_directory(self, temp_dir):
        """Test when parent directory doesn't exist and create_parent=False"""
        output_file = temp_dir / "new_dir" / "output.txt"
        with pytest.raises(ValidationError, match="does not exist"):
            validate_output_file(output_file, create_parent=False)
    
    def test_existing_readonly_file(self, temp_dir):
        """Test validation of read-only file"""
        output_file = temp_dir / "readonly.txt"
        output_file.write_text("test")
        output_file.chmod(0o444)  # Read-only
        
        with pytest.raises(ValidationError, match="not writable"):
            validate_output_file(output_file)

class TestValidateReferenceFile:
    """Test reference file validation"""
    
    def test_valid_reference_file(self, temp_dir):
        """Test validation of valid reference file"""
        ref_file = temp_dir / "reference.txt"
        ref_file.write_text("reference data")
        
        result = validate_reference_file(ref_file)
        assert result == ref_file
    
    def test_nonexistent_reference_file(self):
        """Test validation of non-existent reference file"""
        with pytest.raises(ValidationError, match="not found"):
            validate_reference_file("/path/to/missing.txt")
    
    def test_directory_as_reference_file(self, temp_dir):
        """Test validation when path is directory"""
        with pytest.raises(ValidationError, match="not a file"):
            validate_reference_file(temp_dir)
    
    def test_empty_reference_file_warning(self, temp_dir, caplog):
        """Test warning for empty reference file"""
        ref_file = temp_dir / "empty.txt"
        ref_file.write_text("")
        
        result = validate_reference_file(ref_file)
        assert result == ref_file
        assert "is empty" in caplog.text

class TestValidatePositiveInteger:
    """Test positive integer validation"""
    
    def test_valid_positive_integer(self):
        """Test validation of valid positive integer"""
        assert validate_positive_integer(5) == 5
        assert validate_positive_integer("10") == 10
    
    def test_zero_with_default_min(self):
        """Test zero value with default minimum"""
        with pytest.raises(ValidationError, match="must be at least 1"):
            validate_positive_integer(0)
    
    def test_zero_with_custom_min(self):
        """Test zero value with custom minimum"""
        assert validate_positive_integer(0, min_value=0) == 0
    
    def test_negative_value(self):
        """Test negative value"""
        with pytest.raises(ValidationError, match="must be at least 1"):
            validate_positive_integer(-5)
    
    def test_non_integer_value(self):
        """Test non-integer value"""
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_positive_integer("not a number")
    
    def test_float_value(self):
        """Test float value conversion"""
        assert validate_positive_integer("5.0") == 5

class TestValidateFilePattern:
    """Test file pattern validation"""
    
    def test_valid_patterns(self):
        """Test valid file patterns"""
        assert validate_file_pattern("*.sam") == "*.sam"
        assert validate_file_pattern("test_*.txt") == "test_*.txt"
        assert validate_file_pattern("**/*.bam") == "**/*.bam"
    
    def test_empty_pattern(self):
        """Test empty pattern"""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_file_pattern("")
    
    def test_absolute_path_pattern(self):
        """Test pattern starting with /"""
        with pytest.raises(ValidationError, match="should not start with"):
            validate_file_pattern("/absolute/*.sam")