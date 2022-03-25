#!/bin/env python3

import os
import sys


WWTP_dict = {   2 : [1, "BB", "Queens"],
                4 : [2, "HP", "Bronx"],
                13 : [3, "TI", "Queens"],
                14 : [4, "WI", "Man. & Bronx"],
                6 : [5, "NC", "Man. Qu. & BL"],
                7 : [6, "NR", "Manhattan"],
                10 : [7, "OB", "Staten Is."],
                12 : [8, "PR", "Staten Is."],
                8 : [9, "RH", "Brooklyn"],
                1 : [10, "26W", "Brooklyn"],
                3 : [11, "CI", "Brooklyn"],
                5 : [12, "JA", "Queens"],
                11 : [13, "OH", "Brooklyn"],
                9 : [14, "RK", "Queens"]
}
WWTP_dict2 = {   "BB" : 2,
                "HP" : 4,
                "TI" : 13,
                "WI" : 14,
                "NC" : 6,
                "NR" : 7,
                "OB" : 10,
                "PR" : 12,
                "RH" : 8,
                "26W" : 1,
                "CI" : 3,
                "Ci" : 3,
                "JA" : 5,
                "OH" : 11,
                "RK" : 9
}

cwdpath = os.getcwd()

deconv_dict_dict = {}
cr_dict_dict = {}

wwtp_deconv_dict_dict = {
2  : {},
4  : {},
13 : {},
14 : {},
6  : {},
7  : {},
10 : {},
12 : {},
8  : {},
1  : {},
3  : {},
5  : {},
11 : {},
9  : {}
}
# OH_deconv_dict_dict = {}
# OB_deconv_dict_dict = {}
# WI_deconv_dict_dict = {}

# wwtp_cr_dict_dict = {
# 2  : {},
# 4  : {},
# 13 : {},
# 14 : {},
# 6  : {},
# 7  : {},
# 10 : {},
# 12 : {},
# 8  : {},
# 1  : {},
# 3  : {},
# 5  : {},
# 11 : {},
# 9  : {}
# }
# OH_cr_dict_dict = {}
# OB_cr_dict_dict = {}
# WI_cr_dict_dict = {}

all_deconv = {}
# all_cr = {}

wwtp_deconv = {
2  : {},
4  : {},
13 : {},
14 : {},
6  : {},
7  : {},
10 : {},
12 : {},
8  : {},
1  : {},
3  : {},
5  : {},
11 : {},
9  : {}
}
# OH_deconv = {}
# OB_deconv = {}
# WI_deconv = {}

# OH_cr = {}
# OB_cr = {}
# WI_cr = {}

all_deconv_sampnames = []
# all_cr_sampnames = []


for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:            
        sampname = ""
        if file.endswith('_deconv.tsv'):
            
            if "NY" in file:
                wwtp = int(file.split("_")[0].strip("NYRBDA"))
            else: 
                try:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")]
                except:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")[:-1]]
            
            sampname = "-".join(subdir.split("/")[-2:]) + "_" + WWTP_dict[int(wwtp)][1]
            n = 0
            while sampname in all_deconv_sampnames:
                n += 1
                sampname = "-".join(subdir.split("/")[-2:]) + "_" + WWTP_dict[int(wwtp)][1] + "_" + str(n)
            all_deconv_sampnames.append(sampname)
            deconv_dict_dict[sampname] = {}
            wwtp_deconv_dict_dict[wwtp][sampname] = {}
            # if wwtp == 10: # OB
                # OB_deconv_dict_dict[sampname] = {}
            # elif wwtp == 11: #OH
                # OH_deconv_dict_dict[sampname] = {}                
            # elif wwtp == 14: #WI
                # WI_deconv_dict_dict[sampname] = {}
                
            try:
                samp=open(os.path.join(subdir, file), "r")
            except:
                print("can't open "+file)
            else:
                for line in samp:
                    splitline = line.strip("\n\r").split("\t")
                    try:
                        if not splitline[1] == 'Count':
                            if float(splitline[2]) >= .001:
                                deconv_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                try:
                                    all_deconv[splitline[0]] += 1
                                except:
                                    all_deconv[splitline[0]] = 1
                                wwtp_deconv_dict_dict[wwtp][sampname][splitline[0]] = [splitline[1], splitline[2]]
                                try:
                                    wwtp_deconv[wwtp][splitline[0]] += 1
                                except:
                                    wwtp_deconv[wwtp][splitline[0]] = 1
                                # if wwtp == 10: # OB
                                    # OB_deconv_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                    # try:
                                        # OB_deconv[splitline[0]] += 1
                                    # except:
                                        # OB_deconv[splitline[0]] = 1
                                # elif wwtp == 11: #OH
                                    # OH_deconv_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                    # try:
                                        # OH_deconv[splitline[0]] += 1
                                    # except:
                                        # OH_deconv[splitline[0]] = 1
                                # elif wwtp == 14: #WI
                                    # WI_deconv_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                    # try:
                                        # WI_deconv[splitline[0]] += 1
                                    # except:
                                        # WI_deconv[splitline[0]] = 1
                    except:
                        pass
            samp.close()

        # if file.endswith('_chim_rm.tsv'):
            
            # if "NY" in file:
                # wwtp = int(file.split("_")[0].strip("NYRBDA"))
            # else: 
                # try:
                    # wwtp = WWTP_dict2[file.split("_")[0].strip("0d")]
                # except:
                    # wwtp = WWTP_dict2[file.split("_")[0].strip("0d")[:-1]]
            
            # sampname = "-".join(subdir.split("/")[-2:]) + "_" + WWTP_dict[int(wwtp)][1]
            # n = 1
            # while sampname in all_cr_sampnames:
                # n += 1
                # sampname = "-".join(subdir.split("/")[-2:]) + "_" + WWTP_dict[int(wwtp)][1] + "_" + str(n)
            # cr_dict_dict[sampname] = {}
            # all_cr_sampnames.append(sampname)
            # if wwtp == 10: # OB
                # OB_cr_dict_dict[sampname] = {}
            # elif wwtp == 11: #OH
                # OH_cr_dict_dict[sampname] = {}                
            # elif wwtp == 14: #WI
                # WI_cr_dict_dict[sampname] = {}
                
            # try:
                # samp=open(os.path.join(subdir, file), "r")
            # except:
                # print("can't open "+file)
            # else:
                # for line in samp:
                    # splitline = line.strip("\n\r").split("\t")
                    # try:
                        # if not splitline[1] == 'Count':
                            # if float(splitline[2]) >= .001:
                                # cr_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                # try:
                                    # all_cr[splitline[0]] += 1
                                # except:
                                    # all_cr[splitline[0]] = 1
                                # if wwtp == 10: # OB
                                    # OB_cr_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                    # try:
                                        # OB_cr[splitline[0]] += 1
                                    # except:
                                        # OB_cr[splitline[0]] = 1
                                # elif wwtp == 11: #OH
                                    # OH_cr_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                    # try:
                                        # OH_cr[splitline[0]] += 1
                                    # except:
                                        # OH_cr[splitline[0]] = 1
                                # elif wwtp == 14: #WI
                                    # WI_cr_dict_dict[sampname][splitline[0]] = [splitline[1], splitline[2]]
                                    # try:
                                        # WI_cr[splitline[0]] += 1
                                    # except:
                                        # WI_cr[splitline[0]] = 1
                    # except:
                        # pass
            # samp.close()

if len(deconv_dict_dict) > 0:
  
    Col_deconv_fh = open('Collected_Covar_Deconv.tsv',"w")
    sorted_deconvs = sorted(all_deconv)
    Col_deconv_fh.write("\t")
    for sampline in deconv_dict_dict:
        Col_deconv_fh.write(sampline+"\t")
    Col_deconv_fh.write("\nCovariant\t")
    for sampline in deconv_dict_dict:
        Col_deconv_fh.write("Abundance\t")
    Col_deconv_fh.write("\n")
    for deconv in sorted_deconvs:
        if all_deconv[deconv] > 0:
            Col_deconv_fh.write(deconv+"\t")
            for sample in deconv_dict_dict:
                try:
                    Col_deconv_fh.write(deconv_dict_dict[sample][deconv][1]+"\t") # deconv_dict_dict[sample][deconv][0]+"\t"+
                except:
                    Col_deconv_fh.write("\t")
            Col_deconv_fh.write("\n")
    Col_deconv_fh.close()

# if len(cr_dict_dict) > 0:
    # Col_cr_fh = open('Collected_Chimeras_Removed.tsv',"w")
    # sorted_crs = sorted(all_cr)
    # Col_cr_fh.write("\t")
    # for sampline in cr_dict_dict:
        # Col_cr_fh.write(sampline+"\t")
    # Col_cr_fh.write("\nUnique Sequence\t")
    # for sampline in cr_dict_dict:
        # Col_cr_fh.write("Abundance\t")
    # Col_cr_fh.write("\n")
    # for cr in sorted_crs:
        # if all_cr[cr] > 0:
            # Col_cr_fh.write(cr + "\t")
            # for sample in cr_dict_dict:
                # try:
                    # Col_cr_fh.write(str(cr_dict_dict[sample][cr][1])+"\t") # cr_dict_dict[sample][cr][0]+"\t"+
                # except:
                    # Col_cr_fh.write("\t")
            # Col_cr_fh.write("\n")
    # Col_cr_fh.close()
    
for wwtp in wwtp_deconv_dict_dict:
    if len(wwtp_deconv_dict_dict[wwtp]) > 0:
        # print(WWTP_dict[wwtp][1])
        Col_deconv_fh = open(WWTP_dict[wwtp][1]+'_Collected_Covar_Deconv.tsv',"w")
        sorted_deconvs = sorted(wwtp_deconv[wwtp])
        Col_deconv_fh.write("\t")
        for sampline in wwtp_deconv_dict_dict[wwtp]:
            Col_deconv_fh.write(sampline+"\t")
        Col_deconv_fh.write("\nCovariant\t")
        for sampline in wwtp_deconv_dict_dict[wwtp]:
            Col_deconv_fh.write("Abundance\t")
        Col_deconv_fh.write("\n")
        for deconv in sorted_deconvs:
            if wwtp_deconv[wwtp][deconv] > 0:
                Col_deconv_fh.write(deconv+"\t")
                for sample in wwtp_deconv_dict_dict[wwtp]:
                    try:
                        Col_deconv_fh.write(wwtp_deconv_dict_dict[wwtp][sample][deconv][1]+"\t") # deconv_dict_dict[sample][deconv][0]+"\t"+
                    except:
                        Col_deconv_fh.write("\t")
                Col_deconv_fh.write("\n")
        Col_deconv_fh.close()
    
# if len(OH_deconv_dict_dict) > 0:
  
    # Col_deconv_fh = open('OH_Covar_Deconv.tsv',"w")
    # sorted_deconvs = sorted(OH_deconv)
    # Col_deconv_fh.write("\t")
    # for sampline in OH_deconv_dict_dict:
        # Col_deconv_fh.write(sampline+"\t")
    # Col_deconv_fh.write("\nCovariant\t")
    # for sampline in OH_deconv_dict_dict:
        # Col_deconv_fh.write("Abundance\t")
    # Col_deconv_fh.write("\n")
    # for deconv in sorted_deconvs:
        # if OH_deconv[deconv] > 0:
            # Col_deconv_fh.write(deconv+"\t")
            # for sample in OH_deconv_dict_dict:
                # try:
                    # Col_deconv_fh.write(OH_deconv_dict_dict[sample][deconv][1]+"\t") # deconv_dict_dict[sample][deconv][0]+"\t"+
                # except:
                    # Col_deconv_fh.write("\t")
            # Col_deconv_fh.write("\n")
    # Col_deconv_fh.close()

# if len(OH_cr_dict_dict) > 0:
    # Col_cr_fh = open('OH_Chimeras_Removed.tsv',"w")
    # sorted_crs = sorted(OH_cr)
    # Col_cr_fh.write("\t")
    # for sampline in OH_cr_dict_dict:
        # Col_cr_fh.write(sampline+"\t")
    # Col_cr_fh.write("\nUnique Sequence\t")
    # for sampline in OH_cr_dict_dict:
        # Col_cr_fh.write("Abundance\t")
    # Col_cr_fh.write("\n")
    # for cr in sorted_crs:
        # if OH_cr[cr] > 0:
            # Col_cr_fh.write(cr + "\t")
            # for sample in OH_cr_dict_dict:
                # try:
                    # Col_cr_fh.write(str(OH_cr_dict_dict[sample][cr][1])+"\t") # cr_dict_dict[sample][cr][0]+"\t"+
                # except:
                    # Col_cr_fh.write("\t")
            # Col_cr_fh.write("\n")
    # Col_cr_fh.close()
    
# if len(OB_deconv_dict_dict) > 0:
  
    # Col_deconv_fh = open('OB_Covar_Deconv.tsv',"w")
    # sorted_deconvs = sorted(OB_deconv)
    # Col_deconv_fh.write("\t")
    # for sampline in OB_deconv_dict_dict:
        # Col_deconv_fh.write(sampline+"\t")
    # Col_deconv_fh.write("\nCovariant\t")
    # for sampline in OB_deconv_dict_dict:
        # Col_deconv_fh.write("Abundance\t")
    # Col_deconv_fh.write("\n")
    # for deconv in sorted_deconvs:
        # if OB_deconv[deconv] > 0:
            # Col_deconv_fh.write(deconv+"\t")
            # for sample in OB_deconv_dict_dict:
                # try:
                    # Col_deconv_fh.write(OB_deconv_dict_dict[sample][deconv][1]+"\t") # deconv_dict_dict[sample][deconv][0]+"\t"+
                # except:
                    # Col_deconv_fh.write("\t")
            # Col_deconv_fh.write("\n")
    # Col_deconv_fh.close()

# if len(OB_cr_dict_dict) > 0:
    # Col_cr_fh = open('OB_Chimeras_Removed.tsv',"w")
    # sorted_crs = sorted(OB_cr)
    # Col_cr_fh.write("\t")
    # for sampline in OB_cr_dict_dict:
        # Col_cr_fh.write(sampline+"\t")
    # Col_cr_fh.write("\nUnique Sequence\t")
    # for sampline in OB_cr_dict_dict:
        # Col_cr_fh.write("Abundance\t")
    # Col_cr_fh.write("\n")
    # for cr in sorted_crs:
        # if OB_cr[cr] > 0:
            # Col_cr_fh.write(cr + "\t")
            # for sample in OB_cr_dict_dict:
                # try:
                    # Col_cr_fh.write(str(OB_cr_dict_dict[sample][cr][1])+"\t") # cr_dict_dict[sample][cr][0]+"\t"+
                # except:
                    # Col_cr_fh.write("\t")
            # Col_cr_fh.write("\n")
    # Col_cr_fh.close()
    
# if len(WI_deconv_dict_dict) > 0:
  
    # Col_deconv_fh = open('WI_Covar_Deconv.tsv',"w")
    # sorted_deconvs = sorted(WI_deconv)
    # Col_deconv_fh.write("\t")
    # for sampline in WI_deconv_dict_dict:
        # Col_deconv_fh.write(sampline+"\t")
    # Col_deconv_fh.write("\nCovariant\t")
    # for sampline in WI_deconv_dict_dict:
        # Col_deconv_fh.write("Abundance\t")
    # Col_deconv_fh.write("\n")
    # for deconv in sorted_deconvs:
        # if WI_deconv[deconv] > 0:
            # Col_deconv_fh.write(deconv+"\t")
            # for sample in WI_deconv_dict_dict:
                # try:
                    # Col_deconv_fh.write(WI_deconv_dict_dict[sample][deconv][1]+"\t") # deconv_dict_dict[sample][deconv][0]+"\t"+
                # except:
                    # Col_deconv_fh.write("\t")
            # Col_deconv_fh.write("\n")
    # Col_deconv_fh.close()

# if len(WI_cr_dict_dict) > 0:
    # Col_cr_fh = open('WI_Chimeras_Removed.tsv',"w")
    # sorted_crs = sorted(WI_cr)
    # Col_cr_fh.write("\t")
    # for sampline in WI_cr_dict_dict:
        # Col_cr_fh.write(sampline+"\t")
    # Col_cr_fh.write("\nUnique Sequence\t")
    # for sampline in WI_cr_dict_dict:
        # Col_cr_fh.write("Abundance\t")
    # Col_cr_fh.write("\n")
    # for cr in sorted_crs:
        # if WI_cr[cr] > 0:
            # Col_cr_fh.write(cr + "\t")
            # for sample in WI_cr_dict_dict:
                # try:
                    # Col_cr_fh.write(str(WI_cr_dict_dict[sample][cr][1])+"\t") # cr_dict_dict[sample][cr][0]+"\t"+
                # except:
                    # Col_cr_fh.write("\t")
            # Col_cr_fh.write("\n")
    # Col_cr_fh.close()