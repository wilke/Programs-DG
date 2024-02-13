#!/bin/env python3

import os
import sys
import gzip
import pysam
import shutil

pysam.set_verbosity(0)

def GenPos(PM):
    POS = int(PM.split("\t")[0].split(" ")[0].split("|")[0].split("(")[0].split("-")[0].strip("ATGCNDel"))
    return POS


fetch_dict = {}
accs = []

with open("GenomesAccs.tsv", "r") as genomes_in:
    set_name = ""
    for line in genomes_in:
        if not line.strip().startswith("#"):
            if line.strip().endswith(":"):
                set_name = line.strip().replace(" ", "_").strip(":")
                if not set_name in fetch_dict:
                    fetch_dict[set_name] = [[] , []]
                else:
                    print(f"repeat set name {set_name}")
                    exit(1)
            else:

                entries = line.split("\t")
                if entries[0].strip():
                    fetch_dict[set_name][0].append(entries[0].strip())
                    accs.append(entries[0].strip())
                if len(entries) > 1 and entries[1].strip():
                    fetch_dict[set_name][1].append(entries[1].strip())
                    accs.append(entries[1].strip())

print(len(accs))
accs = list(set(accs))
print(len(accs))

acc_meta = {}
with open("/mnt/g/MU_WW/SARS2/SRAs/Wastewater/SRA_meta.tsv", "r") as meta:
    for line in meta:
        acc = line.split("\t")[0]
        if acc in accs:
            acc_meta[acc] = line

found_acc = {}

dir_path = "/mnt/g/MU_WW/SARS2/SRAs/GenomeComparisons/"

missing = 0

for loc_set in fetch_dict:
    if os.path.isdir(os.path.join(dir_path, loc_set)):
        for i in (0, 1):
            for acc in fetch_dict[loc_set][i]:
                if not os.path.isfile(os.path.join(dir_path, loc_set, f"{acc}.sam")):
                    missing += 1
    else:
        missing += 1

if missing > 0:
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.lower().endswith('.sam') or file.lower().endswith('.sam.gz') or file.lower().endswith('.cram'):
                acc = file.split(".")[0]
                if acc in accs and not acc in found_acc:
                    found_acc[acc] = os.path.join(subdir, file)

    if not len(accs) == len(found_acc):
        print(len(found_acc))
        for acc in accs:
            if not acc in found_acc:
                print(f"{acc} not found")
        exit(1)

# os.chdir()


for loc_set in fetch_dict:
    if not os.path.isdir(os.path.join(dir_path, loc_set)):
        os.makedirs(os.path.join(dir_path, loc_set))
    for i in (0, 1):
        for acc in fetch_dict[loc_set][i]:
            new_file = acc + ".sam"
            if not os.path.exists(os.path.join(dir_path, loc_set, new_file)):
                stored_file = found_acc[acc]
                if stored_file.endswith(".sam"):
                    shutil.copyfile(stored_file, os.path.join(dir_path, loc_set, new_file))
                elif stored_file.endswith(".sam.gz"):
                    with gzip.open(stored_file, "rb") as gzfile:
                        with open(os.path.join(dir_path, loc_set, new_file), "wb") as sam_file:
                            shutil.copyfileobj(gzfile, sam_file)
                elif stored_file.endswith(".cram"):
                    with pysam.AlignmentFile(stored_file, "rc") as cram_file:
                        with pysam.AlignmentFile(os.path.join(dir_path, loc_set, new_file), "w", template=cram_file) as sam_file:
                            for line in cram_file:
                                sam_file.write(line)
                else:
                    print(f"file error {stored_file}")



    os.chdir(os.path.join(dir_path, loc_set))

    for file in os.listdir(os.getcwd()):
        if file.endswith(".sam") and not file.split(".")[0] in fetch_dict[loc_set][0] + fetch_dict[loc_set][1]:
            os.remove(file)
            print(f"{file} removed")
            tsv_file = file.replace(".sam", "_covars.tsv")
            if os.path.isfile(tsv_file):
                os.remove(tsv_file)
                print(f"{tsv_file} removed")

    print(loc_set)
    with open("Assembled_meta.tsv", "w") as metafile:
        for i in (0,1):
            for acc in fetch_dict[loc_set][i]:
                if acc in acc_meta:
                    metafile.write(acc_meta[acc])
                else:
                    metafile.write(f"{acc}\tmeta not found")
    min_abund = "0.001"
    # os.system(f"python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 1 --seq 0 --indel 0 --covar 1 --max_covar 2 --max_dist 120 --AAcentered 0 --nt_call 0 --min_count 2 --min_samp_abund {min_abund} --min_col_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --mp 4 --chim_rm 0 --deconv 0")

    negatives = {}
    for acc in fetch_dict[loc_set][1]:
        print(acc)
        if os.path.isfile(f"{acc}_covars.tsv"):
            with open(f"{acc}_covars.tsv", "r") as neg_file:
                neg_file.readline()
                neg_file.readline()
                for line in neg_file:
                    # if not " " in line:
                    try:
                        negatives[line.split("\t")[0]].append(float(line.split("\t")[2]))
                    except:
                        negatives[line.split("\t")[0]] = [float(line.split("\t")[2])]

    print("+")

    positives = {}
    doubles = {}
    for acc in fetch_dict[loc_set][0]:
        print(acc)
        with open(f"{acc}_covars.tsv", "r") as pos_file:
            pos_file.readline()
            pos_file.readline()
            for line in pos_file:
                if (not " " in line) and not "N|" in line:
                    try:
                        positives[line.split("\t")[0]].append(float(line.split("\t")[2]))
                    except:
                        positives[line.split("\t")[0]] = [float(line.split("\t")[2])]
                elif not "N|" in line:
                    try:
                        doubles[line.split("\t")[0]].append(float(line.split("\t")[2]))
                    except:
                        doubles[line.split("\t")[0]] = [float(line.split("\t")[2])]

    print(f"checking first {len(positives)} positives")
    passed_pos = []
    ubiqs = []
    max_pos_sum = 0
    for hit in positives:
        # if "D614G" in hit:
            # print(hit)
            # print(positives[hit])
            # print(.98 * len(fetch_dict[loc_set][0]))
            # print(len(positives[hit]))
            # print(sum(positives[hit]))
            # print("xxxxxxxxx")
        if len(positives[hit]) > 1:
            if hit in negatives:
                if (sum(positives[hit]) / len(fetch_dict[loc_set][0])) > (50 * sum(negatives[hit]) / len(fetch_dict[loc_set][1])):
                    passed_pos.append(hit)
                    max_pos_sum = max((max_pos_sum, sum(positives[hit])))
                else:
                    ubiq_cutoff = .95 * len(fetch_dict[loc_set][0])
                    if len(positives[hit]) >= ubiq_cutoff and sum(positives[hit]) > ubiq_cutoff:
                        ubiqs.append(hit)
            else:
                passed_pos.append(hit)
                max_pos_sum = max((max_pos_sum, sum(positives[hit])))

    print(f"checking {len(passed_pos)} passed positives")
    new_passed = []
    for var in passed_pos:
        if sum(positives[var]) > (.1 * max_pos_sum):
            new_passed.append(var)
    passed_pos = new_passed
    new_passed = []
    print(f"{len(passed_pos)} positives passed")


    print(f"checking {len(doubles)} doubles")

    double_passed = []
    linked = []
    for hit in doubles:
        if len(doubles[hit]) > 1:
            split_pm = hit.split(" ")
            if (split_pm[0] in passed_pos or split_pm[1] in passed_pos) and not (split_pm[0] in passed_pos and split_pm[1] in passed_pos):
                if sum(doubles[hit]) > .1 * max_pos_sum and split_pm[0] in positives and split_pm[1] in positives:
                    if (sum(doubles[hit]) / len(fetch_dict[loc_set][0])) >= (sum(positives[split_pm[0]]) / len(fetch_dict[loc_set][0])) * (sum(positives[split_pm[1]]) / len(fetch_dict[loc_set][0])):
                        # if "A1841G(D614G)" in hit:
                            # print(hit)
                            # print("xxxxxxxxx")
                        if split_pm[0] in passed_pos and (not split_pm[1] in passed_pos): # and sum(doubles[hit]) > .6 * sum(positives[split_pm[1]]):
                            double_passed.append(hit)
                            linked.append(split_pm[1])
                        elif split_pm[1] in passed_pos and (not split_pm[0] in passed_pos): # and sum(doubles[hit]) > .6 * sum(positives[split_pm[0]]):
                            double_passed.append(hit)
                            linked.append(split_pm[0])

    linked = list(set(linked))
    print(f"{len(double_passed)} doubles passed, {len(linked)} singles")

    all_sing = list(set(passed_pos + linked + ubiqs))
    passed_pos = sorted(all_sing+double_passed, key=lambda x: GenPos(x))

    # totals = {}
    with open(f"{loc_set}_cryptic_covar.tsv", "w") as out_fh:
        out_fh.write(f"\t{len(fetch_dict[loc_set][0])} positive samples, {len(fetch_dict[loc_set][1])} negative samples\n")
        out_fh.write("Position\tVariant\tType\tPositive Sample Count\tPositive Abundance Sum\n")
        for var in passed_pos:
            l = ""
            if var in linked:
                l = "linked"
            if var in ubiqs:
                if l:
                    l += ", "
                l += "ubiq"
            out_fh.write(f"{GenPos(var)}\t{var}\t{l}\t")
            total = 0
            try:
                pos_sum = sum(positives[var])
                total += pos_sum
                out_fh.write(f"{len(positives[var])}\t{pos_sum}\t{positives[var]}")
                # totals[var] = [str(pos_sum)]
                try:
                    neg_sum = sum(negatives[var])
                    total += neg_sum
                    out_fh.write(f"\t{len(negatives[var])}\t{neg_sum}\t{negatives[var]}")
                    # totals[var].append(str(neg_sum))
                except:
                    out_fh.write("\t\t\t")
                    # totals[var].append("0")
            except:
                pos_sum = sum(doubles[var])
                total += pos_sum
                out_fh.write(f"{len(doubles[var])}\t{pos_sum}\t{doubles[var]}")
                # totals[var] = [str(pos_sum)]

                try:
                    neg_sum = sum(negatives[var])
                    total += neg_sum
                    out_fh.write(f"\t{len(negatives[var])}\t{neg_sum}\t{negatives[var]}")
                    # totals[var].append(str(neg_sum))
                except:
                    out_fh.write("\t\t\t")
                    # totals[var].append("0")
            out_fh.write(f"\t{total}\n")
            # totals[var].append(str(total))

    os.system("python3 /mnt/g/MU_WW/SARS2/CrypticCommons/CommonVar.py")
    # os.rename("CommonVars.tsv", f"{loc_set}_CommonVars.tsv")

    with open(f"CommonVars.tsv", "r") as in_fh:
     with open(f"{loc_set}_cryptic_CommonVars.tsv", "w") as out_fh:
        with open(f"{loc_set}_CommonVars.tsv", "w") as cv_out:
            out_fh.write("\t")
            cur_line = in_fh.readline()
            out_fh.write(cur_line)
            cv_out.write(cur_line)
            cur_line = in_fh.readline()
            out_fh.write("\t")
            if "Sequences" in cur_line:
                out_fh.write(cur_line.strip("\n"))
                cv_out.write(cur_line.strip("\n"))
            else:
                out_fh.write(cur_line)
                out_fh.write("\t")
                cv_out.write(cur_line)
                cur_line = in_fh.readline()
                out_fh.write(cur_line.strip("\n"))
                cv_out.write(cur_line.strip("\n"))
            out_fh.write("Total samples\tPositives Sum\tNegatives Sum\tTotal Sum\n")
            cv_out.write("Total samples\tPositives Sum\tNegatives Sum\tTotal Sum\n")
            for line in in_fh:
                split_line = line.split("\t")
                sums =[]
                try:
                    sums.append(sum(positives[split_line[2]]))
                except:
                    sums.append(0)
                try:
                    sums.append(sum(negatives[split_line[2]]))
                except:
                    sums.append(0)
                sums.append(sum(sums))
                for i in range(0, 3):
                    sums[i] = str(sums[i])
                sums = '\t'.join(sums)
                cv_out.write(line.strip("\n"))
                cv_out.write(f"\t{sums}\n")
                if split_line[2] in all_sing:
                    if split_line[2] in linked:
                        out_fh.write("linked")
                    if split_line[2] in ubiqs:
                        out_fh.write("ubiq")
                    out_fh.write("\t")
                    out_fh.write(line.strip("\n"))

                    # sums = '\t'.join(totals[split_line[2]])
                    out_fh.write(f"\t{sums}\n")

    os.system("python3 /mnt/g/MU_WW/SARS2/SRAs/MakeConsensus.py")

os.system("python3 /mnt/g/MU_WW/SARS2/SRAs/SortPMs2.py")