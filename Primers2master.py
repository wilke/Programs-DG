#!/bin/env python3

import os
import sys

rc_dict = {
'A' : 'T',
'T' : 'A',
'C' : 'G',
'G' : 'C',
'U' : 'A'
}

def rc_seq(seq):
    rev_seq = seq[::-1]
    rc_string = ''
    for c in rev_seq.upper():
        try:
            rc_string += rc_dict[c]
        except:
            rc_string += c
    return(rc_string)

### NC_045512.2	25	301	covid19genome_0-200_s0_M1	3	25	covid19genome_0-200_s0_M1F	301	322	covid19genome_200-29703_s7490_U_88R	AAAGGTTTATACCCTTCCCAGG	AGGCAAACTGAGTTGGACGTG
Target_chrome = 'NC_045512.2'
for file in os.listdir(os.getcwd()):
    # if file == 'NEBArctiicv3.sam':
        # primer_name = 'NEBArctiicv3'
        # in_file = open(file, 'r')
        # entry_dict = {}
        # for line in in_file:
            # if not line.startswith('@'):
                # split_line = line.split("\t")
                # pair_name = '_'.join(split_line[0].split('_')[:2])
                # side = ''
                # if 'left' in split_line[0].lower():
                    # side = 'left'
                    # seq = split_line[9]
                # elif 'right' in split_line[0].lower():
                    # side = 'right'
                    # seq = rc_seq(split_line[9])
                # start_pos = int(split_line[3])
                # length = int(split_line[5].strip('M'))
                # try:
                    # entry_dict[pair_name]
                # except:
                    # entry_dict[pair_name] = {}
                    # entry_dict[pair_name][side] = [[split_line[0], seq, start_pos, length]]
                # else:
                    # try:
                        # entry_dict[pair_name][side]
                    # except:
                        # entry_dict[pair_name][side] = [[split_line[0], seq, start_pos, length]]
                    # else:
                        # entry_dict[pair_name][side].append([split_line[0], seq, start_pos, length])
        
        # if entry_dict:
            # out_file = open(primer_name+'masterfile.tsv', 'w')
            # for pair_name in entry_dict:
                # for for_primer in entry_dict[pair_name]['left']:
                    # fp_start = for_primer[2]
                    # fp_end = fp_start + for_primer[3]
                    # for rev_primer in entry_dict[pair_name]['right']:
                        # rp_prestart = rev_primer[2]-1
                        # out_file.write(f"{Target_chrome}\t{fp_end}\t{rp_prestart}\t{pair_name}\t{fp_start}\t{fp_end}\t{for_primer[0]}\t{rp_prestart}\t{rp_prestart+rev_primer[3]}\t{rev_primer[0]}\t{for_primer[1]}\t{rev_primer[1]}\n")
            # out_file.close()
        # in_file.close()
    if file == 'SARS-CoV-2.Arcticv4.primer.bed':
        primer_name = 'NEBArctiicv4'
        in_file = open(file, 'r')
        entry_dict = {}
        for line in in_file:
            split_line = line.split("\t")
            pair_name = '_'.join(split_line[3].split('_')[:2])
            side = ''
            if 'left' in split_line[3].lower():
                side = 'left'
            elif 'right' in split_line[3].lower():
                side = 'right'
            seq = split_line[6].strip("\n\r")
            start_pos = int(split_line[1])
            end_pos = int(split_line[2])
            try:
                entry_dict[pair_name]
            except:
                entry_dict[pair_name] = {}
                entry_dict[pair_name][side] = [[split_line[3], seq, start_pos, end_pos]]
            else:
                try:
                    entry_dict[pair_name][side]
                except:
                    entry_dict[pair_name][side] = [[split_line[3], seq, start_pos, end_pos]]
                else:
                    entry_dict[pair_name][side].append([split_line[3], seq, start_pos, end_pos])

                
        if entry_dict:
            out_file = open(primer_name+'masterfile.tsv', 'w')
            for pair_name in entry_dict:
                for for_primer in entry_dict[pair_name]['left']:
                    fp_start = for_primer[2]+1
                    fp_end = for_primer[3]+1
                    for rev_primer in entry_dict[pair_name]['right']:
                        rp_prestart = rev_primer[2]
                        out_file.write(f"{Target_chrome}\t{fp_end}\t{rp_prestart}\t{pair_name}\t{fp_start}\t{fp_end}\t{for_primer[0]}\t{rp_prestart}\t{rev_primer[3]}\t{rev_primer[0]}\t{for_primer[1]}\t{rev_primer[1]}\n")
            out_file.close() 
        
        in_file.close()
        
        