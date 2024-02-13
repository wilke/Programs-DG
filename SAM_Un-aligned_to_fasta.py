#!/bin/env python3

import os
import sys

# in_file = open("Bat.all.to_contig.sam", "r")
for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam'):
        print(file)
        in_file = open(file, "r")
        out_file = open(file+".miss.fa", "w")
        for line in in_file:
            split_line = line.split('\t')
            if split_line[1] == '4':
                out_file.write(">" + line.split('\t')[0]+"\n")
                out_file.write(line.split('\t')[9]+"\n")

        in_file.close()
        out_file.close()

