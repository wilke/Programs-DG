#!/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
        description='SAM file'
)

parser.add_argument(
    '-i', '--file',
    type=str,
    help='SAM'
)

args = parser.parse_args()
file_names = []
if args.file:
    file_names = [(args.file.name)[:-4]]
else:
    for file in os.listdir(os.getcwd()):
        if file.endswith('.sam'):
            file_names.append(file)

for file_name in file_names:
    in_file = open(file_name, 'r')
    outfile = open(file_name[:-4]+".fasta","w")
    print(file_name)
    for line in in_file:
        if not line.startswith("@"):
            splitline = line.split("\t")
            
            try:
                outfile.write(f">{splitline[2]}:{splitline[0]}\n{splitline[9]}\n")
            except:
                pass
    outfile.close()
    in_file.close()