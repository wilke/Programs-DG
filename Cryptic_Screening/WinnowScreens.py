#!/bin/env python3

import os
import sys

NT_count_cutoff = 10
PM_total_count_cutoff = 10
PM_line_count_cutoff = 2

NT_dict = {}
base_path = os.path.dirname(os.path.realpath(__file__))
meta_dict = {}
with open(f"{base_path}/Meta/SRA_meta.tsv", "r") as meta:
    for line in meta:
        split_line = line.split("\t")
        meta_dict[split_line[0]] = line


if os.path.isfile("NTSeqScreenResults.tsv"):
    with open("NTSeqScreenResults.tsv", "r") as nt_in:
        cur_acc = ""
        for line in nt_in:
            line = line.strip().split("\t")
            if len(line) == 1:
                cur_acc = line[0]
                NT_dict[cur_acc] = {}
            else:
                if cur_acc:
                    NT_dict[cur_acc][line[0]] = int(line[1])

                else:
                    print("Error reading NT screen file: results without accosiated accession\nexiting")
else:
    print("NT screen file not found")

NT_list = []

if not NT_list:
    for entry in NT_dict:
        for nt in NT_dict[entry]:
            NT_list.append(nt)
        break

with open("NTSeqScreen_report.tsv", "w") as nt_out:
    nt_out.write("Accession\tSRA Acc\tBioProject Acc\tBioSample Acc\tSubmitter\tCollection Date\tGeo Loc\tPopulation\tReads\tRelease Date\tLoad Date")
    for nt in NT_list:
        nt_out.write("\t")
        nt_out.write(nt)
    nt_out.write("\n")
    for acc in NT_dict:
        if max(NT_dict[acc].values()) < NT_count_cutoff:
            continue
        nt_out.write(acc)
        nt_out.write("\t")
        try:
            meta_entry = meta_dict[acc].strip()
            nt_out.write(meta_entry)
        except:
            nt_out.write("no metadata found")
        for nt in NT_list:
            nt_out.write("\t")
            nt_out.write(str(NT_dict[acc][nt]))
        nt_out.write("\n")

meta_missing = 0
for file in os.listdir(os.getcwd()):
    if file.endswith("_hits.tsv"):
        report_name = file.replace("_hits.tsv", "_report.tsv")
        out_lines = []
        linked_header = ""
        with open(file, "r") as pm_in:
            if file.startswith("Linked_PM_"):
                linked_header = pm_in.readline()
            entry_set = []
            count = 0
            acc = ""
            for line in pm_in:
                split_line = line.split("\t")
                if len(split_line) == 1:
                    if entry_set and count >= PM_total_count_cutoff:
                        try:
                            meta_entry = meta_dict[acc]
                            entry_set[1:1] = [meta_entry]
                        except:
                            entry_set[1:1] = ["Metadata not found\n"]
                            meta_missing += 1
                        out_lines += entry_set

                    entry_set = [line]
                    acc = split_line[0].split("/")[-1].split(".")[0]
                    count = 0

                elif int(split_line[1]) >= PM_line_count_cutoff:
                    entry_set.append(line)

                    count += int(split_line[1])
            if entry_set and count >= PM_total_count_cutoff:
                try:
                    meta_entry = meta_dict[acc]
                    entry_set[1:1] = [meta_entry]
                except:
                    entry_set[1:1] = ["Metadata not found\n"]
                    meta_missing += 1
                out_lines += entry_set
                

        if out_lines:
            with open(report_name, "w") as pm_out:
                if linked_header:
                    pm_out.write(linked_header)
                pm_out.writelines(out_lines)

print(f"{meta_missing} missing meta")