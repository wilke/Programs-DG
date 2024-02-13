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
name = (args.file.name)
print(name)

samp_count = 0
file_count = 0

ID_dict = {}

meta_fh = name.split(".")[0] + ".metadata.tsv"

if os.path.isfile(meta_fh):
    print(meta_fh)
    with open(meta_fh, "r") as meta_in:
        for line in meta_in:
            split_line = line.split("\t")
            ID_dict[split_line[0]] = split_line[2] 


ID = ""
seq = ""
seq_dict = {}
for line in args.file:
    if line.startswith('>'):
        if seq:
            seq_dict[ID] = seq
            seq = ""
            ID = ""
        splitline = line.strip().split(" ")
        ID = splitline[0].strip(">")
        try:
            ID = ID_dict[ID]
        except:
            pass

    else:
        seq += line.replace("R", "N").replace("Y", "N").replace("W", "N").replace("S", "N").replace("K", "N").replace("M", "N")

if seq and ID:
    seq_dict[ID] = seq


for seq_id in seq_dict:
    with open(seq_id.replace("/", ":")+".fa", "w") as out_fh:
        out_fh.write(">")
        out_fh.write(seq_id)
        out_fh.write("\n")
        out_fh.write(seq_dict[seq_id])
        