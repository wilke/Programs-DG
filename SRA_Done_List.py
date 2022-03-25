#!/bin/env python3

import os
import sys

SRA_list = []

for file in os.listdir(os.getcwd()):
    if file.endswith('.txt') and '_List' in file:
        infile = open(file, 'r')
        for line in infile:
            if not line.strip('\n\r') in SRA_list:
                SRA_list.append(line.strip('\n\r'))
        infile.close()

outfile = open('Done_SRAs.txt', 'w')
for line in SRA_list:
    outfile.write(line+'\n')
outfile.close()