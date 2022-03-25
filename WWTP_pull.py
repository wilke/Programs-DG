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
                9 : [14, "RK", "Queens"],
                '33' : [33, 'CC', 'St. Louis'],
                '45' : [45, 'Lower Meramec', 'Lower Meramec'],
                '033' : [33, 'CC', 'St. Louis'],
                '045' : [45, 'Lower Meramec', 'Lower Meramec'],
                'WI' : ['WI', 'WI', 'WI']
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
test_fh = open('test.tsv', 'w')
file_names = []
cp_lines = []
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.lower().endswith('.sam') and 'RBD' in file and not ('RNA' in subdir.upper() or 'NTD' in file.upper() or 'S1S2' in file.upper() or 'unrep' in file.lower() or 'WWTP_P' in subdir.upper()):
            
            wwtp = ''
            file_split = file.split('.')[0].split('_')
            if "NY" in file:
                try:
                    wwtp = int(file_split[0].strip("NYRBDA"))
                except:
                    print(subdir+file)
            else: 
                try:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")]
                except:
                    try:
                        wwtp = WWTP_dict2[file.split("_")[0].strip("0d")[:-1]]
                    except:
                        wwtp = file.split("_")[0]
                        if 'WI' in wwtp.upper():
                            wwtp = 'WI'
            
            if wwtp in WWTP_dict:
                amp = 'RBD'
                # if 'RBD' in file.upper():
                    # if 'NTD' in file.upper() or 'S1S2' in file.upper():
                        # amp = 'Mixed'
                    # elif 'RBDA' in file.upper():
                        # amp = 'RBDA'
                    # elif 'RBDB' in file.upper():
                        # amp = 'RBDB'
                    # else:
                        # amp = 'RBD'
                # elif 'NTD' in file.upper():
                    # if 'NTDA' in file.upper():
                        # amp = 'NTDA'
                    # elif 'NTDB' in file.upper():
                        # amp = 'NTDB'
                    # else:
                        # amp = 'NTD'
                # elif 'S1S2' in file.upper() or 'S1S1' in file.upper():
                    # amp = 'S1S2'
                # elif 'RRNA' in file.upper():
                    # pass
                # else:
                    # amp = 'RBD'
                if 'alt' in file.lower() or 'nulomi' in subdir.lower():
                    amp = 'RBDalt'
                date = ''
                try:
                    if '-' in file_split[1]:
                        date = file_split[1]
                    elif '-' in file_split[2]:
                        date = file_split[2]
                    elif '-' in file_split[0]:
                        date = file_split[0].split('RBD')[1]
                except:
                    print('date')
                    print(file)
                
                if amp and date:
                    month = ''
                    day = ''
                    try:
                        for c in date.split('-')[0]:
                            if c.isdigit():
                                month += c
                            else:
                                break
                    except:
                        print('month')
                        print(date)
                    try:
                        for c in date.split('-')[1]:
                            if c.isdigit():
                                day += c
                            else:
                                break
                    except:
                        print('day')
                        print(file)
                    year = subdir.split('/')[6]
                    month = int(month)
                    day = int(day)
                    if month == 0:
                        month = 10
                    if year == '2022' and month > 10:
                        year = '2021'
                    # test_fh.write(f"{subdir}/{file}\t{wwtp}_{year}-{month:02d}-{day:02d}_{amp}\n")
                    new_name = f"{WWTP_dict[wwtp][0]}_{year}-{month:02d}-{day:02d}_{amp}"
                    if new_name in file_names:
                        count = 2
                        while (new_name+'-'+str(count)) in file_names:
                            count += 1
                        new_name = new_name+'-'+str(count)
                        # test_fh.write(f"{subdir}/{file}\t{new_name}\trepeat name\n")
                    # else:
                        # test_fh.write(f"{subdir}/{file}\t{new_name}\n")
                    file_names.append(new_name)
                    
                    if not os.path.isdir(os.getcwd()+'/WWTP_Pulls/'+str(WWTP_dict[wwtp][0])+'/'):
                        os.mkdir(os.getcwd()+'/WWTP_Pulls/'+str(WWTP_dict[wwtp][0])+'/')
                    
                    newfile = f"{os.getcwd()}/WWTP_Pulls/{str(WWTP_dict[wwtp][0])}/{new_name}.{'.'.join(file.split('.')[1:])}"
                    test_fh.write(f"{subdir}/{file}\t{newfile}")
                    # os.system(f"cp {subdir}/{file} {newfile}")
                    test_fh.write(f"\t{os.path.isfile(newfile)}")
                    test_fh.write("\n")
                    if not (os.path.isfile(newfile)):
                        cp_lines.append(f"cp {subdir}/{file} {newfile}")
            
test_fh.close()
print(len(cp_lines))
for line in cp_lines:
    os.system(line)