#!/bin/env python3

import os
import sys

base_dir = os.getcwd()
cur_dir = ""
for subdir, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.sam') or file.endswith('.fa') or file.endswith('.fq') or file.endswith('.fasta') or file.endswith('.fastq') or file.endswith('.tsv') or file.endswith('.txt'):
            if not subdir == base_dir:
                if not cur_dir == subdir:
                    cur_dir = subdir
                    print(cur_dir)
                os.system(f"gzip '{os.path.join(subdir, file)}'")