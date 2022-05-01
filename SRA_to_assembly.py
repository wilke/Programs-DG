#!/bin/env python3

import os
import sys

SRA_list = [
'SRR17688887',
'SRR17688888',
'ERR5922175',
'ERR5922177',
'ERR5922185',
'ERR5922187'
]
SRA_list = list(set(SRA_list))
# fh_test = open('test.tsv', 'w')
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.sam') or file.endswith('_nt_calls.tsv'):
            if  file.split('.')[0] in SRA_list and not 'Assemblies' in subdir:
                print(os.path.join(subdir, file))
                os.system(f"cp {os.path.join(subdir, file)} /mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/14/{file}")

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