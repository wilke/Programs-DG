#!/bin/env python3

import os
import sys

query = 'hanta'
print(query.lower())
for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('.sam'):
        print(file)
        in_file = open(file, "r")
        for line in in_file:
            if query.lower() in line.lower():
                print(line)
                    
        in_file.close()
            
            