#!/bin/env python3

import os
import sys
import gzip
import multiprocessing as mp
import pysam

pysam.set_verbosity(0)

prev_results = {}
prev_nts = []

all_files = []

if os.path.isfile("NTSeqScreenResults.tsv"):
    with open("NTSeqScreenResults.tsv", "r") as screen_res_in:
        cur_acc = ""
        for line in screen_res_in:
            line = line.strip().split("\t")
            if len(line) ==1:
                line = line[0]
                if not line in prev_results:
                    prev_results[line] = {}
                cur_acc = line
            else:
                if not cur_acc:
                    print("Failed reading previous results: accessionless entries")
                    exit(1)
                elif line[0] in prev_results[cur_acc]:
                    if prev_results[cur_acc][line[0]] < int(line[1]):
                        prev_results[cur_acc][line[0]] = int(line[1])
                        # print("Failed reading previous results: duplicate entry mismatch")
                        # print(cur_acc)
                        # print(line[0])
                        # exit(1)
                else:
                    prev_results[cur_acc][line[0]] = int(line[1])
else:
    open("NTSeqScreenResults.tsv", "w").close()

for entry in prev_results:
    for nt in prev_results[entry]:
        prev_nts.append(nt)
    break



searches = [
    "GTGTGTCATGCCGCTGTTTAAT",
    "TTGTCTGGTTTTAAG",
    "ATGGAGAACGCAGTG",
    "ATCGAGGGTACAG",
    "CCATTTTTGGACCAC",
    "TACGATCGAGGGTACAGTG", # reversion
    "ATTATAGTGCGTGAGCCAGAAGAT", # BA.1
    "ATGTCTCTAAATGGACCCCA", # alpha
    "GCCACTCGGAGTACGATCGA", # delta
    "CGGAGTACGATCGAG", # pre omi
    "GAAAGTGGAGTTTA", # delta 2
    "CTTTACTTCATAGAAG", # XBC
    "AGTCAGTGTGTTAATCTTATAACCAGA", # pre-JN.1*
    "TATATTCTAAGCACACGCCTATTAATTTAG",
    "CGTGAGCCAGAAGAT",
    "ATCGAGGGTACAGT",
    "ATCGAGGGTACAGTG",
    "CAATGGAGATTGATTAAACG",
    ]

if os.path.isfile("NTSeqScreens.txt"):
    with open("NTSeqScreens.txt", "r") as screens_in:
        for line in screens_in:
            line = line.upper().split()[0]
            if not line in searches:
                searches.append(line)

new_nt = False

for nt in searches:
    if not nt in prev_nts:
        new_nt = True
        break

for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".sam") or file.endswith(".sam.gz") or file.endswith(".cram"):
            acc = file.split(".")[0]
            if new_nt or not acc in prev_results:
                all_files.append(os.path.join(subdir, file))

def search_file2(file):
    out_str = ""
    acc = file.split("/")[-1].split(".")[0]
    hits = {}
    for term in searches:
        if (acc in prev_results and not term in prev_results[acc]) or not acc in prev_results:
            hits[term] = 0
            
    if file.endswith(".sam"):
        with open(file, "r") as in_fh:
            for line in in_fh:
                line = line.upper().split("\t")
                if not line[0].startswith("@"):
                    for term in hits:
                        if term.upper() in line[9]:
                            try:
                                count = int(line[0].split("-")[-1].split("=")[-1])
                            except IndexError:
                                count = 1
                            try:
                                hits[term] += count
                            except KeyError:
                                hits[term] = count

    elif file.endswith("sam.gz"):
        with gzip.open(file, "rb") as in_fh:
            for line in in_fh:
                line = line.decode().upper().split("\t")
                if not line[0].startswith("@"):
                    for term in hits:
                        if term.upper() in line[9]:
                            try:
                                count = int(line[0].split("-")[-1].split("=")[-1])
                            except IndexError:
                                count = 1
                            try:
                                hits[term] += count
                            except KeyError:
                                hits[term] = count

    elif file.endswith(".cram"):
        try:
            with pysam.AlignmentFile(file, "rc") as in_fh:
                for line in in_fh:
                    line = str(line).strip().upper().split("\t")
                    if not line[0].startswith("@"):
                        for term in hits:
                            if term.upper() in line[9]:
                                try:
                                    count = int(line[0].split("-")[-1].split("=")[-1])
                                except IndexError:
                                    count = 1
                                try:
                                    hits[term] += count
                                except KeyError:
                                    hits[term] = count

        except:
            print(f"failed to process {file}")

    out_str = acc
    out_str += "\n"
    for hit in hits:
        out_str += f"{hit}\t{hits[hit]}"
        out_str += "\n"
    with open("NTSeqScreenResults.tsv", "a") as out_fh:
        out_fh.write(out_str)
        out_fh.flush()




with mp.Manager() as manager:
    pool = mp.Pool()

    searchings = []

    for file in all_files:
        search = pool.apply_async(search_file2, (file, ))
        searchings.append(search)

    for search in searchings:
        search.get()

    pool.close()
    pool.join()

# clean output
prev_results = {}

with open("NTSeqScreenResults.tsv", "r") as screen_res_in:
    cur_acc = ""
    for line in screen_res_in:
        line = line.strip().split("\t")
        if len(line) == 1:
            line = line[0]
            if not line in prev_results:
                prev_results[line] = {}
            cur_acc = line
        else:
            if not cur_acc:
                print("Failed reading full results: accessionless entries")
                exit(1)
            elif line[0] in prev_results[cur_acc]:
                if prev_results[cur_acc][line[0]] < int(line[1]):
                    prev_results[cur_acc][line[0]] = int(line[1])
                    # print("Failed reading full results: duplicate entries mismatched")
                    # print(cur_acc)
                    # print(line[0])
                    # exit(1)
            else:
                prev_results[cur_acc][line[0]] = int(line[1])


with open("NTSeqScreenResults.tsv", "w") as screen_res_out:
    for acc in prev_results:
        screen_res_out.write(acc)
        screen_res_out.write("\n")
        for nt in prev_results[acc]:
            screen_res_out.write(f"{nt}\t{prev_results[acc][nt]}")
            screen_res_out.write("\n")
    