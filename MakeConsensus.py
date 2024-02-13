#!/bin/env python3

import os
import sys

ref = ""

with open("/mnt/g/MU_WW/SARS2/SARS2.fasta", "r") as ref_in:
    ref_in.readline()
    for line in ref_in:
        ref += line.strip()

samp = os.getcwd().split("/")[-1]

changes = {}
insertions = {}
dels = {}
max_count = 0
max_abund = 0

cut_off = .001

for ubiq in (True, False):

    with open(f"{samp}_cryptic_covar.tsv", "r") as in_fh:
        in_fh.readline()
        in_fh.readline()
        for line in in_fh:
            split_line = line.split("\t")
            if int(split_line[3]) > max_count:
                max_count = int(split_line[3])
            if float(split_line[4]) > max_abund:
                max_abund = float(split_line[4])
        print(max_count)
        print(max_abund)
        print(max_abund*cut_off)

        in_fh.seek(0)
        in_fh.readline()
        in_fh.readline()

        for line in in_fh:

            split_line = line.split("\t")
            if (not " " in split_line[1]) and (ubiq or not "ubiq" in line):
                abund = float(split_line[4])
                position = int(split_line[0].strip("*"))
                nt_var = split_line[1].split("|")[0]
                if "del" in nt_var:
                    end = int(nt_var.strip("del").split("-")[1])
                    for i in range(position, end+1):
                        try:
                            dels[i] += abund
                        except:
                            dels[i] = abund
                else:
                    if "insert" in nt_var:
                        try:
                            insertions[position]
                        except:
                            insertions[position] = { nt_var.split("-")[1].strip("insert") : abund }
                        else:
                            try:
                                insertions[position][nt_var.split("-")[1].strip("insert")] += abund
                            except:
                                insertions[position][nt_var.split("-")[1].strip("insert")] = abund


                    else:
                        if not nt_var[-1] == "N":
                            try:
                                changes[position]
                            except:
                                changes[position] = {nt_var[-1] : abund}
                            else:
                                try:
                                    changes[position][nt_var[-1]] += abund
                                except:
                                    changes[position][nt_var[-1]] = abund
    passed = {}

    for pos in changes:
        for nt in changes[pos]:
            if changes[pos][nt] >= (cut_off * max_abund):
                try:
                    passed[pos].append(nt)
                except:
                    passed[pos] = {nt : changes[pos][nt]}

    for pos in dels:
        if dels[pos] >= (cut_off * max_abund):
            try:
                passed[pos]["del"] = dels[pos]
            except:
                passed[pos] = {"del" : dels[pos]}


    passed_ins = {}
    for pos in insertions:
        for ins in insertions[pos]:
            if insertions[pos][ins] >= (cut_off * max_abund):
                try:
                    passed_ins[pos][ins] = insertions[pos][ins]
                except:
                    passed_ins[pos] = {ins : insertions[pos][ins]}

    consensus = ""

    for i in range(0, len(ref)):
        pos = i + 1
        if pos in passed:
            if len(passed[pos]) == 1:
                if not "del" in passed[pos]:
                    consensus += list(passed[pos])[0]
            else:
                sorted_changes = sorted(passed[pos], key=lambda x: passed[pos][x], reverse=True)
                if not sorted_changes[0] == "del":
                    consensus += sorted_changes[0]
        else:
            consensus += ref[i]

        if pos in passed_ins:
            if len(passed_ins[pos]) == 1:

                consensus += list(passed_ins[pos])[0]
            else:
                sorted_changes = sorted(passed_ins[pos], key=lambda x: passed_ins[pos][x], reverse=True)
                consensus += sorted_changes[0]

    ubiq_tag = ""
    if not ubiq:
        ubiq_tag = ".noubiq"
    file_name = f"{samp}{ubiq_tag}.consensus.fa"
    with open(file_name, "w") as con_out:
        con_out.write(f">{samp}\n")
        con_out.write(consensus)