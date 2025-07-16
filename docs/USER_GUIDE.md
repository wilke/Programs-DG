# Cryptic Screening Tools - User Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Commands](#commands)
4. [Configuration](#configuration)
5. [Environment Variables](#environment-variables)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

## Installation

The cryptic screening tools are ready to use without installation. Simply ensure the repository is in your PATH or use the full path to the `cryptic-screen` command.

```bash
# Add to PATH (optional)
export PATH="/path/to/Programs:$PATH"

# Or use directly
/path/to/Programs/cryptic-screen --help
```

### Optional Dependencies

For full functionality, install:
```bash
pip install pyyaml  # For configuration file support
```

## Quick Start

### Basic Usage

```bash
# NT screening - search for nucleotide sequences in SAM/BAM files
cryptic-screen nt --input ./samples

# PM screening - search for point mutations
cryptic-screen pm --input ./unique_seqs

# Winnow - filter and create reports
cryptic-screen winnow --nt-results NTSeqScreenResults.tsv

# Derep - deduplicate sequences
cryptic-screen derep input.fasta output.fasta
```

### Using Environment Variables

```bash
# Set default directories
export CRYPTIC_SCREEN_DATA_DIR=/data/references
export CRYPTIC_SCREEN_OUTPUT_DIR=/data/results

# Now commands use these defaults
cryptic-screen nt --input ./samples
```

## Commands

### nt - Nucleotide Sequence Screening

Search for specific nucleotide sequences in SAM/BAM/CRAM files.

```bash
cryptic-screen nt [OPTIONS]
```

**Required Options:**
- `--input PATH` - Directory containing SAM/BAM/CRAM files

**Optional Options:**
- `--output FILE` - Output file (default: ./NTSeqScreenResults.tsv)
- `--sequences FILE` - Custom sequences file (replaces built-in)
- `--append-sequences FILE` - Additional sequences to search
- `--data-dir PATH` - Directory for reference files
- `--output-dir PATH` - Output directory
- `--workers N` - Number of parallel workers
- `--recursive` - Search subdirectories (default: True)
- `--resume` - Resume from existing results
- `--dry-run` - Validate inputs without processing

**Example:**
```bash
cryptic-screen nt \
  --input /data/alignments \
  --output-dir /results \
  --append-sequences custom_sequences.txt \
  --workers 16
```

### pm - Point Mutation Screening

Search for point mutations in unique sequence files.

```bash
cryptic-screen pm [OPTIONS]
```

**Required Options:**
- `--input PATH` - Directory with *_unique_seqs.tsv files

**Optional Options:**
- `--single-pm FILE` - Single PM reference (default: SinglePMs.txt)
- `--linked-pm FILE` - Linked PM reference (default: LinkedPMs.txt)
- `--subset FILE` - Screen only specific accessions
- `--total-cutoff N` - Total count cutoff (default: 10)
- `--per-file-cutoff N` - Per-file count cutoff (default: 1)
- `--data-dir PATH` - Directory for reference files
- `--output-dir PATH` - Output directory

**Example:**
```bash
cryptic-screen pm \
  --input /data/unique_sequences \
  --output-dir /results/pm_screening \
  --total-cutoff 5 \
  --subset priority_samples.txt
```

### winnow - Filter Results

Filter screening results and generate reports.

```bash
cryptic-screen winnow [OPTIONS]
```

**Required Options:**
- `--nt-results FILE` - NT screening results file

**Optional Options:**
- `--pm-dir PATH` - Directory with PM results
- `--metadata FILE` - SRA metadata file
- `--nt-cutoff N` - NT count cutoff (default: 10)
- `--pm-cutoff N` - PM count cutoff (default: 10)
- `--output-dir PATH` - Output directory

**Example:**
```bash
cryptic-screen winnow \
  --nt-results /results/NTSeqScreenResults.tsv \
  --pm-dir /results/pm_screening \
  --metadata /data/sra_metadata.tsv \
  --output-dir /results/reports
```

### derep - Deduplicate Sequences

Remove duplicate sequences keeping count information.

```bash
cryptic-screen derep [OPTIONS] INPUT OUTPUT
```

**Required Arguments:**
- `INPUT` - Input FASTA/FASTQ file
- `OUTPUT` - Output file

**Optional Options:**
- `--min-count N` - Minimum count threshold (default: 2)
- `--memory-limit N` - Memory limit in GB

**Example:**
```bash
cryptic-screen derep \
  sequences.fastq \
  unique_sequences.fasta \
  --min-count 3
```

## Configuration

### Configuration File Format

Create a YAML configuration file to set default values:

```yaml
# config.yaml
global:
  data_dir: /data/references
  output_dir: /data/results
  workers: 16
  log_level: INFO

nt:
  recursive: true
  file_pattern: "*.{sam,bam,cram}"

pm:
  total_cutoff: 5
  per_file_cutoff: 1
  single_pm: SinglePMs_v2.txt
  linked_pm: LinkedPMs_v2.txt

winnow:
  nt_cutoff: 20
  pm_cutoff: 15
  metadata: /data/metadata/sra_meta.tsv
```

### Using Configuration Files

```bash
# Use configuration file
cryptic-screen --config config.yaml nt --input /data/samples

# Command line arguments override config file
cryptic-screen --config config.yaml nt --input /data/samples --workers 32
```

## Environment Variables

All major settings can be controlled via environment variables:

```bash
# Directories
export CRYPTIC_SCREEN_DATA_DIR=/data/references
export CRYPTIC_SCREEN_OUTPUT_DIR=/data/results

# Runtime options
export CRYPTIC_SCREEN_WORKERS=32
export CRYPTIC_SCREEN_LOG_LEVEL=DEBUG

# Reference files
export CRYPTIC_SCREEN_LINKED_PM=LinkedPMs_v2.txt
export CRYPTIC_SCREEN_SINGLE_PM=SinglePMs_v2.txt
export CRYPTIC_SCREEN_METADATA=sra_metadata.tsv
```

## Examples

### Example 1: Basic NT Screening

```bash
# Simple screening in current directory
cryptic-screen nt --input .

# This will:
# 1. Search current directory for SAM/BAM/CRAM files
# 2. Screen for default nucleotide sequences
# 3. Write results to ./NTSeqScreenResults.tsv
```

### Example 2: Production Pipeline

```bash
# Set up environment
export CRYPTIC_SCREEN_DATA_DIR=/production/references
export CRYPTIC_SCREEN_OUTPUT_DIR=/production/results
export CRYPTIC_SCREEN_WORKERS=64

# Run NT screening
cryptic-screen nt \
  --input /production/alignments \
  --log-file /logs/nt_screening.log \
  --resume

# Run PM screening
cryptic-screen pm \
  --input /production/unique_seqs \
  --log-file /logs/pm_screening.log

# Generate reports
cryptic-screen winnow \
  --nt-results $CRYPTIC_SCREEN_OUTPUT_DIR/NTSeqScreenResults.tsv \
  --pm-dir $CRYPTIC_SCREEN_OUTPUT_DIR \
  --metadata $CRYPTIC_SCREEN_DATA_DIR/metadata.tsv
```

### Example 3: Debugging Issues

```bash
# Dry run to validate inputs
cryptic-screen nt --input /data/samples --dry-run

# Run with debug logging
cryptic-screen --log-level DEBUG nt --input /data/samples

# Save debug log to file
cryptic-screen --log-level DEBUG --log-file debug.log nt --input /data/samples
```

### Example 4: Custom Sequences

```bash
# Use completely custom sequences (replaces defaults)
cryptic-screen nt \
  --input ./samples \
  --sequences my_sequences.txt

# Add sequences to defaults
cryptic-screen nt \
  --input ./samples \
  --append-sequences additional_sequences.txt
```

## Troubleshooting

### Common Issues

#### "No SAM/BAM/CRAM files found"
- Check the input directory path
- Verify files have correct extensions (.sam, .bam, .cram)
- Use `--recursive` if files are in subdirectories
- Check file permissions

#### "Reference file not found"
- Ensure reference files (LinkedPMs.txt, SinglePMs.txt) are in:
  - Current directory
  - Directory specified by `--data-dir`
  - Directory set in CRYPTIC_SCREEN_DATA_DIR

#### "PyYAML not installed"
- Configuration files require PyYAML
- Install with: `pip install pyyaml`
- Or use command line arguments instead

#### "Permission denied"
- Check read permissions on input files
- Check write permissions on output directory
- Ensure sufficient disk space

### Debug Mode

For detailed debugging information:

```bash
# Maximum verbosity
cryptic-screen --log-level DEBUG --log-file debug.log COMMAND

# Check what would be processed
cryptic-screen COMMAND --dry-run
```

### Getting Help

```bash
# General help
cryptic-screen --help

# Command-specific help
cryptic-screen nt --help
cryptic-screen pm --help
cryptic-screen winnow --help
cryptic-screen derep --help
```