#!/bin/env python3

import os
import sys

# samps = os.getcwd().split("/")[-1]

# screens = ["C24044T", "C25936G"]

# ATCG : no aa 2345, aa 4567 
# try:
    # infile = open(samps+"_NSP12_P323P.txt","r")

for file in os.listdir(os.getcwd()):
    if ".derepmin1.fa" in file:
        SRR = file.split(".")[0]
        if not os.path.exists(SRR+".wgs_nt_calls.tsv"):
            os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {SRR}.derepmin1.fa.gz -o {SRR}.wgs.sam --sam-hit-only --secondary=no")
            os.system(f"python /mnt/g/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 0 -S {SRR}.wgs.sam")
            # outfile = open(samps+"_"+C24044T_C25936G_NSP12_P323P.txt","w")

            # for line in infile:
                # SRR = line.split(".")[0]
                # os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta {SRR}.derepmin1.fa.gz -o {SRR}.wgs.sam")
                # os.system(f"python /mnt/g/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 0 -S {SRR}.wgs.sam")
        ntcall_file = open(SRR+".wgs_nt_calls.tsv", "r")
        passes = 0
        for ntline in ntcall_file:
            if ntline.split("\t")[0] == "24044":
                if int(ntline.split("\t")[3]) / int(ntline.split("\t")[7]) >= .25:
                    passes = passes + 1
                
            if ntline.split("\t")[0] == "25936":
                if int(ntline.split("\t")[5]) / int(ntline.split("\t")[7]) >= .25:
                    passes = passes + 1
                # outfile.write(SRR)
                # outfile.write("\n")
        if passes == 2:
            print(f"{SRR} passed")
            os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta {SRR}.derepmin1.fa.gz -o {SRR}.Spike.sam --sam-hit-only --secondary=no")
            os.system(f"python /mnt/g/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 1 -S {SRR}.Spike.sam")
    
            os.system(f"minimap2 -a /mnt/g/MU_WW/SARS2/SARS2orf1ab.fasta {SRR}.derepmin1.fa.gz -o {SRR}.ORF1ab.sam --sam-hit-only --secondary=no")
            os.system(f"python /mnt/g/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2orf1ab.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 1 -S {SRR}.ORF1ab.sam")
        
        ntcall_file.close()
        
    # infile.close()
            # outfile.close
# except:
    # print(f"Failed {samps} run")