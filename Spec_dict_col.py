#!/bin/env python3

import os
import sys

spec_dict_file = open("Species_dict.tsv", "r")
spec_dict = {}
for line in spec_dict_file:
    splitline = line.strip("\r\n").split("\t")
    try:
        splitline[1]
    except:
        try:
            spec_dict[splitline[0]]
        except:
            spec_dict[splitline[0]] = "Unknown"
    else:
        try:
            spec_dict[splitline[0]]
        except:
            spec_dict[splitline[0]] = splitline[1]
spec_dict_file.close()

new_file = open("Species_dict2.tsv", "w")
for entry in spec_dict:
    new_file.write(f"{entry}\t{spec_dict[entry]}\n")
new_file.close()