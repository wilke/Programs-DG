#!/bin/env python3

import os
import sys

infile = open("SNAP.Summary.all.tsv", 'r')
outfile = open("SNAP.Summary.all.cleaned.tsv", 'w')
outfile.write("Compare\t\tSequences_names\t\tSd\tSn\tS\tN\tps\tpn\tds\tdn\tds/dn\tps/pn\n")
for line in infile:
    if (not line.startswith("Compare")) and (not line.startswith("Averages")):
        for entry in line.strip("\n\r").split(' '):
            if entry:
                outfile.write(f"{entry}\t")
        outfile.write("\n")
infile.close()
outfile.close()