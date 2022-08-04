#!/bin/env python3

import os
import sys


for file in os.listdir(os.getcwd()):
    if file.endswith('.allv.k2'):
        samp_name = file.split(".")[0]
        print(samp_name)
        with open(file, "r") as in_file:
            with open(samp_name+".allv.noun.k2", "w") as out_file:
                for line in in_file:
                    if line.startswith("C\t"):
                        out_file.write(line)
        