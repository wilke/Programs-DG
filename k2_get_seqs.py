#!/bin/env python3

import os
import sys

tax_ids = {}

with open("/mnt/g/MU_WW/K2_viral/inspect.txt", "r") as tax_ids_in:
    for line in tax_ids_in:
        if not line.startswith("#"):
            split_line = line.split("\t")
            tax_ids[split_line[4]] = split_line[5].strip(" ")

for file in os.listdir(os.getcwd()):
    if file.endswith('.derep1.fa'):
        samp_name = file.split(".")[0]
        matched_ids = {}
        print(samp_name)
        os.system(f"kraken2 --minimum-hit-groups 25 --db /mnt/g/MU_WW/K2_viral {file} --report {samp_name}.derep1.allv.minhitgroup25.k2report > {samp_name}.derep1.allv.minhitgroup25.k2")
        with open(f"{samp_name}.derep1.allv.minhitgroup25.k2", "r") as in_file:
            for line in in_file:
                if line.startswith("C"):
                    split_line = line.strip("\n\r").split("\t")
                    matched_ids[split_line[1]] = split_line[2]
        with open(file, "r") as fa_in:
            with open(f"{samp_name}.minhitgroup25.k2_seq_matched_tax.txt", "w") as out_file:
                seq_id = ""
                sequence = ""
                for line in fa_in:
                    if line.startswith(">"):
                        if seq_id in matched_ids and sequence:
                            out_file.write(f"{seq_id}\t{tax_ids[matched_ids[seq_id]]}\t{sequence}\n")
                        seq_id = line.strip("\n\r")[1:]
                        sequence = ""
                    else:
                        sequence += line.strip("\n\r")
                if seq_id and sequence and seq_id in matched_ids:
                    out_file.write(f"{seq_id}\t{tax_ids[matched_ids[seq_id]]}\t{sequence}\n")

