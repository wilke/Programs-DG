#!/bin/env python3

import os
import sys

#### os.system('cp ./backup/* ./')
#### # os.system('mkdir backup')
filenames = {}
testout = open("test.tsv", "w")
# print(os.getcwd().split('/')[-1])
sstag = os.getcwd().split('/')[-1]
for file in os.listdir(os.getcwd()):
    if not file == "test.tsv" and not 'Collected' in file and '.tsv' in file:
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
        for n in Date[1]:
            if n.isdigit():
                Day += n
            else:
                break
        Day = int(Day)

        newfile = sstag + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + '-1_' + outputtype + '.tsv'
        try:
            filenames[newfile] += 1

        except:
            filenames[newfile] = 1
        else:
            # print(newfile + " repeated name   " + str(filenames[newfile]))
            newfile = sstag + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + '-' + str(filenames[newfile]) + '_' + outputtype + '.tsv'
        filecounter = 0
        # while os.path.isfile(newfile):
            # filecounter = filecounter + 1
            # newfile = sstag + "_" + f"{Month:02d}" + "-" + f"{Day:02d}" + '-' + str(filenames[newfile])+ "-" + str(filecounter) + + '_' + outputtype + '.tsv'
        testout.write(newfile + "\n")
        ##### os.system("cp "+file+" backup/"+file)
        if not os.path.isfile(newfile):
            os.system("mv "+file+" "+newfile)

testout.close()

deconv_dict_dict = {}
cr_dict_dict = {}

all_deconv = {}
all_cr = {}

sample_line = ''

for file in os.listdir(os.getcwd()):

    if file.endswith('_deconv.tsv'):
        try:
            samp=open(file, "r")
        except:
            print("can't open "+file)
        else:
            for line in samp:
                splitline = line.strip("\n\r").split("\t")
                try:
                    splitline[1]
                except:
                    sample_line = splitline[0]
                    deconv_dict_dict[file+'-'+sample_line] = {}

                else:
                    if splitline[1] == 'Count':
                        sample_line = splitline[0]
                        deconv_dict_dict[file+'-'+sample_line] = {}
                    else:
                        if float(splitline[2]) >= .01:
                            deconv_dict_dict[file+'-'+sample_line][splitline[0]] = [splitline[1], splitline[2]]
                            try:
                                all_deconv[splitline[0]] = all_deconv[splitline[0]] + 1
                            except:
                                all_deconv[splitline[0]] = 1
            samp.close()

    if file.endswith('_chim_rm.tsv'):
        try:
            samp=open(file, "r")
        except:
            print("can't open "+file)
        else:
            for line in samp:
                splitline = line.strip("\n\r").split("\t")
                try:
                    splitline[1]
                except:
                    sample_line = splitline[0]
                    cr_dict_dict[file+'-'+sample_line] = {}

                else:
                    if not splitline[1] == 'Count':
                        if float(splitline[2]) >= .01:
                            cr_dict_dict[file+'-'+sample_line][splitline[0]] = [splitline[1], splitline[2]]
                            try:
                                all_cr[splitline[0]] = all_cr[splitline[0]] + 1
                            except:
                                all_cr[splitline[0]] = 1
            samp.close()

if len(deconv_dict_dict) > 0:
    #if args.colID == '':
    Col_deconv_fh = open(os.getcwd().split('/')[-1]+'_Collected_Covar_Deconv.tsv',"w")
    #else:
    #    Col_deconv_fh = open(args.colID+'_Collected_Covar_Deconv.tsv',"w")
    sorted_deconvs = sorted(all_deconv)
    Col_deconv_fh.write("\t")
    for sampline in deconv_dict_dict:
        Col_deconv_fh.write(sampline+"\t\t")
    Col_deconv_fh.write("\nCovariant\t")
    for sampline in deconv_dict_dict:
        Col_deconv_fh.write("Count\tAbundance\t")
    Col_deconv_fh.write("\n")
    for deconv in sorted_deconvs:
        if all_deconv[deconv] >= 1:
            Col_deconv_fh.write(deconv+"\t")
            for sample in deconv_dict_dict:
                try:
                    Col_deconv_fh.write(deconv_dict_dict[sample][deconv][0]+"\t"+deconv_dict_dict[sample][deconv][1]+"\t")
                except:
                    Col_deconv_fh.write("\t\t")

            Col_deconv_fh.write("\n")
    Col_deconv_fh.close()
else:
    print('No deconv files found')

if len(cr_dict_dict) > 0:
    # if args.colID == '':
    Col_cr_fh = open(os.getcwd().split('/')[-1]+'_Collected_Chimeras_Removed.tsv',"w")
    # else:
    #     Col_cr_fh = open(args.colID+'_Collected_Chimeras_Removed.tsv',"w")
    sorted_crs = sorted(all_cr)
    Col_cr_fh.write("\t")
    for sampline in cr_dict_dict:
        Col_cr_fh.write(sampline+"\t\t")
    Col_cr_fh.write("\nUnique Sequence\t")
    for sampline in cr_dict_dict:
        Col_cr_fh.write("Count\tAbundance\t")
    Col_cr_fh.write("\n")
    for cr in sorted_crs:
        if all_cr[cr] >= 1:
            Col_cr_fh.write(cr+"\t")
            for sample in cr_dict_dict:
                try:
                    Col_cr_fh.write(cr_dict_dict[sample][cr][0]+"\t"+cr_dict_dict[sample][cr][1]+"\t")
                except:
                    Col_cr_fh.write("\t\t")

            Col_cr_fh.write("\n")
    Col_cr_fh.close()
else:
    print('No chim_rm files found')
