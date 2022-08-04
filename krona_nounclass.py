#!/bin/env python3

import os
import sys


for file in os.listdir(os.getcwd()):
    if file.endswith('.allv.krona.txt'):
        samp_name = file.split(".")[0]
        with open(file, "r") as in_file:
            with open(samp_name+".allv.noun.krona.txt", "w") as out_file:
                out_file.writelines(in_file.readlines()[1:])
        os.system(f"ktImportText {samp_name}.allv.noun.krona.txt -o {samp_name}.allv.noun.krona.html")