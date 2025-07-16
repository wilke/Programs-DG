#!/usr/bin/env python3
"""
Backward compatibility wrapper for NTSeqScreenMP.py
"""

import sys
import warnings
import subprocess
from pathlib import Path

warnings.warn(
    "NTSeqScreenMP.py is deprecated. Use 'cryptic-screen nt' instead.\n"
    "Example: cryptic-screen nt --input . --output NTSeqScreenResults.tsv\n"
    "To suppress this warning, use the original script directly:\n"
    "  python Cryptic_Screening/NTSeqScreenMP.py",
    DeprecationWarning,
    stacklevel=2
)

# Run the original script
original_script = Path(__file__).parent.parent / 'Cryptic_Screening' / 'NTSeqScreenMP.py'
if original_script.exists():
    subprocess.run([sys.executable, str(original_script)] + sys.argv[1:])
else:
    print(f"Error: Original script not found at {original_script}", file=sys.stderr)
    sys.exit(1)