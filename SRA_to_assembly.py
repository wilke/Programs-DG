#!/bin/env python3
import os
import sys

SRA_list = [
    "SRR26353682",
    "ERR12076557",
    "SRR26353618",
    "SRR26363864",
    "SRR26353622",
    "SRR26353692",
    "SRR26353592",
    "SRR26419239",
]
copied_sras = []
print(len(SRA_list))
SRA_list = list(set(SRA_list))
print(len(SRA_list))

directory = "/mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/"

if not os.path.exists(directory):
    os.makedirs(directory)

# fh_test = open('test.tsv', 'w')
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.sam') or file.endswith('sam.gz') or file.endswith('cram'): # or '_nt_calls' in file: # or "seqs.tsv" in file  # : 
            if file.split('.')[0] in SRA_list and not 'Assemblies' in subdir:
                print(os.path.join(subdir, file))
                if not os.path.isfile(f"/mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/{file}"):
                    os.system(f"cp {os.path.join(subdir, file)} /mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/{file}")
                    copied_sras.append(file.split('.')[0])
            
with open("Assemblies/Assembled_meta.tsv", "w") as meta_out:
    try:
        with open("SRA_meta.tsv", "r") as meta:
            for line in meta:
                if line.split("\t")[0] in SRA_list:
                    meta_out.write(line)
    except:
        print("writing meta failed")

for sra in SRA_list:
    if not sra in copied_sras:
        print(sra)