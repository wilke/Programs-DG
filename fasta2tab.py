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
dict_entries = {}
for line in args.file:
    if line.startswith('>'):
        refID = line[1:].strip("\n\r")
        try:
            dict_entries[refID]
        except:
            dict_entries[refID] = ''
        else:
            i = 1
            newrefID = refID + '.' + str(i)
            while newrefID in dict_entries.keys():
                i += 1
                newrefID = refID + '.' + str(i)
            refID =  newrefID
            dict_entries[refID] = ''
    else:
        dict_entries[refID] += line.strip("\n\r")
        

if dict_entries:
    outfile = open(name+".tsv","w")
    for ID in dict_entries:
        outfile.write(f"{ID}\t{dict_entries[ID]}\n")
    outfile.close()