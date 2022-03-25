#!/bin/env python3

import os
import sys

for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam'):
        print(file)
        readlines = []
        sam_fh = open(file, "r")
        head_count = 0
        for line in sam_fh:
            if not line.startswith("@"):
                if head_count == 0:
                    break
                readlines.append(line)
            else:
                head_count = head_count + 1
        sam_fh.close()
        

        if head_count > 0:
            print(file)
            sam_fh = open(file, "w")
            for line in readlines:
                sam_fh.write(line)
            sam_fh.close()