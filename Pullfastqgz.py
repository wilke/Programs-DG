#!/bin/env python3

import os
import sys
import zipfile


for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".zip"):
            if zipfile.is_zipfile(os.path.join(subdir, file)):
                with zipfile.ZipFile((os.path.join(subdir, file)), 'r') as zf:
                    for name in zf.namelist():
                        if name.endswith('.fastq.gz') and not "trimmed" in name:
                            zf.extract(name, subdir)
                for subdirx, dirsx, filesx in os.walk(subdir):
                    for filex in filesx:
                        if not filex == file and not filex.endswith(".py"):
                            os.system(f"mv {os.path.join(subdirx, filex)} {subdir}")
                os.system(f"rm {os.path.join(subdir, file)}")