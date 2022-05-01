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
def get_ref():
    seq = ''
    for line in open('/mnt/g/MU_WW/SARS2/SARS2.fasta', 'r'):
        if not line.startswith('>'):
            seq += line.strip("\n\r")
    return(seq)
def rc_seq(seq):
    rev_seq = seq[::-1]
    rc_string = ''
    for c in rev_seq.upper():
        try:
            rc_string += rc_dict[c]
        except:
            rc_string += c
    return(rc_string)

for file in os.listdir(os.getcwd()):
    if file.endswith('_masterfile.tsv'):
        infile = open(file, 'r')
        forplus = open(file[:-15]+'_for_plus.fasta', 'w')
        forminus = open(file[:-15]+'_for_minus.fasta', 'w')
        revplus = open(file[:-15]+'_rev_plus.fasta', 'w')
        revminus = open(file[:-15]+'_rev_minus.fasta', 'w')
    
        forwards = {}
        reverses =  {}


        for line in infile:
            splitline = line.strip("\n\r").split("\t")
            if not splitline[10] in forwards:
                forwards[splitline[10]] = splitline[6]
            if not splitline[11] in reverses:
                reverses[splitline[11]] = splitline[9]
        
        for forseq in forwards:
            forplus.write(f">{forwards[forseq]}_plus\n^{forseq}\n")
            forminus.write(f">{forwards[forseq]}_minus\n{rc_seq(forseq)}$\n")
        
        for revseq in reverses:
            revplus.write(f">{reverses[revseq]}_plus\n{rc_seq(revseq)}$\n")
            revminus.write(f">{reverses[revseq]}_minus\n^{revseq}\n")
        
        infile.close()
        forplus.close()
        forminus.close()
        revplus.close()
        revminus.close()
    if file.endswith('.bed'):
        infile = open(file, 'r')
        forplus = open(file[:-4]+'_for_plus.fasta', 'w')
        forminus = open(file[:-4]+'_for_minus.fasta', 'w')
        revplus = open(file[:-4]+'_rev_plus.fasta', 'w')
        revminus = open(file[:-4]+'_rev_minus.fasta', 'w')
    
        ref = get_ref()
        forwards = {}
        reverses =  {}
        
        for line in infile:
            splitline = line.strip("\n\r").split("\t")
            if 'LEFT' in line.upper():
                forwards[splitline[3]] = ref[int(splitline[1])-1:int(splitline[2])]
            if 'RIGHT' in line.upper():
                reverses[splitline[3]] = ref[int(splitline[1])-1:int(splitline[2])]
        
        for forseq in forwards:
            forplus.write(f">{forseq}_plus\n^{forwards[forseq]}\n")
            forminus.write(f">{forseq}_minus\n{rc_seq(forwards[forseq])}$\n")
        
        for revseq in reverses:
            revplus.write(f">{revseq}_plus\n{reverses[revseq]}$\n")
            revminus.write(f">{revseq}_minus\n^{rc_seq(reverses[revseq])}\n")
        
        infile.close()
        forplus.close()
        forminus.close()
        revplus.close()
        revminus.close()
        
