#!/bin/env python3

import os
import sys

#### split fasta into paired seq fastas
fh_main_in = open('LongReads.fa', 'r')

dict_entries = {}
for line in fh_main_in: ### get sequences
    if line.startswith('>'):
        refID = line.strip("\n\r")
        try:
            dict_entries[refID]
        except:
            dict_entries[refID] = ''
        else:
            i = 1
            newrefID = refID + '.' + str(i)
            while newrefID in dict_entries.keys():
                i += 1
                newrefID = refID + '.' + str(i)
            refID =  newrefID
            dict_entries[refID] = ''
    else:
        dict_entries[refID] += line.strip("\n\r")
fh_main_in.close()
if dict_entries:
    for seqID in dict_entries:
        fh_pair_out = open(f"Pair_{seqID[1:]}.fasta", 'w')
        fh_pair_out.write(">Parent\n")
        fh_pair_out.write(dict_entries[">Parent"])
        fh_pair_out.write("\n")
        fh_pair_out.write(seqID)
        fh_pair_out.write("\n")
        fh_pair_out.write(dict_entries[seqID])
        fh_pair_out.write("\n")
        fh_pair_out.close()

#### mafft paired seq fastas

for file in os.listdir(os.getcwd()):
    if file.startswith("Pair_") and file.endswith(".fasta"):
        os.system(f"mafft {file} > {file}.aln") #### mafft paired seq fastas
        os.system(f"python /mnt/g/MU_WW/Programs/fasta2tab.py {file}.aln")
        os.system(f"perl /mnt/g/MU_WW/SNAP/SNAP.pl {file}.aln.tsv") #### snap aligned paired fastas
os.system("cat summary.Pair*tsv.tsv > SNAP.Summary.all.tsv")
os.system(f"python /mnt/g/MU_WW/Programs/SummaryCleaner.py")

