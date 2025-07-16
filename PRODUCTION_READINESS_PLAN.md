# Production Readiness Plan for Cryptic Screening Tools

## What Does "Production Ready" Mean?

Production-ready code must be:

1. **Reliable**: Handles errors gracefully, recovers from failures, provides meaningful error messages
2. **Maintainable**: Well-documented, tested, follows consistent patterns
3. **Scalable**: Handles varying workloads efficiently, manages resources properly
4. **Secure**: Validates inputs, prevents vulnerabilities, protects sensitive data
5. **Observable**: Provides logging, monitoring, and debugging capabilities
6. **Configurable**: Supports different environments without code changes
7. **Tested**: Has comprehensive test coverage including unit, integration, and performance tests
8. **Documented**: Clear API documentation, deployment guides, and operational runbooks

## Phase 1: Foundation (Weeks 1-2)

### 1.1 Project Structure Refactoring
```
cryptic_screening/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── nt_screen.py          # Refactored from NTSeqScreenMP.py
│   │   ├── pm_screen.py          # Refactored from PMScreenMP.py
│   │   ├── winnow.py             # Refactored from WinnowScreens.py
│   │   └── derep.py              # Refactored derep.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_handlers.py      # File I/O utilities
│   │   ├── validators.py         # Input validation
│   │   └── logging_config.py     # Centralized logging
│   └── config/
│       ├── __init__.py
│       └── settings.py           # Configuration management
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
│   ├── api/
│   ├── deployment/
│   └── user_guide/
├── config/
│   ├── development.yaml
│   ├── production.yaml
│   └── testing.yaml
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── scripts/
│   ├── migrate_data.py
│   └── validate_installation.py
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── security-scan.yml
├── pyproject.toml
├── setup.cfg
├── Makefile
└── README.md
```

### 1.2 Core Infrastructure Components

#### Logging Framework
```python
# src/utils/logging_config.py
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    """JSON structured logging formatter"""
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        return json.dumps(log_data)

def setup_logging(
    name: str,
    level: str = "INFO",
    log_dir: Optional[Path] = None,
    enable_console: bool = True,
    enable_file: bool = True,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """Configure structured logging with rotation"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    formatter = StructuredFormatter()
    
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    if enable_file and log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
```

#### Configuration Management
```python
# src/config/settings.py
from typing import Dict, Any, Optional
from pathlib import Path
import yaml
import os
from pydantic import BaseSettings, validator

class ScreeningConfig(BaseSettings):
    """Configuration for screening tools"""
    
    # General settings
    environment: str = "development"
    debug: bool = False
    max_workers: int = os.cpu_count() or 4
    batch_size: int = 1000
    
    # File paths
    data_dir: Path = Path("./data")
    output_dir: Path = Path("./output")
    temp_dir: Path = Path("./temp")
    
    # NT Screening settings
    nt_searches: list[str] = [
        "GTGTGTCATGCCGCTGTTTAAT",
        "CACTGATCAGGTAGGGAGCTTC",
        # ... other sequences
    ]
    
    # PM Screening settings
    pm_total_count_cutoff: int = 10
    pm_per_file_count_cutoff: int = 1
    linked_pm_file: Path = Path("LinkedPMs.txt")
    single_pm_file: Path = Path("SinglePMs.txt")
    
    # Winnow settings
    nt_count_cutoff: int = 10
    meta_file: Path = Path("220609_SARS2_SRA_metadata.txt")
    
    # Derep settings
    derep_min_count: int = 2
    
    # Logging
    log_level: str = "INFO"
    log_dir: Path = Path("./logs")
    
    @validator('data_dir', 'output_dir', 'temp_dir', 'log_dir', pre=True)
    def create_directories(cls, v):
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    class Config:
        env_prefix = "SCREENING_"
        env_file = ".env"
        
    @classmethod
    def from_yaml(cls, config_file: Path) -> "ScreeningConfig":
        """Load configuration from YAML file"""
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
```

#### Error Handling Framework
```python
# src/utils/exceptions.py
class ScreeningError(Exception):
    """Base exception for screening tools"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}

class FileProcessingError(ScreeningError):
    """Raised when file processing fails"""
    pass

class ValidationError(ScreeningError):
    """Raised when input validation fails"""
    pass

class ConfigurationError(ScreeningError):
    """Raised when configuration is invalid"""
    pass

# Context manager for error handling
from contextlib import contextmanager
import traceback

@contextmanager
def handle_errors(logger, operation: str, raise_on_error: bool = True):
    """Context manager for consistent error handling"""
    try:
        yield
    except Exception as e:
        logger.error(
            f"Error during {operation}",
            extra={
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traceback': traceback.format_exc()
            }
        )
        if raise_on_error:
            raise
```

## Phase 2: Refactoring Individual Components (Weeks 3-4)

### 2.1 NT Screening Refactoring

```python
# src/core/nt_screen.py
from typing import List, Dict, Set, Optional, Tuple
from pathlib import Path
import concurrent.futures
from dataclasses import dataclass
import pysam

from ..utils.logging_config import setup_logging
from ..utils.exceptions import FileProcessingError, handle_errors
from ..config.settings import ScreeningConfig

@dataclass
class NTScreenResult:
    """Result of NT screening for a file"""
    file_path: Path
    accession: str
    hits: Dict[str, int]
    total_sequences: int
    processing_time: float

class NTScreener:
    """Nucleotide sequence screening with improved error handling and performance"""
    
    def __init__(self, config: ScreeningConfig):
        self.config = config
        self.logger = setup_logging(
            "nt_screener",
            level=config.log_level,
            log_dir=config.log_dir
        )
        self.search_sequences = config.nt_searches
        self._validate_search_sequences()
    
    def _validate_search_sequences(self) -> None:
        """Validate search sequences are valid nucleotides"""
        valid_chars = set('ACGTN')
        for seq in self.search_sequences:
            if not all(c in valid_chars for c in seq.upper()):
                raise ValueError(f"Invalid nucleotide sequence: {seq}")
    
    def screen_files(
        self,
        file_paths: List[Path],
        resume_from: Optional[Path] = None
    ) -> List[NTScreenResult]:
        """Screen multiple files with resumption support"""
        results = []
        
        # Load previous results if resuming
        if resume_from and resume_from.exists():
            results = self._load_previous_results(resume_from)
            processed_files = {r.file_path for r in results}
            file_paths = [f for f in file_paths if f not in processed_files]
        
        # Process files in parallel
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=self.config.max_workers
        ) as executor:
            future_to_file = {
                executor.submit(self._process_file, file_path): file_path
                for file_path in file_paths
            }
            
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                with handle_errors(self.logger, f"processing {file_path}"):
                    result = future.result()
                    results.append(result)
                    self.logger.info(
                        f"Processed {file_path}",
                        extra={'result': result.__dict__}
                    )
        
        return results
    
    def _process_file(self, file_path: Path) -> NTScreenResult:
        """Process a single file with proper resource management"""
        import time
        start_time = time.time()
        
        hits = {seq: 0 for seq in self.search_sequences}
        total_sequences = 0
        accession = self._extract_accession(file_path)
        
        try:
            if file_path.suffix in ['.sam', '.bam', '.cram']:
                hits, total_sequences = self._process_alignment_file(file_path)
            else:
                raise FileProcessingError(
                    f"Unsupported file type: {file_path.suffix}"
                )
        except Exception as e:
            self.logger.error(f"Failed to process {file_path}: {e}")
            raise
        
        return NTScreenResult(
            file_path=file_path,
            accession=accession,
            hits=hits,
            total_sequences=total_sequences,
            processing_time=time.time() - start_time
        )
    
    def _process_alignment_file(
        self,
        file_path: Path
    ) -> Tuple[Dict[str, int], int]:
        """Process SAM/BAM/CRAM files efficiently"""
        hits = {seq: 0 for seq in self.search_sequences}
        total_sequences = 0
        
        with pysam.AlignmentFile(str(file_path), 'r') as samfile:
            for read in samfile:
                if read.is_unmapped:
                    continue
                
                total_sequences += 1
                sequence = read.query_sequence.upper()
                
                # Efficient substring searching
                for search_seq in self.search_sequences:
                    if search_seq in sequence:
                        hits[search_seq] += 1
        
        return hits, total_sequences
```

### 2.2 Testing Infrastructure

```python
# tests/unit/test_nt_screen.py
import pytest
from pathlib import Path
import tempfile
import pysam

from cryptic_screening.core.nt_screen import NTScreener, NTScreenResult
from cryptic_screening.config.settings import ScreeningConfig

@pytest.fixture
def test_config():
    """Test configuration"""
    return ScreeningConfig(
        environment="testing",
        nt_searches=["ACGT", "GGGG"],
        max_workers=2,
        log_dir=Path(tempfile.mkdtemp())
    )

@pytest.fixture
def sample_sam_file(tmp_path):
    """Create a sample SAM file for testing"""
    sam_path = tmp_path / "test.sam"
    
    # Create SAM with test sequences
    header = {
        'HD': {'VN': '1.0'},
        'SQ': [{'LN': 1000, 'SN': 'ref'}]
    }
    
    with pysam.AlignmentFile(str(sam_path), 'w', header=header) as samfile:
        # Add test reads
        a = pysam.AlignedSegment()
        a.query_name = "read1"
        a.query_sequence = "ACGTACGTACGT"
        a.flag = 0
        a.reference_id = 0
        a.reference_start = 100
        a.mapping_quality = 60
        a.cigar = [(0, 12)]  # 12M
        samfile.write(a)
    
    return sam_path

class TestNTScreener:
    def test_initialization(self, test_config):
        screener = NTScreener(test_config)
        assert screener.search_sequences == ["ACGT", "GGGG"]
    
    def test_invalid_sequence_validation(self, test_config):
        test_config.nt_searches = ["ACGT", "INVALID"]
        with pytest.raises(ValueError, match="Invalid nucleotide sequence"):
            NTScreener(test_config)
    
    def test_process_sam_file(self, test_config, sample_sam_file):
        screener = NTScreener(test_config)
        result = screener._process_file(sample_sam_file)
        
        assert result.file_path == sample_sam_file
        assert result.hits["ACGT"] == 1
        assert result.hits["GGGG"] == 0
        assert result.total_sequences == 1
    
    @pytest.mark.parametrize("num_files", [1, 5, 10])
    def test_parallel_processing(self, test_config, tmp_path, num_files):
        """Test parallel processing of multiple files"""
        screener = NTScreener(test_config)
        
        # Create multiple test files
        test_files = []
        for i in range(num_files):
            # Create files similar to sample_sam_file
            pass
        
        results = screener.screen_files(test_files)
        assert len(results) == num_files
```

## Phase 3: Repository Management Strategy (Week 5)

### 3.1 Fork and Contribution Strategy

Since this is a cloned repository you don't own:

1. **Fork Setup** ✓ COMPLETED
   ```bash
   # Fork already created: wilke/Programs-DG
   # Update remotes to use fork as origin
   git remote set-url origin git@github.com:wilke/Programs-DG.git
   git remote add upstream https://github.com/ORIGINAL_OWNER/Programs.git
   ```

2. **Feature Branch** ✓ CREATED
   ```bash
   # Branch already created: cli-options
   git checkout cli-options
   ```

3. **Maintain Sync with Upstream**
   ```bash
   # Regularly sync with upstream
   git fetch upstream
   git checkout main
   git merge upstream/main
   git checkout feature/production-ready-cryptic-screening
   git rebase main
   ```

### 3.2 Migration Strategy

Create migration scripts to help users transition:

```python
# scripts/migrate_to_production.py
#!/usr/bin/env python3
"""
Migrate existing screening data to production format
"""
import argparse
from pathlib import Path
import shutil
import json

def migrate_nt_results(old_file: Path, output_dir: Path):
    """Convert old NT screening results to new format"""
    # Implementation here
    pass

def validate_migration(old_dir: Path, new_dir: Path):
    """Validate that migration preserved all data"""
    # Implementation here
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate to production format")
    parser.add_argument("--old-data", required=True, help="Old data directory")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--validate", action="store_true", help="Validate migration")
    
    args = parser.parse_args()
    # Migration logic here
```

### 3.3 Backward Compatibility

Maintain compatibility during transition:

```python
# src/legacy/wrapper.py
"""Wrapper scripts for backward compatibility"""
import warnings
from pathlib import Path
import sys

def legacy_nt_screen():
    """Wrapper for NTSeqScreenMP.py compatibility"""
    warnings.warn(
        "NTSeqScreenMP.py is deprecated. Use 'cryptic-screen nt' instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Import new implementation
    from cryptic_screening.core.nt_screen import NTScreener
    from cryptic_screening.config.settings import ScreeningConfig
    
    # Map old command line args to new config
    # Run new implementation
```

## Phase 4: DevOps and CI/CD (Week 6)

### 4.1 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements/development.txt
        pip install -e .
    
    - name: Run linting
      run: |
        black --check src tests
        flake8 src tests
        mypy src
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Security scan
      run: |
        pip install bandit safety
        bandit -r src/
        safety check
```

### 4.2 Docker Production Image

```dockerfile
# Dockerfile.production
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt

# Production stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 screening
USER screening

# Copy application
WORKDIR /app
COPY --chown=screening:screening src/ ./src/
COPY --chown=screening:screening config/ ./config/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import cryptic_screening; print('OK')"

ENTRYPOINT ["python", "-m", "cryptic_screening"]
```

## Phase 5: Monitoring and Observability (Week 7)

### 5.1 Performance Monitoring

```python
# src/utils/monitoring.py
import time
import psutil
import functools
from typing import Callable, Any
from prometheus_client import Counter, Histogram, Gauge

# Metrics
file_processing_duration = Histogram(
    'file_processing_duration_seconds',
    'Time spent processing files',
    ['file_type', 'operation']
)

sequences_processed = Counter(
    'sequences_processed_total',
    'Total number of sequences processed',
    ['file_type']
)

memory_usage = Gauge(
    'memory_usage_bytes',
    'Current memory usage in bytes'
)

def monitor_performance(operation: str):
    """Decorator to monitor function performance"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            # Record memory before
            process = psutil.Process()
            mem_before = process.memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                
                # Record metrics
                duration = time.time() - start_time
                file_processing_duration.labels(
                    file_type='sam',
                    operation=operation
                ).observe(duration)
                
                # Memory usage
                mem_after = process.memory_info().rss
                memory_usage.set(mem_after)
                
                return result
                
            except Exception as e:
                # Record failure metrics
                raise
        
        return wrapper
    return decorator
```

## Phase 6: Documentation and Training (Week 8)

### 6.1 API Documentation

```python
# docs/api/example.py
"""
Cryptic Screening API Documentation

Example usage:

    from cryptic_screening import NTScreener, ScreeningConfig
    
    # Configure screening
    config = ScreeningConfig(
        nt_searches=["ACGT", "GGGG"],
        max_workers=4,
        output_dir="./results"
    )
    
    # Initialize screener
    screener = NTScreener(config)
    
    # Screen files
    results = screener.screen_files([
        Path("sample1.sam"),
        Path("sample2.bam")
    ])
    
    # Process results
    for result in results:
        print(f"{result.file_path}: {result.hits}")
"""
```

### 6.2 Deployment Guide

```markdown
# Deployment Guide

## Prerequisites
- Python 3.8+
- Docker (optional)
- PostgreSQL (for production metrics storage)

## Installation

### From PyPI
```bash
pip install cryptic-screening
```

### From Source
```bash
git clone https://github.com/your-username/cryptic-screening.git
cd cryptic-screening
pip install -e .
```

## Configuration

Create a configuration file:

```yaml
# config/production.yaml
environment: production
max_workers: 16
batch_size: 5000

# Database for metrics
database:
  host: localhost
  port: 5432
  name: screening_metrics
  
# Logging
log_level: INFO
log_dir: /var/log/cryptic-screening
```

## Running in Production

### Using systemd

```ini
# /etc/systemd/system/cryptic-screening.service
[Unit]
Description=Cryptic Screening Service
After=network.target

[Service]
Type=simple
User=screening
WorkingDirectory=/opt/cryptic-screening
Environment="SCREENING_ENVIRONMENT=production"
ExecStart=/opt/venv/bin/python -m cryptic_screening.api
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Using Docker

```bash
docker run -d \
  --name cryptic-screening \
  -v /data:/data \
  -v /config:/config \
  -e SCREENING_ENVIRONMENT=production \
  cryptic-screening:latest
```
```

## Implementation Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 1 | Weeks 1-2 | Project structure, logging, config, error handling |
| Phase 2 | Weeks 3-4 | Refactored components with tests |
| Phase 3 | Week 5 | Repository fork, migration scripts |
| Phase 4 | Week 6 | CI/CD pipeline, Docker images |
| Phase 5 | Week 7 | Monitoring and metrics |
| Phase 6 | Week 8 | Documentation and deployment guides |

## Success Metrics

1. **Code Quality**
   - 80%+ test coverage
   - Zero high/critical security vulnerabilities
   - All functions documented with type hints

2. **Performance**
   - 2x faster processing through optimizations
   - Memory usage reduced by 50%
   - Support for files >10GB

3. **Reliability**
   - 99.9% uptime in production
   - Graceful error recovery
   - No data loss on failures

4. **Maintainability**
   - Onboarding new developers <1 day
   - Bug fix turnaround <24 hours
   - Feature additions without breaking changes

## Next Steps

1. Review plan with stakeholders
2. Set up development environment
3. Create feature branch
4. Begin Phase 1 implementation
5. Schedule weekly progress reviews