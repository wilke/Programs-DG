"""
Pytest configuration and fixtures
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add lib directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_config(temp_dir):
    """Create a sample configuration file"""
    config_path = temp_dir / "test_config.yaml"
    config_content = """
global:
  data_dir: ./test_data
  output_dir: ./test_output
  workers: 2
  log_level: DEBUG

nt:
  file_pattern: "*.sam"
  recursive: true

pm:
  total_cutoff: 5
  per_file_cutoff: 1
"""
    config_path.write_text(config_content)
    return config_path

@pytest.fixture
def mock_environment(monkeypatch):
    """Mock environment variables for testing"""
    monkeypatch.setenv("CRYPTIC_SCREEN_DATA_DIR", "/test/data")
    monkeypatch.setenv("CRYPTIC_SCREEN_OUTPUT_DIR", "/test/output")
    monkeypatch.setenv("CRYPTIC_SCREEN_WORKERS", "4")
    monkeypatch.setenv("CRYPTIC_SCREEN_LOG_LEVEL", "INFO")
    
@pytest.fixture
def sample_sam_content():
    """Sample SAM file content for testing"""
    return """@HD\tVN:1.0\tSO:unsorted
@SQ\tSN:ref\tLN:1000
read1\t0\tref\t100\t60\t12M\t*\t0\t0\tACGTACGTACGT\t************
read2\t0\tref\t200\t60\t12M\t*\t0\t0\tGGGGACGTACGT\t************
"""

@pytest.fixture
def sample_sequences_file(temp_dir):
    """Create a sample sequences file"""
    seq_file = temp_dir / "sequences.txt"
    seq_file.write_text("ACGT\nGGGG\nTTTT\n")
    return seq_file