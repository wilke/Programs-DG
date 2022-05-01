#!/bin/env python3

import os
import sys
from multiprocessing import Process, Pool
import itertools

def SRR_proc(subdir, file):
    if '.fa' in file:
        if not '.fasta' in file:
            SRA = file.split('.')[0]
            if not os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg.sam')):
                os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {os.path.join(subdir, file)} -o {os.path.join(subdir, SRA+'.SARS2.wg.sam')} --sam-hit-only --secondary no")
            # if (not os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg_covars.tsv'))) and os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg.sam')):
                # os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 1 --max_covar 2 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, SRA+'.SARS2.wg.sam')}")
            if (not os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg_nt_calls.tsv'))) and (not os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg_unique_seqs.tsv'))) and os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg.sam')):
                os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, SRA+'.SARS2.wg.sam')}")
            elif (not os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg_nt_calls.tsv'))) and os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg.sam')):
                os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, SRA+'.SARS2.wg.sam')}")
            elif (not os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg_unique_seqs.tsv'))) and os.path.isfile(os.path.join(subdir, SRA+'.SARS2.wg.sam')):
                os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 0 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {os.path.join(subdir, SRA+'.SARS2.wg.sam')}")


for subdir, dirs, files in os.walk(os.getcwd()):
    with Pool(processes=3) as pool:
        pool.starmap(SRR_proc, zip(itertools.repeat(subdir),  files))

