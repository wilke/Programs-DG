#!/bin/env python3

import os
import sys

SAMs = []
spec_dict = {}
spec_dict_file = open("/mnt/g/MU_WW/SARS2/Species_dict.tsv", "r")
for line in spec_dict_file:
    splitline = line.strip("\r\n").split("\t")
    spec_dict[splitline[0]] = splitline[1]
spec_dict_file.close()

for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam'):
        SAMs.append(file)

Species_dict_dict = {}
all_species = {}

if SAMs:
    for sam in SAMs:
        print(sam)
        samp_name = sam[:-4]
        samp = open(sam, "r")
        Species_dict_dict[samp_name] = {}
        total = 0
        for line in samp:
            if not line.startswith('@'):
                splitline = line.strip("\n\r").split("\t")
                try:
                    splitline[4]
                except:
                    pass
                else:
                    if (splitline[1] == "0" or splitline[1] == "16" or splitline[1] == "4"):
                        species = 'Unmatched'
                        counts = int(splitline[0].split('-')[-1])
                        total += counts
                        matchline = splitline[2].split('_')
                        if matchline[0] == "*":
                            species = 'Unmatched'
                        elif int(splitline[4]) in (0, 1, 2, 3, 4, 255):
                            species = 'Poor match'
                        elif 'de:f:' in line:
                            if float(splitline[19][5:]) > .02:
                                species = 'Poor match'
                            else:
                                if len(matchline) > 1:
                                    if matchline[2] == "PREDICTED:":
                                        species = matchline[3]+' '+matchline[4]
                                    elif matchline[1][0].isdigit():
                                        species = matchline[2]+" "+matchline[3]
                                    else:
                                        species = matchline[1]+' '+matchline[2]
                                else:
                                    species = matchline[0]
                        elif len(matchline) > 1:
                            if matchline[2] == "PREDICTED:":
                                species = matchline[3]+' '+matchline[4]
                            elif matchline[1][0].isdigit():
                                species = matchline[2]+" "+matchline[3]
                            else:
                                species = matchline[1]+' '+matchline[2]
                        else:
                            species = matchline[0]
                        all_species[species] = 1
                        try:
                            Species_dict_dict[samp_name][species] += counts
                        except:
                            Species_dict_dict[samp_name][species] = counts
        Species_dict_dict[samp_name]['total'] = total
        samp.close()

if all_species:
    rs_fh = open('rRNA_Species.tsv', "w")
    rs_fh.write(f"Species\t")
    for samps in Species_dict_dict:
        rs_fh.write(f"\t{samps}({Species_dict_dict[samps]['total']})\t")
    rs_fh.write("\n")
    rs_fh.write("\t")
    for samps in Species_dict_dict:
        rs_fh.write(f"\tCount\tAbundance")
    rs_fh.write("\n")
    sorted_species = sorted(all_species)
    for spec in sorted_species:
        rs_fh.write(spec)
        try:
            rs_fh.write("\t"+spec_dict[spec])
        except:
            rs_fh.write("\t")
        for samps in Species_dict_dict:
            try:
                rs_fh.write(f"\t{Species_dict_dict[samps][spec]}\t{Species_dict_dict[samps][spec]/Species_dict_dict[samps]['total']}")
            except:
                rs_fh.write(f"\t\t")

        rs_fh.write("\n")
