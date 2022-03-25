#!/bin/env python3

import os
import sys
ref = ''
ref_fh = open('/mnt/g/MU_WW/SARS2/SARS2.fasta', 'r')
for line in ref_fh:
    if not line.startswith('>'):
        ref = ref + line.strip('\n\r')
ref_fh.close()
nt_call_dict = {}
for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('_nt_calls.tsv'):
        in_file = open(file, "r")
        consensus = {}
        samp = '_'.join(file.split('_')[:-2])
        mode = 0
        for line in in_file:
            splitline = line.split("\t")
            try:
                splitline[2]
            except:
                pass
            else:
                if splitline[0] == 'Position':
                    for i in range(0, len(splitline)):
                        nt_call_dict[splitline[i]] = i
                    # if splitline[2] == "AA POS":
                        # mode = 1
                    # elif splitline[2] == "AAs":
                        # mode = 2
                else:
                    if (int(splitline[nt_call_dict['Total']]) >= 5) and ( int(splitline[nt_call_dict[splitline[nt_call_dict['Primary NT']]]]) > .5 *int(splitline[nt_call_dict['Total']])):
                        consensus[int(splitline[0])] = splitline[nt_call_dict['Primary NT']]
                    
                    # if mode == 0:
                        # consensus[int(splitline[0])] = splitline[8]
                    # elif mode == 1:
                        # consensus[int(splitline[0])] = splitline[10]
                    # else:
                        # consensus[int(splitline[0])] = splitline[9]
        in_file.close()
        out_file = open(samp+"_consensus.fasta", "w")
        out_ref_file = open(samp+"_consensus_ref.fasta", "w")
        out_file.write(f">{samp}\n")
        out_ref_file.write(f">{samp}_ref_filled\n")
        for i in range(1, len(ref)+1):
            try:
                out_file.write(f"{consensus[i]}")
                out_ref_file.write(f"{consensus[i]}")
            except:
                out_file.write("N")
                out_ref_file.write(ref[i-1])
        out_file.write("\n")
        out_ref_file.write("\n")
        out_file.close()
        out_ref_file.close()