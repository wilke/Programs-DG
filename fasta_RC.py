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


for file in os.listdir(os.getcwd()):
    if file.endswith('.fasta') and not file.endswith('_rc.fasta'):
        in_file = open(file, 'r')
        out_file = open(file[:-6]+'_rc.fasta', 'w')
        fasta_seq = ''
        fasta_id = ''
        for line in in_file:
            if line.startswith('>'):
                if fasta_id and fasta_seq:
                    fasta_seq = fasta_seq[::-1]
                    rc_string = ''
                    for c in fasta_seq.upper():
                        try:
                            rc_string += rc_dict[c]
                        except:
                            rc_string += c
                    out_file.write(fasta_id)
                    out_file.write(rc_string)
                    out_file.write("\n")
                fasta_id = line
                fasta_seq = ''
            else:
                fasta_seq += line.strip("\n\r")
        in_file.close()
        out_file.close()