#!/bin/env python3
import os
import sys


GSV_dict = {}

with open("/mnt/g/MU_WW/ViralMetagenome/mmc3.tsv", "r") as GSV_fh:
    GSV_fh.readline()
    GSV_fh.readline()
    for line in GSV_fh:
        GSV_dict[line.split("\t")[0]] = line.strip()

for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam'):
        print(file)
        hits = {}
        total_counts = 0
        with open(file, "r") as sam_fh:
            for line in sam_fh:
                if not line.startswith("@"):
                    split_line = line.split("\t")
                    try:
                        count = int(split_line[0].split("-")[-1].split("=")[-1])
                    except:
                        count = 1
                    if split_line[1] in ("0", "16") and int(split_line[4]) > 50:
                        try:
                            hits[split_line[2]] += count
                        except:
                            hits[split_line[2]] = count
                    total_counts += count
        sorted_hits = sorted(hits, key=lambda x: int(hits[x]), reverse=True)
        with open(file+".counts.tsv", "w") as out_fh:
            out_fh.write(f"Match\tcounts\tmapped fraction\n")
            for hit in sorted_hits:
                out_fh.write(f"{hit}\t{hits[hit]}\t{int(hits[hit])/total_counts}")
                if hit in GSV_dict:
                    out_fh.write("\t")
                    out_fh.write(GSV_dict[hit])
                out_fh.write("\n")