#!/bin/env python3

import os
import sys
import gzip

samps = os.getcwd().split("/")[-1]

SRR_meta = {}
meta = 0
try:
    with open("SRA_meta.tsv", "r") as meta_fh:
        for line in meta_fh:
            if line.startswith("SRR") or line.startswith("ERR"):
                splitline = line.split("\t")
                SRR_meta[splitline[0]] = line
except:
    pass

with open(samps+"_Q493KQ498HorY.tsv","w") as multivar_fhs:
    multivar_fhs.write("Q493K3KandQ498Y|H\n")

    files_read = []

    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if not file in files_read and "_unique_seqs.tsv" in file:
                files_read.append(file)
                mv_matches = []
                if (file.endswith('_unique_seqs.tsv')):
                    with open(os.path.join(subdir, file), "r") as in_file:
                        for line in in_file:
                            if not (line.startswith("\t") or line.startswith("Unique") or line.startswith("SRR") or line.startswith("/mnt/") or "Ref" in line):
                                splitline = line.split("\t")
                                count = 0
                                try:
                                    count = int(splitline[1])
                                except:
                                    continue
                                if count > 0 and "Q493K" in splitline[0] and ( "Q498H" in splitline[0] or "Q498Y" in splitline[0]):
                                    try:
                                        mv_matches.append(line)
                                    except:
                                        mv_matches = [line]
                elif (file.endswith('_unique_seqs.tsv.gz')):
                    with gzip.open(os.path.join(subdir, file), "rb") as in_file:
                        mv_matches = []
                        for line in in_file:
                            line = line.decode()
                            if not (line.startswith("\t") or line.startswith("Unique") or line.startswith("SRR") or line.startswith("/mnt/") or "Ref" in line):
                                splitline = line.split("\t")
                                count = 0
                                try:
                                    count = int(splitline[1])
                                except:
                                    continue
                                if count > 0 and "Q493K" in splitline[0] and ( "Q498H" in splitline[0] or "Q498Y" in splitline[0]):
                                    try:
                                        mv_matches.append(line)
                                    except:
                                        mv_matches = [line]

                if mv_matches:
                    multivar_fhs.write(subdir+"/"+file[:-4]+"\t")
                    multivar_fhs.write("\n")
                    try:
                        multivar_fhs.write(SRR_meta[file.split(".")[0]])
                    except KeyError:
                        pass
                    for line in mv_matches:
                        multivar_fhs.write(line)



