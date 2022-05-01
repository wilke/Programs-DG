#!/bin/env python3

import os
import sys

seq_dict = {}
cur_samp = ''
omi_rbd = ["K417N", "N440K", "G446S", "S477N", "T478K", "E484A", "Q493R", "G496S", "Q498R", "N501Y", "Y505H", "T547K", "notQ498Y", "notQ498H", "notQ493R"]
in_file = open('20220323_K444TandY449RandN460KandE484AandF486PandQ493KandQ493RandQ498HandQ498YandN501SandN501TandY505H.tsv', 'r')
for line in in_file:
    if line.startswith('/mnt/'):
        cur_samp = line.strip('\n\r')
        seq_dict[cur_samp] = []
    else:
        omi_matches = 0
        for pm in omi_rbd:
            if 'not' in pm:
                if pm.strip('not') in line:
                    omi_matches -= 1
            elif pm in line:
                omi_matches += 1
        if omi_matches < ((len(line.split('\t')[0].split(' '))-3)*.6): # and len(line.split('\t')[0].split(' ')) > :
            seq_dict[cur_samp].append(line)
in_file.close()

out_file = open('20220323_K444TandY449RandN460KandE484AandF486PandQ493KandQ493RandQ498HandQ498YandN501SandN501TandY505H.NoOmi.tsv', 'w')
for samp in seq_dict:
    if seq_dict[samp]:
        out_file.write(samp+'\n')
        for line in seq_dict[samp]:
            out_file.write(line)
out_file.close()

