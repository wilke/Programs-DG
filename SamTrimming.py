#!/bin/env python3

import os
import sys
import pandas as pd

SRAs = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.sam') and (not 'sorted' in file) and (not '.cut.' in file):
        samp = file[:-4]
        acc_num = file.split('.')[0]
        SRAs.append(acc_num)

        if not os.path.exists(f"{samp}.fasta"):
            os.system(f"python /mnt/g/MU_WW/Programs/SAM2Fasta.py {file}")

        # os.system(f"cutadapt -g file:/mnt/g/MU_WW/SARS2/Primers/NEBArticv3_for_plus.fasta -a file:/mnt/g/MU_WW/SARS2/Primers/NEBArticv3_rev_plus.fasta -o {samp}.cut.fasta {samp}.fasta &>> {samp}_trim_info.txt") # -e .2
        # os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {samp}.cut.fasta -o {samp}.cut.sam --secondary=no --sam-hit-only")
        # os.system(f"python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --read 0 --min_count 1 --min_samp_abund 0 --min_col_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {samp}.cut.sam")

        # SRAs.append(file.split('.')[0])
        # if not os.path.exists(f"{file[:-4]}.sorted.sam"):
            # os.system(f'samtools sort -n {file} -o {file[:-4]}.sorted.sam')
        # os.system(f'primerclip /mnt/g/MU_WW/SARS2/SRAs/Wastewater/Collected_primer_masterfile.tsv -s {file[:-4]}.sorted.sam {file[:-4]}.Allclipped.sam')
# for SRA in SRAs:
    # print(SRA)

# SRA_collectors = {}

# fh_meta = open("/mnt/g/MU_WW/SARS2/SRAs/Wastewater/SraRunTable.csv", 'r')
# for line in fh_meta:
    # splitline = line.split(",")
    # if splitline[0] in SRAs:
        # SRA_collectors[splitline[0]] = splitline[7]

# fh_meta.close()

for SRA in SRAs:
    if not os.path.exists(f"{SRA}.SARS2.wg.cut.fasta"):
        # if SRA_collectors[SRA] == 'BIOBOT ANALYTICS':
        os.system(f"cutadapt -g file:/mnt/g/MU_WW/SARS2/Primers/NEBArticv3_for_plus.fasta -a file:/mnt/g/MU_WW/SARS2/Primers/NEBArticv3_rev_plus.fasta -o {SRA}.SARS2.wg.cut.fasta {SRA}.SARS2.wg.fasta &>> {SRA}_trim_info.txt") # e .2
        # else:
            # print(SRA)
            # print('v4')
            # os.system(f"cutadapt -g file:/mnt/g/MU_WW/SARS2/SRAs/Wastewater/NEBArticv4_for_plus.fasta -a file:/mnt/g/MU_WW/SARS2/SRAs/Wastewater/NEBArticv4_for_plus.fasta -o {SRA}.SARS2.wg.cut.fasta -e .2 {SRA}.SARS2.wg.fasta &>> {SRA}_trim_info.txt")

    if not os.path.exists(f"{SRA}.SARS2.wg.cut.sam"):
        os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {SRA}.SARS2.wg.fasta -o {SRA}.SARS2.wg.cut.sam --secondary=no --sam-hit-only")

    if not os.path.exists(f"{SRA}.SARS2.wg.cut_nt_calls.tsv"):
        os.system(f"python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 0 --indel 0 --covar 1 --max_covar 1 --nt_call 1 --ntvar 1 --read 0 --min_count 1 --min_samp_abund 0.01 --min_col_abund 0 --ntabund 0.01 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 -S {SRA}.SARS2.wg.cut.sam")