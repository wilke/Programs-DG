# Programs

![Test Coverage](./coverage.svg)

A collection of random scripts / small programs

## Cryptic Screening CLI

A production-ready command-line interface for the Cryptic Screening toolkit, designed for SARS-CoV-2 sequence analysis and viral surveillance.

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the CLI tool
cd Cryptic_Screening/
pip install -e .
```

### Usage

```bash
# Run NT screening
cryptic-screen nt --input /path/to/sam/files --output-dir results/

# Run PM screening  
cryptic-screen pm --input /path/to/unique_seqs --output-dir results/

# Run winnow filtering
cryptic-screen winnow --nt-results results/NTSeqScreenResults.tsv --pm-dir results/

# Deduplicate sequences
cryptic-screen derep input.fa output.fa
```

See [USER_GUIDE.md](USER_GUIDE.md) for detailed usage instructions.

### Testing

```bash
# Run tests with coverage
pytest tests/unit/ -v --cov=lib/cryptic_screening --cov-report=term-missing

# Generate coverage badge
coverage-badge -o coverage.svg
```

### Docker

Multi-platform Docker images are available:

```bash
docker pull wilke/cryptic-screening:latest
docker run -v $(pwd):/work wilke/cryptic-screening:latest cryptic-screen --help
```
