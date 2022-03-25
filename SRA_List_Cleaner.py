#!/bin/env python3

import os
import sys

done_SRAs = []
try:
    done_SRAs_fh = open('Done_SRAs.txt', 'r')
    for line in done_SRAs_fh:
        if not line.strip('\n\r') in done_SRAs:
            done_SRAs.append(line.strip('\n\r'))
    done_SRAs_fh.close()
except:
    pass
    
try:
    done_SRAs_fh = open('Done_SRAs.csv', 'r')
    for line in done_SRAs_fh:
        if not line.split(',')[0] in done_SRAs:
            done_SRAs.append(line.split(',')[0])
    done_SRAs_fh.close()
except:
    pass

todo_SRAs = []
try:
    table_fh = open('SraRunTable.csv', 'r')
    outfile = open('Table_clean.csv', 'w')
    for line in table_fh:
        SRR = line.split(',')[0]
        if (not SRR in done_SRAs) and (not ('PRJNA748354' in line or 'PRJNA715712' in line or 'PRJNA809641' in line)):
            outfile.write(line)
            if not SRR.lower() == 'run':
                todo_SRAs.append(SRR)
        if 'PRJNA748354' in line or 'PRJNA715712' in line:
            if SRR not in done_SRAs:
                done_SRAs.append(SRR)
    outfile.close()
    table_fh.close()
except:
    pass
    
outfile = open('List_clean.txt', 'w')
try:
    list_fh = open('SRR_Acc_List.txt', 'r')
    for line in list_fh:
        if not line.strip('\n\r') in done_SRAs:
            outfile.write(line)
    list_fh.close()
except:
    for SRR in todo_SRAs:
        outfile.write(SRR)
        outfile.write("\n")

outfile.close()
    
