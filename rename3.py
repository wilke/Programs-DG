#!/bin/env python3

import os
import sys

#### os.system('cp ./backup/* ./')
#### # os.system('mkdir backup')
filenames = {}
testout = open("test.tsv", "w")
# print(os.getcwd().split('/')[-1])
# sstag = os.getcwd().split('/')[-1]
for file in os.listdir(os.getcwd()):
    if not file == "test.tsv" and not 'Collected' in file and not 'counts' in file and '.tsv' in file:
        testout.write(file +"\t")
        Month = ""
        Day = ""
        outputtype = ""
        if 'deconv' in file:
            outputtype = "covar_deconv"
        elif 'chim_rm' in file:
            outputtype = 'chim_rm'
        splitname = file.split('.')[0].split('_')
        Site = splitname[0]
        Date = splitname[1].split('-')
        Month = int(Date[0])
        if Month == 0:
            Month = 10
        for n in Date[1]:
            if n.isdigit():
                Day += n
            else:
                break
        Day = int(Day)

        newfile = Site + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + '-1_' + outputtype + '.tsv'
        try:
            filenames[newfile] += 1

        except:
            filenames[newfile] = 1
        else:
            # print(newfile + " repeated name   " + str(filenames[newfile]))
            newfile = Site + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + '-' + str(filenames[newfile]) + '_' + outputtype + '.tsv'
        filecounter = 0
        # while os.path.isfile(newfile):
            # filecounter = filecounter + 1
            # newfile = Site + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + '-' + str(filenames[newfile])+ "-" + str(filecounter) + + '_' + outputtype + '.tsv'
        testout.write(newfile + "\n")
        ##### os.system("cp "+file+" backup/"+file)
        if not os.path.isfile(newfile):
            os.system("mv "+file+" "+newfile)

testout.close()

