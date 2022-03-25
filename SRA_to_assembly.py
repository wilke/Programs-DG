#!/bin/env python3

import os
import sys

SRA_list = [
'SRR14789293',
'SRR14789297',
'SRR15128983',
'SRR15129106',
'SRR15202278',
'SRR15202279',
'SRR15291257',
'SRR15291304',
'SRR15384049',
'SRR15434992',
'SRR15529311',
'SRR15529348',
'SRR15529394',
'SRR15709811',
'SRR15709845',
'SRR16038150',
'SRR16038156',
'SRR16641296',
'SRR17688888',
'SRR17689171',
'SRR15128983',
'SRR15129106',
'SRR15202278',
'SRR15202279',
'SRR15291257',
'SRR15291304',
'SRR15384002',
'SRR15384049',
'SRR15434992',
'SRR15529311',
'SRR15529348',
'SRR15529394',
'SRR15709811',
'SRR15709845',
'SRR16038150',
'SRR16038156',
'SRR16542132',
'SRR16639006',
'SRR16641296',
'SRR17120722',
'SRR17689171'
]
SRA_list = list(set(SRA_list))
# fh_test = open('test.tsv', 'w')
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.sam') or file.endswith('_nt_calls.tsv'):
            if  file.split('.')[0] in SRA_list and not 'Assemblies' in subdir:
                print(os.path.join(subdir, file))
                os.system(f"cp {os.path.join(subdir, file)} /mnt/g/MU_WW/SARS2/SRAs/Wastewater/Assemblies/13/{file}")

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