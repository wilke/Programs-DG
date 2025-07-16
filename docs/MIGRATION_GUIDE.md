# Migration Guide: From Original Scripts to cryptic-screen CLI

This guide helps you migrate from the original Python scripts to the new unified CLI.

## Quick Reference

| Old Command | New Command |
|-------------|-------------|
| `python NTSeqScreenMP.py` | `cryptic-screen nt --input .` |
| `python PMScreenMP.py` | `cryptic-screen pm --input .` |
| `python WinnowScreens.py` | `cryptic-screen winnow --nt-results NTSeqScreenResults.tsv` |
| `python derep.py input.fa output.fa 2` | `cryptic-screen derep input.fa output.fa --min-count 2` |

## Detailed Migration

### NT Screening (NTSeqScreenMP.py)

**Old way:**
```bash
cd /data/samples
python /path/to/NTSeqScreenMP.py
```

**New way:**
```bash
cryptic-screen nt --input /data/samples
```

**Key differences:**
- No need to change directories
- Can specify custom output location with `--output`
- Can control number of workers with `--workers`
- Can add custom sequences with `--append-sequences`

**Advanced example:**
```bash
# Old: Had to modify script or use NTSeqScreens.txt
# New: Direct command line control
cryptic-screen nt \
  --input /data/samples \
  --output /results/nt_results.tsv \
  --append-sequences /refs/custom_sequences.txt \
  --workers 32
```

### PM Screening (PMScreenMP.py)

**Old way:**
```bash
cd /data/unique_seqs
python /path/to/PMScreenMP.py
```

**New way:**
```bash
cryptic-screen pm --input /data/unique_seqs
```

**Key differences:**
- Reference files (SinglePMs.txt, LinkedPMs.txt) can be specified
- Output directory can be controlled
- Cutoff values are command line options

**Advanced example:**
```bash
# Old: Had to have files in specific locations
# New: Full control over all paths
cryptic-screen pm \
  --input /data/unique_seqs \
  --output-dir /results/pm_screening \
  --single-pm /refs/SinglePMs_v2.txt \
  --linked-pm /refs/LinkedPMs_v2.txt \
  --total-cutoff 5 \
  --subset priority_samples.txt
```

### Winnow (WinnowScreens.py)

**Old way:**
```bash
cd /data/results
python /path/to/WinnowScreens.py
```

**New way:**
```bash
cryptic-screen winnow --nt-results /data/results/NTSeqScreenResults.tsv
```

**Key differences:**
- Can specify locations of all input files
- Metadata file is optional and configurable
- Output directory can be specified

**Advanced example:**
```bash
# Old: Expected specific file structure
# New: Flexible file locations
cryptic-screen winnow \
  --nt-results /results/nt/NTSeqScreenResults.tsv \
  --pm-dir /results/pm \
  --metadata /data/metadata/sra_meta_2024.tsv \
  --output-dir /results/reports \
  --nt-cutoff 20 \
  --pm-cutoff 15
```

### Derep (derep.py)

**Old way:**
```bash
python derep.py sequences.fasta unique.fasta 2
```

**New way:**
```bash
cryptic-screen derep sequences.fasta unique.fasta --min-count 2
```

**Key differences:**
- Named parameter for min-count
- Can add memory limits
- Consistent interface with other commands

## Environment-Based Configuration

Instead of modifying scripts, use environment variables:

```bash
# Set defaults for all commands
export CRYPTIC_SCREEN_DATA_DIR=/data/references
export CRYPTIC_SCREEN_OUTPUT_DIR=/data/results
export CRYPTIC_SCREEN_WORKERS=32

# Now commands use these defaults
cryptic-screen nt --input /data/samples
cryptic-screen pm --input /data/unique_seqs
```

## Automation Scripts

If you have scripts that call the old commands, update them:

**Old automation script:**
```bash
#!/bin/bash
cd /data/samples
python /tools/NTSeqScreenMP.py
cd /data/unique_seqs
python /tools/PMScreenMP.py
cd /data/results
python /tools/WinnowScreens.py
```

**New automation script:**
```bash
#!/bin/bash
# No need to change directories!
cryptic-screen nt --input /data/samples
cryptic-screen pm --input /data/unique_seqs
cryptic-screen winnow --nt-results /data/results/NTSeqScreenResults.tsv
```

## Using Configuration Files

For complex pipelines, use a configuration file:

```yaml
# pipeline.yaml
global:
  data_dir: /data/references
  output_dir: /data/results
  workers: 32
  log_level: INFO

nt:
  recursive: true

pm:
  total_cutoff: 5
  per_file_cutoff: 1

winnow:
  nt_cutoff: 20
  pm_cutoff: 15
  metadata: /data/metadata/sra_meta.tsv
```

Then run:
```bash
cryptic-screen --config pipeline.yaml nt --input /data/samples
cryptic-screen --config pipeline.yaml pm --input /data/unique_seqs
cryptic-screen --config pipeline.yaml winnow --nt-results /data/results/NTSeqScreenResults.tsv
```

## Backward Compatibility

The original scripts still work if needed:
```bash
python Cryptic_Screening/NTSeqScreenMP.py
```

But you'll see a deprecation warning suggesting the new command.

## Benefits of Migration

1. **No directory changes needed** - Work from anywhere
2. **All paths configurable** - No hardcoded locations
3. **Better error messages** - Clear validation and helpful hints
4. **Dry run mode** - Test before running
5. **Progress indicators** - See what's happening
6. **Unified logging** - Consistent log format and levels
7. **Environment variables** - Easy automation
8. **Configuration files** - Reproducible pipelines

## Getting Help

```bash
# See all available options
cryptic-screen --help
cryptic-screen nt --help

# Test your migration
cryptic-screen nt --input /data/samples --dry-run

# Debug issues
cryptic-screen --log-level DEBUG nt --input /data/samples
```