#!/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
        description='Split SAM file into smaller SAM files'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='SAM'
)

args = parser.parse_args()

line_count = 0
file_name = (args.file.name)[:-4]
outfile = open(file_name+"_1.sam","w")
outfile_count = 1
print(file_name)
for line in args.file:
    if not line.startswith("@"):
        line_count += 1
        if line_count % 50000 == 0:
            outfile.close()
            outfile_count += 1
            outfile = open(file_name+"_"+ str(outfile_count) +".sam","w")
        outfile.write(line)
outfile.close()
    