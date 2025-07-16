# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a bioinformatics toolkit focused on **SARS-CoV-2 sequence analysis and viral surveillance**. The repository contains Python scripts and shell workflows for processing sequencing data from SRA databases, MiSeq platforms, and other sources to detect viral variants and cryptic lineages.

## Build and Deployment Commands

### Docker Build (Cryptic Screening Module)
```bash
cd Cryptic_Screening/
./build.sh  # Builds and pushes multi-platform images to wilke/cryptic-screening
```

### Local Development Setup
```bash
# Install all dependencies
pip install -r requirements.txt

# Install Cryptic Screening module
cd Cryptic_Screening/
pip install -e .
```

### Run Containerized Tools
```bash
# Pull and run the container
docker pull wilke/cryptic-screening:latest
docker run -v $(pwd):/work wilke/cryptic-screening:latest

# Execute specific screening tools
docker run -v $(pwd):/work wilke/cryptic-screening:latest NTSeqScreenMP.py
docker run -v $(pwd):/work wilke/cryptic-screening:latest PMScreenMP.py
docker run -v $(pwd):/work wilke/cryptic-screening:latest WinnowScreens.py
```

## Core Architecture

### Main Analysis Pipelines

1. **SRA Processing Pipeline**:
   ```
   SRA_fetch.py → derep.py → minimap2 alignment → SAM_Refiner → Variant analysis
   ```

2. **MiSeq SARS-CoV-2 Pipeline**:
   ```
   Raw FASTQ → bbmerge → cutadapt → minimap2 → SAM processing → Consensus generation
   ```

3. **Cryptic Screening Pipeline** (containerized):
   ```
   NTSeqScreenMP.py → PMScreenMP.py → WinnowScreens.py → Filtered reports
   ```

### Workflow Scripts

The repository uses **shell-based workflows** for complex analyses:

- `Workflow.sh`: Main SARS-CoV-2 analysis pipeline
- `MiSeqSARS2SpikeWorkflow.sh`: Interactive MiSeq processing with user prompts
- `WorkflowWGS.sh`: Whole genome sequencing analysis
- `WorkflowNY.sh`, `WorkflowE.sh`: Region-specific variant tracking
- `WorkflowrRNA.sh`: Ribosomal RNA analysis

These workflows orchestrate multiple Python scripts and external tools (minimap2, samtools, etc.).

### Key Components

**Data Processing**:
- `SRA_fetch.py`: Downloads SRA data using prefetch/fasterq-dump
- `derep.py`, `derep2.py`: Sequence deduplication with multiprocessing
- `Pullfastqgz.py`: FASTQ extraction and compression

**Sequence Analysis**:
- `SAM2Fasta.py`: Converts SAM alignments to FASTA
- `Consensus.py`, `MakeConsensus.py`: Generates consensus sequences
- `Variant_extractor.py`: Extracts variant information from alignments

**Specialized Tools**:
- `NYC_Variant_Counter.py`: Location-specific variant surveillance
- `CrypticPMFinder.py`: Detects cryptic point mutations
- `WGSLineageNet.py`: Performs lineage classification

## Working with the Codebase

### Reference Data
- `GP.fasta`: Primary SARS-CoV-2 glycoprotein reference sequence
- `LinkedPMs.txt`, `SinglePMs.txt`: Point mutation reference data for cryptic screening

### Dependencies and External Tools
The project integrates with several external bioinformatics tools:
- **SAM_Refiner**: Installed via GitHub (degregory/SAM_Refiner)
- **minimap2**: For sequence alignment
- **samtools**: For SAM/BAM processing
- **bbtools**: For read preprocessing (bbmerge)

### Multiprocessing Architecture
Many scripts use Python's multiprocessing module for performance:
- `NTSeqScreenMP.py`, `PMScreenMP.py`: Parallel screening of multiple files
- `derep.py`: Parallel sequence deduplication
- Core analysis scripts scale based on available CPU cores

### File Organization Patterns
Scripts automatically create working directories and expect specific file structures:
- Input files: FASTQ, SAM, FASTA formats
- Output directories: Created automatically by workflows
- Intermediate files: Preserved for debugging and pipeline resumption

### Development Patterns
- **Script-based architecture**: Each Python file handles specific analysis tasks
- **Shell workflow orchestration**: Complex analyses use shell scripts to coordinate
- **File-based communication**: Scripts communicate primarily through file I/O
- **Modular design**: Individual scripts can be combined for custom analyses

## Deployment Considerations

### Container Usage
The Cryptic Screening module is containerized for reproducible deployment:
- Multi-platform support (AMD64/ARM64)
- All dependencies pre-installed
- Non-root user configuration for security

### Local Installation
For development or custom workflows, install dependencies locally and run scripts directly. Most scripts accept command-line arguments and can process individual files or directories.

### Large-Scale Processing
The toolkit is designed for batch processing of large sequencing datasets:
- Multiprocessing support for CPU-intensive tasks
- Efficient memory usage for handling large SAM/BAM files
- Checkpoint capabilities in workflows for resuming interrupted analyses