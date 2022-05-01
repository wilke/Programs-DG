#!/bin/env python3

import os
import sys
# ref = ''
# ref_fh = open('/mnt/g/MU_WW/SARS2/SARS2.fasta', 'r')
# for line in ref_fh:
    # if not line.startswith('>'):
        # ref = ref + line.strip('\n\r')
# ref_fh.close()
nt_call_dict = {}
for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('_nt_calls.tsv'):
        in_file = open(file, "r")
        plurality = {}
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
                    if (int(splitline[nt_call_dict['Total']]) >= 5): # and ( int(splitline[(nt_call_dict['Total'])+2]) > .5 *int(splitline[nt_call_dict['Total']])):
                        try:
                            plurality[int(splitline[0])]
                        except:
                            if not splitline[1] == '-': 
                                plurality[int(splitline[0])] = splitline[nt_call_dict['Primary NT']]
                            elif ( int(splitline[(nt_call_dict['Total'])+2]) > .5 *int(splitline[nt_call_dict['Total']])):
                                print(samp+': insertion in plurality at position '+splitline[0])
                                plurality[int(splitline[0])] = splitline[nt_call_dict['Primary NT']]
                        else:
                            if splitline[1] != '-':
                                plurality[int(splitline[0])+.5] = splitline[nt_call_dict['Primary NT']]
                            
                            
        in_file.close()
        out_file = open(samp+"_plurality.fasta", "w")
        # out_ref_file = open(samp+"_plurality_ref.fasta", "w")
        out_file.write(f">{samp}\n")
        # out_ref_file.write(f">{samp}_ref_filled\n")
        last_position = 0
        for position in plurality:
            if last_position != 0 and (int(position)-last_position > 1):
                while ((int(position)-last_position > 1)):
                    out_file.write("N")
                    last_position += 1
            if plurality[position] != '-':
                out_file.write(f"{plurality[position]}")
            last_position = position
        # for i in range(1, len(ref)+1):
            # try:
                # out_file.write(f"{plurality[i]}")
                # # out_ref_file.write(f"{plurality[i]}")
            # except:
                # out_file.write("N")
                # # out_ref_file.write(ref[i-1])
        out_file.write("\n")
        # out_ref_file.write("\n")
        out_file.close()
        # out_ref_file.close()