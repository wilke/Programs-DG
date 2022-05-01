#!/bin/env python3

import os
import sys
import argparse


parser = argparse.ArgumentParser(
        description='Dereplicates fasta or fastq reads with counts'
)

parser.add_argument(
    'in_file',
    type=argparse.FileType('r'),
    help='fasta or fastq file'
)
parser.add_argument(
    'out_file',
    type=argparse.FileType('w'),
    help='output fasta name'
)
parser.add_argument(
    'min_count',
    type=int,
    default=1,
    help='min count for a sequence to be included.  default 1'
)

args = parser.parse_args()

seq_dict = {}
total_reads = 0
# firstline = args.in_file.readline()
if args.in_file.startswith('>'):
    cur_seq = ''
    for line in args.in_file:
        if line.startswith('>') and cur_seq:
            try:
                seq_dict[cur_seq] += 1
            except:
                seq_dict[cur_seq] = 1
            cur_seq = ''
            total_reads += 1
        else:
            cur_seq += line.strip('\n\r')
    if cur_seq:
        try:
            seq_dict[cur_seq] += 1
        except:
            seq_dict[cur_seq] = 1
        
elif args.in_file.startswith('@'):
    mode = 'seq'
    cur_seq = ''
    for line in args.in_file:
        if mode == 'seq':
            if line.startswith('+'):
                mode = 'qual'
                try:
                    seq_dict[cur_seq] += 1
                except:
                    seq_dict[cur_seq] = 1
                cur_seq = ''
                total_reads += 1
            else:
                cur_seq += line.strip('\n\r')
        elif mode == 'qual':
            if line.startswith('@'):
                mode = 'seq'
                
else:
    print('input file not recognized as fasta/q')
args.in_file.close()

print(f"{total_reads} sequences collected.  Dereplicated to {len(seq_dict)} unique sequences.  Writing output file")
sorted_seqs = sorted(seq_dict.items(), key=lambda x:x[1], reverse=True )

counter = 1
for seq in sorted_seqs:
    if seq_dict[seq[0]] >= args.min_count:
        args.out_file.write(f">{counter}-{seq_dict[seq[0]]}\n{seq[0]}\n")
        counter += 1
    else:
        break
args.out_file.close()