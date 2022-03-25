#!/bin/env python3

import os
import sys

for file in os.listdir(os.getcwd()):
    if file.endswith(".sam"):
        SRA_ID = file[0:-4]
        if not (os.path.isfile(SRA_ID+'_unique_seqs.tsv') or os.path.isfile(SRA_ID+'_nt_calls.tsv')):
            os.system("python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --indel 0 --covar 0 --chim_rm 0 --mp 1 -S " +file)
            # print(SRA_ID)