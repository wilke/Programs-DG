#!/bin/env python3

import os
import sys
import argparse
import time
from multiprocessing import Process, Pool
import itertools

parser = argparse.ArgumentParser(
        description='x'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='SRA Acc list or metadata table'
)

args = parser.parse_args()

def fetch(SRA_ID):
    if os.path.isfile(SRA_ID+'.collapsed.fa.gz') or os.path.isfile(SRA_ID+'.collapsed.fa'):
        print(SRA_ID+" found")
        if not os.path.isfile(SRA_ID+'.SARS2.wg.sam'):
            if not os.path.isfile(SRA_ID+'.collapsed.fa.gz'):
                os.system('gzip ' +SRA_ID+'.collapsed.fa')
            os.system("minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta "+SRA_ID+".collapsed.fa.gz --sam-hit-only --secondary=no -o "+SRA_ID+".SARS2.wg.sam")
            # os.system("gzip *.fa")
            os.system("rm " + SRA_ID + "*fastq")
            os.system("rm " + SRA_ID + ".*.fq")
    elif os.path.isfile(SRA_ID+'.SARS2.wg.sam'):
        print(SRA_ID+" found, no derep")
    else:


        print(SRA_ID)
        print(time.ctime(time.time()))
        # os.system('gzip -d ' +SRA_ID+'*.gz')
        os.system('prefetch ' + SRA_ID)
        os.system('fasterq-dump ' + SRA_ID + ' --split-3')
        time.sleep(5)

        if os.path.isfile(SRA_ID+'_1.fastq') and os.path.isfile(SRA_ID+'_2.fastq'):
            print('paired reads')
            os.system(f"bash /mnt/g/MU_WW/BBTools/bbmap/bbmerge.sh qtrim=t in1={SRA_ID}_1.fastq in2={SRA_ID}_2.fastq  out={SRA_ID}.merge.fq outu1={SRA_ID}.un1.fq outu2={SRA_ID}.un2.fq")
            os.system(f"cat {SRA_ID}.merge.fq {SRA_ID}.un1.fq {SRA_ID}.un2.fq > {SRA_ID}.all.fq")
            if os.path.isfile(SRA_ID+'.fastq'):
                os.system(f"cat {SRA_ID}.fastq >> {SRA_ID}.all.fq")
            os.system(f"python /mnt/g/MU_WW/Programs/derep.py {SRA_ID}.all.fq {SRA_ID}.collapsed.fa 1")

        elif os.path.isfile(SRA_ID+'.fastq'):
            print('singleton reads')
            os.system(f"python /mnt/g/MU_WW/Programs/derep.py {SRA_ID}.fastq {SRA_ID}.collapsed.fa 1")

        elif os.path.isfile(SRA_ID+'_1.fastq'):
            print('singleton reads')
            os.system(f"python /mnt/g/MU_WW/Programs/derep.py {SRA_ID}_1.fastq {SRA_ID}.collapsed.fa 1")

        elif os.path.isfile(SRA_ID+'_2.fastq'):
            print("------------------------------------------ ")
            print("------------------------------------------ ")
            print("------------------------------------------ ")
            print("Single pair orphanned")
            print("Single ")
            print("Single ")
            print("------------------------------------------ ")
            print("------------------------------------------ ")
            print("------------------------------------------ ")

        if os.path.isfile(SRA_ID+'.collapsed.fa'):
            os.system("minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta "+SRA_ID+".collapsed.fa --sam-hit-only --secondary=no -o "+SRA_ID+".SARS2.wg.sam")
            # os.system("gzip *.fa")
            os.system("rm " + SRA_ID + "*fastq")
            os.system("rm " + SRA_ID + ".*.fq")
        elif os.path.isfile(SRA_ID+'.collapsed.fa.gz'):
            os.system("minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta "+SRA_ID+".collapsed.fa.gz --sam-hit-only --secondary=no -o "+SRA_ID+".SARS2.wg.sam")
            os.system("rm " + SRA_ID + "*fastq")
            os.system("rm " + SRA_ID + ".*.fq")
        print(SRA_ID+" done")

SRA_IDs = []
for line in args.file:
    SRA_IDs.append(line.strip("\n\r"))

for SRA in SRA_IDs:
    fetch(SRA)
# with Pool(processes=1) as pool:
    # pool.starmap(fetch, zip(SRA_IDs))