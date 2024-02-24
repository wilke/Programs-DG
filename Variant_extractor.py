#!/bin/env python3

import os
import sys
import gzip

samps = os.getcwd().split("/")[-1]


nt_strings = ["TTGTCTGGTTTTAAG", "ATGGAGAACGCAGTG", "ATCGAGGGTACAG", "CCATTTTTGGACCAC"]

meta_dict = {}

hits=[]

processed = []

subscreen = []

with open("subscreen.txt", "r") as redo_fh:
    for line in redo_fh:
        line = line.strip()
        if line:
            subscreen.append(line.split("\t")[0])

subscreen = list(set(subscreen))

if os.path.isfile(".processed"):
    with open(".processed", "r") as proced:
        for line in proced:
            processed.append(line.strip())


# for file in os.listdir(os.getcwd()):
    # if file.endswith("_hits.txt"):
        # match = 0
        # for string in nt_strings:
            # if string in file.upper():
                # match = 1
        # if match == 1:
            # with open(file, "r") as in_fh:
                # for line in in_fh:
                    # hits.append(line.strip())

# with open("tmp_hits.txt", "w") as out_fh:
    # for hit in hits:
        # out_fh.write(f"{hit}\n")

# print(len(hits))

# with open("hits_meta.tsv", "r") as intact_fh:
    # for line in intact_fh:
        # if line.split("\t")[0]: # in incompletes:
            # meta_dict[line.split("\t")[0]] = line

with open("/mnt/g/MU_WW/SARS2/SRAs/Wastewater/SRA_meta.tsv", "r") as meta:
    for line in meta:
        split_line = line.split("\t")
        if hits:
            if split_line[0] in hits:
                meta_dict[split_line[0]] = line
        else:
            # date = split_line[4].split("-")
            # if date and ((date[0].isnumeric() and int(date[0]) < 2023) or not date[0].isnumeric()):
                # # if ((len(date) > 1 and int(date[1]) > 5) or len(date) == 1 or int(date[0]) > 2022) or not date[0].isnumeric():
                # meta_dict[split_line[0]] = line
            # elif not date:
            # if "verily" in line.lower():
            meta_dict[split_line[0]] = line


print(len(meta_dict))

for hit in hits:
    if not hit in meta_dict:
        print(hit)

NT_positions = []
asdflas = [
    '100',
    '178',
    '241',
    '335',
    '378',
    '632',
    '647',
    '686',
    '687',
    '689',
    '691',
    '692',
    '2269',
    '2470',
    '2832',
    '3037',
    '3745',
    '3967',
    '4181',
    '4184',
    '5386',
    '5648',
    '5779',
    '6080',
    '6120',
    '6135',
    '6441',
    '6513',
    '6514',
    '6515',
    '7977',
    '8140',
    '8393',
    '8739',
    '9204',
    '9344',
    '9707',
    '9711',
    '9751',
    '9992',
    '9994',
    '10029',
    '10030',
    '10039',
    '11081',
    '11279',
    '11283',
    '11284',
    '11285',
    '11286',
    '11287',
    '11288',
    '11289',
    '11290',
    '11291',
    '11537',
    '11947',
    '11950',
    '11956',
    '11960',
    '11963',
    '13195',
    '13647',
    '13729',
    '13730',
    '13731',
    '13732',
    '13827',
    '13828',
    '13829',
    '13830',
    '13831',
    '13832',
    '13833',
    '13834',
    '13835',
    '13836',
    '13837',
    '13838',
    '13839',
    '13840',
    '13928',
    '13929',
    '13930',
    '14201',
    '14320',
    '14408',
    '14409',
    '14410',
    '14411',
    '14412',
    '14413',
    '14414',
    '14415',
    '14416',
    '14419',
    '14420',
    '14543',
    '14541',
    '14542',
    '14543',
    '14544',
    '14545',
    '15414',
    '15424',
    '15240',
    '15474',
    '15490',
    '15735',
    '15907',
    '15956',
    '17051',
    '17054',
    '18105',
    '18163',
    '18421',
    '19080',
    '19684',
    '19955',
    '20055',
    '20393',
    '20407',
    '21255',
    '21595',
    '21603',
    '21762',
    '21765',
    '21766',
    '21767',
    '21768',
    '21769',
    '21770',
    '21846',
    '21789',
    '21846',
    '21987',
    '21988',
    '21989',
    '21990',
    '21991',
    '21992',
    '21993',
    '21994',
    '21995',
    '22194',
    '22195',
    '22196',
    '22012',
    '22069',
    '22070',
    '22079',
    '22081',
    '22083',
    '22104',
    '22194',
    '22195',
    '22196',
    '22449',
    '22566',
    '22578',
    '22661',
    '22673',
    '22682',
    '22685',
    '22686',
    '22690',
    '22691',
    '22692',
    '22713',
    '22813',
    '22882',
    '22884',
    '22896',
    '22898',
    '22907',
    '22942',
    '22992',
    '22995',
    '23010',
    '23012',
    '23013',
    '23018',
    '23019',
    '23039',
    '23040',
    '23048',
    '23055',
    '23063',
    '23075',
    '23140',
    '23141',
    '23142',
    '23179',
    '23180',
    '23184',
    '23188',
    '23200',
    '23202',
    '23212',
    '23219',
    '23237',
    '23403',
    '23481',
    '23483',
    '23525',
    '23599',
    '23604',
    '23854',
    '23948',
    '24130',
    '24153',
    '24380',
    '24424',
    '24469',
    '24480',
    '24503',
    '25000',
    '25020',
    '25584',
    '25708',
    '26111',
    '26182',
    '26183',
    '26270',
    '26527',
    '26530',
    '26538',
    '26577',
    '26590',
    '26709',
    '27259',
    '27476',
    '27807',
    '28085',
    '28311',
    '28362',
    '28363',
    '28364',
    '28365',
    '28366',
    '28367',
    '28368',
    '28369',
    '28370',
    '28472',
    '28881',
    '28882',
    '28883',
    '29249',
    '29332',
    '29510'
]
NTcall_variants = []
NT_multi_variants = [] # ["A29039TandG29049A"]
AA_variants = [
    # "F490Y", "E484P",
    # "A372T",
    # "K458T", "482S","485D", "498F",
    # "417T",
    # "439K",
    # "440E",
    # "N440R",
    # "447C",
    # "456V",
    # "470N",
    # "472T",
    # "475V",
    # "477D",
    # "483I",
    # "486H",
    # "23008-23010DEL",
    # "N460S", "K1793Q", "G496S", "K440D","Y449N","Y453F","L455F","F456L","E484D","F486L","N501D", "Y449R", "Q498H", "Q498Y", "Y449Y", " F490Y", "Q493K", "N501S", "N501T", "E484V", "E484T", "E484Q", "Y449H", "K444DEL", "V445DEL", "G446DEL", "N447DEL", "Y448DEL", "V483DEL", "E484DEL", "Q498Y", "444DEL", "445DEL", "483DEL", "484DEL", "L828F",
    # "T478R", "N450D", "K444N", "F456L", "L455F", "A475V", "F486P", "S494P",
    # "Q498L",
    # "G496D",
    # "Q493T",
    # "Q493V",
    # "V446A",
    # "T22882A",
    # "T29758G",
    # "23151-23153DEL",
    # "28362G",
    # "28890-28903DEL",
    # "T500S",
    # "449DEL", 
    # "478N",
    # "496N",
    # "G4181T",
    # "A11201G",
    # "A11332G",
    ]
multi_var = [
    # [2, [
    # "G413R",
    # "G413K",
    # "K417T",
    # "K417R",
    # "D420N",
    # "N439K",
    # "N440E",
    # "N440D",
    # "N440H",
    # "N440R",
    # "L441R",
    # "K444DEL",
    # "K444S",
    # "V445DEL",
    # "V445DEL",
    # "V445G",
    # "V445R",
    # "V445N",
    # "V446DEL",
    # "G446T",
    # "G446N",
    # "G446D",
    # "G446V",
    # "G447C",
    # "N447DEL",
    # "Y448DEL",
    # "Y449N",
    # "Y449H",
    # "Y449R",
    # "Y449S",
    # "Y453F",
    # "R454K",
    # "L455M",
    # "L455W",
    # "F456V",
    # "N460S",
    # "T470N",
    # "I472L",
    # "S477D",
    # "V483DEL",
    # "V483A",
    # "V483I",
    # "E484DEL",
    # "E484P",
    # "E484Q",
    # "E484V",
    # "E484D",
    # "E484T",
    # "F486H",
    # "F486A",
    # "F490H",
    # "F490Y",
    # "F490V",
    # "Q493K",
    # "G496V",
    # "Q498H",
    # "Q498Y",
    # "Q498K",
    # "P499S",
    # "P499T",
    # "P499H",
    # "T500S",
    # "N501S",
    # "N501T",
    # "445A",
    # "450k",
    # "478Q",
    # "493T",
    # "493V",
    # "498L",
    # "504D"
    # "Q498L",
    # "G496D",
    # "Q493T",
    # "Q493V",
    # "V446A",
    # ]],
    # [2, [
    # "G413R",
    # "G413K",
    # "K417T",
    # "K417R",
    # "D420N",
    # "N439K",
    # "N440E",
    # "N440D",
    # "N440H",
    # "N440R",
    # "L441R",
    # "K444DEL",
    # "K444S",
    # "V445DEL",
    # "V445DEL",
    # "V445G",
    # "V445R",
    # "V445N",
    # "V446DEL",
    # "G446T",
    # "G446N",
    # "G446D",
    # "G446V",
    # "G447C",
    # "N447DEL",
    # "Y448DEL",
    # "Y449N",
    # "Y449H",
    # "Y449R",
    # "Y449S",
    # "Y453F",
    # "R454K",
    # "L455M",
    # "L455W",
    # "F456V",
    # "N460S",
    # "T470N",
    # "I472L",
    # "S477D",
    # "V483DEL",
    # "V483A",
    # "V483I",
    # "E484DEL",
    # "E484P",
    # "E484Q",
    # "E484V",
    # "E484D",
    # "E484T",
    # "F486H",
    # "F486A",
    # "F490H",
    # "F490Y",
    # "F490V",
    # "Q493K",
    # "G496V",
    # "Q498H",
    # "Q498Y",
    # "Q498K",
    # "P499S",
    # "P499T",
    # "P499H",
    # "T500S",
    # "N501S",
    # "N501T",
    # "445A",
    # "450k",
    # "478Q",
    # "493T",
    # "493V",
    # "498L",
    # "504D",
    # "T478R", "N450D", "K444N", "F456L", "L455F", "A475V", "F486P", "S494P",
    # "Q498L",
    # "G496D",
    # "Q493T",
    # "Q493V",
    # "V446A",
    # ]],
    # [3, [
    # "C22916T", "T22917G", "T22926C"
    # ]],
    # [2, [
    # "K417T", "Q498H"
    # ]],
    # [3, [
    # "N439K", "Y449R", "L452Q"
    # ]],
    # [3, ["T23119A", "A23148G", "A23156G", ]],
    [1, ["G4181T", "A11201G", "A11332G",]]
    ]
Omis = {"1" : {'NTD' : ["A67V", "T95I", "425-433Del", "632-634Del", "215EPE"], 'RBD' : ["1251T(K417N)", "1320G(N440K)", "1336A(G446S)", "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "1478G(Q493R)", "1486A(G496S)", "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", "1640A(T547K)"]},
        "2" : {'NTD' : ["not A67V", "not T95I", "G142D", "not 425-433Del", "not 632-634Del", "V213G"], 'RBD' : ["1251T(K417N)", "1320G(N440K)", "not G446", "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "1478G(Q493R)", "not G496", "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", "not T547"]},
        "3" : {'NTD' : ["A67V", "T95I", "425-433Del", "632-634Del", "not 215EPE"], 'RBD' : ["1251T(K417N)", "1320G(N440K)", "1336A(G446S)", "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "1478G(Q493R)", "not G496", "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", "not T547"]}}

AA_variants = list(set(AA_variants))

Search_Omis = 0
search_ref = 0
Omi_matches = {}
NT_outfiles = {}
NT_mult_outfiles = {}
AA_outfiles = {}
multivar_fhs = {}
nt_call_dict = {}
NT_SRAs = {}
NT_Sample_dict = {}
NT_mult_Sample_dict = {}
Ref_Sample_dict = {}
POS_Sample_dict = {}
ref_NT_dict = {}

if processed:
    if NTcall_variants:
        i = 2
        for variant in NTcall_variants:
            NT_Sample_dict[variant] = {}
            Ref_Sample_dict[variant] = {}
            NT_outfiles[variant] = open(samps+"_NT_"+str(i)+".tsv","a")
            i += 1
    if NT_multi_variants:
        for variant in NT_multi_variants:
            NT_mult_Sample_dict[variant] = {}
            NT_mult_outfiles[variant] = open(samps+"_NTmult_"+variant+".tsv","a")

    if AA_variants:
        AA_variants = list(set(AA_variants))
        for variant in AA_variants:
            AA_outfiles[variant] = open(samps+"_AA_"+variant+".tsv","a")
    if multi_var:
        i = 1
        for variant in multi_var:
            multivar_fhs["and".join(variant[1])] = open(samps+"_multi"+str(i)+".tsv","a")
            i += 1
    if search_ref == 1:
        ref_fh = open(samps+'_refs.tsv', 'a')

else:

    if NTcall_variants:
        i = 2
        for variant in NTcall_variants:
            NT_Sample_dict[variant] = {}
            Ref_Sample_dict[variant] = {}
            NT_outfiles[variant] = open(samps+"_NT_"+str(i)+".tsv","w")
            i += 1
    if NT_multi_variants:
        for variant in NT_multi_variants:
            NT_mult_Sample_dict[variant] = {}
            NT_mult_outfiles[variant] = open(samps+"_NTmult_"+variant+".tsv","w")

    if AA_variants:
        AA_variants = list(set(AA_variants))
        for variant in AA_variants:
            AA_outfiles[variant] = open(samps+"_AA_"+variant+".tsv","w")
    if multi_var:
        i = 1
        for variant in multi_var:
            multivar_fhs["and".join(variant[1])] = open(samps+"_multi"+str(i)+".tsv","w")
            multivar_fhs["and".join(variant[1])].write("and".join(variant[1]))
            multivar_fhs["and".join(variant[1])].write("\n")
            i += 1
    if search_ref == 1:
        ref_fh = open(samps+'_refs.tsv', 'w')

files_read = []
SRAs_read = []
testcounter = 0
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        acc = file.split(".")[0]
        if subscreen and not acc in subscreen:
            continue
        if (not file in files_read) and ((not hits) or acc in hits) and ((not processed) or not os.path.join(subdir, file) in processed): # and file.split(".")[0] in meta_dict:  # and not 'Assemblies' in subdir:
            files_read.append(file)
            if (file.endswith('_unique_seqs.tsv') or file.endswith('_unique_seqs.tsv.gz')) and (AA_variants or multi_var or NT_multi_variants) and not '_AA_' in file: # and not 'wgs' in file:  or file.endswith('_reads.tsv') or file.endswith('_covars.tsv')
                SRAs_read.append(acc)
                print(f"{subdir}/{file}")
                gz = 0
                if file.endswith("gz"):
                    in_file = gzip.open(os.path.join(subdir, file), "rb")
                    gz = 1
                else:
                    in_file = open(os.path.join(subdir, file), "r")
                NT_multi_matches = {}
                AA_matches = {}
                mv_matches = {}
                counts = 0
                ft = 0
                if file.endswith('_reads.tsv'):
                    ft = 1

                try:
                    for line in in_file:
                        if gz == 1:
                            line = line.decode()
                        splitline = line.split("\t")
                        try:
                            splitline[1]
                        except:
                            pass
                        else:
                            if not splitline[1] == "Count":
                                freq = 0
                                if ft == 1:
                                    count = int(splitline[0].split("-")[-1])
                                else:
                                    count = int(splitline[1])
                                    freq = float(splitline[2])
                                if count < 1:
                                    break
                                if NT_multi_variants:
                                    for variant in NT_multi_variants:
                                        mismatch = 0
                                        first = variant.split('and')[0][1:-1]
                                        try:
                                            if int(splitline[ft].split(' ')[0]) > int(first):
                                                continue
                                        except:
                                            pass

                                        for PM in variant.split('and'):
                                            if 'not' in PM:
                                                curPM = PM.strip('not')
                                                if curPM[0] == curPM[-1]:
                                                    if PM[:-1] in splitline[ft]:
                                                        # for nt in ['A', 'T', 'C', 'G', 'N', '-']:
                                                            # if PM[:-1]+nt in splitline[0]:
                                                        mismatch += 1
                                                elif curPM in splitline[ft]:
                                                    mismatch += 1
                                            elif PM[0] == PM[-1]:
                                                if PM[:-1] in splitline[ft]:
                                                    # for nt in ['A', 'T', 'C', 'G', 'N', '-']:
                                                        # if PM[:-1]+nt in splitline[0]:
                                                    mismatch += 1
                                            elif not PM in splitline[ft]:
                                                mismatch += 1
                                        if mismatch == 0:
                                            try:
                                                NT_multi_matches[variant].append(line) # str(mismatch) + "\t" + line)
                                                # counts += int(splitline[1])
                                            except:
                                                NT_multi_matches[variant] = [line]
                                # if ft == 1 or (int(splitline[1]) >= 4):
                                if multi_var: # and "surface" in line or "S_nt" in line: #
                                    for variant in multi_var:
                                        mismatch = 0
                                        match = 0
                                        for PM in variant[1]:
                                            if 'not' in PM:
                                                if PM.strip('not') in splitline[ft]:
                                                    mismatch += 1
                                            else:
                                                if PM in splitline[ft]:
                                                    match += 1

                                        if ((match - mismatch) >= variant[0]) and splitline[ft].count("insert") < 5 and splitline[ft].count("Del") < 6:
                                            try:
                                                mv_matches["and".join(variant[1])].append(line)
                                            except:
                                                mv_matches["and".join(variant[1])] = [line]
                                if AA_variants: # and "surface" in line or "S_nt" in line: # and count > 9
                                    if (int(splitline[1]) > 0 or ft == 1):
                                        for variant in AA_variants:
                                            if variant in line.upper():
                                                try:
                                                    AA_matches[variant].append(line)
                                                except:
                                                    AA_matches[variant] = [line]
                except Exception as Err:
                    print(f"file reading failed for {subdir} {file} {Err}")

                if NT_multi_matches:
                    for variant in NT_multi_matches:
                        if NT_multi_matches[variant]:
                            count = 0
                            for line in NT_multi_matches[variant]:
                                if ft == 1:
                                    count += int(line.split("\t")[0].split("-")[-1])
                                else:
                                    if int(line.split("\t")[1]) > 1:
                                        count += int(line.split("\t")[1])
                            if count > 0:
                                NT_mult_outfiles[variant].write(subdir+"/"+file+"\n")
                                try:
                                    NT_mult_outfiles[variant].write(meta_dict[file.split(".")[0]])
                                except:
                                    NT_mult_outfiles[variant].write("metadata not present\n")
                                count = 0
                                for line in NT_multi_matches[variant]:
                                    NT_mult_outfiles[variant].write(line)
                                    count += 1
                                    if count > 10:
                                        break
                if mv_matches:
                    for variant in mv_matches:
                        count = 0
                        passed_lines = []
                        for line in mv_matches[variant]:
                            read_count = 0
                            if ft == 1:
                                read_count += int(line.split("\t")[0].split("-")[-1])
                            else:
                                read_count += int(line.split("\t")[1])
                            if read_count > 0:
                                count += read_count
                                passed_lines.append(line)
                        if count > 0 and passed_lines:
                            multivar_fhs[variant].write(subdir+"/"+file[:-4]+"\t")
                            multivar_fhs[variant].write("\n")
                            try:
                                multivar_fhs[variant].write(meta_dict[file.split(".")[0]])
                            except:
                                multivar_fhs[variant].write("metadata not present\n")
                            count = 0
                            for line in passed_lines:
                                multivar_fhs[variant].write(line)
                                count += 1
                                if count > 8:
                                    break
                if AA_matches:
                    for variant in AA_matches:
                        if AA_matches[variant]:
                            count = 0
                            for line in AA_matches[variant]:
                                line_count = 0
                                if ft == 1:
                                    line_count += int(line.split("\t")[0].split("-")[-1])
                                else:
                                    line_count += int(line.split("\t")[1])
                                if line_count > 0:
                                    count += line_count
                            if count > 0:
                                AA_outfiles[variant].write(subdir+"/"+file+"\n")
                                try:
                                    AA_outfiles[variant].write(meta_dict[file.split(".")[0]])
                                except:
                                    AA_outfiles[variant].write("metadata not present\n")
                                count = 0
                                for line in AA_matches[variant]:
                                    AA_outfiles[variant].write(line)
                                    count += 1
                                    if count > 10:
                                        break

                in_file.close()
                with open(".processed", "a") as proced:
                    proced.write(f"{os.path.join(subdir, file)}\n")

            if file.endswith("_nt_calls.tsv") and (NTcall_variants or NT_positions):
                in_file = open(os.path.join(subdir, file), "r")
                match_lines = {}
                match_dict = {}
                ref_dict = {}
                for line in in_file:
                    splitline = line.split("\t")
                    try:
                        splitline[1]
                    except:
                        pass
                    else:
                        if splitline[0] == 'Position':
                            PosLine = line
                            for i in range(0, len(splitline)):
                                nt_call_dict[splitline[i]] = i
                        if NT_positions:
                            if splitline[0] in NT_positions:
                                try:
                                    POS_Sample_dict[file.split('_nt_calls')[0]][splitline[0]] = (int(splitline[int(nt_call_dict[splitline[1]])]) / int(splitline[int(nt_call_dict['Total'])]))
                                except:
                                    POS_Sample_dict[file.split('_nt_calls')[0]] = { splitline[0] : (int(splitline[int(nt_call_dict[splitline[1]])]) / int(splitline[int(nt_call_dict['Total'])]))}
                                try:
                                    ref_NT_dict[splitline[0]]
                                except:
                                    ref_NT_dict[splitline[0]] = splitline[1]


                        if NTcall_variants:
                            for var in NTcall_variants:
                                try:
                                    match_lines[var]
                                except:
                                    match_lines[var] = []
                                # if 'and' in var:
                                varPMs = var.split("and")
                                for subvar in varPMs:
                                    if subvar[1:-1] == splitline[0]:
                                        if int(splitline[int(nt_call_dict['Total'])]) > 50 and (int(splitline[int(nt_call_dict[subvar[-1]])]) > (.2 * int(splitline[int(nt_call_dict['Total'])]))):
                                            match_lines[var].append(line)
                                            try:
                                                match_dict[var][subvar] = (int(splitline[int(nt_call_dict[subvar[-1]])]) / int(splitline[int(nt_call_dict['Total'])]))
                                            except:
                                                match_dict[var] = { subvar : (int(splitline[int(nt_call_dict[subvar[-1]])]) / int(splitline[int(nt_call_dict['Total'])])) }
                                            try:
                                                ref_dict[var][subvar] = (int(splitline[int(nt_call_dict[subvar[0]])]) / int(splitline[int(nt_call_dict['Total'])]))
                                            except:
                                                ref_dict[var] = { subvar : (int(splitline[int(nt_call_dict[subvar[0]])]) / int(splitline[int(nt_call_dict['Total'])])) }
                            # elif var[1:-1] == splitline[0]:
                                # if int(splitline[int(nt_call_dict['Total'])]): # > 50 and (int(splitline[int(nt_call_dict[subvar[-1]])]) > (.01 * int(splitline[int(nt_call_dict['Total'])]))):
                                    # match_lines[var].append(line)

                if match_lines:

                    for variant in match_lines:
                        if len(match_lines[variant]) == len(variant.split('and')):
                            try:
                                NT_Sample_dict[variant][file.split('.')[0]] = match_dict[variant]
                                Ref_Sample_dict[variant][file.split('.')[0]] = ref_dict[variant]
                                NT_outfiles[variant].write(file.split('.')[0]+"\n")
                                NT_outfiles[variant].write("\t".join(PosLine.split("\t")[:int(nt_call_dict['Total'])+1])+"\tVarient\tAbundance\n")
                                for line in match_lines[variant]:
                                    splitline= line.split("\t")
                                    NT_outfiles[variant].write("\t".join(splitline[:int(nt_call_dict['Total'])+1]))
                                    for subvar in var.split("and"):
                                        if subvar[1:-1] == splitline[0]:
                                            NT_outfiles[variant].write(f"\t{subvar}\t{match_dict[variant][subvar]}")
                                    NT_outfiles[variant].write("\n")
                                try:
                                    NT_SRAs[variant].append(file.split('.')[0])
                                except:
                                    NT_SRAs[variant] = [(file.split('.')[0])]
                            except:
                                pass


                in_file.close()

                with open(".processed", "a") as proced:
                    proced.write(f"{file}\n")

            if file.endswith("_chim_rm.tsv") or file.endswith("_covar_deconv.tsv"):
                if Search_Omis == 1 or search_ref == 1:
                    samp_name = ""
                    if file.endswith("_covar_deconv.tsv"):
                        samp_name = file.strip("_covar_deconv.tsv")
                    else:
                        samp_name = "_".join(file.split("_")[:-3])
                    ref_lines = []
                    amp = ''
                    if 'NTD' in file:
                        amp = 'NTD'
                    elif 'S1S2' in file:
                        amp = 'S1S2'
                    elif 'RBD' in file:
                        amp = 'RBD'
                    if amp:
                        in_file = open(os.path.join(subdir, file), "r")
                        counts = {'1' : [0 ,0 ,0],
                                  '2' : [0 ,0 ,0],
                                  '3' : [0 ,0 ,0]} # counts['2'][1] == abundance of seq that had 1 mismatches to BA.2
                        matched = 0
                        for line in in_file:
                            splitline = line.strip("\n\r").split("\t")
                            try:
                                splitline[2]
                            except:
                                pass
                            else:
                                if not splitline[1] == "Count":
                                    split_seq = splitline[0].split(' ')
                                    if Search_Omis == 1:
                                        if not amp == 'S1S2':
                                            for sub in Omis:
                                                mismatches = 0
                                                for PM in Omis[sub][amp]:
                                                    if 'not' in PM:
                                                        if PM.split(' ')[1] in splitline[0]:
                                                            mismatches += 1
                                                    elif not PM in splitline[0]:
                                                        mismatches += 1
                                                if mismatches < 3:
                                                    matched = 1
                                                    counts[sub][mismatches] += float(splitline[2])
                                                    # print(splitline[0] + "\t" + sub + "\t" + str(mismatches) + "\t" + splitline[2])
                                                    # print(counts[sub][mismatches])
                                    if search_ref == 1:
                                        # if float(splitline[2]) >= .01: # and not '/NY/' in subdir:
                                        if amp == 'S1S2' and '1841G(D614G)' == splitline[0]:
                                            ref_lines.append(line)
                                        elif 'Reference' == splitline[0]:
                                            ref_lines.append(line)
                    if ref_lines:
                        ref_fh.write(os.path.join(subdir, file)+"\n")
                        for line in ref_lines:
                            ref_fh.write(line)
                        ref_fh.write("\n")



                            # print(counts)
                        if matched == 1:
                            try:
                                Omi_matches[samp_name]
                            except:
                                Omi_matches[samp_name] = counts
                            else:
                                for subvar in Omi_matches[samp_name]:
                                    for i in range(0, 3):
                                        Omi_matches[samp_name][subvar][i] += counts[subvar][i]


                    in_file.close()

                with open(".processed", "a") as proced:
                    proced.write(f"{file}\n")

if search_ref == 1:
    ref_fh.close()

SRAs_read = list(set(SRAs_read))

if subscreen and not len(SRAs_read) == len(subscreen):
    for acc in subscreen:
        if not acc in SRAs_read:
            print(f"{acc} not found")

if os.path.isfile(".processed"):
    os.remove(".processed")

if multi_var:
    for variant in multivar_fhs:
        multivar_fhs[variant].close()
if NT_mult_outfiles:
    for variant in NT_mult_outfiles:
        NT_mult_outfiles[variant].close()
if NTcall_variants:
    for variant in NTcall_variants:
        NT_outfiles[variant].close()
if AA_variants:
    for variant in AA_variants:
        AA_outfiles[variant].close()
if NT_SRAs:
    for variant in NT_SRAs:
        print(variant + ' ' + str(len(NT_SRAs[variant])))
        # for SRA in NT_SRAs[variant]:
            # print(SRA)

if POS_Sample_dict:
    fh_POS_table = open(samps + "_RefNTtable.tsv", 'w')
    fh_POS_table.write(f"Position")
    for sample in POS_Sample_dict:
        fh_POS_table.write(f"\t{sample}")
    fh_POS_table.write(f"\n")
    for position in NT_positions:
        fh_POS_table.write(ref_NT_dict[position]+position)
        for sample in POS_Sample_dict:
            try:
                fh_POS_table.write(f"\t{POS_Sample_dict[sample][position]:04f}")
            except:
                fh_POS_table.write(f"\t")
        fh_POS_table.write(f"\n")


    fh_POS_table.close()

if NT_Sample_dict:
    i = 2
    for variant in NT_Sample_dict:
        fh_NT_table = open(samps + "_" + str(i) + "_NTtable.tsv", 'w')
        i += 1
        fh_NT_table.write(f"mut")
        for sample in NT_Sample_dict[variant]:
            fh_NT_table.write(f"\t{sample}")
        fh_NT_table.write(f"\n")
        for subvar in variant.split("and"):
            fh_NT_table.write(subvar)
            for sample in NT_Sample_dict[variant]:
                try:
                    fh_NT_table.write(f"\t{NT_Sample_dict[variant][sample][subvar]:04f}")
                except:
                    fh_NT_table.write(f"\t")
            fh_NT_table.write(f"\n")


        fh_NT_table.close()

if Ref_Sample_dict:
    i = 2
    for variant in Ref_Sample_dict:
        fh_Ref_table = open(samps + "_" + str(i) + "_Reftable.tsv", 'w')
        i += 1
        fh_Ref_table.write(f"mut")
        for sample in Ref_Sample_dict[variant]:
            fh_Ref_table.write(f"\t{sample}")
        fh_Ref_table.write(f"\n")
        for subvar in variant.split("and"):
            fh_Ref_table.write(subvar[:-1]+subvar[0])
            for sample in Ref_Sample_dict[variant]:
                try:
                    fh_Ref_table.write(f"\t{Ref_Sample_dict[variant][sample][subvar]:04f}")
                except:
                    fh_Ref_table.write(f"\t")
            fh_Ref_table.write(f"\n")


        fh_Ref_table.close()


if Omi_matches:
    Omi_out_fh = open(samps+"_Omis.tsv","w")
    sorted_samps = sorted(Omi_matches.keys())
    for subvar in Omis:
        for domain in Omis[subvar]:
            Omi_out_fh.write(f"BA.{subvar}\t{domain}\t{', '.join(Omis[subvar][domain])}")
            Omi_out_fh.write("\n")
    Omi_out_fh.write("\n")
    # Omi_out_fh.write(f"\t\t[Perfect match, 1 mismatch, 2 mismatch]")
    for key in sorted_samps:
        Omi_out_fh.write(key+ "\t\tPerfect match\t1 mismatch\t2 mismatch\n")
        for subvar in Omi_matches[key]:
            Omi_out_fh.write(f"\tBA.{subvar}")
            for val in Omi_matches[key][subvar]:
                Omi_out_fh.write(f"\t{val}")
            Omi_out_fh.write("\n")
        Omi_out_fh.write("\n")
    Omi_out_fh.close()

for sra in hits:
    if not sra in SRAs_read:
        print(f"{sra} not found")