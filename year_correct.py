#!/bin/env python3

import os
import sys


for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if '2022-12' in file:
            print(file)
            # os.system(f"mv {os.path.join(subdir, file)} {os.path.join(subdir, file.replace('2022-12','2021-12'))}")