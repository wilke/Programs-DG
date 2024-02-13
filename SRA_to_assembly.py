#!/bin/env python3
import os
import sys

SRA_list = [
"SRR26363703",
"SRR26363704",
"SRR26363705",
"SRR26363706",
"SRR26363707",
]
copied_sras = []
print(len(SRA_list))
SRA_list = list(set(SRA_list))
print(len(SRA_list))
# fh_test = open('test.tsv', 'w')
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if '_nt_calls' in file: # or "seqs.tsv" in file  # : file.endswith('.sam') or file.endswith('sam.gz') or file.endswith('cram'): # or 
            if file.split('.')[0] in SRA_list and not 'Assemblies' in subdir:
                print(os.path.join(subdir, file))
                os.system(f"cp {os.path.join(subdir, file)} /mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/{file}")
                copied_sras.append(file.split('.')[0])
                
with open("Assemblies/Assembled_meta.tsv", "w") as meta_out:
    with open("SRA_meta.tsv", "r") as meta:
        for line in meta:
            if line.split("\t")[0] in SRA_list:
                meta_out.write(line)

for sra in SRA_list:
    if not sra in copied_sras:
        print(sra)