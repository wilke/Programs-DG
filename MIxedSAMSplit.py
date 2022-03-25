#!/bin/env python3

import os
import sys

SAMs = []
for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam'):
        SAMs.append(file)

for SAM in SAMs:
    amp_count = 0
    if "RBD" in SAM.upper():
        amp_count += 1
    if "NTD" in SAM.upper():
        amp_count += 1
    if "S1S2" in SAM.upper():
        amp_count += 1
    if amp_count > 1 or 'mixed' in SAM.lower():
        NTDlines = []
        RBDlines = []
        S1S2lines = []
        headers = []
        if '_RBD' in SAM:
            samp = SAM.split('_RBD')[0]
        elif '_Mixed' in SAM:
            samp = SAM.split('_Mixed')[0]
        elif 'RBD' in SAM:
            samp = SAM.split('RBD')[0]
        elif 'Mixed' in SAM:
            samp = SAM.split('Mixed')[0]
        elif 'NTD' in SAM:
            samp = SAM.split('NTD')[0]
        
        # split_name = SAM.split('_')
        # if 'RBD'NTD' in split_name[0]:
            # wwtp = split_name[0].split("RBD")[0]
            # date = split_name[0].split("RBDNTD")[1]
            # month = int(date.split('-')[0])
            # day = int(''.join([c for c in date.split('-')[1][:2] if c.isdigit()]))
        # else:
            # wwtp = split_name[0]
            # date = split_name[1]
            # month = int(date.split('-')[0])
            # day = int(''.join([c for c in date.split('-')[1][:2] if c.isdigit()]))
        # print(SAM)
        # print(day)
        infile = open(SAM, 'r')
        print(SAM)
        for line in infile:
            if line.startswith('@'):
                headers.append(line)
            else:
                split_line = line.split('\t')
                if int(split_line[3]) < 1000:
                    NTDlines.append(line)
                elif int(split_line[3]) < 1600:
                    RBDlines.append(line)
                elif int(split_line[3]) < 2500:
                    S1S2lines.append(line)
        infile.close()

        if NTDlines:
            outfile = open(f'{samp}_NTD.sam', 'w')
            for line in headers:
                outfile.write(line)
            for line in NTDlines:
                outfile.write(line)
            outfile.close()
        if RBDlines:
            outfile = open(f'{samp}_RBD.sam', 'w')
            for line in headers:
                outfile.write(line)
            for line in RBDlines:
                outfile.write(line)

            outfile.close()
        if S1S2lines:
            outfile = open(f'{samp}_S1S2.sam', 'w')
            for line in headers:
                outfile.write(line)
            for line in S1S2lines:
                outfile.write(line)

            outfile.close()