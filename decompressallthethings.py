#!/bin/env python3

import os
import sys

for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.gz'):
            os.system(f"gzip -d {os.path.join(subdir, file)}")