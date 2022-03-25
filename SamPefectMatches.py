#!/bin/env python3

import os
import sys

for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam') and not 'peferctmatches' in file:
        print(file)
        Matchlines = []
        sam_fh = open(file, "r")
        for line in sam_fh:
            if not line.startswith("@"):
                splitline = line.split("\t")
                if not 'S' in splitline[5] and not 'H' in splitline[5] and not 'D' in splitline[5] and not 'I' in splitline[5]:
                    seqlen = splitline[5].strip('M')
                    for i in range(10, len(splitline)):
                        if 'cs:Z' in splitline[i]:
                            if splitline[i].split('::')[-1] == seqlen:
                                Matchlines.append(line)
        sam_fh.close()
        
        if Matchlines:
            newfilename = file[:-3] + 'peferctmatches.sam'
            sam_fh = open(newfilename, "w")
            for line in Matchlines:
                sam_fh.write(line)
            sam_fh.close()