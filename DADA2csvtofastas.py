#!/bin/env python3

import os
import sys

infile = open("results.csv", "r")
samps = {}
seqs = []
linecount = 0
for line in infile:
    splitline = line.strip("\n\r").split("\t")
    if linecount == 0:
        for cell in splitline:
            seqs.append(cell[1:-1])
    else:
        sampName = splitline[0][1:-1]
        samps[sampName] = {}
        for i in range(1, len(seqs)):
            if not splitline[i] == '0':
                samps[sampName][seqs[i-1]] = int(splitline[i])
    
    
    linecount += 1
infile.close()

for samp in samps:
    outfile = open(samp+".fasta", "w")
    num = 1
    for seq in samps[samp]:
        outfile.write(f">{num}_count={samps[samp][seq]}\n")
        outfile.write(f"{seq}\n")
        outfile.write("\n")
    outfile.close()