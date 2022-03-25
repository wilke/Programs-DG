#!/bin/env python3

import os
import sys

filenames = {}
testout = open("test.tsv", "w")
for file in os.listdir(os.getcwd()):
    if not file == "test.tsv": # and file.endswith(".sam"):
        newfile = file
        Amp = "RBD"
        if "RBDA" in file:
            Amp = "RBDA"
        elif "RBDB" in file:
            Amp = "RBDB"
        elif "NTD" in file:
            Amp = "NTD"
        elif "S1S2" in file:
            Amp = "S1S2"
        elif "S1S1" in file:
            Amp = "S1S2"
        Site = ""
        Month = ""
        Day = ""
        # ft = file[-3:]
        # if "__" in file:
            # newfile = file.replace("__", "_")
            # # print(file +"\n"+ newfile)
            # os.system("mv "+file+" "+newfile)



        splitname = file.split('.')[0].split('_')
        Site = splitname[0]
        Date = splitname[1].split('-')
        Month = int(Date[0])
        for n in Date[1]:
            if n.isdigit():
                Day += n
            else:
                break
        Day = int(Day)
        # for n in splitname[0]:
            # if n.isdigit():
                # Site += n
            # else:
                # break
        # if splitname[0].startswith('CC'):

            # try:
                # splitname[0].split('-')[1]
            # except:
                # Site = splitname[0]
                # Date = splitname[1].split('-')
                # Month = Date[0]
                # for n in Date[1]:
                    # if n.isdigit():
                        # Day += n
                    # else:
                        # break
            # else:
                # Site = "CC"
                # Date = splitname[0].split('-')
                # for n in Date[0]:
                    # if n.isdigit():
                        # Month += n
                # for n in Date[1]:
                    # if n.isdigit():
                        # Day += n
                    # else:
                        # break

        # elif splitname[2][0].isdigit():
            # try:
                # Date = splitname[2].split('-')
            # except:
                # print("date1   "+file)
                # Date = splitname[1]
            # Month = Date[0]
            # try:
                # Day = Date[1]
            # except:
                # print("Day1   "+ file)
        # elif splitname[1][0].isdigit():
            # try:
                # splitname[1].split('-')[1]
            # except:
                # print("date2   "+file)
                # Date = splitname[1]
            # else:
                # Date = splitname[1].split('-')

            # Month = Date[0]
            # try:
                # for n in Date[1]:
                    # if n.isdigit():
                        # Day += n
                    # else:
                        # break
            # except:
                # print("Day2   "+ file + "   " + Date[0])
        # else:
            # try:
                # splitname[1].split('-')[1]
            # except:
                # print("date3   "+file)
                # Date = splitname[1]
            # else:
                # Date = splitname[1].split('-')

            # try:
                # for n in Date[0]:
                    # if n.isdigit():
                        # Month += n
            # except:
                # print("Month  " + file)
            # try:
                # Day = Date[1]
            # except:
                # print("Day3   "+ file + "   " + Date[0])
        newfile = Site + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + "_" + Amp + "." + file.split(".")[-1] #+ "_" + "_".join(splitname[2:]) + "." + ".".join(file.split(".")[1:])
        try:
            filenames[newfile] += 1
            newfile = Site + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + "_" + Amp + str(filenames[newfile]) + "." + file.split(".")[-1]
            print(newfile + " repeated name")
        except:
            filenames[newfile] = 1
        testout.write(file +"\t"+ newfile + "\n")
        # os.system("mv "+file+" "+newfile)

testout.close()
