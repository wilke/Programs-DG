#!/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
        description='process Sam files for variant information'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='SRA Acc List'
)

args = parser.parse_args()
setID = args.file.name.split(".")[0].split("_")[3]
# checker = 0
if not os.path.isdir("./"+setID):
    os.system("mkdir "+setID)
for line in args.file:
    SRA_ID = line.strip("\n\r")
    print(SRA_ID)
    # checker += 1
    # if checker > 9:
        # break
    if os.path.isfile(SRA_ID+'_1.fastq.gz'):
        os.system("gzip -d " + SRA_ID + "_1.fastq.gz")
    if os.path.isfile(SRA_ID+'_2.fastq.gz'):
        os.system("gzip -d " + SRA_ID + "_2.fastq.gz")
    if os.path.isfile(SRA_ID+'.fastq.gz'):
        os.system("gzip -d " + SRA_ID + ".fastq.gz")

    if os.path.isfile(SRA_ID+'_1.fastq'):
        os.system("/mnt/d/MU_WW/vsearch/bin/vsearch --fastq_mergepairs " + SRA_ID+ "_1.fastq --reverse " + SRA_ID + "_2.fastq --fastqout " + SRA_ID + ".merged.fq --fastqout_notmerged_fwd " + SRA_ID + ".nmfwd.fq --fastqout_notmerged_rev " + SRA_ID + ".nmrev.fq --fastq_minlen 40")
        os.system("cat " + SRA_ID + ".merged.fq " + SRA_ID + ".nmfwd.fq " + SRA_ID + ".nmrev.fq > "+SRA_ID+".all.fq")
        os.system("/mnt/d/MU_WW/vsearch/bin/vsearch --derep_fulllength "+SRA_ID+".all.fq --output "+SRA_ID+".derepmin1.fa --sizeout --minuniquesize 1")
        # os.system("rm " + SRA_ID + "_1.fastq")
        # os.system("rm " + SRA_ID + "_2.fastq")


    elif os.path.isfile(SRA_ID+'.fastq'):
        os.system("/mnt/d/MU_WW/vsearch/bin/vsearch --derep_fulllength "+SRA_ID+".fastq --output "+SRA_ID+".derepmin1.fa --sizeout --minuniquesize 1")

    if os.path.isfile(SRA_ID+'.derepmin1.fa'):
        os.system("minimap2 -a /mnt/d/MU_WW/SARS2/GP.fasta "+SRA_ID+".derepmin1.fa --sam-hit-only --secondary=no -o "+SRA_ID+".sam")
        os.system("gzip *.fa")
        os.system("rm " + SRA_ID + "*fastq")
        os.system("rm " + SRA_ID + ".*.fq")
        os.system("mv "+SRA_ID+"* ./"+setID+"/")



