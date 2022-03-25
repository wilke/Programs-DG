#!/bin/env python3

import os
import sys


for file in os.listdir(os.getcwd()):
    if file.endswith('.sam'):
        file_name = file[:-4]
        in_file = open(file, 'r')
        outfile = open(file_name+"trimmed.fasta","w")
        print(file_name)
        for line in in_file:
            if not line.startswith("@"):
                splitline = line.split("\t")
                
                try:
                    splitline[9]
                except:
                    pass
                else:
                    if len(splitline[9]) > 60:
                        outfile.write(f">{splitline[0]}\n{splitline[9][25:-24]}\n")
        outfile.close()