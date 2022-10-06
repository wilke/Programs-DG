#!/bin/env python3
import os
import sys

SRA_list = [
"SRR20681669",
"SRR20681672",
"SRR20681689",
"SRR20681703",
"SRR20681796",
"SRR20681805",
"SRR20681904",
"SRR20681918",
"SRR20681925",
"SRR20698910",
"SRR20966724",
]
SRA_list = list(set(SRA_list))
# fh_test = open('test.tsv', 'w')
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('_nt_calls.tsv'): # file.endswith('.sam') or file.endswith('sam.gz') or
            if  file.split('.')[0] in SRA_list and not 'Assemblies' in subdir:
                print(os.path.join(subdir, file))
                os.system(f"cp {os.path.join(subdir, file)} /mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/{file}")
fh_meta = open("/mnt/g/MU_WW/SARS2/SRAs/Wastewater/SraRunTable.csv", 'r')
meta_out = open('Collected_SRA_meta.csv','w')
for line in fh_meta:
    splitline = line.split(",")
    if splitline[0] in SRA_list:
        meta_out.write(line)
        #print(line)
        # SRA_collectors[splitline[0]] = splitline[7]
fh_meta.close()
meta_out.close()