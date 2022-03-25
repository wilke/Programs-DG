#!/bin/env python3

import os
import sys

for file in os.listdir(os.getcwd()):
    if file.endswith('.sam') and (not 'sorted' in file) and (not 'clipped' in file):
        in_file = open(file, 'r')
        tiles = {}
        for line in in_file:
            if not line.startswith('@'):
                split_line = line.split("\t")
                if not split_line[2] == '*':
                    count = int(split_line[0].split('=')[-1])
                    start = int(split_line[3])
                    cigar = split_line[5]
                    length = 0
                    run_length = 0
                    for C in cigar: # process sequence based on standard CIGAR line
                        if C == 'M' or C == 'I' or C == 'D' or C == 'S' or C == 'H':

                            if C == 'D' or C == 'M':
                               length += run_length
                               run_length = 0
                            else:
                                run_length = 0
                        else:
                            run_length = (10 * run_length) + int(C)
                    
                    end = start + length - 1
                    try:
                        tiles[start][end] += count
                    except: 
                        try:
                            tiles[start][end] = count
                        except:
                            tiles[start] = {end : count}
        
        if tiles:
            outfile = open(file[:-4]+'.tiles.tsv', 'w')
            for tile in sorted(tiles):
                for end in sorted(tiles[tile]):
                    outfile.write(f"{tile}\t{end}\t{tiles[tile][end]}\n")
            outfile.close