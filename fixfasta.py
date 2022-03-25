#!/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
        description='fasta file'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='fasta'
)

args = parser.parse_args()
file_name = (args.file.name)[:-6]
lines = []

for line in args.file:
    if line[0].isdigit():
        lines.append("\n>"+line.strip("\n\r ")+"\n")
    else:
        lines.append(line.strip("\n\r"))

args.file.close()

outfile = open(file_name + "x.fasta", "w")
for line in lines:
    outfile.write(line)
        
outfile.close()