#!/bin/env python3

import os
import sys
import gzip

samps = os.getcwd().split("/")[-1]

deltahap = ["L452R", "notS477N", "T478K"] # "notK417", , "notN460K", "notE484A", "notQ493R", "notQ498R"

SRR_list = []
with open(samps+"deltas.tsv","w") as delta_fhs:
    delta_fhs.write("Deltas\n")

    files_read = []

    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if not file in files_read and "_unique_seqs.tsv" in file:
                files_read.append(file)
                if (file.endswith('_unique_seqs.tsv')):
                    with open(os.path.join(subdir, file), "r") as in_file:
                        delta_matches = []
                        for line in in_file:
                            if not (line.startswith("\t") or line.startswith("Unique") or "SRR" in line or line.startswith("/mnt/") or "Ref" in line):
                                splitline = line.split("\t")
                                count = 0
                                try:
                                    count = int(splitline[1])
                                except:
                                    pass
                                if count > 2:
                                    match = 0
                                    hap = splitline[0]
                                    for PM in deltahap:
                                        if 'not' in PM:
                                            if PM.strip('not') in line:
                                                match -= 1
                                        elif PM in line:
                                            match += 1
                                    if (match ==  2) and len(hap.split(" ")) < 25 and hap.count("insert") < 3 and hap.count("Del") < 4:
                                        try:
                                            delta_matches.append(line)
                                        except:
                                            delta_matches = [line]
                                else:
                                    break
                        if delta_matches:
                            delta_fhs.write(subdir+"/"+file[:-4]+"\t")
                            delta_fhs.write("\n")
                            for line in delta_matches:
                                delta_fhs.write(line)
                if (file.endswith('_unique_seqs.tsv.gz')):
                    with gzip.open(os.path.join(subdir, file), "rb") as in_file:
                        delta_matches = []
                        for line in in_file:
                            line = line.decode()
                            if not (line.startswith("\t") or line.startswith("Unique") or "SRR" in line or line.startswith("/mnt/") or "Ref" in line):
                                splitline = line.split("\t")
                                count = 0
                                try:
                                    count = int(splitline[1])
                                except:
                                    pass
                                if count > 2:
                                    match = 0
                                    hap = splitline[0]
                                    for PM in deltahap:
                                        if 'not' in PM:
                                            if PM.strip('not') in line:
                                                match -= 1
                                        elif PM in line:
                                            match += 1
                                    if (match ==  2) and len(hap.split(" ")) < 25 and hap.count("insert") < 3 and hap.count("Del") < 4:
                                        try:
                                            delta_matches.append(line)
                                        except:
                                            delta_matches = [line]
                                else:
                                    break
                        if delta_matches:
                            delta_fhs.write(subdir+"/"+file[:-4]+"\t")
                            delta_fhs.write("\n")
                            for line in delta_matches:
                                delta_fhs.write(line)
                            
                


