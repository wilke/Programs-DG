#!/bin/env python3

import os
import sys

import argparse

parser = argparse.ArgumentParser(
        description='fasta file'
)

parser.add_argument(
    'file',
    type=argparse.FileType('r'),
    help='fasta'
)

args = parser.parse_args()
name = (args.file.name)
print(name)
dict_entries = {}
with open(name+".tsv","w") as out_fh:
    with open(name+"2.fa","w") as out2_fh:
        out_fh.write("ID\tflag\tmulti\tlen\tsequence\n")
        length = 0
        ID = ""
        for line in args.file:
            if line.startswith('>'):
                length = int(line.split("len=")[1].split(" ")[0])
                if length > 1:
                    # out_fh.write("\n")
                    splitline = line.strip().split(" ")
                    ID = splitline[0].strip(">")
                    try:
                        dict_entries[ID]
                    except:
                        pass
                    else:
                        print(f"Repeat ID {ID}") 
                        # newID = ""
                        # repeated_id = True
                        # x = 1
                        # while repeated_id:
                            # newID = ID + "_" + str(x)
                            # try:
                                # dict_entries[newID]
                            # except:
                                
                            # else:
                                # x += 1
                    dict_entries[ID] = {"seq" : ""}
                    # out_fh.write(splitline[0].strip(">"))
                    # out_fh.write("\t")
                    for segment in splitline[1:]:
                        dict_entries[ID][segment.split("=")[0]] = segment.split("=")[1]
                        # out_fh.write(segment.split("=")[1])
                        # out_fh.write("\t")
            else:
                if length > 1:
                    dict_entries[ID]["seq"] += line.strip()
                    # out_fh.write(line.strip())
        
        sorted_ids = sorted(dict_entries, key=lambda x: int(dict_entries[x]["len"]), reverse=True)
        for ident in sorted_ids:
            out_fh.write(f"{ident}\t{dict_entries[ident]['flag']}\t{dict_entries[ident]['multi']}\t{dict_entries[ident]['len']}\t{dict_entries[ident]['seq']}\n")
            out2_fh.write(f">{ident} flag={dict_entries[ident]['flag']} multi={dict_entries[ident]['multi']} len={dict_entries[ident]['len']}\n{dict_entries[ident]['seq']}\n")
        
            # refID = line[1:].strip("\n\r")
            # try:
                # dict_entries[refID]
            # except:
                # dict_entries[refID] = ''
            # else:
                # i = 1
                # newrefID = refID + '.' + str(i)
                # while newrefID in dict_entries.keys():
                    # i += 1
                    # newrefID = refID + '.' + str(i)
                # refID =  newrefID
                # dict_entries[refID] = ''
        # else:
            # dict_entries[refID] += line.strip("\n\r")
            

# if dict_entries:
    # outfile = open(name+".tsv","w")
    # for ID in dict_entries:
        # outfile.write(f"{ID}\t{dict_entries[ID]}\n")
    # outfile.close()