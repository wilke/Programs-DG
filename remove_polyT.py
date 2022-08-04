#!/bin/env python3

import os
import sys
# import argparse

# parser = argparse.ArgumentParser(
        # description='Dereplicates fasta or fastq reads with counts'
# )

# parser.add_argument(
    # 'in_file',
    # type=argparse.FileType('r'),
    # help='sam input file'
# )
# parser.add_argument(
    # 'out_file',
    # type=argparse.FileType('w'),
    # help='sam output name'
# )


# args = parser.parse_args()

for file in os.listdir(os.getcwd()):
    if file.endswith(".sam") and not "culled" in file:
        with open(file, "r") as in_file:
            with open(f"{file[:-3]}culled.sam", "w") as out_file:
                for line in in_file:
                    if not line.startswith("@"):
                        if not "TTTTTTTTTT" in line.split("\t")[9].upper():
                            out_file.write(line)
