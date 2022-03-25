#!/bin/env python3

import os
import sys

#### split fasta into paired seq fastas
fh_main_in = open('All.S_reads.tsv', 'r')
fh_out = open('All.S_reads.dNdS.tsv', 'w')
fh_out.write("SeqID\tSyn\tNonSyn\tNonSyn2\n")
for line in fh_main_in:
    split_line = line.strip("\n\r").split("\t")
    dS = 0
    dN = 0
    dN2 = 0
    if not split_line[1] =='Reference':
        for PM in split_line[1].split(' '):
            if "(" in PM:
                if 'insert' in PM or 'del' in PM.lower():
                    dN2 += 1
                elif PM.split('(')[1][0] == PM.split('(')[1][-2]:
                    dS += 1
                else:
                    dN += 1
                    dN2 += 1
    fh_out.write(f"{split_line[0]}\t{dS}\t{dN}\t{dN2}\n")




fh_main_in.close()
fh_out.close()