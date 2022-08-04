#!/bin/env python3

import os
import sys

SRA_list = [
"ERR9861727",
"ERR9861721",
"ERR9861713",
"ERR9861710",
"ERR9861709",
"ERR9861708",
"ERR9861707",
"ERR9861706",
"ERR9861705",
"ERR9861704",
"ERR9861701",
"ERR9861699",
"ERR9861698",
"ERR9861697",
"ERR9861672",
"ERR9861669",
"ERR9813728",
"ERR9813649",
"ERR9813631",
"ERR9813607",
"ERR9813552",
"ERR9813413",
"ERR9813375",
"ERR9813306",
"ERR9813292",
"ERR9813259",
"ERR9813240",
"ERR9813093",
"ERR9812959",
"ERR9812944",
"ERR9812936",
"ERR9812921",
"ERR9812915",
"ERR9812738",
"ERR9812659",
"ERR9812452",
]
SRA_list = list(set(SRA_list))
# fh_test = open('test.tsv', 'w')
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.sam') or file.endswith('sam.gz') or file.endswith('_nt_calls.tsv'):
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