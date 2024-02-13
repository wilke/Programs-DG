#!/bin/env python3

import os
import sys

for file in os.listdir(os.getcwd()):
    if file.endswith(".fa"):
        file_lines = []
        with open(file, "r") as in_fh:
            for line in in_fh:
                if not line.startswith(">"):
                    for nt_ch in ("R", "Y", "K", "M", "S", "W", "B", "D", "H", "V"):
                        if nt_ch in line:
                            line = line.replace(nt_ch, "N")
                file_lines.append(line)
        with open(file, "w") as out_fh:
            out_fh.writelines(file_lines)

