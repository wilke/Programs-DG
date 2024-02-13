#!/bin/env python3

import os
import sys
from multiprocessing import Process, Pool
import itertools

def SRR_proc(subdir, file):
    if file.endswith('.sam'):
        if not '.fasta' in file:
            SRA = file.split('.')[0]
            # if not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg.sam')):
                # os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {os.path.join(subdir, file)} -o {os.path.join(subdir, file.strip(".sam")+'wg.sam')} --sam-hit-only --secondary no")
            # if (not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg_covars.tsv'))) and os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg.sam')):
                # os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 1 --max_covar 2 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, file.strip(".sam")+'wg.sam')}")
            if (not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'_nt_calls.tsv'))) or (not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'_unique_seqs.tsv'))):
                os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 1 --max_covar 1 --nt_call 1 --min_count 1 --use_count 0 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, file)}")
            # elif (not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg_nt_calls.tsv'))) and os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg.sam')):
                # os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, file.strip(".sam")+'wg.sam')}")
            # elif (not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg_unique_seqs.tsv'))) and os.path.isfile(os.path.join(subdir, file.strip(".sam")+'wg.sam')):
                # os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, file.strip(".sam")+'wg.sam')}")


for subdir, dirs, files in os.walk(os.getcwd()):
    sam_files = []
    for file in files:
        if file.endswith('.sam'):
            SRA = file.split('.')[0]
            if ((not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'_nt_calls.tsv'))) or (not os.path.isfile(os.path.join(subdir, file.strip(".sam")+'_unique_seqs.tsv')))):
                sam_files.append(os.path.join(subdir, file))
    print(len(sam_files))
    if len(sam_files) < 20:
        print(sam_files)
    with Pool(processes=2) as pool:
        pool.starmap(SRR_proc, zip(itertools.repeat(subdir), sam_files))

