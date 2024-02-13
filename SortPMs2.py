#!/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
import datetime



def GenPos(PM):
    try:
        POS = int(PM.split("\t")[0].split("|")[0].split("(")[0].split("-")[0].strip("ATGCNDel"))
    except:
        POS = PM
    return POS



rats = []
with open("/mnt/g/MU_WW/SARS2/RATG13/RATG13_covars.tsv", "r") as rat_in:
    rat_in.readline()
    rat_in.readline()
    for line in rat_in:
        rats.append(line.split("|")[0].split("\t")[0])


def CheckRat(PM):
    check = ""
    if PM.split("|")[0] in rats:
        check = 'X'

    return check

def ProcTsv(files):

    df = pd.DataFrame([])
    for file in files:
        file_df = pd.read_csv(file, skiprows=2, sep='\t', header=None)
        # print(file_df[1])

        df[file.split("/")[-1].split("_")[0]] = file_df[1]

    df = df.melt(var_name='SS', value_name='PM').dropna()

    df = df[df.PM.str.contains(" ") == False]

    df["1"] = 1

    df = df.pivot(index="PM", columns="SS")["1"]

    df["count"] = df[list(df.columns)].sum(axis=1)

    df["Position"] = df.index
    df["RATG13"] = df.Position.apply(lambda x: CheckRat(x))
    df["Position"] = df.Position.apply(lambda x: GenPos(x))

    df = df.sort_values("Position")

    df = df[['Position'] + ["RATG13"] + [x for x in df.columns if not x in ('Position', 'RATG13')]]

    date = datetime.datetime.today().strftime('%Y%m%d')
    count = 0
    while os.path.isfile(f"{date}.{count}_SortedVariance.tsv"):
        count += 1

    df.to_csv(f"SortedVariance.{date}.{count}.tsv", sep='\t')

    return 0

file_list = []
for subdir, dirs, files in os.walk("/mnt/g/MU_WW/SARS2/SRAs/GenomeComparisons/"):
    for file in files:
        if file.endswith("_cryptic_covar.tsv"):
            file_list.append(os.path.join(subdir, file))

ProcTsv(file_list)




"""
all_pms = []

for col in df:
    all_pms += df[col].tolist()

# print(len(all_pms))

all_pms = list(set(all_pms))
# all_pms.remove("nan")
print(len(all_pms))


all_pms = sorted(all_pms, key=lambda x: GenPos(x))

with open("SortedVariance.tsv", "w") as out_fh:
    out_fh.write("Positions\tPM")
    for col in df:
        out_fh.write(f"\t{col}")
    out_fh.write("\ttotal\n")
    for PM in all_pms[1:]:
        out_fh.write(f"{GenPos(PM)}\t{PM}")
        count = 0
        for col in df:
            if PM in df[col].values:
                count += 1
                out_fh.write("\t1")
            else:
                out_fh.write("\t")
        out_fh.write(f"\t{str(count)}\n")
"""
