#!/bin/env python3

import os
import sys


for file in os.listdir(os.getcwd()):
    if file.endswith('.k2_seq_matched_tax.txt') and "minhitgroup" in file:
        count_dict = {}
        with open(file, "r") as in_file:
            for line in in_file:
                split_line = line.strip("\n\r").split("\t")
                try:
                    count = int(split_line[0].split("-")[-1].split("=")[-1])
                    try:
                        count_dict[split_line[1]] += count
                    except:
                        count_dict[split_line[1]] = count
                except ValueError:
                    pass
        with open(f"{file.split('.')[0]}.{file.split('.')[1]}.counts.txt", "w") as out_file:
            sorted_count_dict = sorted(count_dict, key=count_dict.__getitem__, reverse=True)
            for tax in sorted_count_dict:
                out_file.write(f"{tax}\t{count_dict[tax]}\n")