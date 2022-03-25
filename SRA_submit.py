#!/bin/env python3

import os
import sys

ss_pop_dict = {
                "1":"12000",
                "2":"15000",
                "3":"7500",
                "4":"490000",
                "5":"151966",
                "6":"3300",
                "7":"12000",
                "8":"270",
                "9":"9100",
                "01":"12000",
                "02":"15000",
                "03":"7500",
                "04":"490000",
                "05":"151966",
                "06":"3300",
                "07":"12000",
                "08":"270",
                "09":"9100",
                "10":"34403",
                "11":"11883",
                "12":"4000",
                "13":"506",
                "14":"1730",
                "15":"451367",
                "16":"7936",
                "17":"7300",
                "18":"12790",
                "19":"115895",
                "20":"6155",
                "22":"22818",
                "23":"1960",
                "24":"16000",
                "25":"60000",
                "26":"41153",
                "27":"27391",
                "28":"15906",
                "29":"10730",
                "30":"3282",
                "31":"10114",
                "32":"43200",
                "33":"149112",
                "34":"14477",
                "35":"8250",
                "36":"3784",
                "37":"5471",
                "38":"17000",
                "39":"306647",
                "40":"10000",
                "41":"9000",
                "42":"6000",
                "43":"900",
                "44":"123180",
                "45":"66738",
                "46":"24174",
                "47":"10113",
                "48":"27000",
                "49":"174537",
                "50":"360000",
                "51":"10559",
                "52":"3979",
                "53":"33540",
                "54":"684",
                "55":"1500",
                "56":"11500",
                "58":"8000",
                "59":"20000",
                "60":"1198",
                "61":"199",
                "62":"300",
                "64":"600",
                "65":"2417",
                "66":"1321",
                "68":"3189",
                "69":"1730",
                "70":"8082",
                "71":"13300",
                "72":"130P/400S",
                "73":"Not Collected",
                "74":"Not Collected",
                "75":"450",
                "76":"652",
                "77":"545",
                "78":"316",
                "79":"2976",
                "80":"319",
                "81":"405",
                "82":"413",
                "83":"322",
                "84":"Not Collected",
                "85":"Not Collected",
                "86":"Not Collected",
                "87":"Not Collected",
                "88":"Not Collected",
                "89":"Not Collected",
                "90":"Not Collected",
                "91":"Not Collected",
                "92":"Not Collected",
                "93":"Not Collected",
                "94":"Not Collected",
                "95":"Not Collected",
                "96":"Not Collected",
                "97":"Not Collected",
                "98":"Not Collected",
                "99":"Not Collected",
                "001":"12000",
                "002":"15000",
                "003":"7500",
                "004":"490000",
                "005":"151966",
                "006":"3300",
                "007":"12000",
                "008":"270",
                "009":"9100",
                "010":"34403",
                "011":"11883",
                "012":"4000",
                "013":"506",
                "014":"1730",
                "015":"451367",
                "016":"7936",
                "017":"7300",
                "018":"12790",
                "019":"115895",
                "020":"6155",
                "022":"22818",
                "023":"1960",
                "024":"16000",
                "025":"60000",
                "026":"41153",
                "027":"27391",
                "028":"15906",
                "029":"10730",
                "030":"3282",
                "031":"10114",
                "032":"43200",
                "033":"149112",
                "034":"14477",
                "035":"8250",
                "036":"3784",
                "037":"5471",
                "038":"17000",
                "039":"306647",
                "040":"10000",
                "041":"9000",
                "042":"6000",
                "043":"900",
                "044":"123180",
                "045":"66738",
                "046":"24174",
                "047":"10113",
                "048":"27000",
                "049":"174537",
                "050":"360000",
                "051":"10559",
                "052":"3979",
                "053":"33540",
                "054":"684",
                "055":"1500",
                "056":"11500",
                "058":"8000",
                "059":"20000",
                "060":"1198",
                "061":"199",
                "062":"300",
                "064":"600",
                "065":"2417",
                "066":"1321",
                "068":"3189",
                "069":"1730",
                "070":"8082",
                "071":"13300",
                "072":"130P/400S",
                "073":"Not Collected",
                "074":"Not Collected",
                "075":"450",
                "076":"652",
                "077":"545",
                "078":"316",
                "079":"2976",
                "080":"319",
                "081":"405",
                "082":"413",
                "083":"322",
                "084":"Not Collected",
                "085":"Not Collected",
                "086":"Not Collected",
                "087":"Not Collected",
                "088":"Not Collected",
                "089":"Not Collected",
                "090":"Not Collected",
                "091":"Not Collected",
                "092":"Not Collected",
                "093":"Not Collected",
                "094":"Not Collected",
                "095":"Not Collected",
                "096":"Not Collected",
                "097":"Not Collected",
                "098":"Not Collected",
                "099":"Not Collected",
                "100":"Not Collected",
                "101":"297P/800S",
                "102":"373",
                "103":"310",
                "104":"Not Collected",
                "106":"Not Collected",
                "107":"Not Collected",
                "108":"Not Collected",
                "109":"Not Collected",
                "110":"10500",
                "111":"4895",
                "112":"12000",
                "113":"7001",
                "114":"35300",
                "115":"1500",
                "116":"61250",
                "117":"76759",
                "118":"13940",
                "119":"12000",
                "120":"12855",
                "121":"25000",
                "122":"434",
                "123":"1530",
                "124":"2100",
                "125":"1822",
                "126":"15000",
                "127":"8000",
                "128":"2200",
                "129":"Not Collected",
                "130":"Not Collected",
                "131":"Not Collected",
                "132":"Not Collected",
                "133":"Not Collected",
                "134":"Not Collected",
                "135":"Not Collected",
                "136":"Not Collected",
                "137":"9000"
            }

biosamps_dict = {}
for file in os.listdir(os.getcwd()):
    if (file).startswith('BioSampleObjects'):
        fh_biosamps_in = open(file, 'r')
        for line in fh_biosamps_in:
            splitline = line.split("\t")
            try:
                biosamps_dict[splitline[1]]
                print(f"repeat date {splitline[1]}")
            except:
                biosamps_dict[splitline[1]] = splitline[0]

        fh_biosamps_in.close()


sampnames = []
out_file = open("SRA_sub_list.tsv", "w")
out_file.write("library_ID\ttitle\tlibrary_strategy\tlibrary_source\tlibrary_selection\tlibrary_layout\tplatform\tinstrument_model\tdesign_description\tfiletype\tfilename\tfilename2\tbiosample_accession")
out_file.write("\torganism\tcollection_date\tgeo_loc_name\tisolation_source\tww_population\tww_sample_duration\tww_sample_matrix\tww_sample_type\tww_surv_target_1\tww_surv_target_1_known_present\tcollected_by\n")
for file in os.listdir(os.getcwd()):
    if (file.lower()).endswith('_r1_001.fastq.gz'):
        # print(file)
        splitname = file.split('_')
        
        domain = ''
        if 'RBD' in file.upper():
            if 'NTD' in file.upper() or 'S1S2' in file.upper():
                domain = 'Mixed'
            else:
                domain = 'RBD'
        elif 'MIX' in file.upper():
            domain = 'Mixed'
        elif 'NTD' in file.upper():
            domain = 'NTD'
        elif 'S1S2' in file.upper():
            domain = 'S1S2'
        else:
            print(f"no domain found for {file}")        
        
        if 'RBD' in splitname[0]:
            site = splitname[0].split('RBD')[0].upper().strip('ABCDOC-')
            Date = splitname[0].split('RBD')[1].strip('NTD')
        else:
            site = splitname[0].upper().strip('ABCDOC-')
            Date = splitname[1].upper().strip('RBDNTDALT')
        try:
            site = f"{int(site):03d}"
        except Exception as e:
            print(e)
            print('site')
            print(site)
            print(file)
        
        Month = ''
        try:
            Month = f"{int(Date.split('-')[0]):02d}"
        except Exception as e:
            print(e)
            print('month')
            print(file)
        Day = ''
        try:
            Day = f"{int(Date.split('-')[1]):02d}"
        except Exception as e:
            print(e)
            print('day')
            print(file)
        # for c in Date.split('-')[1]:
            # if c.isdigit():
                # Day += c
            # else:
                # break
        Year = 2022
        if int(Month) > 11:
            Year = 2021
        
        full_date = f"{Year}-{Month}-{Day}"
        sample = f"{site}-{full_date}-{domain}"
        
        if sample in sampnames:
            i = 2
            print(f"Repeat name {sample}")
            while (f"{sample}-{i}") in sampnames:
                i += 1
            sampname =f"{sample}-{i}"
            
        else:
            sampname = sample
        
        sampnames.append(sampname)
        newbiosampacc = ''
        try:
            newbiosampacc = biosamps_dict['Missouri-'+full_date]
        except Exception as e:
            print(e)
            print('biosamp')
            print(file)
            print(full_date)
            pass
        out_file.write(f"{sampname}\t")
        try:
            ww_pop = ss_pop_dict[site]
        except:
            ww_pop = 'Not Collected'

        # if "RBD" in file and "NTD" in file and "S1S2" in file:
            # out_file.write("Mixed Spike N-Terminus Domain, Receptor Binding Domain and S1S2 Junction Domain amplicons")
        if "RBD" in file and "NTD" in file:
            out_file.write("Mixed Spike N-Terminus Domain and Receptor Binding Domain amplicons")
        elif "RBD" in file:
            out_file.write("Spike Receptor Binding Domain amplicon")
        elif "NTD" in file:
            out_file.write("Spike N-Terminus Domain amplicon")
        else:
            out_file.write("Spike S1-S2 Junction Domain amplicon")
        out_file.write(f"\tAmplicon\tViral RNA\tRT-PCR\tPaired\tIllumina\tIllumina MiSeq\tDomain Amplification\tfastq\t{file}\t" + "_".join(splitname[0:-2]) + "_R2_001.fastq.gz")
        out_file.write(f"\t{newbiosampacc}")
        out_file.write("\twastewater metagenome")
        out_file.write(f"\t{full_date}\tUSA: Missouri\twastewater\t")
        out_file.write(f"{ww_pop}\t24h\traw wastewater\tcomposite\tSARS-CoV-2\tYes\tMO DHSS\t")


        out_file.write("\n")



out_file.close()