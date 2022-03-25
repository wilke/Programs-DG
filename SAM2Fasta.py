#!/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
        description='SAM file'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='SAM'
)

args = parser.parse_args()
file_name = (args.file.name)[:-4]
outfile = open(file_name+".fasta","w")
print(file_name)
for line in args.file:
    if not line.startswith("@"):
        splitline = line.split("\t")
        
        try:
            outfile.write(f">{splitline[2]}:{splitline[0]}\n{splitline[9]}\n")
        except:
            pass
outfile.close()