#!/bin/env python3

import os
import sys

SAMs = []

for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('bt.sam'):
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
                    if len(splitline[9]) == 110: # (splitline[1] == "0" or splitline[1] == "16" or splitline[1] == "4") and 
                        species = splitline[9] # 'Unmatched'
                        counts = int(splitline[0].split('-')[-1])
                        total += counts
                        matchline = splitline[2] # .split('_')
                        # if matchline[0] == "*":
                            # species = 'Unmatched'
                        # else:
                            # species = splitline[2]
                        try:
                            all_species[species]["total"] += counts
                        except:
                            all_species[species] = {
                                        "total" : counts,
                                        "match" : matchline,
                                        }
                        else:
                            if not matchline in all_species[species]["match"]:
                                print(f"different mapping of {species} to {all_species[species]['match']} and {matchline}")
                                all_species[species]["match"] += "+"+matchline
                        
                        try:
                            Species_dict_dict[samp_name][species] += counts
                        except:
                            Species_dict_dict[samp_name][species] = counts
        Species_dict_dict[samp_name]['total'] = total
        samp.close()

if all_species:
    rs_fh = open('Enteros.tsv', "w")
    rs_fh.write(f"Sequence\tmatch\tTotal Coun t")
    for samps in Species_dict_dict:
        rs_fh.write(f"\t{samps}({Species_dict_dict[samps]['total']})\t")
    rs_fh.write("\n")
    rs_fh.write("\t")
    for samps in Species_dict_dict:
        rs_fh.write(f"\tCount\tAbundance")
    rs_fh.write("\n")
    sorted_species = sorted(all_species, key=lambda x: all_species[x]["total"], reverse=True)
    for spec in sorted_species:
        if int(all_species[spec]['total']) >= 100:
            rs_fh.write(f"{spec}\t{all_species[spec]['match']}\t{all_species[spec]['total']}")
            for samps in Species_dict_dict:
                try:
                    rs_fh.write(f"\t{Species_dict_dict[samps][spec]}\t{Species_dict_dict[samps][spec]/Species_dict_dict[samps]['total']}")
                except:
                    rs_fh.write(f"\t\t")

            rs_fh.write("\n")
        else:
            break
            
