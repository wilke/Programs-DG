#!/bin/env python3

import os
import sys


for file in os.listdir(os.getcwd()):
    if "_consensus_ref.fasta" in file:
        SRR = file.split("_consensus_ref")[0]
        
        os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {file} -o {SRR}.Con.sam --sam-hit-only --secondary=no")
        os.system(f"python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 0 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 0 --chim_rm 0 --deconv 0 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 1 --read 1 -S {SRR}.Con.sam")

        # os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta {file} -o {SRR}.Con.Spike.sam --sam-hit-only --secondary=no")
        # os.system(f"python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 0 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 1 --read 1 -S {SRR}.Con.Spike.sam")

        # os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2orf1ab.fasta {file} -o {SRR}.Con.ORF1ab.sam --sam-hit-only --secondary=no")
        # os.system(f"python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2orf1ab.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 0 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 1 --read 1 -S {SRR}.Con.ORF1ab.sam")
