#!/bin/env python3

import os
import sys
import gzip
import multiprocessing as mp

line_count_threshold = 1
total_count_threshold = 1

subscreen = []

if os.path.isfile("subscreen.txt"):
    with open("subscreen.txt", "r") as redo_fh:
        for line in redo_fh:
            line = line.strip()
            if line:
                subscreen.append(line.split("\t")[0])

    subscreen = list(set(subscreen))

prev_singles = {}
prev_linked = {}

for file in os.listdir(os.getcwd()):
    if file.startswith("Linked_PM_"):
        linked_num = int(file.split("_")[2])
        with open(file, "r") as prev_linked_in:
            pm_line = prev_linked_in.readline().strip()
            try:
                prev_linked[pm_line]
            except:
                prev_linked[pm_line] = [linked_num]
            for line in prev_linked_in:
                if len(line.split("\t")) == 1:
                    prev_linked[pm_line].append(line.strip().split("/")[-1].split(".")[0])

    elif file.endswith("_hits.tsv") or file.endswith("_misses.tsv"):
        split_file = file.split("_")
        if len(split_file) == 2:
            try:
                prev_singles[split_file[0]]
            except:
                prev_singles[split_file[0]] = []
            with open(file, "r") as prev_sings_in:
                for line in prev_sings_in:
                    if len(line.split("\t")) == 1:
                        prev_singles[split_file[0]].append(line.strip().split("/")[-1].split(".")[0])

Sings_file = ""

singles = []

if os.path.isfile("SinglePMs.txt"):
    Sings_file = "SinglePMs.txt"
elif os.path.isfile("/mnt/f/SRA/SARS2/Wastewater/SinglePMs.txt"):
    Sings_file = "/mnt/f/SRA/SARS2/Wastewater/SinglePMs.txt"

if Sings_file:
    with open(Sings_file, "r") as sings_in:
        for line in sings_in:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line:
                singles.append(line)
    singles = list(set(singles))

new_sings = []
for sing in singles:
    if not sing in prev_singles:
        new_sings.append(sing)

Linked_file = ""

if os.path.isfile("LinkedPMs.txt"):
    Linked_file = "LinkedPMs.txt"
elif os.path.isfile("/mnt/f/SRA/SARS2/Wastewater/LinkedPMs.txt"):
    Linked_file = "/mnt/f/SRA/SARS2/Wastewater/LinkedPMs.txt"


used_nums = []
linked = {}
new_linked = []

if Linked_file:
    with open(Linked_file, "r") as linked_in:
        entry = []
        for line in linked_in:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line.isnumeric():
                if entry:
                    entry = [entry[0]] + sorted(list(set(entry[1:])))
                    entry_str = " ".join(entry)
                    if entry_str in prev_linked:
                        linked[prev_linked[entry_str][0]] = [int(entry[0])] + entry[1:]
                        used_nums.append(prev_linked[entry_str][0])
                    else:
                        new_linked.append(entry)
                entry = [line]
            elif line and entry:
                entry.append(line)
            elif line:
                print(line)
                print("Error reading LinkedPMs.txt")
                exit(1)

        if entry:
            entry = [entry[0]] + sorted(list(set(entry[1:])))
            entry_str = " ".join(entry)
            if entry_str in prev_linked:
                linked[prev_linked[entry_str][0]] = [int(entry[0])] + entry[1:]
                used_nums.append(prev_linked[entry_str][0])
            else:
                new_linked.append(entry)



linked_count = 0
new_linked_nums = []

for entry in new_linked:
    entry_str = " ".join(entry)
    while linked_count in used_nums:
        linked_count += 1

    linked[linked_count] = [int(entry[0])] + entry[1:]
    used_nums.append(linked_count)
    new_linked_nums.append(linked_count)

all_files = []



files_read = []
SRAs_found = []
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if (file.endswith('_unique_seqs.tsv') or file.endswith('_unique_seqs.tsv.gz')):
            acc = file.split(".")[0]
            if subscreen and not acc in subscreen:
                continue
            if file in files_read:
                print(f"{file} in {subdir} is a duplicate, processing of duplicate will be skipped")
                continue
            files_read.append(file)
            all_files.append(os.path.join(subdir, file))
            SRAs_found.append(acc)

if subscreen and not len(SRAs_found) == len(subscreen):
    missings = False
    for acc in subscreen:
        if not acc in SRAs_found:
            print(f"{acc} not found")
            missings = True
    if missings:
        print("Missing accessions, exiting")
        exit(0)

subscreen = ""

missing_screen = []

if not (new_linked or new_sings):
    for acc in SRAs_found:
        found = False
        for link in prev_linked:
            if not acc in prev_linked[link]:
                found = True
                missing_screen.append(acc)
                break
        if not found:
            for pm in prev_singles:
                if not acc in prev_singles[pm]:
                    missing_screen.append(acc)
                    break
else:
    missing_screen = SRAs_found

SRAs_found = ""
print(len(all_files))


for variant in linked:
    PM_list = str(linked[variant][0]) + " " + " ".join(linked[variant][1:])
    if not os.path.isfile(f"Linked_PM_{variant}_hits.tsv"):
        with open(f"Linked_PM_{variant}_hits.tsv", "a") as link_out:
            link_out.write(f"{PM_list}\n")
    if not os.path.isfile(f"Linked_PM_{variant}_misses.tsv"):
        with open(f"Linked_PM_{variant}_misses.tsv", "a") as link_out:
            link_out.write(f"{PM_list}\n")

def screen_file(file):
    acc = file.split("/")[-1].split(".")[0]
    if not acc in missing_screen:
        return
    samp_linked = []
    samp_sings = []
    if prev_linked:
        for link in prev_linked:
            if not acc in prev_linked[link]:
                samp_linked.append(prev_linked[link][0])
        samp_linked += new_linked_nums
        
    else:
        samp_linked = list(linked.keys())
    if prev_singles:
        for pm in prev_singles:
            if not acc in prev_singles[pm]:
                samp_sings.append(pm)
        samp_sings += new_sings
    else:
        samp_sings = singles
    
    gz = 0
    if file.endswith("gz"):
        in_file = gzip.open(file, "rb")
        gz = 1
    else:
        in_file = open(file, "r")
    Sings_matches = {}
    Linked_matches = {}
    counts = 0
    try:
        in_file.readline()
        in_file.readline()
        for line in in_file:
            if gz == 1:
                line = line.decode()
            splitline = line.upper().strip().split("\t")
            freq = 0
            count = int(splitline[1])
            freq = float(splitline[2])
            if count < line_count_threshold:
                break
            if samp_linked:
                for variant in samp_linked:
                    mismatch = 0
                    match = 0
                    for PM in linked[variant][1:]:
                        if PM in splitline[0]:
                            match += 1
                    if match >= linked[variant][0] and splitline[0].count("insert") < 5 and splitline[0].count("Del") < 6:
                        try:
                            Linked_matches[variant].append(line)
                        except:
                            Linked_matches[variant] = [line]
            if samp_sings:
                if int(splitline[1]) > 0:
                    for variant in samp_sings:
                        if variant.upper() in line.upper():
                            try:
                                Sings_matches[variant].append(line)
                            except:
                                Sings_matches[variant] = [line]


    except Exception as Err:
        print(f"file reading failed for {file} {Err}\nresults not recorded")
        return

    in_file.close()

    for variant in linked:
        count = 0
        if variant in Linked_matches:
            for line in Linked_matches[variant]:
                read_count = int(line.split("\t")[1])
                count += read_count
                if count > total_count_threshold:
                    break
        if count > total_count_threshold:
            out_str = f"{file}\n"
            count = 0
            for line in Linked_matches[variant]:
                out_str += line
                count += 1
                if count > 14:
                    break
            with open(f"Linked_PM_{variant}_hits.tsv", "a") as linked_out:
                linked_out.write(out_str)
        else:
            with open(f"Linked_PM_{variant}_misses.tsv", "a") as linked_out:
                linked_out.write(f"{acc}\n")



    for variant in singles:
        count = 0
        if variant in Sings_matches:
            for line in Sings_matches[variant]:
                line_count = int(line.split("\t")[1])
                count += line_count
                if count > total_count_threshold:
                    break
        if count > total_count_threshold:
            out_str = f"{file}\n"
            count = 0
            for line in Sings_matches[variant]:
                out_str += line
                count += 1
                if count > 14:
                    break
            with open(f"{variant}_hits.tsv", "a") as sings_out:
                sings_out.write(out_str)
        else:
            with open(f"{variant}_misses.tsv", "a") as sings_out:
                sings_out.write(f"{acc}\n")
            

    return




with mp.Manager() as manager:
    pool = mp.Pool()

    searchings = []
    for file in all_files:
        search = pool.apply_async(screen_file, (file, ))
        searchings.append(search)

    for search in searchings:
        search.get()

    pool.close()
    pool.join()
