#!/bin/env python3

import os
import sys
import argparse
import time

parser = argparse.ArgumentParser(
        description='x'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='SRA Acc List'
)

args = parser.parse_args()

for line in args.file:
    SRA_ID = line.strip("\n\r")
    if os.path.isfile(SRA_ID+'.derepmin1.fa.gz') or os.path.isfile(SRA_ID+'.derepmin1.fa'):
        print(SRA_ID+" found")
        if not os.path.isfile(SRA_ID+'.SARS2.wg.sam'):
            os.system('gzip ' +SRA_ID+'.derepmin1.fa')
            os.system("minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta "+SRA_ID+".derepmin1.fa.gz --sam-hit-only --secondary=no -o "+SRA_ID+".SARS2.wg.sam")
            os.system("gzip *.fa")
    elif os.path.isfile(SRA_ID+'.SARS2.wg.sam'):
        print(SRA_ID+" found, no derep")
    else: 


        print(SRA_ID)
        # os.system('gzip -d ' +SRA_ID+'*.gz')
        os.system('prefetch ' + SRA_ID)
        os.system('fastq-dump ' + SRA_ID + ' --split-files')
        time.sleep(3)
        # # os.system('gzip -d ' +SRA_ID+'.derepmin1.fa.gz')
        if os.path.isfile(SRA_ID+'_1.fastq'):
            os.system("/mnt/g/MU_WW/vsearch/bin/vsearch --fastq_mergepairs " + SRA_ID+ "_1.fastq --reverse " + SRA_ID + "_2.fastq --fastqout " + SRA_ID + ".merged.fq --fastqout_notmerged_fwd " + SRA_ID + ".nmfwd.fq --fastqout_notmerged_rev " + SRA_ID + ".nmrev.fq --fastq_minlen 40")
            os.system("cat " + SRA_ID + ".merged.fq " + SRA_ID + ".nmfwd.fq " + SRA_ID + ".nmrev.fq > "+SRA_ID+".all.fq")
            os.system("/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength "+SRA_ID+".all.fq --output "+SRA_ID+".derepmin1.fa --sizeout --minuniquesize 1")

        # elif os.path.isfile(SRA_ID+'.fastq'):
            # os.system("/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength "+SRA_ID+".fastq --output "+SRA_ID+".derepmin1.fa --sizeout --minuniquesize 1")
            
        # # else:
            

        # if os.path.isfile(SRA_ID+'.derepmin1.fa'):
            # os.system("minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta "+SRA_ID+".derepmin1.fa --sam-hit-only --secondary=no -o "+SRA_ID+".SARS2.wg.sam")
            # os.system("gzip *.fa")
            # os.system("rm " + SRA_ID + "*fastq")
            # os.system("rm " + SRA_ID + ".*.fq")

